#!/usr/bin/env python3
"""Voix BRITED locale, clonée depuis la référence autorisée, beat par beat."""

from __future__ import annotations

import argparse
import importlib
import json
import wave
from pathlib import Path

import huggingface_hub
from mlx_audio.tts.generate import generate_audio
from mlx_audio.tts.utils import load_model


MODEL = Path.home() / "Library/Caches/BRITED/huggingface/models--mlx-community--chatterbox-multilingual-v3/snapshots/03565773edd72e949572557597af8063bb49a18a"
S3 = Path("/Users/Shared/BRITED-Models/S3TokenizerV2")
DEFAULT_REFERENCE = Path("/private/tmp/voix-reference-video-exemple.wav")
PAUSE = 0.25


def _wav(path: Path):
    with wave.open(str(path), "rb") as handle:
        return handle.getparams(), handle.readframes(handle.getnframes()), handle.getnframes() / handle.getframerate()


def generate(spec_path: Path, output: Path, reference: Path) -> None:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    if not MODEL.exists() or not S3.exists() or not reference.exists():
        raise SystemExit("Modèle ou voix de référence BRITED introuvable")

    cb = importlib.import_module("mlx_audio.tts.models.chatterbox.chatterbox")
    cb.snapshot_download = lambda *args, **kwargs: str(S3)
    huggingface_hub.snapshot_download = lambda *args, **kwargs: str(S3)
    model = load_model(MODEL)

    paths: list[Path] = []
    durations: list[float] = []
    for index, beat in enumerate(spec["beats"], start=1):
        path = output / f"{index:02d}_{beat['id']}.wav"
        if not path.exists():
            generate_audio(
                text=beat["narration"], model=model, ref_audio=str(reference),
                lang_code="fr", speed=1.03, output_path=str(output),
                file_prefix=path.stem, join_audio=True, exaggeration=.38,
                cfg_weight=.32, temperature=.5, top_p=.86, min_p=.08,
                repetition_penalty=1.5, verbose=False,
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
            chunks.append(silence)
            durations[index] += PAUSE
    joined = output / "voice.wav"
    with wave.open(str(joined), "wb") as handle:
        handle.setparams(params)
        handle.writeframes(b"".join(chunks))
    (output / "timing.json").write_text(
        json.dumps({"audio": str(joined), "durations": durations}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    args = parser.parse_args()
    generate(args.spec, args.output, args.reference)


if __name__ == "__main__":
    main()
