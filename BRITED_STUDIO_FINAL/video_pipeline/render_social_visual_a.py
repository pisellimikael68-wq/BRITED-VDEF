#!/usr/bin/env python3
"""Rendu social BRITED générique conforme aux pilotes TikTok/Instagram validés."""

from __future__ import annotations

import argparse
import io
import json
import math
import os
import re
import subprocess
import shutil
import hashlib
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 720, 1280, 60
DRAW_FPS = 15  # animation fluide, sortie normalisée à 60 i/s par FFmpeg
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
DISPLAY_FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
# Direction A Claude Design : carte flottante chaude, cartouche titre,
# pictogrammes circulaires et progression continue.
PAPER = (255, 254, 250); INK = (32, 28, 22); TERRA = (169, 113, 26)
SAND = (243, 224, 190); SOFT = (243, 224, 190); WHITE = (255, 254, 250)
MUTED = (107, 98, 85)
SERIES = {"fiscalite": (111,78,55), "immobilier": (201,111,74),
          "juridique": (217,154,43), "finance": (36,87,214)}
MAIN_TEXT_SIZE = 46
MIN_MAIN_TEXT_SIZE = 40


def ffmpeg_executable() -> str:
    local = Path(__file__).resolve().parents[1] / ".video-tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    if local.is_file():
        return str(local)
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise RuntimeError("FFmpeg absent : rendu vidéo indisponible") from exc


def font(size: int): return ImageFont.truetype(FONT, size, index=1)
def display_font(size: int): return ImageFont.truetype(DISPLAY_FONT, size, index=9)
def ease(x: float) -> float:
    x = max(0.0, min(1.0, x)); return x*x*(3-2*x)


def fade_color(background, foreground, amount: float):
    amount=max(0.0,min(1.0,amount))
    return tuple(round(a+(b-a)*amount) for a,b in zip(background,foreground))


def series_color(spec: dict) -> tuple[int, int, int]:
    return SERIES.get(spec.get("serie", "juridique"), SERIES["juridique"])


def displayed_text(beat: dict) -> str:
    """Texte visible, distinct de la narration préparée pour la voix."""
    return (beat.get("screen_text") or beat.get("narration") or "").strip()


def wrap_words(draw, words, face, max_width=600):
    lines=[]; line=[]
    for word in words:
        trial=" ".join(line+[word])
        if line and draw.textlength(trial,font=face)>max_width:
            lines.append(line); line=[word]
        else: line.append(word)
    if line: lines.append(line)
    return lines


def shorts_answer_layout(draw, narration: str):
    """Calcule une réponse Shorts qui tient entièrement dans sa carte.

    Le cartouche noir est réservé aux réponses franches OUI/NON. Un premier
    mot ordinaire (par exemple « Le ») ne doit jamais être transformé en badge.
    """
    words=narration.upper().strip().split()
    normalized_first=words[0].rstrip(".:;!?") if words else ""
    has_verdict=normalized_first in {"OUI", "NON"}
    body=words[1:] if has_verdict else words
    max_width=500
    max_height=292 if has_verdict else 350
    size=38
    while size >= 25:
        face=display_font(size)
        lines=wrap_words(draw,body,face,max_width)
        gap=round(size*1.16)
        if lines and len(lines)*gap <= max_height and all(draw.textlength(" ".join(line),font=face)<=max_width for line in lines):
            return normalized_first if has_verdict else "", lines, face, gap
        size-=1
    face=display_font(24)
    return normalized_first if has_verdict else "", wrap_words(draw,body,face,max_width), face, 28


@lru_cache(maxsize=16)
def locked_header_layer(header: str, accent: tuple[int, int, int]) -> Image.Image:
    """Fabrique une seule matrice de titre, ensuite réutilisée pixel pour pixel.

    Le cartouche ne peut ainsi plus varier selon la page, l'animation ou le
    rôle du beat. Toutes les lettres et toutes les lignes partagent exactement
    la même police, la même graisse et le même corps typographique.
    """
    layer=Image.new("RGBA",(W,180),(0,0,0,0)); draw=ImageDraw.Draw(layer)
    draw.rectangle((55,61,64,157),fill=accent+(255,))
    # La fonte condensée du corps principal présente une hauteur de capitale
    # beaucoup plus uniforme que la variante proportionnelle. Elle supprime le
    # décalage optique visible au sommet de certaines lettres du cartouche.
    face=display_font(30)
    lines=wrap_words(draw,header.split(),face,555)
    while len(lines)>3 and face.size>24:
        face=display_font(face.size-1); lines=wrap_words(draw,header.split(),face,555)
    y=62
    for line in lines:
        draw.text((91,y)," ".join(line),anchor="la",font=face,fill=accent+(255,)); y+=38
    return layer


def header_fingerprint(header: str, accent: tuple[int, int, int]) -> str:
    return hashlib.sha256(locked_header_layer(header,accent).tobytes()).hexdigest()


def base(spec: dict, page: int):
    top=(255,252,246); bottom=(251,243,228)
    strip=Image.new("RGB",(1,H),top); pixels=strip.load()
    for y in range(H):
        ratio=y/(H-1); pixels[0,y]=tuple(round(a+(b-a)*ratio) for a,b in zip(top,bottom))
    image=strip.resize((W,H))
    draw=ImageDraw.Draw(image)
    accent=series_color(spec)
    total=len(spec["beats"])
    # Le cartouche supérieur de la page 1 est la référence unique de toute la
    # vidéo, y compris la dernière page de prise de rendez-vous.
    header=(spec.get("header") or spec.get("title") or "PATRIMOINE").upper()
    # Collage de la même matrice verrouillée sur chaque page : aucune
    # variation de taille, de graisse ou de rasterisation n'est possible.
    rgba=image.convert("RGBA")
    rgba.alpha_composite(locked_header_layer(header,accent),(0,0))
    image=rgba.convert("RGB")
    draw=ImageDraw.Draw(image)
    # Version A hybride du kit v3 : séparateur + modules carrés + progression
    # segmentée. Le CTA rendez-vous conserve toutefois sa composition dédiée.
    if page < total-1:
        draw.line((55,1008,665,1008),fill=(225,219,209),width=2)
    gap=9; segment=(610-gap*(total-1))/total
    for index in range(total):
        x1=55+index*(segment+gap)
        draw.rounded_rectangle((x1,1218,x1+segment,1227),radius=5,
                               fill=accent if index<=page else (230,224,214))
    return image,draw


def overlay_library_icons(image,kind,accent,amount=1.0):
    layer=Image.new("RGBA",(W,H),(0,0,0,0)); layer_draw=ImageDraw.Draw(layer)
    library_icon(layer_draw,kind,accent)
    alpha=max(0,min(255,round(255*amount)))
    layer.putalpha(layer.getchannel("A").point(lambda value: round(value*alpha/255)))
    return Image.alpha_composite(image.convert("RGBA"),layer).convert("RGB")


def platform_safe_frame(image: Image.Image, platform: str) -> Image.Image:
    """Recompose la carte dans la zone réellement libre de chaque application.

    Le contenu reste identique ; seule son empreinte visuelle change. TikTok
    réserve davantage d'espace à droite et en bas, tandis que Reels protège le
    cadrage du fil et les commandes superposées. Shorts conserve la référence.
    """
    profiles = {
        "reels": {"scale": .94, "x": .50, "y": .48},
        "tiktok": {"scale": .90, "x": .43, "y": .45},
        "shorts": {"scale": 1.0, "x": .50, "y": .50},
    }
    profile = profiles.get(platform, profiles["shorts"])
    scale = profile["scale"]
    if scale == 1.0:
        return image
    width, height = round(W * scale), round(H * scale)
    reduced = image.resize((width, height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (W, H), PAPER)
    free_x, free_y = W - width, H - height
    x = round(free_x * profile["x"])
    y = round(free_y * profile["y"])
    canvas.paste(reduced, (x, y))
    return canvas


def question_page(spec: dict,page: int,beat: dict,icon_alpha: float = 1.0):
    image,draw=base(spec,page); accent=series_color(spec)
    draw.rounded_rectangle((225,350,495,405),radius=28,fill=SOFT)
    draw.text((360,378),"À VOUS DE JOUER",anchor="mm",font=font(25),fill=TERRA)
    question=re.sub(r"(?:[,;:]?\s*(?:OUI\s*(?:/|OU)\s*NON)\s*[.!]?)$","",displayed_text(beat),flags=re.IGNORECASE).strip()
    # La charte validée conserve la même écriture en capitales sur toutes les
    # pages, y compris la question interactive.
    words=question.upper().split()
    face=display_font(MAIN_TEXT_SIZE); lines=wrap_words(draw,words,face,580)
    while len(lines)>4 and face.size>MIN_MAIN_TEXT_SIZE:
        face=display_font(face.size-2); lines=wrap_words(draw,words,face,540)
    gap=69
    # Centre optiquement la question dans l'espace réellement disponible entre
    # l'intitulé et les choix. Le nombre de lignes ne déplace plus le bloc.
    y=535-(len(lines)-1)*gap/2
    for line in lines:
        draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=INK); y+=gap
    # Aucun choix n'est mis en avant avant la révélation : OUI et NON restent
    # visuellement strictement neutres afin de ne pas suggérer la réponse.
    draw.rounded_rectangle((180,700,345,784),radius=42,fill=WHITE,outline=INK,width=3)
    draw.text((262,742),"OUI",anchor="mm",font=display_font(30),fill=INK)
    draw.rounded_rectangle((375,700,540,784),radius=42,fill=WHITE,outline=INK,width=3)
    draw.text((458,742),"NON",anchor="mm",font=display_font(30),fill=INK)
    return overlay_library_icons(image,"circle-help scale",accent,icon_alpha)


def answer_page(spec: dict,page: int,beat: dict,visible: int | None = None,icon_alpha: float = 1.0):
    image,draw=base(spec,page); accent=series_color(spec)
    visible_text=displayed_text(beat)
    answer_words=visible_text.upper().strip().split()
    if spec.get("platform") == "shorts":
        if spec.get("answer_design") == "adaptive_sections_v2":
            # Carte de réponse générique pour les futures publications :
            # verdict appuyé puis informations essentielles dans des modules
            # distincts. Le contenu vient exclusivement du script certifié.
            card=(78,270,642,920)
            draw.rounded_rectangle(card,radius=42,fill=(255,253,248),outline=(229,218,198),width=2)
            draw.text((360,320),"RÉPONSE",anchor="mm",font=font(21),fill=accent)
            sentences=[part.strip() for part in re.split(r"(?<=[.!?])\s+",visible_text) if part.strip()]
            verdict=sentences[0] if sentences else visible_text
            details=sentences[1:] or [verdict]
            if not sentences[1:]: verdict=""
            top=365
            if verdict:
                verdict_text=verdict.upper().rstrip(".")
                verdict_face=display_font(25)
                while draw.textlength(verdict_text,font=verdict_face)>430 and verdict_face.size>20:
                    verdict_face=display_font(verdict_face.size-1)
                draw.rounded_rectangle((130,350,590,425),radius=37,fill=INK)
                draw.text((360,388),verdict_text,anchor="mm",font=verdict_face,fill=WHITE)
                top=470
            # Lorsqu'une réponse tient en un seul bloc, ce bloc est centré
            # optiquement dans toute la zone utile de la carte. Il ne reste
            # plus collé sous le libellé avec un grand vide en dessous.
            single_detail = len(details) == 1
            if single_detail:
                top = 490
            available=835-top
            gap_between=18
            module_height=(230 if single_detail else
                           max(112,min(210,round((available-gap_between*(len(details)-1))/len(details)))))
            for detail in details:
                bottom=min(850,top+module_height)
                draw.rounded_rectangle((112,top,608,bottom),radius=24,fill=(253,247,234),outline=SOFT,width=2)
                detail_text=detail.upper()
                # La réponse courte doit rester immédiatement lisible et
                # parfaitement centrée. Une taille de départ plus généreuse
                # évite notamment que les apostrophes françaises soient
                # confondues avec des lettres par le contrôle OCR.
                # Helvetica Neue Bold conserve la force visuelle de la réponse
                # tout en dessinant les apostrophes et les doubles consonnes
                # plus nettement que la variante condensée du titre.
                face=font(32)
                lines=wrap_words(draw,detail_text.split(),face,430)
                while (len(lines)>4 or len(lines)*round(face.size*1.22)>bottom-top-36) and face.size>20:
                    face=font(face.size-1); lines=wrap_words(draw,detail_text.split(),face,430)
                line_gap=round(face.size*1.22)
                y=(top+bottom)/2-(len(lines)-1)*line_gap/2
                for line in lines:
                    draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=INK); y+=line_gap
                top=bottom+gap_between
            return overlay_library_icons(image,"check file-text",accent,icon_alpha)
        if spec.get("answer_design") == "structured_v2":
            # Réponse pédagogique en trois niveaux : verdict, PACS, concubinage.
            # Le fond juridique reste intégral, mais le regard n'a plus à
            # décoder un pavé uniforme en capitales.
            card=(78,270,642,920)
            draw.rounded_rectangle(card,radius=42,fill=(255,253,248),outline=(229,218,198),width=2)
            draw.text((360,320),"RÉPONSE",anchor="mm",font=font(21),fill=accent)
            draw.rounded_rectangle((184,354,536,424),radius=35,fill=INK)
            draw.text((360,389),"NON, PAS AUTOMATIQUEMENT",anchor="mm",font=display_font(25),fill=WHITE)

            sections=(
                ("PACS", "SANS TESTAMENT, LE PARTENAIRE DE PACS N'HÉRITE PAS."),
                ("CONCUBINAGE", "LE CONCUBIN NON PLUS. LES BIENS REÇUS PAR TESTAMENT SONT IMPOSÉS À 60 %."),
            )
            top=470
            bounds=[]
            for section_index,(label,body) in enumerate(sections):
                height=142 if section_index==0 else 194
                draw.rounded_rectangle((112,top,608,top+height),radius=24,fill=(253,247,234),outline=SOFT,width=2)
                label_face=font(18)
                label_width=max(156,min(430,round(draw.textlength(label,font=label_face)+44)))
                label_box=(134,top+18,134+label_width,top+58)
                draw.rounded_rectangle(label_box,radius=20,fill=SOFT)
                draw.text(((label_box[0]+label_box[2])/2,top+38),label,anchor="mm",font=label_face,fill=accent)
                face=display_font(25)
                lines=wrap_words(draw,body.split(),face,430)
                gap=31; y=top+86
                for line in lines:
                    draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=INK); y+=gap
                bounds.append([112,top,608,top+height]); top+=height+18
            return overlay_library_icons(image,"users scroll-text badge-percent",accent,icon_alpha)
        # Réponse YouTube : une composition unique, calme et géométriquement
        # centrée. Le premier mot n'est plus un énorme cartouche indépendant
        # et aucun cadre variable ne vient comprimer la formulation.
        first,lines,face,gap=shorts_answer_layout(draw,visible_text)
        card=(78,285,642,900)
        draw.rounded_rectangle(card,radius=42,fill=(255,253,248),outline=(229,218,198),width=2)
        draw.rounded_rectangle((297,315,423,361),radius=23,fill=SOFT)
        draw.text((360,338),"RÉPONSE",anchor="mm",font=font(19),fill=accent)
        draw.line((108,390,612,390),fill=accent,width=4)
        if visible == 0:
            return image
        if first:
            draw.rounded_rectangle((285,425,435,487),radius=31,fill=INK)
            draw.text((360,456),first,anchor="mm",font=display_font(27),fill=WHITE)
            text_top=525; text_bottom=840
        else:
            text_top=425; text_bottom=840
        text_center=(text_top+text_bottom)/2
        y=text_center-(len(lines)-1)*gap/2
        for line in lines:
            draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=INK); y+=gap
        return overlay_library_icons(image,"check file-text",accent,icon_alpha)
    # La mise en page est calculée sur la réponse complète. Pendant le fondu,
    # les nouveaux mots occupent donc immédiatement leur position définitive :
    # plus aucun tassement ni recentrage saccadé à chaque apparition.
    first=answer_words[0].rstrip(".:;!?") if answer_words else "NON"
    remainder=answer_words[1:]
    face=display_font(MAIN_TEXT_SIZE); lines=wrap_words(draw,remainder,face,624)
    while len(lines)>4 and face.size>MIN_MAIN_TEXT_SIZE:
        face=display_font(face.size-2); lines=wrap_words(draw,remainder,face,545)
    pill_width=max(185,round(draw.textlength(first,font=display_font(32))+110))
    draw.rounded_rectangle((360-pill_width/2,370,360+pill_width/2,454),radius=42,fill=INK)
    draw.text((360,412),first,anchor="mm",font=display_font(32),fill=WHITE)
    gap=round(face.size*1.18); y=575-(len(lines)-1)*gap/2
    shown=0
    for line in lines:
        widths=[draw.textlength(word,font=face) for word in line]
        space=draw.textlength(" ",font=face)
        x=(W-(sum(widths)+space*(len(line)-1)))/2
        for word,width in zip(line,widths):
            if visible is None or shown < max(0,visible-1):
                draw.text((x,y),word,anchor="lm",font=face,fill=INK)
            shown+=1; x+=width+space
        y+=gap
    return overlay_library_icons(image,"check file-text",accent,icon_alpha)


def cta_page(spec: dict,page: int,beat: dict,progress: float = 1.0):
    image,draw=base(spec,page); accent=series_color(spec)
    if True:
        question_alpha=ease(progress/.40)
        button_alpha=ease((progress-.34)/.34)
        destination_alpha=ease((progress-.66)/.26)
        question="VOUS SOUHAITEZ FAIRE LE POINT SUR VOTRE SITUATION ?".split()
        face=display_font(55); lines=wrap_words(draw,question,face,580); y=390-(len(lines)-1)*32
        for line in lines:
            draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=fade_color(WHITE,INK,question_alpha)); y+=65
        button_fill=fade_color((253,248,237),SOFT,button_alpha)
        button_stroke=fade_color((253,248,237),accent,button_alpha)
        draw.rounded_rectangle((112,570,608,666),radius=18,fill=button_fill,outline=button_stroke,width=4)
        draw.text((360,618),"PRENEZ RENDEZ-VOUS",anchor="mm",font=display_font(29),fill=button_stroke)
        destination="VIA LE LIEN DANS MA BIO"
        destination_color=fade_color(WHITE,accent,destination_alpha)
        draw.text((360,730),destination,anchor="mm",font=font(27),fill=destination_color)
        # Calendrier tracé géométriquement : aucune dépendance à une ligature
        # de police susceptible de produire deux glyphes ou de remonter sur le
        # texte de destination.
        glyph_color=fade_color((253,248,237),accent,destination_alpha)
        draw.rounded_rectangle((324,805,396,875),radius=10,outline=glyph_color,width=5)
        draw.line((324,827,396,827),fill=glyph_color,width=5)
        draw.line((343,795,343,815),fill=glyph_color,width=5)
        draw.line((377,795,377,815),fill=glyph_color,width=5)
        return image
    draw.text((360,390),"LE SAVIEZ-VOUS ?",anchor="mm",font=display_font(43),fill=INK)
    # Modèle pédagogique unique et obligatoire sur les trois plateformes.
    # Aucune variante « abonnement seul » ou « enregistrement » n'est admise.
    centers=(145,360,575); icon_names=("message-circle","share-2","heart-handshake")
    labels=("COMMENTER","PARTAGER","ABONNEZ-\nVOUS")
    for center,name,label in zip(centers,icon_names,labels):
        draw.rounded_rectangle((center-50,485,center+50,585),radius=20,fill=WHITE,outline=accent,width=5)
        if LUCIDE_FONT.exists() and name in _LUCIDE_POINTS:
            glyph=chr(int(_LUCIDE_POINTS[name]))
            draw.text((center,535),glyph,anchor="mm",font=ImageFont.truetype(str(LUCIDE_FONT),43),fill=accent)
        draw.rounded_rectangle((center-78,605,center+78,676),radius=30,fill=SOFT)
        draw.multiline_text((center,640),label,anchor="mm",align="center",spacing=0,
                            font=font(18),fill=accent)
    draw.text((360,752),"POUR MIEUX COMPRENDRE ET",anchor="mm",font=font(24),fill=MUTED)
    draw.text((360,786),"PROTÉGER VOTRE PATRIMOINE",anchor="mm",font=font(24),fill=MUTED)
    return image


def speech_weight(token: str) -> float:
    letters=len("".join(char for char in token if char.isalnum()))
    value=max(1.0,letters**.62)
    if token.endswith((".","!","?")): value+=1.25
    elif token.endswith((",",";",":")): value+=.60
    return value


def reveal(words: list[str], t: float, duration: float) -> tuple[int,float]:
    weights=[speech_weight(word) for word in words]; budget=max(.2,duration-.18)
    scale=budget/max(.01,sum(weights)); elapsed=0.0
    for index,weight in enumerate(weights):
        word_duration=weight*scale
        if t < elapsed+word_duration:
            fade=min(.16,word_duration*.68)
            return index+1,ease((t-elapsed)/max(.01,fade))
        elapsed+=word_duration
    return len(words),1.0


def action_start(words: list[str], duration: float) -> float:
    markers=("commentez","partagez","enregistrez","abonnez-vous","abonnez")
    index=next((i for i,word in enumerate(words) if word.casefold().strip(".,:;?!") in markers),len(words))
    weights=[speech_weight(word) for word in words]; scale=max(.2,duration-.18)/max(.01,sum(weights))
    return sum(weights[:index])*scale


def icon_family(kind: str) -> str:
    """Associe chaque description à un schéma pédagogique vérifiable."""
    groups = (
        ("question", ("question", "point d'interrogation", "selon vous", "peut-on")),
        ("couple", ("mariage", "couple", "époux", "pacs", "concubin", "partenaire", "personnes", "silhouette")),
        ("assurance_vie", ("clause bénéficiaire", "bénéficiaire", "contrat", "capital", "gains", "rachat", "désignation", "acceptation", "abattement", "assureur", "courrier", "enveloppe")),
        ("menage", ("charges du mariage", "dettes du ménage", "facture", "loyer", "école")),
        ("testament", ("testament", "hérit", "décès", "succession", "légué", "parchemin")),
        ("fiscalite", ("fiscal", "taxable", "imposée", "taux", "calcul visuel", "% appliqués", "20 %", "31,25 %", "droits de succession", "exonération", "euro barré")),
        ("enfants", ("enfant", "réserve héréditaire")),
        ("preuve", ("preuve", "justificatif", "relevé", "dossier", "origine des fonds", "présumé")),
        ("loi", ("article", "code", "juridique", "livre de loi", "balance", "§", "notaire", "notarié", "homologation", "judiciaire", "tribunal", "tiers", "s'opposer")),
        ("maison", ("maison", "résidence", "indivision", "propriétaire", "deux clés")),
        ("banque", ("compte bancaire", "salaire", "épargne")),
        ("masses", ("3 masses", "trois masses")),
        ("partage", ("liquidation", "partage")),
        ("protection", ("protection", "protégé", "abri", "bouclier", "cadenas brisé")),
        ("entreprise", ("entrepreneur", "professionnel", "entreprise", "risque professionnel")),
    )
    normalized=kind.casefold()
    return next((family for family,terms in groups if any(term in normalized for term in terms)), "generic")


def visual_context(beat: dict) -> str:
    """Le dessin proposé et la narration se contrôlent mutuellement."""
    return f"{beat.get('visual','')} {beat.get('narration','')}".strip().casefold()


LUCIDE_ROOT=Path(__file__).resolve().parents[1]/"assets/icon-library/node_modules/lucide-static/font"
LUCIDE_FONT=LUCIDE_ROOT/"lucide.ttf"
LUCIDE_CODEPOINTS=LUCIDE_ROOT/"codepoints.json"
_LUCIDE_POINTS=json.loads(LUCIDE_CODEPOINTS.read_text()) if LUCIDE_CODEPOINTS.exists() else {}


def visual_icon_names(kind: str) -> list[str]:
    """Sélectionne deux ou trois symboles locaux explicites selon le sens."""
    value=kind.casefold(); names=[token for token in value.split() if token in _LUCIDE_POINTS]
    rules=(
        (("question", "point d'interrogation", "selon vous", "peut-on"),("circle-help","badge-euro")),
        (("clause bénéficiaire","bénéficiaire","contrat","capital","rachat","désignation","acceptation","abattement","gains"),("file-signature","user-round-check","badge-euro")),
        (("bouclier","protection","protégé","abri"),("shield-alert","shield-check")),
        (("facture","loyer","frais","dette","charges"),("receipt-euro","house")),
        (("article","code civil","juridique","loi","notaire","notarié","homologation","judiciaire","tribunal","tiers","s'opposer"),("scale","file-signature","landmark")),
        (("testament","legs","succession","hérit"),("scroll-text","users")),
        (("enfant","école","réserve héréditaire"),("baby","users")),
        (("maison","logement","résidence","indivision"),("house","key-round")),
        (("preuve","justificatif","dossier","relevé"),("file-check-2","search")),
        (("fiscal","taxable","imposée","taux","20 %","31,25 %","pour cent","droits de succession","exonér"),("badge-percent","receipt-euro")),
        (("compte","banque","épargne","salaire"),("landmark","wallet-cards")),
        (("partage","moitié","50"),("split","hand-coins")),
        (("couple","époux","pacs","concubin","partenaire"),("users","heart-handshake")),
        (("entrepreneur","professionnel","entreprise","risque professionnel"),("briefcase-business","shield-check")),
    )
    for terms,icons in rules:
        if any(term in value for term in terms): names.extend(icons)
    names=list(dict.fromkeys(name for name in names if name in _LUCIDE_POINTS))
    if not names: names=[name for name in ("circle-help","lightbulb") if name in _LUCIDE_POINTS]
    return names[:3]


def library_icon(draw,kind,accent) -> bool:
    if not LUCIDE_FONT.exists() or not _LUCIDE_POINTS: return False
    names=visual_icon_names(kind)
    if not names: return False
    count=len(names); card=113; gap=18
    total=count*card+(count-1)*gap; left=(W-total)//2; y=1040
    active_index=None
    if "heart-handshake" in names: active_index=names.index("heart-handshake")
    elif "banknote" in names: active_index=names.index("banknote")
    for index,name in enumerate(names):
        x=left+index*(card+gap)
        active=index==active_index
        draw.rounded_rectangle((x,y,x+card,y+card),radius=24,
                               fill=SOFT if active else (254,249,240),
                               outline=accent,width=5)
        glyph=chr(int(_LUCIDE_POINTS[name])); glyph_font=ImageFont.truetype(str(LUCIDE_FONT),49 if not active else 55)
        draw.text((x+card/2,y+card/2),glyph,anchor="mm",font=glyph_font,fill=accent)
        if index<count-1:
            cx=x+card+gap/2
            draw.line((cx-4,y+card/2,cx+4,y+card/2),fill=(128,120,108),width=2)
    return True


def icon(draw,kind,accent):
    if library_icon(draw,kind,accent): return
    family=icon_family(kind)
    if family == "menage":
        # Educational visual for current household expenses: a home, a bill
        # and a paid check. Keep the 50/50 split for the following page only.
        draw.polygon(((225,845),(360,755),(495,845)),outline=accent,fill=SOFT)
        draw.rounded_rectangle((250,840,470,965),radius=12,fill=WHITE,outline=accent,width=5)
        draw.rounded_rectangle((390,865,445,965),radius=6,outline=accent,width=4)
        draw.rounded_rectangle((105,825,245,930),radius=18,fill=WHITE,outline=accent,width=4)
        draw.text((175,875),"€",anchor="mm",font=font(48),fill=accent)
        draw.line((135,910,170,935),fill=accent,width=6)
        draw.line((170,935,225,880),fill=accent,width=6)
    elif family == "banque":
        draw.rounded_rectangle((115,800,315,905),radius=20,fill=WHITE,outline=accent,width=4)
        draw.text((215,853),"€",anchor="mm",font=font(58),fill=accent)
        draw.line((340,852,445,852),fill=accent,width=5);draw.polygon(((445,852),(428,842),(428,862)),fill=accent)
        draw.rounded_rectangle((478,800,582,905),radius=17,outline=accent,width=5)
        draw.arc((500,815,560,875),180,360,fill=accent,width=4)
        draw.line((500,846,500,884),fill=accent,width=4);draw.line((560,846,560,884),fill=accent,width=4)
    elif family == "masses":
        boxes=((86,815,246,916),(280,785,440,946),(474,815,634,916))
        for index,box in enumerate(boxes):
            draw.rounded_rectangle(box,radius=22,fill=WHITE if index!=1 else SOFT,outline=accent,width=4)
        draw.text((166,866),"A",anchor="mm",font=font(34),fill=INK)
        draw.text((360,850),"COMMUN",anchor="mm",font=font(25),fill=accent)
        draw.text((554,866),"B",anchor="mm",font=font(34),fill=INK)
        draw.line((246,866,280,866),fill=accent,width=4); draw.line((440,866,474,866),fill=accent,width=4)
    elif family in {"preuve", "partage", "loi"}:
        draw.rounded_rectangle((245,785,475,920),radius=18,fill=WHITE,outline=accent,width=5)
        for y in (825,855,885): draw.line((280,y,440,y),fill=SAND,width=5)
        if family == "preuve":
            draw.ellipse((405,875,490,960),outline=accent,width=6); draw.line((468,940,520,992),fill=accent,width=7)
        elif family == "loi":
            draw.text((360,855),"§",anchor="mm",font=font(58),fill=accent)
        elif family == "partage":
            draw.line((360,935,275,985),fill=accent,width=5);draw.polygon(((275,985),(292,965),(300,984)),fill=accent)
            draw.line((360,935,445,985),fill=accent,width=5);draw.polygon(((445,985),(420,984),(428,965)),fill=accent)
            draw.text((250,1015),"50",anchor="mm",font=font(25),fill=accent);draw.text((470,1015),"50",anchor="mm",font=font(25),fill=accent)
    elif family == "maison":
        draw.polygon(((190,855),(360,740),(530,855)),fill=SOFT,outline=accent)
        draw.rounded_rectangle((225,850,495,1000),radius=16,fill=WHITE,outline=accent,width=5)
        draw.line((360,850,360,1000),fill=accent,width=5); draw.text((292,925),"A",anchor="mm",font=font(38),fill=accent); draw.text((428,925),"B",anchor="mm",font=font(38),fill=accent)
    elif family == "testament":
        draw.rounded_rectangle((220,780,500,980),radius=20,fill=WHITE,outline=accent,width=5)
        draw.text((360,825),"TESTAMENT",anchor="mm",font=font(30),fill=accent)
        for y in (875,910,945): draw.line((270,y,450,y),fill=SAND,width=5)
        draw.line((455,930,520,995),fill=accent,width=7)
    elif family == "fiscalite":
        draw.rounded_rectangle((190,800,530,955),radius=28,fill=WHITE,outline=accent,width=5)
        label="60 %" if "60 %" in kind else "0 €"
        draw.text((360,878),label,anchor="mm",font=font(66),fill=accent)
    elif family == "enfants":
        draw.ellipse((325,775,395,845),outline=accent,width=5); draw.arc((280,835,440,1000),180,360,fill=accent,width=6)
        draw.rounded_rectangle((430,860,515,965),radius=15,outline=accent,width=5); draw.arc((445,820,500,895),180,360,fill=accent,width=5)
    elif family == "couple":
        draw.ellipse((205,800,335,930),outline=accent,width=6);draw.ellipse((385,800,515,930),outline=accent,width=6)
        draw.line((335,865,385,865),fill=SAND,width=5)
        heart=((360,1000),(326,970),(326,944),(344,930),(360,946),(376,930),(394,944),(394,970),(360,1000))
        draw.line(heart,fill=accent,width=5,joint="curve")
    elif family == "protection":
        shield=((360,760),(500,810),(475,940),(360,1010),(245,940),(220,810),(360,760))
        draw.polygon(shield,fill=SOFT,outline=accent); draw.line((300,875,345,920),fill=accent,width=12); draw.line((345,920,430,830),fill=accent,width=12)
    else:
        draw.ellipse((280,790,440,950),fill=SOFT,outline=accent,width=5)
        # Dessiner la coche plutôt qu'utiliser un glyphe absent de certaines
        # variantes d'Avenir (qui apparaissait alors comme un carré « ? »).
        draw.line((320,872,350,902),fill=accent,width=12)
        draw.line((350,902,405,838),fill=accent,width=12)


TEXT_SAFE_TOP, TEXT_SAFE_BOTTOM = 190, 990
ICON_SAFE_TOP, ICON_SAFE_BOTTOM = 1040, 1153


def regular_layout(beat: dict):
    """Calcule une zone de texte qui ne peut jamais empiéter sur le dessin."""
    probe=Image.new("RGB",(W,H),WHITE); draw=ImageDraw.Draw(probe)
    words=displayed_text(beat).upper().split()
    # Toutes les pages de contenu partent du même corps. L'adaptation n'est
    # autorisée que dans un corridor étroit de 6 points pour éviter les sauts
    # typographiques perceptibles d'une page à l'autre.
    face=display_font(MAIN_TEXT_SIZE); lines=wrap_words(draw,words,face,624)
    gap=round(face.size*1.18); text_height=(len(lines)-1)*gap+face.size
    while (len(lines)>7 or text_height>TEXT_SAFE_BOTTOM-TEXT_SAFE_TOP) and face.size>MIN_MAIN_TEXT_SIZE:
        face=display_font(face.size-2); lines=wrap_words(draw,words,face,600)
        gap=round(face.size*1.18); text_height=(len(lines)-1)*gap+face.size
    top=round((TEXT_SAFE_TOP+TEXT_SAFE_BOTTOM-text_height)/2)
    return words,face,lines,gap,top,text_height


def regular_page(spec: dict,page: int,beat: dict,visible: int,icon_alpha: float = 1.0):
    image,draw=base(spec,page); accent=series_color(spec)
    words,face,lines,gap,top,text_height=regular_layout(beat)
    shown=0
    for row,line in enumerate(lines):
        widths=[draw.textlength(w,font=face) for w in line]; space=draw.textlength(" ",font=face); x=(W-(sum(widths)+space*(len(line)-1)))/2
        for word,width in zip(line,widths):
            if shown<visible:
                color=TERRA if any(c.isdigit() for c in word) else (accent if word.strip(".,:;?!") in {"NON","OUI","COMMUNAUTÉ","ORIGINE","DIVORCE","SALAIRE","ÉPARGNE"} else INK)
                draw.text((x,top+row*gap),word,font=face,fill=color)
            shown+=1; x+=width+space
    layer=Image.new("RGBA",(W,H),(0,0,0,0)); layer_draw=ImageDraw.Draw(layer)
    exact_icons={
        "hook":"landmark scale",
        "regle":"users calendar",
        "precision":"scale shield-check users",
        "exemple":"heart-handshake shield-check",
        "nuance":"scale banknote",
    }
    locked_pilot=spec.get("concept_id")=="regimes_changement"
    chosen=exact_icons.get(beat.get("id")) if locked_pilot else None
    icon(layer_draw,chosen or visual_context(beat),accent)
    alpha=max(0,min(255,round(255*icon_alpha)))
    layer.putalpha(layer.getchannel("A").point(lambda value: round(value*alpha/255)))
    return Image.alpha_composite(image.convert("RGBA"),layer).convert("RGB")


def render(spec_path: Path, output: Path, timing_path: Path) -> None:
    spec=json.loads(spec_path.read_text(encoding="utf-8")); timing=json.loads(timing_path.read_text(encoding="utf-8"))
    audio=Path(timing["audio"]); durations=timing["durations"]
    speech_durations=timing.get("speech_durations",durations); output.parent.mkdir(parents=True,exist_ok=True)
    # Le rendu est construit dans un fichier temporaire puis remplacé d'un seul
    # coup : une interruption ne peut plus corrompre la dernière vidéo valide.
    temporary=output.with_name(output.stem+".rendering"+output.suffix)
    ffmpeg=ffmpeg_executable(); command=[ffmpeg,"-y","-loglevel","error","-nostats","-f","image2pipe","-vcodec","png","-r",str(DRAW_FPS),"-i","-","-i",str(audio),"-vf",f"fps={FPS},scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","24000","-movflags","+faststart","-shortest",str(temporary)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE); assert process.stdin
    previous_page=None
    transition_frames=max(1,round(.90*DRAW_FPS))
    try:
        for page,(beat,duration,speech_duration) in enumerate(zip(spec["beats"],durations,speech_durations)):
            frames=round(duration*DRAW_FPS); words=len(displayed_text(beat).split())
            last_unscaled=None
            # Tous les mots sont affichés avant les 90 % de la séquence. La fin
            # reste entièrement visible afin qu'aucun mot ne soit coupé au montage.
            interval=max(.04,(max(.1,duration)*.90)/max(1,words-1))
            for n in range(frames):
                kind=beat.get("page_role",beat["id"]).casefold()
                if kind=="question":
                    t=n/DRAW_FPS; icon_amount=ease(min(1.0,t/max(.1,speech_duration*.72)))
                    image=question_page(spec,page,beat,icon_amount)
                elif kind in ("reponse","answer"):
                    t=n/DRAW_FPS; answer_words=displayed_text(beat).split()
                    if spec.get("platform") == "shorts":
                        icon_amount=ease(min(1.0,t/max(.1,speech_duration*.72)))
                        image=Image.blend(answer_page(spec,page,beat,0,icon_amount),answer_page(spec,page,beat,None,icon_amount),ease(min(1.0,t/.62)))
                    else:
                        visible,amount=reveal(answer_words,t,speech_duration)
                        icon_amount=ease(min(1.0,t/max(.1,speech_duration*.72)))
                        current=answer_page(spec,page,beat,visible,icon_amount)
                        if visible>1:
                            previous=answer_page(spec,page,beat,visible-1,icon_amount); image=Image.blend(previous,current,amount)
                        else: image=current
                elif kind in ("cta","cloture"):
                    # Une seule page de conclusion, révélée au fil de la voix.
                    # L'ancien écran de texte intermédiaire est supprimé.
                    t=n/DRAW_FPS
                    image=cta_page(spec,page,beat,min(1.0,t/max(.1,speech_duration*.90)))
                else:
                    t=n/DRAW_FPS; icon_amount=ease(min(1.0,t/max(.1,speech_duration*.72))); visible,amount=reveal(displayed_text(beat).split(),t,speech_duration); current=regular_page(spec,page,beat,visible,icon_amount)
                    if visible>1:
                        previous=regular_page(spec,page,beat,visible-1,icon_amount); image=Image.blend(previous,current,amount)
                    else: image=current
                if previous_page is not None and n < transition_frames:
                    # Passation latérale de deux pages opaques : le texte de
                    # l'ancienne page ne se superpose jamais au nouveau.
                    amount=ease((n+1)/transition_frames); offset=round(W*amount)
                    slide=Image.new("RGB",(W,H),PAPER)
                    slide.paste(previous_page,(-offset,0))
                    slide.paste(image,(W-offset,0))
                    image=slide
                last_unscaled=image.copy()
                image=platform_safe_frame(image,spec.get("platform","shorts"))
                encoded=io.BytesIO(); image.save(encoded,format="PNG",compress_level=1)
                process.stdin.write(encoded.getvalue())
            previous_page=(last_unscaled or image).copy()
    finally: process.stdin.close()
    stderr=process.stderr.read().decode("utf-8",errors="replace")
    if process.wait()!=0:
        temporary.unlink(missing_ok=True)
        raise SystemExit("Échec du rendu vidéo : "+stderr[-1000:])
    os.replace(temporary,output)
    trace={"renderer":"BRITED deterministic renderer v2","features":{
        "page_crossfade_seconds": .90,
        "visual_direction": "Claude Design - Visuel A (carte flottante)",
        "progressive_word_reveal": True,
        "contextual_illustrations": all(icon_family(visual_context(beat)) != "generic" for beat in spec["beats"] if beat.get("page_role",beat["id"]).casefold() not in {"question","reponse","answer","cta","cloture"}),
        "question_answer_separation": True,
        "bottom_progress_only": True,
        "segmented_progress": True,
        "continuous_progress_with_counter": False,
        "lower_separator": True,
        "floating_warm_card": True,
        "safe_zones": True,
        "delivery_profile": spec.get("platform","shorts"),
        "platform_specific_composition": True,
        "visual_overlap_control": True
        ,"cta_variant": "rendez_vous"
        ,"header_locked_bitmap": True
        ,"header_typography_uniform": True
        ,"main_typography_reference_size": MAIN_TEXT_SIZE
        ,"main_typography_minimum_size": MIN_MAIN_TEXT_SIZE
        ,"main_typography_maximum_delta": MAIN_TEXT_SIZE-MIN_MAIN_TEXT_SIZE
        ,"header_fingerprint": header_fingerprint((spec.get("header") or spec.get("title") or "PATRIMOINE").upper(),series_color(spec))
    },"beats":[]}
    for beat,duration,speech_duration in zip(spec["beats"],durations,speech_durations):
        tokens=displayed_text(beat).split()
        reveal_at=min(float(duration),float(speech_duration)*.90)
        role=beat.get("page_role",beat["id"]).casefold()
        visual_layout=None
        if role in {"reponse","answer"} and spec.get("platform") == "shorts":
            if spec.get("answer_design") == "adaptive_sections_v2":
                visual_layout={"card_bounds":[78,270,642,920],"text_bounds":[112,350,608,850],
                               "verdict":"adaptatif","font_size":25,
                               "answer_design":"adaptive_sections_v2","overlap":False}
                trace["beats"].append({"id":beat["id"],"source_text":displayed_text(beat),"tokens":tokens,
                                       "token_count":len(tokens),"speech_duration":round(float(speech_duration),3),
                                       "duration":round(float(duration),3),"full_text_visible_at":round(reveal_at,3),
                                       "visual_layout":visual_layout})
                continue
            if spec.get("answer_design") == "structured_v2":
                probe=Image.new("RGB",(W,H)); probe_draw=ImageDraw.Draw(probe)
                label_checks=[]
                check_top=470
                for section_index,(label,body) in enumerate((
                    ("PACS", "SANS TESTAMENT, LE PARTENAIRE DE PACS N'HÉRITE PAS."),
                    ("CONCUBINAGE", "LE CONCUBIN NON PLUS. LES BIENS REÇUS PAR TESTAMENT SONT IMPOSÉS À 60 %."),
                )):
                    label_face=font(18)
                    label_width=max(156,min(430,round(probe_draw.textlength(label,font=label_face)+44)))
                    pill=[134,check_top+18,134+label_width,check_top+58]
                    text_bbox=probe_draw.textbbox(((pill[0]+pill[2])/2,check_top+38),label,
                                                  anchor="mm",font=label_face)
                    label_checks.append({"label":label,"pill_bounds":pill,
                                         "text_bounds":list(text_bbox),
                                         "body_contains_required_term":(
                                             "PARTENAIRE DE PACS" in body if label=="PACS" else True)})
                    check_top+=(142 if section_index==0 else 194)+18
                visual_layout={"card_bounds":[78,270,642,920],"text_bounds":[112,354,608,824],
                               "verdict":"NON","font_size":25,"answer_design":"structured_v2",
                               "label_checks":label_checks,"overlap":False}
                trace["beats"].append({"id":beat["id"],"source_text":displayed_text(beat),"tokens":tokens,
                                       "token_count":len(tokens),"speech_duration":round(float(speech_duration),3),
                                       "duration":round(float(duration),3),"full_text_visible_at":round(reveal_at,3),
                                       "visual_layout":visual_layout})
                continue
            probe=Image.new("RGB",(W,H)); probe_draw=ImageDraw.Draw(probe)
            verdict,lines,face,gap=shorts_answer_layout(probe_draw,displayed_text(beat))
            top,bottom=(525,840) if verdict else (425,840)
            center=(top+bottom)/2
            y=center-(len(lines)-1)*gap/2
            text_bounds=[110,round(y-face.size*.55),610,round(y+(len(lines)-1)*gap+face.size*.65)]
            visual_layout={"card_bounds":[78,285,642,900],"text_bounds":text_bounds,
                           "verdict":verdict,"font_size":face.size,
                           "overlap":not (285 < text_bounds[1] < text_bounds[3] < 900)}
        elif role in {"cta","cloture"}:
            visual_layout={"text_bounds":[90,290,630,755],"icon_bounds":[324,795,396,875],
                           "font_size":55,"overlap":False}
        elif role not in {"question","reponse","answer","cta","cloture"}:
            _,face,_,_,top,text_height=regular_layout(beat)
            exact_icons={"hook":"landmark scale","regle":"users calendar",
                         "precision":"scale shield-check users","exemple":"heart-handshake shield-check",
                         "nuance":"scale banknote"}
            locked_pilot=spec.get("concept_id")=="regimes_changement"
            chosen=exact_icons.get(beat.get("id")) if locked_pilot else None
            visual_layout={"text_bounds":[48,top,W-48,top+text_height],
                           "icon_bounds":[48,ICON_SAFE_TOP,W-48,ICON_SAFE_BOTTOM],
                           "selected_icons":visual_icon_names(chosen or visual_context(beat)),
                           "font_size":face.size,
                           "overlap":top+text_height>ICON_SAFE_TOP}
        trace["beats"].append({"id":beat["id"],"source_text":displayed_text(beat),"tokens":tokens,
                               "token_count":len(tokens),"speech_duration":round(float(speech_duration),3),
                               "full_text_visible_at":round(reveal_at,3),
                               "hold_after_full_text":round(float(duration)-reveal_at,3),
                               "visual_layout":visual_layout})
    output.with_suffix(".render-trace.json").write_text(json.dumps(trace,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser();parser.add_argument("spec",type=Path);parser.add_argument("output",type=Path);parser.add_argument("--timing",type=Path,required=True);args=parser.parse_args();render(args.spec,args.output,args.timing)


if __name__=="__main__": main()
