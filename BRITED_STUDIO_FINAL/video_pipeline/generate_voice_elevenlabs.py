#!/usr/bin/env python3
"""Synthèse ElevenLabs BRITED, segmentée et contrôlée comme la voix locale."""

from __future__ import annotations

import argparse
import hashlib
import json
import ssl
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

import certifi

from generate_voice_local import (
    MASTERING_FILTER,
    PAGE_SWITCH_HOLD,
    PAUSE,
    SEGMENT_LEVEL_FILTER,
    TARGET_WPM,
    canonical_voice_role,
    _ffmpeg,
    _spoken_word_count,
    _wav,
    calibrated_atempo,
    speech_text,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/voice-provider.json"
KEYCHAIN_SERVICE = "BRITED_ELEVENLABS_API_KEY"
TLS_CONTEXT = ssl.create_default_context(cafile=certifi.where())

# Empreinte prosodique officielle extraite de la vidéo de référence
# regimes_changement__shorts (SHA-256 2d11925d...). Les pages ordinaires
# conservent exactement ses réglages ElevenLabs. Seules la page Réponse et la
# clôture reçoivent le supplément d'énergie explicitement validé par Mikael.
DEFAULT_ROLE_SETTINGS = {
    # La synthèse brute de certaines accroches courtes dépasse 230 mots/minute.
    # Un débit fournisseur légèrement retenu préserve l'articulation, puis le
    # recalage déterministe ramène réellement la page à 189,5 mots/minute.
    "hook": {"stability": 0.56, "similarity_boost": 0.86, "style": 0.20, "use_speaker_boost": True, "speed": 0.96},
    "question": {"stability": 0.62, "similarity_boost": 0.82, "style": 0.10, "use_speaker_boost": True, "speed": 1.00},
    "reponse": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.32, "use_speaker_boost": True, "speed": 1.08},
    "regle": {"stability": 0.62, "similarity_boost": 0.82, "style": 0.10, "use_speaker_boost": True, "speed": 1.00},
    "precision": {"stability": 0.62, "similarity_boost": 0.82, "style": 0.10, "use_speaker_boost": True, "speed": 1.00},
    "exemple": {"stability": 0.62, "similarity_boost": 0.82, "style": 0.10, "use_speaker_boost": True, "speed": 1.00},
    "nuance": {"stability": 0.62, "similarity_boost": 0.82, "style": 0.10, "use_speaker_boost": True, "speed": 1.00},
    "cta": {"stability": 0.44, "similarity_boost": 0.82, "style": 0.38, "use_speaker_boost": True, "speed": 1.10},
}


def keychain_secret() -> str:
    result = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
        check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def synthesize(text: str, target: Path, config: dict, api_key: str, voice_settings: dict | None = None) -> None:
    voice_id = config["voice_id"]
    query = urllib.parse.urlencode({"output_format": "mp3_44100_128"})
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?{query}"
    payload = {
        "text": text,
        "model_id": config.get("model_id", "eleven_multilingual_v2"),
        "voice_settings": voice_settings or config.get("voice_settings", {}),
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    try:
        audio = urllib.request.urlopen(request, timeout=120, context=TLS_CONTEXT).read()
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"ElevenLabs a refusé la synthèse ({error.code}) : {detail}") from error
    mp3 = target.with_suffix(".mp3")
    mp3.write_bytes(audio)
    subprocess.run([
        str(_ffmpeg()), "-y", "-loglevel", "error", "-i", str(mp3),
        "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(target),
    ], check=True)
    mp3.unlink(missing_ok=True)


def generate(spec_path: Path, output: Path) -> None:
    if not CONFIG.exists():
        raise RuntimeError("Configuration ElevenLabs absente")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if not config.get("voice_id"):
        raise RuntimeError("Identifiant de voix ElevenLabs absent")
    api_key = keychain_secret()
    if not api_key:
        raise RuntimeError("Clé ElevenLabs absente du Trousseau macOS")

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec_sha256 = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    output.mkdir(parents=True, exist_ok=True)
    beats = spec["beats"]
    spoken = [speech_text(beat["narration"]) for beat in beats]
    profile = spec.get("voice_profile", {})
    # La vidéo fournie est une référence globale verrouillée : un ancien spec ne peut
    # plus réintroduire silencieusement une autre cadence.
    target_wpm = dict(TARGET_WPM)
    base_settings = {**config.get("voice_settings", {}), **profile.get("voice_settings", {})}
    role_settings = dict(DEFAULT_ROLE_SETTINGS)
    reference_page_durations = profile.get("reference_page_durations", [])
    fingerprint = {
        "provider": "elevenlabs", "voice_reference": "regimes_changement__shorts-2d11925d",
        "voice_id": config["voice_id"],
        "model_id": config.get("model_id"), "voice_settings": base_settings,
    }
    paths: list[Path] = []
    speech_durations: list[float] = []
    hashes: dict[str, str] = {}
    for index, (beat, text) in enumerate(zip(beats, spoken), 1):
        key = f"{index:02d}_{beat['id']}"
        # Le débit cible fait partie de l'identité du segment. Une évolution
        # de charte invalide uniquement les rôles concernés (accroche/CTA),
        # sans repayer la synthèse de toutes les autres pages.
        role = canonical_voice_role(beat.get("id", ""))
        if role == "default":
            raise RuntimeError(f"Rôle vocal non reconnu : {beat.get('id', '')!r}")
        role_target = target_wpm[role]
        active_settings = {**base_settings, **role_settings.get(role, {})}
        reference_duration = (
            float(reference_page_durations[index - 1])
            if index - 1 < len(reference_page_durations)
            else None
        )
        segment_fingerprint = {**fingerprint, "target_wpm": role_target,
                               "reference_duration": reference_duration,
                               "active_voice_settings": active_settings}
        if role == "hook":
            segment_fingerprint["hook_tempo_floor"] = .75
        digest = hashlib.sha256((text + json.dumps(segment_fingerprint, sort_keys=True)).encode()).hexdigest()
        hashes[key] = digest
        path = output / f"{key}.wav"
        raw = output / f"{key}-raw.wav"
        marker = output / f"{key}.sha256"
        if not path.exists() or not raw.exists() or not marker.exists() or marker.read_text().strip() != digest:
            synthesize(text, raw, config, api_key, active_settings)
            words = max(1, _spoken_word_count(text))
            raw_duration = _wav(raw)[2]
            observed_wpm = words * 60.0 / max(raw_duration, .01)
            # Les phrases juridiques longues demandent parfois une correction
            # supérieure à 22 %. Le corridor reste piloté par le WPM cible ;
            # cette borne évite qu'une page isolée paraisse sensiblement plus
            # lente que le reste de la vidéo.
            if reference_duration:
                # La référence validée fixe la respiration de chaque page.
                # Le texte doit être calibré en amont pour que cette correction
                # reste naturelle ; le verrou empêche toutefois toute dérive
                # perceptible entre deux productions successives.
                tempo = min(1.60, max(.65, raw_duration / reference_duration))
            else:
                # ElevenLabs peut livrer une accroche très courte au-delà de
                # 240 mots/minute. Le plancher à 0,75 permet alors d'atteindre
                # réellement la cible de charte sans changer le texte.
                tempo = min(1.35, max(.75, role_target / observed_wpm))
            subprocess.run([
                str(_ffmpeg()), "-y", "-loglevel", "error", "-i", str(raw),
                "-filter:a", f"atempo={tempo:.6f},{SEGMENT_LEVEL_FILTER}",
                "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(path),
            ], check=True)
            marker.write_text(digest + "\n", encoding="utf-8")
        paths.append(path)
        speech_durations.append(_wav(path)[2])

    # Nettoie uniquement les anciens segments numérotés qui ne correspondent
    # plus au découpage courant. Sans cela, un changement du nombre ou de
    # l'ordre des pages laisse des fichiers fantômes dans les rapports audio.
    expected_stems = {path.stem for path in paths}
    for stale in output.glob("[0-9][0-9]_*.wav"):
        stem = stale.stem.removesuffix("-raw")
        if stem not in expected_stems:
            stale.unlink(missing_ok=True)
            stale.with_suffix(".sha256").unlink(missing_ok=True)

    params, _, _ = _wav(paths[0])
    sample_size = params.nchannels * params.sampwidth
    durations = list(speech_durations)
    post_pauses = [0.0 for _ in paths]
    chunks: list[bytes] = []
    for index, path in enumerate(paths):
        _, data, _ = _wav(path)
        chunks.append(data)
        if index < len(paths) - 1:
            beat_id = beats[index].get("id")
            pause = PAGE_SWITCH_HOLD if beat_id in {"hook", "question", "nuance"} else PAUSE
            if beat_id == "question":
                pause = max(pause, 4.0 - speech_durations[index])
            chunks.append(b"\0" * (round(pause * params.framerate) * sample_size))
            durations[index] += pause
            post_pauses[index] = pause
    # Une narration naturellement dynamique peut terminer légèrement avant la
    # durée minimale éditoriale. Dans ce cas, on conserve le débit validé et
    # on ajoute une respiration finale, au lieu de ralentir artificiellement
    # toute la voix.
    # La clarté et l'exhaustivité priment désormais sur une durée de plateforme.
    # Aucune narration n'est raccourcie, ralentie ou refusée pour tenir un plafond.
    low, high = 0.0, None
    current_duration = sum(len(chunk) for chunk in chunks) / (params.framerate * sample_size)
    if low and current_duration < low:
        tail_pause = low - current_duration
        chunks.append(b"\0" * (round(tail_pause * params.framerate) * sample_size))
        durations[-1] += tail_pause
        post_pauses[-1] += tail_pause

    joined = output / "voice.wav"
    with wave.open(str(joined), "wb") as handle:
        handle.setparams(params)
        handle.writeframes(b"".join(chunks))

    actual = _wav(joined)[2]
    mastered = output / "voice-mastered.wav"
    subprocess.run([
        str(_ffmpeg()), "-y", "-loglevel", "error", "-i", str(joined),
        "-filter:a", MASTERING_FILTER, "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(mastered),
    ], check=True)
    mastered.replace(joined)
    rates = [round(_spoken_word_count(text) * 60 / max(duration, .01), 1) for text, duration in zip(spoken, speech_durations)]
    (output / "timing.json").write_text(json.dumps({
        "audio": str(joined), "durations": durations, "speech_durations": speech_durations,
        "speech_rates_wpm": rates, "post_pauses": post_pauses,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "voice-config.json").write_text(json.dumps({
        **fingerprint, "spec_sha256": spec_sha256,
        "beat_hashes": hashes, "target_wpm": target_wpm,
        "voice_profile": profile,
        "key_storage": "macOS Keychain", "api_key_recorded": False,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    generate(args.spec, args.output)


if __name__ == "__main__":
    main()
