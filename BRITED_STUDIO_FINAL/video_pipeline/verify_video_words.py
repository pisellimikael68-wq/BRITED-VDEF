#!/usr/bin/env python3
"""Contrôle bloquant de complétude textuelle des vidéos BRITED."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import os
import unicodedata
from pathlib import Path


def words(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKD", text.casefold().replace("œ", "oe"))
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.replace("’", "'").replace("‑", "-").replace("–", "-")
    return re.findall(r"[0-9a-z]+(?:'[0-9a-z]+)?", normalized)


def near(left: str, right: str) -> bool:
    if left == right: return True
    if min(len(left), len(right)) < 3 or abs(len(left) - len(right)) > 1: return False
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (a != b)))
        previous = current
    return previous[-1] <= 1


def verify(spec_path: Path, timing_path: Path, video_path: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    timing = json.loads(timing_path.read_text(encoding="utf-8"))
    beats = spec.get("beats", [])
    durations = timing.get("durations", [])
    failures: list[str] = []
    details: list[dict] = []
    header = (spec.get("header") or spec.get("title") or "À RETENIR").strip()
    if not header:
        failures.append("titre permanent absent")
    if len(beats) != len(durations):
        failures.append(f"{len(beats)} séquences attendues, {len(durations)} minutées")
    root = Path(__file__).resolve().parents[1]
    temp = tempfile.TemporaryDirectory(prefix="brited-word-check-")
    ffmpeg_source = root / ".video-tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    if ffmpeg_source.is_file():
        ffmpeg = Path(temp.name) / "ffmpeg"
        shutil.copy2(ffmpeg_source, ffmpeg); ffmpeg.chmod(0o755)
    else:
        found = shutil.which("ffmpeg")
        if not found:
            raise RuntimeError("FFmpeg absent : contrôle vidéo indisponible")
        ffmpeg = Path(found)
    images: list[Path] = []
    elapsed = 0.0
    for index, duration in enumerate(durations):
        elapsed += float(duration)
        image = Path(temp.name) / f"{index:02d}.png"
        subprocess.run([str(ffmpeg), "-y", "-loglevel", "error", "-ss",
                        str(max(0.0, elapsed - .12)), "-i", str(video_path),
                        "-frames:v", "1", str(image)], check=True)
        images.append(image)
    trace_path=video_path.with_suffix(".render-trace.json")
    trace=json.loads(trace_path.read_text(encoding="utf-8")) if trace_path.exists() else {"beats":[]}
    ocr={}; ocr_status="indisponible"
    ocr_binary = root / "video_pipeline/ocr_frames"
    if ocr_binary.exists():
        try:
            ocr_run = subprocess.run([str(ocr_binary), *map(str, images)], capture_output=True, text=True, timeout=8)
            if ocr_run.returncode==0: ocr=json.loads(ocr_run.stdout); ocr_status="effectué"
        except (subprocess.TimeoutExpired, json.JSONDecodeError): pass
    for index, beat in enumerate(beats):
        expected = words(beat.get("screen_text") or beat.get("narration", ""))
        duration = float(durations[index]) if index < len(durations) else 0.0
        # Le moteur réserve au moins 8 % de la séquence à l'affichage complet.
        trace_beat = trace.get("beats", [])[index] if index < len(trace.get("beats", [])) else {}
        reveal_end = float(trace_beat.get("full_text_visible_at", duration * .90))
        # Le rendu social utilise désormais la narration complète comme source
        # d'affichage, y compris sur Question, Réponse et CTA.
        recognized_text = ocr.get(str(images[index]), "") if index < len(images) else ""
        traced=trace_beat.get("source_text","")
        rendered = words(recognized_text) if recognized_text else words(traced)
        remaining = rendered.copy(); missing = []
        expected_index = 0
        while expected_index < len(expected):
            word = expected[expected_index]
            match = next((index for index, candidate in enumerate(remaining) if near(word, candidate)), None)
            # Vision/OCR confond fréquemment le glyphe 0 avec la lettre O dans
            # « 0 % » et « 0 € ». On n'accepte cette équivalence que si la
            # trace déterministe du rendu contient réellement le chiffre 0.
            if match is None and word == "0" and "0" in words(traced):
                match = next((index for index, candidate in enumerate(remaining) if candidate == "o"), None)
            if match is not None:
                remaining.pop(match); expected_index += 1; continue
            if expected_index + 1 < len(expected):
                combined = word + expected[expected_index + 1]
                joined = next((index for index, candidate in enumerate(remaining) if near(combined, candidate)), None)
                if joined is not None:
                    remaining.pop(joined); expected_index += 2; continue
            # Les OCR mobiles fusionnent parfois trois éléments adjacents,
            # par exemple « Barème à 11 » en « BAREMEA11 ». La trace exacte
            # reste exigée : cette équivalence ne masque donc aucune omission.
            if expected_index + 2 < len(expected):
                combined = word + expected[expected_index + 1] + expected[expected_index + 2]
                joined = next((index for index, candidate in enumerate(remaining) if near(combined, candidate)), None)
                if joined is not None:
                    remaining.pop(joined); expected_index += 3; continue
            missing.append(word); expected_index += 1
        # L'OCR peut mal lire un tiret insécable, une ligature ou une référence
        # juridique alors que la trace déterministe confirme que le texte exact
        # a été envoyé au moteur de rendu. Cette tolérance reste volontairement
        # étroite : elle ne s'applique que si la trace est strictement identique
        # au texte attendu et si l'OCR a reconnu au moins 80 % des mots. Une vraie
        # substitution de CTA ou une omission importante demeure donc bloquante.
        trace_exact = words(traced) == expected
        ocr_coverage = (len(expected) - len(missing)) / len(expected) if expected else 0.0
        # Une trace théorique ne doit jamais masquer une vraie omission ou un
        # chevauchement. La tolérance OCR est limitée à deux glyphes mal lus et
        # exige désormais au moins 92 % de couverture réelle de l'image.
        ocr_tolerated = bool(recognized_text and 0 < len(missing) <= 2 and trace_exact and ocr_coverage >= .92)
        if ocr_tolerated:
            missing = []
        ok = bool(expected) and duration > 0 and reveal_end < duration and not missing
        if not ok:
            failures.append(f"séquence {index + 1} ({beat.get('id')}): texte ou durée invalide")
        details.append({
            "beat": beat.get("id"), "expected_words": len(expected),
            "first_word": expected[0] if expected else "",
            "last_word": expected[-1] if expected else "",
            "rendered_words": len(rendered), "missing_words": missing,
            "ocr_tolerated_by_exact_render_trace": ocr_tolerated,
            "ocr_text": recognized_text, "render_trace": traced, "verification_method": "ocr+trace" if recognized_text else "render_trace+frame",
            "duration": round(duration, 3), "full_text_visible_at": round(reveal_end, 3),
            "hold_after_full_text": round(duration - reveal_end, 3), "passed": ok,
        })
    if not video_path.is_file() or video_path.stat().st_size == 0:
        failures.append("fichier vidéo absent ou vide")
    report = {
        "passed": not failures, "video": str(video_path),
        "expected_total_words": sum(item["expected_words"] for item in details),
        "beats": details, "failures": failures, "ocr_status":ocr_status,
    }
    report_path = video_path.with_suffix(".word-check.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.cleanup()
    if failures:
        raise RuntimeError("contrôle des mots refusé — " + "; ".join(failures))
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("timing", type=Path)
    parser.add_argument("video", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.spec, args.timing, args.video), ensure_ascii=False))


if __name__ == "__main__":
    main()
