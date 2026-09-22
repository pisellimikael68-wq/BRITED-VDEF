#!/usr/bin/env python3
"""Contrôle audio bloquant, indépendant du moteur de synthèse."""

from __future__ import annotations

import argparse
import array
import json
import math
import wave
from pathlib import Path


def wav_metrics(path: Path) -> dict:
    with wave.open(str(path), "rb") as handle:
        channels, width, rate, frames = handle.getnchannels(), handle.getsampwidth(), handle.getframerate(), handle.getnframes()
        raw = handle.readframes(frames)
    if width != 2 or channels != 1:
        return {"rate": rate, "channels": channels, "width": width, "duration": frames / max(1, rate), "unsupported": True}
    samples = array.array("h"); samples.frombytes(raw)
    if not samples:
        return {"rate": rate, "channels": channels, "width": width, "duration": 0.0, "empty": True}
    peak = max(abs(value) for value in samples) / 32768
    rms = math.sqrt(sum(value * value for value in samples) / len(samples)) / 32768
    dc = abs(sum(samples) / len(samples)) / 32768
    clipped = sum(abs(value) >= 32700 for value in samples) / len(samples)
    jumps = sum(abs(samples[i] - samples[i - 1]) >= 30000 for i in range(1, len(samples))) / len(samples)
    return {"rate": rate, "channels": channels, "width": width, "duration": round(frames / rate, 3),
            "peak": round(peak, 5), "rms": round(rms, 5), "dc": round(dc, 6),
            "clipped_ratio": round(clipped, 7), "abrupt_jump_ratio": round(jumps, 7)}


def pause_noise_metrics(path: Path, timing: dict) -> dict:
    """Mesure le bruit résiduel au cœur des respirations ajoutées par BRITED."""
    with wave.open(str(path), "rb") as handle:
        rate, width, channels = handle.getframerate(), handle.getsampwidth(), handle.getnchannels()
        raw = handle.readframes(handle.getnframes())
    if width != 2 or channels != 1:
        return {"passed": False, "reason": "format non mesurable", "regions": []}
    samples = array.array("h"); samples.frombytes(raw)
    cursor=0.0; regions=[]
    speech=timing.get("speech_durations",[]); pauses=timing.get("post_pauses",[])
    for index,duration in enumerate(speech):
        cursor += float(duration)
        pause=float(pauses[index]) if index < len(pauses) else 0.0
        if pause >= .2:
            margin=min(.12,pause*.25); start=int((cursor+margin)*rate); end=int((cursor+pause-margin)*rate)
            region=samples[start:end]
            rms=math.sqrt(sum(value*value for value in region)/len(region))/32768 if region else 0.0
            peak=max((abs(value) for value in region),default=0)/32768
            regions.append({"after_beat":index+1,"rms":round(rms,6),"peak":round(peak,6)})
        cursor += pause
    passed=bool(regions) and all(item["rms"] <= .003 and item["peak"] <= .025 for item in regions)
    return {"passed":passed,"regions":regions,"rms_limit":.003,"peak_limit":.025}


def verify(timing_path: Path) -> dict:
    timing = json.loads(timing_path.read_text(encoding="utf-8"))
    final = Path(timing["audio"])
    voice_dir = final.parent
    segments = sorted(path for path in voice_dir.glob("[0-9][0-9]_*.wav") if "slowed" not in path.name and "-raw" not in path.name)
    failures: list[str] = []
    final_metrics = wav_metrics(final) if final.is_file() else {}
    segment_metrics = {path.name: wav_metrics(path) for path in segments}
    noise_metrics = pause_noise_metrics(final, timing) if final.is_file() else {"passed":False,"regions":[]}
    if not final_metrics:
        failures.append("voix finale absente")
    if not segments:
        failures.append("segments vocaux absents")
    if not noise_metrics.get("passed"):
        failures.append("bruit résiduel détecté dans les respirations")
    expected_rate = 24000
    if final_metrics.get("rate") != expected_rate:
        failures.append(f"fréquence audio finale anormale : {final_metrics.get('rate')} Hz au lieu de {expected_rate} Hz")
    for name, metrics in segment_metrics.items():
        if metrics.get("rate") != expected_rate or metrics.get("channels") != 1 or metrics.get("width") != 2:
            failures.append(f"format audio incohérent : {name}")
        if metrics.get("clipped_ratio", 0) > .0005:
            failures.append(f"écrêtage audible potentiel : {name}")
        if metrics.get("abrupt_jump_ratio", 0) > .0002:
            failures.append(f"ruptures audio anormales : {name}")
        if metrics.get("dc", 0) > .04:
            failures.append(f"décalage continu anormal : {name}")
    expected = sum(float(value) for value in timing.get("durations", []))
    if final_metrics and abs(final_metrics.get("duration", 0) - expected) > .12:
        failures.append("durée audio différente du minutage")
    report = {"passed": not failures, "failures": failures, "final": final_metrics,
              "segments": segment_metrics, "background_noise": noise_metrics,
              "checks": ["sample_rate", "format", "clipping", "abrupt_jumps", "dc_offset", "duration", "background_noise"]}
    target = final.with_suffix(".audio-check.json") if final else timing_path.with_name("audio-check.json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise RuntimeError("contrôle audio refusé — " + "; ".join(failures))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("timing", type=Path); args = parser.parse_args()
    print(json.dumps(verify(args.timing), ensure_ascii=False))
