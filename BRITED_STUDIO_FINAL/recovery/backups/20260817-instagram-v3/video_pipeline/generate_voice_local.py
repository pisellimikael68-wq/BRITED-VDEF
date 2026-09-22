#!/usr/bin/env python3
"""Voix BRITED locale, clonée depuis la référence autorisée, beat par beat."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import wave
from pathlib import Path

import huggingface_hub
from mlx_audio.tts.generate import generate_audio
from mlx_audio.tts.utils import load_model


MODEL = Path.home() / "Library/Caches/BRITED/huggingface/models--mlx-community--chatterbox-multilingual-v3/snapshots/03565773edd72e949572557597af8063bb49a18a"
S3 = Path("/Users/Shared/BRITED-Models/S3TokenizerV2")
DEFAULT_REFERENCE = Path(__file__).resolve().parents[1] / "assets/voice_reference.wav"
PAUSE = 0.25
VOICE_CONFIG = {"version": 2, "speed": 0.88, "exaggeration": 0.38, "cfg_weight": 0.32,
                "temperature": 0.5, "top_p": 0.86, "min_p": 0.08,
                "repetition_penalty": 1.5}


def _wav(path: Path):
    with wave.open(str(path), "rb") as handle:
        return handle.getparams(), handle.readframes(handle.getnframes()), handle.getnframes() / handle.getframerate()


def _ffmpeg() -> Path:
    local = Path(__file__).resolve().parents[1] / ".video-tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    if local.is_file(): return local
    raise SystemExit("FFmpeg local introuvable pour calibrer la durée de la voix")


def generate(spec_path: Path, output: Path, reference: Path) -> None:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    if not MODEL.exists() or not S3.exists() or not reference.exists():
        raise SystemExit("Modèle ou voix de référence BRITED introuvable")

    cb = importlib.import_module("mlx_audio.tts.models.chatterbox.chatterbox")
    cb.snapshot_download = lambda *args, **kwargs: str(S3)
    huggingface_hub.snapshot_download = lambda *args, **kwargs: str(S3)
    model = load_model(MODEL)
    config_path = output / "voice-config.json"
    regenerate = not config_path.exists() or json.loads(config_path.read_text(encoding="utf-8")) != VOICE_CONFIG

    paths: list[Path] = []
    durations: list[float] = []
    for index, beat in enumerate(spec["beats"], start=1):
        path = output / f"{index:02d}_{beat['id']}.wav"
        if regenerate or not path.exists():
            if path.exists(): path.unlink()
            generate_audio(
                text=beat["narration"], model=model, ref_audio=str(reference),
                lang_code="fr", speed=VOICE_CONFIG["speed"], output_path=str(output),
                file_prefix=path.stem, join_audio=True, exaggeration=VOICE_CONFIG["exaggeration"],
                cfg_weight=VOICE_CONFIG["cfg_weight"], temperature=VOICE_CONFIG["temperature"],
                top_p=VOICE_CONFIG["top_p"], min_p=VOICE_CONFIG["min_p"],
                repetition_penalty=VOICE_CONFIG["repetition_penalty"], verbose=False,
            )
        paths.append(path)
        durations.append(_wav(path)[2])

    params, _, _ = _wav(paths[0])
    sample_size = params.nchannels * params.sampwidth
    silence = b"\0" * (round(PAUSE * params.framerate) * sample_size)
    chunks: list[bytes] = []
    for index, path in enumerate(paths):
        _, data, _ = _wav(path)
        chunks.append(data)
        if index < len(paths) - 1:
            minimum = 4.0 if spec["beats"][index].get("id") == "question" else 0.0
            pause = max(PAUSE, minimum - durations[index])
            chunks.append(b"\0" * (round(pause * params.framerate) * sample_size))
            durations[index] += pause
    joined = output / "voice.wav"
    with wave.open(str(joined), "wb") as handle:
        handle.setparams(params)
        handle.writeframes(b"".join(chunks))
    targets = {"tiktok": (38.0, 42.0), "reels": (28.0, 40.0), "shorts": (40.0, 58.0)}
    low, high = targets.get(spec.get("platform"), (0.0, 60.0))
    actual = _wav(joined)[2]
    if not low <= actual <= high:
        target = (low + high) / 2
        ratio = actual / target
        calibrated = output / "voice-calibrated.wav"
        subprocess.run([str(_ffmpeg()), "-y", "-loglevel", "error", "-i", str(joined),
                        "-filter:a", f"atempo={ratio:.8f}", str(calibrated)], check=True)
        os.replace(calibrated, joined)
        scale = target / actual
        durations = [value * scale for value in durations]
    (output / "timing.json").write_text(
        json.dumps({"audio": str(joined), "durations": durations}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    config_path.write_text(json.dumps(VOICE_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    args = parser.parse_args()
    generate(args.spec, args.output, args.reference)


if __name__ == "__main__":
    main()
