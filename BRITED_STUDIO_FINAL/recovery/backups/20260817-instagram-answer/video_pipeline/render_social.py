#!/usr/bin/env python3
"""Rendu social BRITED générique conforme aux pilotes TikTok/Instagram validés."""

from __future__ import annotations

import argparse
import io
import json
import math
import os
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
    words=beat["narration"].upper().split()
    face=font(43); lines=wrap_words(draw,words,face,500)
    while len(lines)>4 and face.size>30:
        face=font(face.size-2); lines=wrap_words(draw,words,face,500)
    y=405
    for line in lines:
        draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=INK); y+=54
    draw.rounded_rectangle((112,650,350,717),radius=20,fill=SOFT,outline=accent,width=3)
    draw.text((231,684),"OUI",anchor="mm",font=font(30),fill=accent)
    draw.rounded_rectangle((371,650,609,717),radius=20,fill=SOFT,outline=INK,width=3)
    draw.text((490,684),"NON",anchor="mm",font=font(30),fill=INK)
    draw.text((360,778),"LA RÉPONSE ARRIVE…",anchor="mm",font=font(21),fill=MUTED)
    return image


def answer_page(spec: dict,page: int,beat: dict):
    image,draw=base(spec,page); accent=series_color(spec)
    answer=beat["narration"].upper().strip()
    answer=answer.split(":",1)[-1].strip() if ":" in answer else answer
    draw.rounded_rectangle((92,300,628,660),radius=34,fill=WHITE,outline=SAND,width=3)
    draw.text((360,390),"LA RÉPONSE EST",anchor="mm",font=font(27),fill=TERRA)
    face=font(54); lines=wrap_words(draw,answer.split(),face,455)
    while len(lines)>4 and face.size>36:
        face=font(face.size-2); lines=wrap_words(draw,answer.split(),face,455)
    gap=face.size+10; y=500-(len(lines)-1)*gap/2
    for line in lines:
        draw.text((360,y)," ".join(line),anchor="mm",font=face,fill=accent); y+=gap
    return image


def cta_page(spec: dict,page: int,beat: dict):
    image,draw=base(spec,page); accent=series_color(spec)
    draw.rounded_rectangle((72,275,648,880),radius=36,fill=WHITE,outline=SAND,width=3)
    draw.text((360,365),"LE SAVIEZ-VOUS ?",anchor="mm",font=font(55),fill=INK)
    boxes=[(91,555,251,710),(280,555,440,710),(469,555,629,710)]
    for i,box in enumerate(boxes): draw.rounded_rectangle(box,radius=25,fill=SOFT if i!=1 else WHITE,outline=accent if i!=1 else TERRA,width=3)
    draw.line((137,609,207,609),fill=accent,width=5);draw.polygon(((207,609),(190,598),(190,620)),fill=accent)
    first = "ENREGISTREZ" if spec.get("platform") == "reels" else "COMMENTEZ"
    draw.text((171,671),first,anchor="mm",font=font(18),fill=accent)
    draw.rounded_rectangle((337,579,383,638),radius=7,outline=TERRA,width=4);draw.polygon(((341,630),(360,617),(379,630)),fill=TERRA)
    draw.text((360,671),"PARTAGEZ",anchor="mm",font=font(18),fill=TERRA)
    draw.ellipse((523,579,559,615),outline=accent,width=4);draw.arc((510,608,572,657),180,360,fill=accent,width=4)
    draw.line((579,590,579,622),fill=TERRA,width=4);draw.line((563,606,595,606),fill=TERRA,width=4)
    draw.text((549,671),"ABONNEZ-VOUS",anchor="mm",font=font(19),fill=accent)
    draw.rounded_rectangle((129,758,591,822),radius=22,fill=(247,235,224))
    draw.text((360,778),"POUR MIEUX COMPRENDRE",anchor="mm",font=font(22),fill=TERRA)
    draw.text((360,804),"ET PROTÉGER VOTRE PATRIMOINE",anchor="mm",font=font(20),fill=INK)
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


def icon(draw,kind,accent):
    if any(x in kind for x in ("montant","argent","salaire","compte","épargne")):
        draw.rounded_rectangle((115,800,315,905),radius=20,fill=WHITE,outline=accent,width=4)
        draw.text((215,853),"€",anchor="mm",font=font(58),fill=TERRA)
        draw.line((340,852,445,852),fill=TERRA,width=5);draw.polygon(((445,852),(428,842),(428,862)),fill=TERRA)
        draw.ellipse((485,797,575,887),outline=accent,width=5)
    elif any(x in kind for x in ("mariage","époux","partage","divorce","commun")):
        draw.ellipse((205,800,335,930),outline=accent,width=6);draw.ellipse((385,800,515,930),outline=TERRA,width=6)
        draw.text((360,965),"50 / 50 ?",anchor="mm",font=font(30),fill=INK)
    else:
        draw.ellipse((280,790,440,950),fill=SOFT,outline=accent,width=5)
        draw.text((360,870),"✓",anchor="mm",font=font(76),fill=accent)


def regular_page(spec: dict,page: int,beat: dict,visible: int):
    image,draw=base(spec,page); accent=series_color(spec)
    words=beat["narration"].upper().split(); size=int(beat.get("font_size") or (38 if len(words)>25 else 43)); face=font(size)
    lines=wrap_words(draw,words,face,600); gap=49 if len(lines)>5 else 57; top=230 if len(lines)>5 else 270
    shown=0
    for row,line in enumerate(lines):
        widths=[draw.textlength(w,font=face) for w in line]; space=draw.textlength(" ",font=face); x=(W-(sum(widths)+space*(len(line)-1)))/2
        for word,width in zip(line,widths):
            if shown<visible:
                color=TERRA if any(c.isdigit() for c in word) else (accent if word.strip(".,:;?!") in {"NON","OUI","COMMUNAUTÉ","ORIGINE","DIVORCE","SALAIRE","ÉPARGNE"} else INK)
                draw.text((x,top+row*gap),word,font=face,fill=color)
            shown+=1; x+=width+space
    icon(draw,(beat.get("visual") or beat["narration"]).casefold(),accent)
    return image


def render(spec_path: Path, output: Path, timing_path: Path) -> None:
    spec=json.loads(spec_path.read_text(encoding="utf-8")); timing=json.loads(timing_path.read_text(encoding="utf-8"))
    audio=Path(timing["audio"]); durations=timing["durations"]; output.parent.mkdir(parents=True,exist_ok=True)
    # Le rendu est construit dans un fichier temporaire puis remplacé d'un seul
    # coup : une interruption ne peut plus corrompre la dernière vidéo valide.
    temporary=output.with_name(output.stem+".rendering"+output.suffix)
    ffmpeg=ffmpeg_executable(); command=[ffmpeg,"-y","-loglevel","error","-nostats","-f","image2pipe","-vcodec","png","-r",str(DRAW_FPS),"-i","-","-i",str(audio),"-vf",f"fps={FPS},scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-movflags","+faststart","-shortest",str(temporary)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE); assert process.stdin
    try:
        for page,(beat,duration) in enumerate(zip(spec["beats"],durations)):
            frames=round(duration*DRAW_FPS); words=len(beat["narration"].split())
            # Tous les mots sont affichés avant les 90 % de la séquence. La fin
            # reste entièrement visible afin qu'aucun mot ne soit coupé au montage.
            interval=max(.04,(max(.1,duration)*.90)/max(1,words-1))
            for n in range(frames):
                kind=beat.get("page_role",beat["id"]).casefold()
                if kind=="question": image=question_page(spec,page,beat)
                elif kind in ("reponse","answer"): image=answer_page(spec,page,beat)
                elif kind in ("cta","cloture"):
                    cta_words=beat["narration"].split(); t=n/DRAW_FPS; switch=action_start(cta_words,duration)
                    if t < switch:
                        visible,amount=reveal(cta_words,t,duration)
                        current=regular_page(spec,page,beat,visible)
                        if visible>1:
                            previous=regular_page(spec,page,beat,visible-1); image=Image.blend(previous,current,amount)
                        else: image=current
                    else:
                        image=cta_page(spec,page,beat)
                else:
                    t=n/DRAW_FPS; visible,amount=reveal(beat["narration"].split(),t,duration); current=regular_page(spec,page,beat,visible)
                    if visible>1:
                        previous=regular_page(spec,page,beat,visible-1); image=Image.blend(previous,current,amount)
                    else: image=current
                encoded=io.BytesIO(); image.save(encoded,format="PNG",compress_level=1)
                process.stdin.write(encoded.getvalue())
    finally: process.stdin.close()
    stderr=process.stderr.read().decode("utf-8",errors="replace")
    if process.wait()!=0:
        temporary.unlink(missing_ok=True)
        raise SystemExit("Échec du rendu vidéo : "+stderr[-1000:])
    os.replace(temporary,output)
    trace={"renderer":"BRITED deterministic renderer v1","beats":[]}
    for beat,duration in zip(spec["beats"],durations):
        tokens=beat["narration"].split()
        trace["beats"].append({"id":beat["id"],"source_text":beat["narration"],"tokens":tokens,
                               "token_count":len(tokens),"full_text_visible_at":round(float(duration)*.90,3),
                               "hold_after_full_text":round(float(duration)*.10,3)})
    output.with_suffix(".render-trace.json").write_text(json.dumps(trace,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser();parser.add_argument("spec",type=Path);parser.add_argument("output",type=Path);parser.add_argument("--timing",type=Path,required=True);args=parser.parse_args();render(args.spec,args.output,args.timing)


if __name__=="__main__": main()
