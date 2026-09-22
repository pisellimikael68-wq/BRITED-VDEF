#!/usr/bin/env python3
"""Routeur vocal BRITED : ElevenLabs validé ou moteur local certifié."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/voice-provider.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reference", type=Path)
    args = parser.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    provider = config.get("active_provider", "local")
    script = ROOT / "video_pipeline" / (
        "generate_voice_elevenlabs.py" if provider == "elevenlabs" else "generate_voice_local.py"
    )
    command = [sys.executable, str(script), str(args.spec), str(args.output)]
    if args.reference and provider == "local":
        command += ["--reference", str(args.reference)]
    subprocess.run(command, check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
