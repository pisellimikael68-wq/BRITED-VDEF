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
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 720, 1280, 60
DRAW_FPS = 15  # animation fluide, sortie normalisée à 60 i/s par FFmpeg
FONT = "/System/Library/Fonts/Avenir Next Condensed.ttc"
PAPER = (250, 246, 238); INK = (38, 33, 29); TERRA = (169, 77, 31)
SAND = (238, 220, 198); SOFT = (249, 233, 225); WHITE = (255, 252, 247)
MUTED = (107, 91, 78)
SERIES = {"fiscalite": (111,78,55), "immobilier": (201,111,74),
          "juridique": (217,154,43), "finance": (36,87,214)}


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


def font(size: int): return ImageFont.truetype(FONT, size)
def ease(x: float) -> float:
    x = max(0.0, min(1.0, x)); return x*x*(3-2*x)


def fade_color(background, foreground, amount: float):
    amount=max(0.0,min(1.0,amount))
    return tuple(round(a+(b-a)*amount) for a,b in zip(background,foreground))


def series_color(spec: dict) -> tuple[int, int, int]:
    return SERIES.get(spec.get("serie", "juridique"), SERIES["juridique"])


def wrap_words(draw, words, face, max_width=600):
    lines=[]; line=[]
    for word in words:
        trial=" ".join(line+[word])
        if line and draw.textlength(trial,font=face)>max_width:
            lines.append(line); line=[word]
        else: line.append(word)
    if line: lines.append(line)
    return lines


def base(spec: dict, page: int):
    image=Image.new("RGB",(W,H),PAPER); draw=ImageDraw.Draw(image)
    accent=series_color(spec)
    title=(spec.get("header") or spec.get("title") or "À RETENIR").upper()
    face=font(44)
    while draw.textlength(title,font=face)>620 and face.size>24: face=font(face.size-2)
    title_width=draw.textlength(title,font=face)
    draw.rounded_rectangle((max(24,360-title_width/2-24),68,min(696,360+title_width/2+24),154),radius=24,fill=(247,235,224))
    draw.text((360,112),title,anchor="mm",font=face,fill=INK)
    draw.line((173,142,547,142),fill=TERRA,width=3)
    draw.line((32,228,32,730),fill=SAND,width=3)
    total=len(spec["beats"])
    draw.rectangle((55,1108,666,1114),fill=SAND)
    draw.rectangle((55,1108,55+round(611*(page+1)/total),1114),fill=accent)
    draw.text((657,1141),f"{page+1:02d} / {total:02d}",anchor="ra",font=font(19),fill=TERRA)
    draw.line((160,1190,560,1190),fill=(218,190,169),width=2)
    draw.text((360,1217),spec.get("disclaimer","Information générale • pas un conseil personnalisé"),anchor="mm",font=font(16),fill=MUTED)
    return image,draw


def question_page(spec: dict,page: int,beat: dict):
    image,draw=base(spec,page); accent=series_color(spec)
    draw.rounded_rectangle((70,280,650,835),radius=34,fill=WHITE,outline=SAND,width=4)
    draw.rounded_rectangle((249,316,471,357),radius=20,fill=SOFT)
    draw.text((360,337),"À VOUS DE JOUER",anchor="mm",font=font(25),fill=TERRA)
    question=re.sub(r"(?:[,;:]?\s*(?:OUI\s*(?:/|OU)\s*NON)\s*[.!]?)$","",beat["narration"].upper()).strip()
    words=question.split()
    face=font(43); lines=wrap_words(draw,words,face,500)
    while len(lines)>4 and face.size>30:
        face=font(face.size-2); lines=wrap_words(draw,words,face,500)
    gap=54
    # Centre optiquement la question dans l'espace réellement disponible entre
    # l'intitulé et les choix. Le nombre de lignes ne déplace plus le bloc.
    y=500-(len(lines)-1)*gap/2
    for line in lines:
        draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=INK); y+=gap
    draw.rounded_rectangle((112,650,350,717),radius=20,fill=SOFT,outline=accent,width=3)
    draw.text((231,684),"OUI",anchor="mm",font=font(30),fill=accent)
    draw.rounded_rectangle((371,650,609,717),radius=20,fill=SOFT,outline=INK,width=3)
    draw.text((490,684),"NON",anchor="mm",font=font(30),fill=INK)
    draw.text((360,778),"LA RÉPONSE ARRIVE…",anchor="mm",font=font(21),fill=MUTED)
    return image


def answer_page(spec: dict,page: int,beat: dict,visible: int | None = None):
    image,draw=base(spec,page); accent=series_color(spec)
    answer_words=beat["narration"].upper().strip().split()
    if spec.get("platform") == "shorts":
        face=font(40); lines=wrap_words(draw,answer_words[1:],face,490)
        while len(lines)>5 and face.size>28:
            face=font(face.size-2); lines=wrap_words(draw,answer_words[1:],face,490)
        box_bottom=max(720,min(900,555+(len(lines)-1)*(face.size+11)+95))
        draw.rounded_rectangle((78,285,642,box_bottom),radius=34,fill=WHITE,outline=SAND,width=3)
        if visible == 0:
            return image
        first = answer_words[0].rstrip(".:;!?") if answer_words else "NON"
        remainder = answer_words[1:]
        draw.rounded_rectangle((255,330,465,415),radius=28,fill=SOFT,outline=accent,width=3)
        draw.text((360,372),first,anchor="mm",font=font(50),fill=accent)
        lines=wrap_words(draw,remainder,face,490)
        gap=face.size+11; y=545-(len(lines)-1)*gap/2
        for line in lines:
            draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=INK); y+=gap
        return image
    # La mise en page est calculée sur la réponse complète. Pendant le fondu,
    # les nouveaux mots occupent donc immédiatement leur position définitive :
    # plus aucun tassement ni recentrage saccadé à chaque apparition.
    full_words=answer_words
    face=font(52); lines=wrap_words(draw,full_words,face,455)
    while len(lines)>4 and face.size>36:
        face=font(face.size-2); lines=wrap_words(draw,full_words,face,455)
    box_bottom=max(660,min(890,480+(len(lines)-1)*(face.size+12)/2+face.size+95))
    draw.rounded_rectangle((92,300,628,box_bottom),radius=34,fill=WHITE,outline=SAND,width=3)
    gap=face.size+12; y=480-(len(lines)-1)*gap/2
    shown=0
    for line in lines:
        widths=[draw.textlength(word,font=face) for word in line]
        space=draw.textlength(" ",font=face)
        x=(W-(sum(widths)+space*(len(line)-1)))/2
        for word,width in zip(line,widths):
            if visible is None or shown < visible:
                draw.text((x,y),word,anchor="lm",font=face,fill=accent)
            shown+=1; x+=width+space
        y+=gap
    return image


def cta_page(spec: dict,page: int,beat: dict,progress: float = 1.0):
    image,draw=base(spec,page); accent=series_color(spec)
    draw.rounded_rectangle((72,275,648,880),radius=36,fill=WHITE,outline=SAND,width=3)
    if True:
        question_alpha=ease(progress/.40)
        button_alpha=ease((progress-.34)/.34)
        destination_alpha=ease((progress-.66)/.26)
        question="VOUS SOUHAITEZ FAIRE LE POINT SUR VOTRE SITUATION ?".split()
        face=font(40); lines=wrap_words(draw,question,face,500); y=405-(len(lines)-1)*26
        for line in lines:
            draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=fade_color(WHITE,INK,question_alpha)); y+=49
        button_fill=fade_color(WHITE,SOFT,button_alpha)
        button_stroke=fade_color(WHITE,accent,button_alpha)
        draw.rounded_rectangle((120,570,600,690),radius=30,fill=button_fill,outline=button_stroke,width=4)
        draw.text((360,630),"PRENEZ RENDEZ-VOUS",anchor="mm",font=font(42),fill=button_stroke)
        destination="VIA LE LIEN DANS MA BIO"
        destination_color=fade_color(WHITE,TERRA,destination_alpha)
        draw.text((360,765),destination,anchor="mm",font=font(29),fill=destination_color)
        # Petit calendrier chaleureux, dessiné dans la même carte et révélé
        # avec l'appel à l'action pour renforcer l'intention de rendez-vous.
        draw.rounded_rectangle((305,815,415,905),radius=14,fill=WHITE,outline=destination_color,width=4)
        draw.line((306,844,414,844),fill=destination_color,width=4)
        draw.line((331,802,331,829),fill=destination_color,width=5)
        draw.line((389,802,389,829),fill=destination_color,width=5)
        draw.text((360,875),"✓",anchor="mm",font=font(40),fill=destination_color)
        return image
    draw.text((360,365),"LE SAVIEZ-VOUS ?",anchor="mm",font=font(55),fill=INK)
    # Centre géométrique des actions entre le bas du titre (425) et le haut
    # du cartouche final (738) : aucun CTA ne flotte vers le bas.
    boxes=[(91,505,251,660),(280,505,440,660),(469,505,629,660)]
    for i,box in enumerate(boxes): draw.rounded_rectangle(box,radius=25,fill=SOFT if i!=1 else WHITE,outline=accent if i!=1 else TERRA,width=3)
    draw.line((137,549,207,549),fill=accent,width=5);draw.polygon(((207,549),(190,538),(190,560)),fill=accent)
    draw.text((171,611),"COMMENTER",anchor="mm",font=font(18),fill=accent)
    draw.rounded_rectangle((337,519,383,578),radius=7,outline=TERRA,width=4);draw.polygon(((341,570),(360,557),(379,570)),fill=TERRA)
    draw.text((360,611),"PARTAGEZ",anchor="mm",font=font(18),fill=TERRA)
    draw.ellipse((523,519,559,555),outline=accent,width=4);draw.arc((510,548,572,597),180,360,fill=accent,width=4)
    draw.line((579,530,579,562),fill=TERRA,width=4);draw.line((563,546,595,546),fill=TERRA,width=4)
    draw.text((549,611),"ABONNEZ-VOUS",anchor="mm",font=font(19),fill=accent)
    draw.rounded_rectangle((129,738,591,822),radius=22,fill=(247,235,224))
    draw.text((360,766),"POUR MIEUX COMPRENDRE",anchor="mm",font=font(22),fill=TERRA)
    draw.text((360,798),"ET PROTÉGER VOTRE PATRIMOINE",anchor="mm",font=font(20),fill=INK)
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
        ("couple", ("mariage", "couple", "époux", "pacs", "concubin", "partenaire", "personnes", "silhouette")),
        ("assurance_vie", ("clause bénéficiaire", "bénéficiaire", "contrat", "capital", "rachat", "désignation", "acceptation", "abattement", "assureur", "courrier", "enveloppe")),
        ("menage", ("charges du mariage", "dettes du ménage", "facture", "loyer", "école")),
        ("testament", ("testament", "hérit", "décès", "succession", "légué", "parchemin")),
        ("fiscalite", ("fiscal", "taxable", "imposée", "taux", "20 %", "31,25 %", "droits de succession", "exonération", "euro barré")),
        ("enfants", ("enfant", "réserve héréditaire")),
        ("preuve", ("preuve", "justificatif", "relevé", "dossier", "origine des fonds", "présumé")),
        ("loi", ("article", "code", "juridique", "livre de loi", "balance", "§", "notaire", "notarié", "homologation", "judiciaire", "tribunal", "tiers", "s'opposer")),
        ("maison", ("maison", "résidence", "indivision", "propriétaire", "deux clés")),
        ("banque", ("compte bancaire", "salaire", "épargne")),
        ("masses", ("3 masses", "trois masses")),
        ("partage", ("liquidation", "partage")),
        ("protection", ("protection", "protégé", "abri", "bouclier", "cadenas brisé")),
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
    value=kind.casefold(); names=[]
    rules=(
        (("clause bénéficiaire","bénéficiaire","contrat","capital","rachat","désignation","acceptation"),("file-signature","user-round-check","badge-euro")),
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
    count=len(names); card=150; gap=24
    total=count*card+(count-1)*gap; left=(W-total)//2; y=805
    for index,name in enumerate(names):
        x=left+index*(card+gap); fill=WHITE if index%2==0 else SOFT
        stroke=accent if index%2==0 else TERRA
        draw.rounded_rectangle((x,y,x+card,y+card),radius=30,fill=fill,outline=stroke,width=5)
        glyph=chr(int(_LUCIDE_POINTS[name])); glyph_font=ImageFont.truetype(str(LUCIDE_FONT),82)
        draw.text((x+card/2,y+card/2),glyph,anchor="mm",font=glyph_font,fill=stroke)
        if index<count-1:
            cx=x+card+gap/2; draw.line((cx-7,y+card/2,cx+7,y+card/2),fill=SAND,width=5)
    return True


def icon(draw,kind,accent):
    if library_icon(draw,kind,accent): return
    family=icon_family(kind)
    if family == "menage":
        # Educational visual for current household expenses: a home, a bill
        # and a paid check. Keep the 50/50 split for the following page only.
        draw.polygon(((225,845),(360,755),(495,845)),outline=accent,fill=SOFT)
        draw.rounded_rectangle((250,840,470,965),radius=12,fill=WHITE,outline=accent,width=5)
        draw.rounded_rectangle((390,865,445,965),radius=6,outline=TERRA,width=4)
        draw.rounded_rectangle((105,825,245,930),radius=18,fill=WHITE,outline=TERRA,width=4)
        draw.text((175,875),"€",anchor="mm",font=font(48),fill=TERRA)
        draw.line((135,910,170,935),fill=accent,width=6)
        draw.line((170,935,225,880),fill=accent,width=6)
    elif family == "banque":
        draw.rounded_rectangle((115,800,315,905),radius=20,fill=WHITE,outline=accent,width=4)
        draw.text((215,853),"€",anchor="mm",font=font(58),fill=TERRA)
        draw.line((340,852,445,852),fill=TERRA,width=5);draw.polygon(((445,852),(428,842),(428,862)),fill=TERRA)
        draw.rounded_rectangle((478,800,582,905),radius=17,outline=accent,width=5)
        draw.arc((500,815,560,875),180,360,fill=TERRA,width=4)
        draw.line((500,846,500,884),fill=TERRA,width=4);draw.line((560,846,560,884),fill=TERRA,width=4)
    elif family == "masses":
        boxes=((86,815,246,916),(280,785,440,946),(474,815,634,916))
        for index,box in enumerate(boxes):
            draw.rounded_rectangle(box,radius=22,fill=WHITE if index!=1 else SOFT,outline=accent if index!=2 else TERRA,width=4)
        draw.text((166,866),"A",anchor="mm",font=font(34),fill=INK)
        draw.text((360,850),"COMMUN",anchor="mm",font=font(25),fill=accent)
        draw.text((554,866),"B",anchor="mm",font=font(34),fill=INK)
        draw.line((246,866,280,866),fill=TERRA,width=4); draw.line((440,866,474,866),fill=TERRA,width=4)
    elif family in {"preuve", "partage", "loi"}:
        draw.rounded_rectangle((245,785,475,920),radius=18,fill=WHITE,outline=accent,width=5)
        for y in (825,855,885): draw.line((280,y,440,y),fill=SAND,width=5)
        if family == "preuve":
            draw.ellipse((405,875,490,960),outline=TERRA,width=6); draw.line((468,940,520,992),fill=TERRA,width=7)
        elif family == "loi":
            draw.text((360,855),"§",anchor="mm",font=font(58),fill=TERRA)
        elif family == "partage":
            draw.line((360,935,275,985),fill=TERRA,width=5);draw.polygon(((275,985),(292,965),(300,984)),fill=TERRA)
            draw.line((360,935,445,985),fill=TERRA,width=5);draw.polygon(((445,985),(420,984),(428,965)),fill=TERRA)
            draw.text((250,1015),"50",anchor="mm",font=font(25),fill=accent);draw.text((470,1015),"50",anchor="mm",font=font(25),fill=TERRA)
    elif family == "maison":
        draw.polygon(((190,855),(360,740),(530,855)),fill=SOFT,outline=accent)
        draw.rounded_rectangle((225,850,495,1000),radius=16,fill=WHITE,outline=accent,width=5)
        draw.line((360,850,360,1000),fill=TERRA,width=5); draw.text((292,925),"A",anchor="mm",font=font(38),fill=accent); draw.text((428,925),"B",anchor="mm",font=font(38),fill=TERRA)
    elif family == "testament":
        draw.rounded_rectangle((220,780,500,980),radius=20,fill=WHITE,outline=accent,width=5)
        draw.text((360,825),"TESTAMENT",anchor="mm",font=font(30),fill=TERRA)
        for y in (875,910,945): draw.line((270,y,450,y),fill=SAND,width=5)
        draw.line((455,930,520,995),fill=accent,width=7)
    elif family == "fiscalite":
        draw.rounded_rectangle((190,800,530,955),radius=28,fill=WHITE,outline=accent,width=5)
        label="60 %" if "60 %" in kind else "0 €"
        draw.text((360,878),label,anchor="mm",font=font(66),fill=TERRA)
    elif family == "enfants":
        draw.ellipse((325,775,395,845),outline=accent,width=5); draw.arc((280,835,440,1000),180,360,fill=accent,width=6)
        draw.rounded_rectangle((430,860,515,965),radius=15,outline=TERRA,width=5); draw.arc((445,820,500,895),180,360,fill=TERRA,width=5)
    elif family == "couple":
        draw.ellipse((205,800,335,930),outline=accent,width=6);draw.ellipse((385,800,515,930),outline=TERRA,width=6)
        draw.line((335,865,385,865),fill=SAND,width=5)
        heart=((360,1000),(326,970),(326,944),(344,930),(360,946),(376,930),(394,944),(394,970),(360,1000))
        draw.line(heart,fill=TERRA,width=5,joint="curve")
    elif family == "protection":
        shield=((360,760),(500,810),(475,940),(360,1010),(245,940),(220,810),(360,760))
        draw.polygon(shield,fill=SOFT,outline=accent); draw.line((300,875,345,920),fill=TERRA,width=12); draw.line((345,920,430,830),fill=TERRA,width=12)
    else:
        draw.ellipse((280,790,440,950),fill=SOFT,outline=accent,width=5)
        # Dessiner la coche plutôt qu'utiliser un glyphe absent de certaines
        # variantes d'Avenir (qui apparaissait alors comme un carré « ? »).
        draw.line((320,872,350,902),fill=accent,width=12)
        draw.line((350,902,405,838),fill=accent,width=12)


TEXT_SAFE_TOP, TEXT_SAFE_BOTTOM = 210, 690
ICON_SAFE_TOP, ICON_SAFE_BOTTOM = 740, 1040


def regular_layout(beat: dict):
    """Calcule une zone de texte qui ne peut jamais empiéter sur le dessin."""
    probe=Image.new("RGB",(W,H),WHITE); draw=ImageDraw.Draw(probe)
    words=beat["narration"].upper().split()
    size=int(beat.get("font_size") or (38 if len(words)>25 else 43)); face=font(size)
    lines=wrap_words(draw,words,face,600)
    gap=max(38,min(57,face.size+9)); text_height=(len(lines)-1)*gap+face.size
    while (len(lines)>8 or text_height>TEXT_SAFE_BOTTOM-TEXT_SAFE_TOP) and face.size>27:
        face=font(face.size-2); lines=wrap_words(draw,words,face,600)
        gap=max(38,min(57,face.size+9)); text_height=(len(lines)-1)*gap+face.size
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
    icon(layer_draw,visual_context(beat),accent)
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
    ffmpeg=ffmpeg_executable(); command=[ffmpeg,"-y","-loglevel","error","-nostats","-f","image2pipe","-vcodec","png","-r",str(DRAW_FPS),"-i","-","-i",str(audio),"-vf",f"fps={FPS},scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart","-shortest",str(temporary)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE); assert process.stdin
    previous_page=None
    transition_frames=max(1,round(.24*DRAW_FPS))
    try:
        for page,(beat,duration,speech_duration) in enumerate(zip(spec["beats"],durations,speech_durations)):
            frames=round(duration*DRAW_FPS); words=len(beat["narration"].split())
            # Tous les mots sont affichés avant les 90 % de la séquence. La fin
            # reste entièrement visible afin qu'aucun mot ne soit coupé au montage.
            interval=max(.04,(max(.1,duration)*.90)/max(1,words-1))
            for n in range(frames):
                kind=beat.get("page_role",beat["id"]).casefold()
                if kind=="question": image=question_page(spec,page,beat)
                elif kind in ("reponse","answer"):
                    t=n/DRAW_FPS; answer_words=beat["narration"].split()
                    if spec.get("platform") == "shorts":
                        image=Image.blend(answer_page(spec,page,beat,0),answer_page(spec,page,beat,None),ease(min(1.0,t/.62)))
                    else:
                        visible,amount=reveal(answer_words,t,speech_duration)
                        current=answer_page(spec,page,beat,visible)
                        if visible>1:
                            previous=answer_page(spec,page,beat,visible-1); image=Image.blend(previous,current,amount)
                        else: image=current
                elif kind in ("cta","cloture"):
                    # Une seule page de conclusion, révélée au fil de la voix.
                    # L'ancien écran de texte intermédiaire est supprimé.
                    t=n/DRAW_FPS
                    image=cta_page(spec,page,beat,min(1.0,t/max(.1,speech_duration*.90)))
                else:
                    t=n/DRAW_FPS; icon_amount=ease(min(1.0,t/max(.1,speech_duration*.72))); visible,amount=reveal(beat["narration"].split(),t,speech_duration); current=regular_page(spec,page,beat,visible,icon_amount)
                    if visible>1:
                        previous=regular_page(spec,page,beat,visible-1,icon_amount); image=Image.blend(previous,current,amount)
                    else: image=current
                if previous_page is not None and n < transition_frames:
                    image=Image.blend(previous_page,image,ease((n+1)/transition_frames))
                encoded=io.BytesIO(); image.save(encoded,format="PNG",compress_level=1)
                process.stdin.write(encoded.getvalue())
            previous_page=image.copy()
    finally: process.stdin.close()
    stderr=process.stderr.read().decode("utf-8",errors="replace")
    if process.wait()!=0:
        temporary.unlink(missing_ok=True)
        raise SystemExit("Échec du rendu vidéo : "+stderr[-1000:])
    os.replace(temporary,output)
    trace={"renderer":"BRITED deterministic renderer v2","features":{
        "page_crossfade_seconds": .90,
        "progressive_word_reveal": True,
        "contextual_illustrations": all(icon_family(visual_context(beat)) != "generic" for beat in spec["beats"] if beat.get("page_role",beat["id"]).casefold() not in {"question","reponse","answer","cta","cloture"}),
        "question_answer_separation": True,
        "bottom_progress_only": True,
        "safe_zones": True,
        "visual_overlap_control": True,
        "cta_variant": "rendez_vous"
    },"beats":[]}
    for beat,duration,speech_duration in zip(spec["beats"],durations,speech_durations):
        tokens=beat["narration"].split()
        reveal_at=min(float(duration),float(speech_duration)*.90)
        role=beat.get("page_role",beat["id"]).casefold()
        visual_layout=None
        if role not in {"question","reponse","answer","cta","cloture"}:
            _,face,_,_,top,text_height=regular_layout(beat)
            visual_layout={"text_bounds":[60,top,W-60,top+text_height],
                           "icon_bounds":[80,ICON_SAFE_TOP,W-80,ICON_SAFE_BOTTOM],
                           "selected_icons":visual_icon_names(visual_context(beat)),
                           "font_size":face.size,
                           "overlap":top+text_height>ICON_SAFE_TOP}
        trace["beats"].append({"id":beat["id"],"source_text":beat["narration"],"tokens":tokens,
                               "token_count":len(tokens),"speech_duration":round(float(speech_duration),3),
                               "full_text_visible_at":round(reveal_at,3),
                               "hold_after_full_text":round(float(duration)-reveal_at,3),
                               "visual_layout":visual_layout})
    output.with_suffix(".render-trace.json").write_text(json.dumps(trace,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser();parser.add_argument("spec",type=Path);parser.add_argument("output",type=Path);parser.add_argument("--timing",type=Path,required=True);args=parser.parse_args();render(args.spec,args.output,args.timing)


if __name__=="__main__": main()
