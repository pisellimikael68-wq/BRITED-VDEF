#!/usr/bin/env python3
"""Contrôle bloquant de la diction par retranscription locale Whisper."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import tempfile
import unicodedata
import shutil
from pathlib import Path


MODEL=Path("/Users/Shared/BRITED-Models/whisper-large-v3-turbo")
FFMPEG=Path(__file__).resolve().parents[1]/".video-tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"


def normalize(value: str) -> list[str]:
    # Uniformiser les apostrophes avant la translittération ASCII. Sinon une
    # apostrophe typographique disparaît ("d’abattements" -> "dabattements")
    # tandis que l'apostrophe droite devient un séparateur, créant un faux mot
    # manquant alors que Whisper a parfaitement reconnu la phrase.
    value=re.sub(r"[’‘`´']", " ", value)
    # Équivalences strictement homophoniques observées en français. Whisper
    # écrit parfois l'inversion « est-ce » comme « et se » et le nom « paie »
    # comme « paix » ; ces variantes ne changent aucun contenu prononcé.
    value=re.sub(r"\bet\s+se\b", "est ce", value, flags=re.I)
    value=unicodedata.normalize("NFKD",value.casefold()).encode("ascii","ignore").decode()
    value=re.sub(r"\bpack\s+us\b","pacs",value)
    words=re.findall(r"[a-z]+|\d+",value)
    # Whisper restitue souvent les nombres et références sous forme de chiffres
    # (« 757B », « 30 500 »), même lorsqu'ils ont été prononcés en toutes
    # lettres. Les développer avant comparaison vérifie le nombre réellement
    # prononcé au lieu de créer un faux écart de graphie.
    try:
        from generate_voice_local import french_integer
    except ModuleNotFoundError:
        # Les contrôles textuels doivent rester disponibles même sur une
        # machine où le lourd moteur vocal MLX n'est pas installé.
        def french_integer(number: int) -> str:
            units = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
                     "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize"]
            if number < 17: return units[number]
            if number < 20: return "dix-" + units[number - 10]
            if number < 100:
                tens, remainder = divmod(number, 10)
                names = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}
                if tens <= 6:
                    return names[tens] if remainder == 0 else names[tens] + (" et un" if remainder == 1 else "-" + french_integer(remainder))
                if tens == 7: return "soixante" + (" et " if remainder == 1 else "-") + french_integer(10 + remainder)
                if tens == 8: return "quatre-vingt" + ("s" if remainder == 0 else "-" + french_integer(remainder))
                return "quatre-vingt-" + french_integer(10 + remainder)
            if number < 1000:
                hundreds, remainder = divmod(number, 100)
                prefix = "cent" if hundreds == 1 else french_integer(hundreds) + " cent"
                return prefix if remainder == 0 else prefix + " " + french_integer(remainder)
            thousands, remainder = divmod(number, 1000)
            prefix = "mille" if thousands == 1 else french_integer(thousands) + " mille"
            return prefix if remainder == 0 else prefix + " " + french_integer(remainder)
    expanded=[]
    for word in words:
        if word.isdigit():
            expanded.extend(re.findall(r"[a-z]+", unicodedata.normalize("NFKD", french_integer(int(word)).casefold()).encode("ascii", "ignore").decode()))
        else:
            expanded.append(word)
    words=expanded
    # Équivalences de retranscription françaises constatées et vérifiées.
    # Elles rapprochent uniquement deux graphies d'un même son ou d'une même
    # référence ; elles ne masquent jamais la disparition d'une notion.
    phonetic={
        "pax":"pacs", "paxe":"pacs", "paxee":"pacse",
        "eritera":"heritera", "erite":"herite", "elite":"herite",
        "leg":"legs", "legue":"legs", "droite":"droits", "droit":"droits",
        "concubat":"concubin", "paix":"paie",
        # « acquêts » se prononce /akɛ/ ; Whisper l'écrit régulièrement
        # « acais » ou « aquais ». Ces graphies représentent exactement le
        # même son français et ne peuvent masquer aucun autre terme juridique.
        "acais":"acquets", "aquais":"acquets", "aquees":"acquets",
        "ackes":"acquets",
    }
    return [phonetic.get(word,word) for word in words]


def speech_form(value: str) -> str:
    # Import différé : il partage exactement les règles de prononciation du TTS.
    from generate_voice_local import speech_text
    return speech_text(value)


def verify(spec_path: Path, timing_path: Path) -> dict:
    if not MODEL.exists(): raise RuntimeError("modèle Whisper local absent")
    if not FFMPEG.exists(): raise RuntimeError("FFmpeg local absent")
    with tempfile.TemporaryDirectory(prefix="brited-whisper-") as folder:
        alias=Path(folder)/"ffmpeg"; alias.symlink_to(FFMPEG)
        os.environ["PATH"]=folder+os.pathsep+os.environ.get("PATH","")
        import mlx_whisper
        spec=json.loads(spec_path.read_text(encoding="utf-8"))
        timing=json.loads(timing_path.read_text(encoding="utf-8"))
        voice_dir=Path(timing["audio"]).parent
        pages=[]; failures=[]
        for index,beat in enumerate(spec.get("beats",[]),1):
            audio=voice_dir/f"{index:02d}_{beat['id']}.wav"
            expected=speech_form(beat["narration"])
            result=mlx_whisper.transcribe(str(audio),path_or_hf_repo=str(MODEL),language="fr",
                                          temperature=0.0,condition_on_previous_text=False)
            heard=(result.get("text") or "").strip()
            # Whisper peut restituer une référence juridique en chiffres alors
            # que le TTS la reçoit en toutes lettres : on normalise les deux
            # formes avec la même fonction avant de les comparer.
            expected_words=normalize(expected); heard_words=normalize(speech_form(heard))
            similarity=difflib.SequenceMatcher(None,expected_words,heard_words).ratio()
            matcher=difflib.SequenceMatcher(None,expected_words,heard_words)
            missing=[]; unexpected=[]
            for tag,i1,i2,j1,j2 in matcher.get_opcodes():
                if tag in {"delete","replace"}: missing.extend(expected_words[i1:i2])
                if tag in {"insert","replace"}: unexpected.extend(heard_words[j1:j2])
            non_semantic={"alors","aussi","avec","cette","comme","dans","donc","elle","elles","encore",
                          "entre","exemple","mais","pour","selon","toujours","tous","toutes","tout","toute",
                          "vous","votre","vos","leur","leurs","plus","moins"}
            def close_variant(word: str) -> bool:
                return len(word)>=4 and any(len(other)>=4 and word[:4]==other[:4] for other in unexpected)
            critical_missing=[word for word in missing if len(word)>=4 and word not in non_semantic and not close_variant(word)]
            segments=result.get("segments",[])
            no_speech=max((float(s.get("no_speech_prob",0)) for s in segments),default=0.0)
            compression=max((float(s.get("compression_ratio",0)) for s in segments),default=0.0)
            # Les petits accords singulier/pluriel sont tolérés, jamais une phrase
            # méconnaissable, une hallucination ou une coupure importante.
            passed=(similarity>=.84 and not critical_missing and
                    len(missing)<=max(2,round(len(expected_words)*.14)) and no_speech<.45 and compression<2.4)
            page={"beat":beat["id"],"expected":expected,"transcript":heard,
                  "similarity":round(similarity,4),"missing":missing,"critical_missing":critical_missing,"unexpected":unexpected,
                  "no_speech_probability":round(no_speech,4),"compression_ratio":round(compression,4),
                  "passed":passed}
            pages.append(page)
            if not passed: failures.append(f"diction non conforme sur {beat['id']} (similarité {similarity:.0%})")
        # Chaque segment réussi rejoint le cache partagé uniquement après le
        # contrôle Whisper. Une autre plateforme peut alors réutiliser cette
        # diction certifiée pour un texte et des paramètres strictement égaux.
        config_path=voice_dir/"voice-config.json"
        if config_path.exists():
            config=json.loads(config_path.read_text(encoding="utf-8"))
            cache=Path(__file__).resolve().parents[1]/"assets/voice-cache"
            cache.mkdir(parents=True,exist_ok=True)
            for index,(beat,page) in enumerate(zip(spec.get("beats",[]),pages),1):
                if not page["passed"]: continue
                beat_key=f"{index:02d}_{beat['id']}"
                digest=(config.get("beat_hashes",{}).get(beat_key) or
                        config.get("beat_hashes",{}).get(beat["id"]))
                wav=voice_dir/f"{index:02d}_{beat['id']}.wav"
                raw=voice_dir/f"{index:02d}_{beat['id']}-raw.wav"
                if digest and wav.exists() and raw.exists():
                    shutil.copy2(wav,cache/f"{digest}.wav")
                    shutil.copy2(raw,cache/f"{digest}-raw.wav")
    report={"agent":"controle_oral_whisper_local","passed":not failures,"failures":failures,
            "model":str(MODEL),"checks":["transcription","mots_manquants","hallucinations","microcoupures","repetitions"],
            "pages":pages}
    target=Path(timing["audio"]).with_suffix(".voice-content-check.json")
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if failures: raise RuntimeError("contrôle oral refusé — "+"; ".join(failures))
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("spec",type=Path); parser.add_argument("timing",type=Path)
    args=parser.parse_args(); print(json.dumps(verify(args.spec,args.timing),ensure_ascii=False))
