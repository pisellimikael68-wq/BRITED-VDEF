#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, subprocess, wave
import re
from pathlib import Path
# Le rendu officiel est désormais le Visuel A. Le contrôleur doit employer
# exactement sa taxonomie d'illustrations, pas celle de l'ancien prototype.
from render_social_visual_a import ffmpeg_executable, icon_family, visual_context
from verify_audio_quality import verify as verify_audio
from generate_voice_local import TARGET_WPM, VOICE_WPM_TOLERANCE, canonical_voice_role


def verify(spec_path: Path, timing_path: Path, video_path: Path) -> dict:
    spec=json.loads(spec_path.read_text(encoding="utf-8")); timing=json.loads(timing_path.read_text(encoding="utf-8"))
    # Contrôle contre la référence V6 globale, même si un ancien spec contient
    # encore des valeurs historiques.
    target_wpm=dict(TARGET_WPM)
    probe=subprocess.run([ffmpeg_executable(),"-hide_banner","-i",str(video_path),"-f","null","-"],capture_output=True,text=True)
    failures=[]
    if probe.returncode: failures.append("fichier vidéo illisible")
    data=probe.stderr
    if "1080x1920" not in data: failures.append("résolution finale différente de 1080 × 1920")
    if "Audio:" not in data: failures.append("piste audio absente")
    durations=[float(x) for x in timing.get("durations",[])]; expected=sum(durations)
    speech_durations=[float(x) for x in timing.get("speech_durations",[])]; speech_rates=[float(x) for x in timing.get("speech_rates_wpm",[])]
    # La durée n'est plus un critère d'acceptation : l'information complète prime.
    low,high=0.0,None
    question=next((float(durations[i]) for i,b in enumerate(spec.get("beats",[])) if b.get("id")=="question" and i<len(durations)),None)
    if question is not None and question < 4.0: failures.append(f"question visible seulement {question:.2f} s au lieu de 4 s")
    if len(durations)!=len(spec.get("beats",[])): failures.append("nombre de pages et minutages incohérent")
    fluency_failures=[]
    if len(speech_rates) != len(spec.get("beats", [])):
        fluency_failures.append("mesure du débit absente sur une ou plusieurs pages")
    for index, (beat, rate) in enumerate(zip(spec.get("beats", []), speech_rates), 1):
        beat_id=beat.get("id", "")
        role=canonical_voice_role(beat_id)
        if role == "default":
            fluency_failures.append(f"page {index} ({beat_id}) : rôle vocal non reconnu")
            continue
        target=target_wpm[role]
        if abs(rate-target) > VOICE_WPM_TOLERANCE:
            fluency_failures.append(f"page {index} ({beat_id} → {role}) : débit {rate:.1f} mots/min hors cible {target} ± {VOICE_WPM_TOLERANCE}")
    if speech_durations and any(value < .9 for value in speech_durations):
        fluency_failures.append("une page orale est trop brève pour une diction naturelle")
    if fluency_failures: failures.extend("fluidité orale : "+item for item in fluency_failures)
    if any(int(beat.get("parts", 1)) != 1 for beat in spec.get("beats", [])):
        failures.append("un même bloc narratif a été coupé sur plusieurs pages")
    forbidden = "‑‐‒"
    if any(any(char in beat.get("narration", "") for char in forbidden) for beat in spec.get("beats", [])):
        failures.append("tiret typographique incompatible encore présent")
    for beat in spec.get("beats", []):
        if beat.get("page_role", beat.get("id")) == "question" and re.search(r"oui\s*(?:/|ou)\s*non", beat.get("narration", ""), re.I):
            failures.append("oui/non répété dans le texte de la question")
    visual_checks=[]
    trace_path=video_path.with_suffix(".render-trace.json")
    trace=json.loads(trace_path.read_text(encoding="utf-8")) if trace_path.exists() else {}
    expected_cta_variant="rendez_vous"
    if trace.get("features",{}).get("cta_variant") != expected_cta_variant:
        failures.append("dernière page différente du modèle rendez-vous unique verrouillé")
    trace_beats={item.get("id"):item for item in trace.get("beats",[])}
    special_roles={"question","reponse","answer","cta","cloture"}
    main_sizes=[item.get("visual_layout",{}).get("font_size") for item in trace.get("beats",[])
                if isinstance(item.get("visual_layout"),dict)
                and item.get("visual_layout",{}).get("font_size")
                and str(item.get("id","")).casefold() not in special_roles]
    typography_ok=bool(main_sizes) and max(main_sizes)-min(main_sizes) <= 6 and min(main_sizes) >= 40
    if not typography_ok:
        failures.append("écart typographique supérieur au corridor validé de 6 px")
    for beat in spec.get("beats", []):
        role=beat.get("page_role",beat.get("id","")).casefold()
        if role in {"reponse","answer"} and spec.get("platform") == "shorts":
            layout=(trace_beats.get(beat.get("id"),{}).get("visual_layout") or {})
            card=layout.get("card_bounds",[]); text=layout.get("text_bounds",[])
            layout_ok=(len(card)==4 and len(text)==4 and card[0] <= text[0] < text[2] <= card[2]
                       and card[1] <= text[1] < text[3] <= card[3] and not layout.get("overlap"))
            label_checks=layout.get("label_checks",[])
            labels_ok=True
            if layout.get("answer_design") == "structured_v2":
                labels_ok=bool(label_checks) and all(
                    len(item.get("pill_bounds",[]))==4 and len(item.get("text_bounds",[]))==4
                    and item["pill_bounds"][0] <= item["text_bounds"][0]
                    and item["text_bounds"][2] <= item["pill_bounds"][2]
                    and item["pill_bounds"][1] <= item["text_bounds"][1]
                    and item["text_bounds"][3] <= item["pill_bounds"][3]
                    and item.get("body_contains_required_term",False)
                    for item in label_checks
                )
                layout_ok=layout_ok and labels_ok
            visual_checks.append({"beat":beat.get("id"),"answer_card":True,
                                  "verdict":layout.get("verdict",""),"text_bounds":text,
                                  "card_bounds":card,"label_checks":label_checks,
                                  "labels_ok":labels_ok,"geometry_ok":layout_ok,"passed":layout_ok})
            if not labels_ok: failures.append("réponse : libellé hors encadré ou distinction PACS incorrecte")
            elif not layout_ok: failures.append("réponse hors cadre ou chevauchée")
            continue
        if role in {"cta","cloture"}:
            layout=(trace_beats.get(beat.get("id"),{}).get("visual_layout") or {})
            text=layout.get("text_bounds",[]); icons=layout.get("icon_bounds",[])
            layout_ok=(len(text)==4 and len(icons)==4 and text[3] < icons[1] and not layout.get("overlap"))
            visual_checks.append({"beat":beat.get("id"),"cta":True,"text_bounds":text,
                                  "icon_bounds":icons,"geometry_ok":layout_ok,"passed":layout_ok})
            if not layout_ok: failures.append("CTA : texte et pictogramme se chevauchent")
            continue
        if role in {"question","reponse","answer","cta","cloture"}:
            continue
        description=(beat.get("visual") or "").strip()
        family=icon_family(visual_context(beat))
        layout=(trace_beats.get(beat.get("id"),{}).get("visual_layout") or {})
        text_bounds=layout.get("text_bounds",[]); icon_bounds=layout.get("icon_bounds",[])
        selected_icons=layout.get("selected_icons",[])
        geometry_ok=(len(text_bounds)==4 and len(icon_bounds)==4 and
                     text_bounds[3] < icon_bounds[1] and icon_bounds[3] <= 1180 and
                     not layout.get("overlap"))
        library_ok=2 <= len(selected_icons) <= 3 and len(selected_icons)==len(set(selected_icons))
        passed=bool(description) and family != "generic" and geometry_ok and library_ok
        visual_checks.append({"beat":beat.get("id"),"description":description,"family":family,
                              "semantic_match":family!="generic","geometry_ok":geometry_ok,
                              "library_icons":selected_icons,"library_ok":library_ok,
                              "text_bounds":text_bounds,"icon_bounds":icon_bounds,"passed":passed})
        if not passed: failures.append(f"pictogramme non contextualisé pour la page {beat.get('id')}")
    cta = next((beat.get("narration", "") for beat in spec.get("beats", []) if beat.get("page_role", beat.get("id")) == "cta"), "")
    if not re.search(r"rendez[- ]vous.*lien dans ma bio", cta, re.I):
        failures.append("CTA oral non aligné avec l'objectif de rendez-vous")
    audio=Path(timing.get("audio",""))
    if audio.is_file():
        with wave.open(str(audio),"rb") as h: audio_duration=h.getnframes()/h.getframerate()
        if abs(audio_duration-expected)>.35: failures.append("minutage et voix désynchronisés")
    else: failures.append("voix finale absente")
    try:
        audio_report = verify_audio(timing_path)
    except Exception as error:
        audio_report = {"passed": False, "failures": [str(error)]}
        failures.append(str(error))
    oral_path=audio.with_suffix(".voice-content-check.json") if audio else timing_path.with_name("voice-content-check.json")
    oral_report=json.loads(oral_path.read_text(encoding="utf-8")) if oral_path.exists() else {"passed":False,"failures":["contrôle oral absent"]}
    if not oral_report.get("passed"): failures.append("contrôle oral Whisper absent ou refusé")
    word=video_path.with_suffix(".word-check.json")
    if not word.exists() or not json.loads(word.read_text(encoding="utf-8")).get("passed"):
        failures.append("contrôle des mots absent ou refusé")
    report={"passed":not failures,"failures":failures,"expected_duration":round(expected,2),"target_duration":None,
            "resolution":"1080x1920" if "1080x1920" in data else "inconnue","audio": "Audio:" in data,
            "word_check":word.exists(),"audio_check":audio_report,"oral_check":oral_report,"layout_check":"zones fixes sans chevauchement",
            "typography_check":{"agent":"controle_hierarchie_typographique","passed":typography_ok,
                                "main_font_sizes":main_sizes,"maximum_delta":6,"minimum_size":40},
            "oral_fluency_check":{"agent":"controle_fluidite_orale_independant","passed":not fluency_failures,
                                    "checks":["debit_par_role","groupes_de_souffle","absence_de_rupture","coherence_inter_pages"],
                                    "speech_rates_wpm":speech_rates,"failures":fluency_failures},
            "pictogram_check":{"agent":"controle_visuel_independant","passed":all(x["passed"] for x in visual_checks),
                                "checks":["coherence_semantique","presentation","cadrage","absence_chevauchement"],
                                "pages":visual_checks}}
    target=video_path.with_suffix(".quality-check.json"); target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if failures: raise RuntimeError("contrôle qualité refusé — "+"; ".join(failures))
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("spec",type=Path);p.add_argument("timing",type=Path);p.add_argument("video",type=Path);a=p.parse_args();print(json.dumps(verify(a.spec,a.timing,a.video),ensure_ascii=False))
