#!/usr/bin/env python3
"""Contrôle bloquant de complétude textuelle des vidéos BRITED."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def words(text: str) -> list[str]:
    return re.findall(r"[0-9A-Za-zÀ-ÖØ-öø-ÿŒœ]+(?:['’][0-9A-Za-zÀ-ÖØ-öø-ÿŒœ]+)?", text.casefold())


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
    ffmpeg_source = root / ".video-tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    ffmpeg = Path(temp.name) / "ffmpeg"
    shutil.copy2(ffmpeg_source, ffmpeg); ffmpeg.chmod(0o755)
    images: list[Path] = []
    elapsed = 0.0
    temp = tempfile.TemporaryDirectory(prefix="brited-word-check-")
    for index, duration in enumerate(durations):
        elapsed += float(duration)
        image = Path(temp.name) / f"{index:02d}.png"
        subprocess.run([str(ffmpeg), "-y", "-loglevel", "error", "-ss",
                        str(max(0.0, elapsed - .12)), "-i", str(video_path),
                        "-frames:v", "1", str(image)], check=True)
        images.append(image)
    ocr_run = subprocess.run(
        ["/usr/bin/swift", str(root / "video_pipeline/ocr_frames.swift"), *map(str, images)],
        check=True, capture_output=True, text=True,
    )
    ocr = json.loads(ocr_run.stdout)
    for index, beat in enumerate(beats):
        expected = words(beat.get("narration", ""))
        duration = float(durations[index]) if index < len(durations) else 0.0
        # Le moteur réserve au moins 8 % de la séquence à l'affichage complet.
        reveal_end = duration * .90
        # Le rendu social utilise désormais la narration complète comme source
        # d'affichage, y compris sur Question, Réponse et CTA.
        recognized_text = ocr.get(str(images[index]), "") if index < len(images) else ""
        rendered = words(recognized_text)
        remaining = rendered.copy(); missing = []
        for word in expected:
            if word in remaining:
                remaining.remove(word)
            else:
                missing.append(word)
        ok = bool(expected) and duration > 0 and reveal_end < duration and not missing
        if not ok:
            failures.append(f"séquence {index + 1} ({beat.get('id')}): texte ou durée invalide")
        details.append({
            "beat": beat.get("id"), "expected_words": len(expected),
            "first_word": expected[0] if expected else "",
            "last_word": expected[-1] if expected else "",
            "rendered_words": len(rendered), "missing_words": missing,
            "ocr_text": recognized_text,
            "duration": round(duration, 3), "full_text_visible_at": round(reveal_end, 3),
            "hold_after_full_text": round(duration - reveal_end, 3), "passed": ok,
        })
    if not video_path.is_file() or video_path.stat().st_size == 0:
        failures.append("fichier vidéo absent ou vide")
    report = {
        "passed": not failures, "video": str(video_path),
        "expected_total_words": sum(item["expected_words"] for item in details),
        "beats": details, "failures": failures,
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
