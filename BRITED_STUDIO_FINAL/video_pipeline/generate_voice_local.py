#!/usr/bin/env python3
"""Voix BRITED locale, clonée depuis la référence autorisée, beat par beat."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import wave
import hashlib
import re
from pathlib import Path

MODEL = Path.home() / "Library/Caches/BRITED/huggingface/models--mlx-community--chatterbox-multilingual-v3/snapshots/03565773edd72e949572557597af8063bb49a18a"
S3 = Path("/Users/Shared/BRITED-Models/S3TokenizerV2")
DEFAULT_REFERENCE = Path(__file__).resolve().parents[1] / "assets/voice_reference_donny.wav"
CERTIFIED_CACHE = Path(__file__).resolve().parents[1] / "assets/voice-cache"
PAUSE = 0.22
PAGE_SWITCH_HOLD = 0.9
AUDIO_FORMAT_VERSION = 15
# Le moteur fixe directement le débit. Aucun second changement de vitesse n'est
# appliqué après génération : son cumul avec le ralentissement spécial du hook
# produisait une diction inégale et une empreinte trop artificielle.
SPEECH_POST_ATEMPO = 1.0
VOICE_SEED = 20260822
VOICE_CONFIG = {"version": 14, "speed": 1.0, "exaggeration": 0.28, "cfg_weight": 0.52,
                "temperature": 0.22, "top_p": 0.70, "min_p": 0.08,
                "repetition_penalty": 1.45}
# L'introduction conserve la même identité et le même débit que le corps. Une
# légère expressivité supplémentaire suffit à créer l'accroche sans rupture.
HOOK_CONFIG = {"version": 14, "speed": 1.02, "exaggeration": 0.34, "cfg_weight": 0.52,
               "temperature": 0.22, "top_p": 0.70, "post_atempo": 1.0}
# La variation est éditoriale, jamais aléatoire : chaque rôle narratif reçoit
# une intention mesurée tout en conservant exactement la même empreinte vocale.
PROSODY = {
    "hook":      {"speed": 1.05, "exaggeration": .36, "cfg_weight": .52},
    "question":  {"speed": 1.02, "exaggeration": .32, "cfg_weight": .53},
    "reponse":   {"speed": 1.05, "exaggeration": .34, "cfg_weight": .52},
    "regle":     {"speed": 1.01, "exaggeration": .26, "cfg_weight": .54},
    "precision": {"speed": .99,  "exaggeration": .24, "cfg_weight": .55},
    "exemple":   {"speed": 1.01, "exaggeration": .31, "cfg_weight": .52},
    "nuance":    {"speed": .99,  "exaggeration": .23, "cfg_weight": .55},
    # La réponse et le CTA partagent exactement la même intention :
    # appuyée, chaleureuse et dynamique, jamais publicitaire.
    "cta":       {"speed": 1.05, "exaggeration": .34, "cfg_weight": .52},
}
# Empreinte rythmique officielle extraite de regimes_changement__shorts.
# Pages 2 et finale volontairement renforcées conformément à la validation.
TARGET_WPM = {
    "hook": 189.5,
    "question": 160.0,
    "reponse": 195.0,
    "regle": 205.0,
    "precision": 205.0,
    "exemple": 205.0,
    "nuance": 205.0,
    "cta": 208.0,
    "default": 172.0,
}
VOICE_WPM_TOLERANCE = 3.0


def canonical_voice_role(beat_id: str) -> str:
    """Résout aussi les identifiants éditoriaux composés sans repli silencieux."""
    role = (beat_id or "").strip().casefold()
    if role in TARGET_WPM and role != "default":
        return role
    aliases = (
        ("hook", "hook"), ("accroche", "hook"),
        ("question", "question"),
        ("reponse", "reponse"), ("answer", "reponse"),
        ("cta", "cta"), ("cloture", "cta"),
        ("nuance", "nuance"), ("reserve", "nuance"),
        ("precision", "precision"),
        ("regle", "regle"),
        ("exemple", "exemple"),
    )
    for token, canonical in aliases:
        if token in role:
            return canonical
    return "default"
MIN_ATEMPO = 0.82
MAX_ATEMPO = 1.22
SEGMENT_LEVEL_FILTER = "loudnorm=I=-18:TP=-2:LRA=5"
MASTERING_FILTER = (
    "highpass=f=85,lowpass=f=13500,"
    "adeclick=w=20:o=75:a=2:t=2:b=2,"
    "afftdn=nf=-28:tn=1:tr=1:om=o,"
    "equalizer=f=2800:t=q:w=1.2:g=2.5,"
    "acompressor=threshold=0.12:ratio=2:attack=15:release=120:makeup=1.4,"
    "loudnorm=I=-16:TP=-1.5:LRA=7"
)


def _under_thousand(number: int) -> str:
    units = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
             "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize"]
    if number < 17:
        return units[number]
    if number < 20:
        return "dix-" + units[number - 10]
    if number < 100:
        tens = number // 10
        remainder = number % 10
        names = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}
        if tens <= 6:
            base = names[tens]
            if remainder == 0: return base
            if remainder == 1: return base + " et un"
            return base + "-" + _under_thousand(remainder)
        if tens == 7:
            return "soixante" + (" et " if remainder == 1 else "-") + _under_thousand(10 + remainder)
        if tens == 8:
            base = "quatre-vingt" + ("s" if remainder == 0 else "")
            return base if remainder == 0 else base + "-" + _under_thousand(remainder)
        return "quatre-vingt-" + _under_thousand(10 + remainder)
    hundreds, remainder = divmod(number, 100)
    base = "cent" if hundreds == 1 else _under_thousand(hundreds) + " cent"
    if remainder == 0:
        return base + ("s" if hundreds > 1 else "")
    return base + " " + _under_thousand(remainder)


def french_integer(number: int) -> str:
    """Écrit oralement un entier français, y compris les longues références."""
    if number < 0:
        return "moins " + french_integer(-number)
    if number < 1000:
        return _under_thousand(number)
    scales = ((1_000_000_000_000, "billion", "billions"),
              (1_000_000_000, "milliard", "milliards"),
              (1_000_000, "million", "millions"),
              (1000, "mille", "mille"))
    parts: list[str] = []
    remainder = number
    for value, singular, plural in scales:
        amount, remainder = divmod(remainder, value)
        if not amount:
            continue
        if value == 1000:
            prefix = french_integer(amount)
            # « cent » et « vingt » perdent leur s lorsqu'ils sont suivis de
            # « mille » : sept cent mille, quatre-vingt mille.
            prefix = re.sub(r"cents$", "cent", prefix)
            prefix = re.sub(r"vingts$", "vingt", prefix)
            parts.append("mille" if amount == 1 else prefix + " mille")
        else:
            parts.append(french_integer(amount) + " " + (singular if amount == 1 else plural))
    if remainder:
        parts.append(_under_thousand(remainder))
    return " ".join(parts)


def speech_text(text: str) -> str:
    """Prépare uniquement l'oral : l'affichage conserve les chiffres d'origine."""
    grouped_number = r"(?:\d{1,3}(?:[ \u00a0\u202f]\d{3})+|\d+)"
    parse_number = lambda raw: int(re.sub(r"[ \u00a0\u202f]", "", raw))
    value = re.sub(
        rf"(?<!\w)({grouped_number})\s*€",
        lambda m: french_integer(parse_number(m.group(1))) + (" euro" if parse_number(m.group(1)) in (0, 1) else " euros"),
        text,
    )
    value = re.sub(
        rf"(?<!\w)({grouped_number})\s*[,\.]\s*(\d+)\s*%",
        lambda m: f"{french_integer(parse_number(m.group(1)))} virgule {french_integer(int(m.group(2)))} pour cent",
        value,
    )
    value = value.replace("%", " pour cent")
    # Le moteur hésite entre « pax » et « pack us » pour le sigle. Cette
    # graphie phonétique stabilise la prononciation française sans modifier
    # l'orthographe affichée.
    value = re.sub(r"\bpacsé\b", "paxée", value, flags=re.I)
    value = re.sub(r"\bPACS\b", "paxe", value, flags=re.I)
    value = re.sub(r"\bqualité d'héritier\b", "qualité, d'héritier", value, flags=re.I)
    # Les inversions avec traits d'union sont plus nettes pour le moteur vocal
    # lorsqu'elles sont espacées ; l'orthographe affichée reste inchangée.
    value = re.sub(r"(?<=\w)-(?=[a-zà-ÿ])", " ", value, flags=re.I)
    # Empêche la fusion récurrente « sépare les biens » -> « c'est parlé bien »
    # tout en conservant strictement les mêmes mots à l'écran et à l'oral.
    value = re.sub(r"\bsépare les biens\b", "sépare. Les biens", value, flags=re.I)
    value = re.sub(r"\bbien indivis par moitié\b", "bien indivis. Par moitié", value, flags=re.I)
    # Une réponse négative isolée par un point produit une pause trop lourde
    # chez les moteurs TTS (notamment ElevenLabs). À l'oral uniquement, on la
    # relie à l'explication qui suit. Le texte et le visuel restent inchangés.
    value = re.sub(r"^\s*Non\.\s+(?=\S)", "Non, ", value, flags=re.I)
    # Les références du type 796-0 sont lues comme deux nombres successifs,
    # jamais comme une soustraction ni chiffre par chiffre.
    value = re.sub(r"(?<!\w)(\d+)[-‐‑–—](\d+)(?!\w)",
                   lambda m: f"{french_integer(int(m.group(1)))} {french_integer(int(m.group(2)))}", value)
    value = re.sub(rf"(?<![\w]){grouped_number}(?![\w])",
                   lambda m: french_integer(parse_number(m.group())), value)
    return re.sub(r"\s+", " ", value).strip()


def _wav(path: Path):
    with wave.open(str(path), "rb") as handle:
        return handle.getparams(), handle.readframes(handle.getnframes()), handle.getnframes() / handle.getframerate()


def _spoken_word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)?", text))


def calibrated_atempo(text: str, duration: float, beat_id: str) -> float:
    """Ramène chaque page vers un débit cohérent sans altérer la voix."""
    words = max(1, _spoken_word_count(text))
    observed_wpm = words * 60.0 / max(duration, 0.01)
    role = canonical_voice_role(beat_id)
    target_wpm = TARGET_WPM[role]
    factor = target_wpm / observed_wpm
    return min(MAX_ATEMPO, max(MIN_ATEMPO, factor))


def prosody_for(beat_id: str) -> dict:
    role = canonical_voice_role(beat_id)
    return PROSODY.get(role, {"speed": VOICE_CONFIG["speed"],
                                 "exaggeration": VOICE_CONFIG["exaggeration"],
                                 "cfg_weight": VOICE_CONFIG["cfg_weight"]})


def join_clauses(paths: list[Path], target: Path, pause_seconds: float = .08) -> None:
    params,_,_=_wav(paths[0]); chunks=[]
    pause=b"\0"*(round(pause_seconds*params.framerate)*params.nchannels*params.sampwidth)
    for index,path in enumerate(paths):
        current,data,_=_wav(path)
        if current[:3] != params[:3]: raise RuntimeError("clauses vocales incompatibles")
        chunks.append(data)
        if index<len(paths)-1: chunks.append(pause)
    with wave.open(str(target),"wb") as handle:
        handle.setparams(params); handle.writeframes(b"".join(chunks))


def _ffmpeg() -> Path:
    local = Path(__file__).resolve().parents[1] / ".video-tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    if local.is_file(): return local
    raise SystemExit("FFmpeg local introuvable pour calibrer la durée de la voix")


def generate(spec_path: Path, output: Path, reference: Path) -> None:
    # Imports différés : le fournisseur ElevenLabs réutilise uniquement les
    # utilitaires audio de ce module. Charger MLX à l'import faisait planter
    # les rendus distants dans les sessions sans accès au GPU Metal.
    import huggingface_hub
    import mlx.core as mx
    from mlx_audio.tts.generate import generate_audio
    from mlx_audio.tts.utils import load_model

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    if not MODEL.exists() or not S3.exists() or not reference.exists():
        raise SystemExit("Modèle ou voix de référence BRITED introuvable")

    cb = importlib.import_module("mlx_audio.tts.models.chatterbox.chatterbox")
    cb.snapshot_download = lambda *args, **kwargs: str(S3)
    huggingface_hub.snapshot_download = lambda *args, **kwargs: str(S3)
    model = load_model(MODEL)
    config_path = output / "voice-config.json"
    # Un même rôle peut apparaître sur plusieurs pages (par exemple trois beats
    # « regle »). La position fait donc partie de la clé de cache afin qu'une
    # phrase ne puisse jamais remplacer silencieusement une autre.
    beat_keys = [f"{index:02d}_{beat['id']}" for index, beat in enumerate(spec["beats"], 1)]
    spoken_texts = {
        key: speech_text(beat["narration"])
        for key, beat in zip(beat_keys, spec["beats"])
    }
    reference_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
    script_hash = hashlib.sha256("\n".join(spoken_texts[key] for key in beat_keys).encode("utf-8")).hexdigest()
    beat_hashes = {
        key: hashlib.sha256(
            (spoken_texts[key]
             + json.dumps(VOICE_CONFIG, sort_keys=True)
             + json.dumps(prosody_for(beat.get("id", "")), sort_keys=True)
             + json.dumps({"target_wpm": TARGET_WPM[canonical_voice_role(beat.get("id", ""))],
                           "bounds": [MIN_ATEMPO, MAX_ATEMPO]}, sort_keys=True)
             + reference_hash).encode("utf-8")
        ).hexdigest()
        for key, beat in zip(beat_keys, spec["beats"])
    }
    previous_config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    cache_config = {"voice": VOICE_CONFIG, "hook_voice": HOOK_CONFIG, "reference_sha256": reference_hash,
                    "voice_signature": hashlib.sha256((reference_hash + json.dumps(VOICE_CONFIG, sort_keys=True) + json.dumps(HOOK_CONFIG, sort_keys=True)).encode()).hexdigest(),
                    "audio_format_version": AUDIO_FORMAT_VERSION, "mastering": MASTERING_FILTER,
                    "script_hash": script_hash, "beat_hashes": beat_hashes, "spoken_texts": spoken_texts,
                    "platform_speed_calibration": False, "speech_post_atempo": SPEECH_POST_ATEMPO,
                    "target_wpm": TARGET_WPM, "atempo_bounds": [MIN_ATEMPO, MAX_ATEMPO],
                    "prosody": PROSODY, "voice_seed": VOICE_SEED,
                    "segment_level_filter": SEGMENT_LEVEL_FILTER}
    voice_changed = (previous_config.get("voice", previous_config) != VOICE_CONFIG or
                     previous_config.get("audio_format_version") != AUDIO_FORMAT_VERSION or
                     previous_config.get("target_wpm") != TARGET_WPM or
                     previous_config.get("atempo_bounds") != [MIN_ATEMPO, MAX_ATEMPO] or
                     previous_config.get("prosody") != PROSODY or
                     previous_config.get("voice_seed") != VOICE_SEED)
    tempo_changed = previous_config.get("speech_post_atempo") != SPEECH_POST_ATEMPO
    # Écrit l'empreinte avant la boucle : si le moteur vocal doit être relancé,
    # chaque segment déjà terminé est réutilisé et la reprise se fait exactement
    # au premier fichier manquant. L'existence du WAV reste exigée ci-dessous.
    config_path.write_text(json.dumps(cache_config, ensure_ascii=False, indent=2), encoding="utf-8")

    paths: list[Path] = []
    durations: list[float] = []
    for index, beat in enumerate(spec["beats"], start=1):
        beat_key = beat_keys[index - 1]
        path = output / f"{index:02d}_{beat['id']}.wav"
        raw_path = output / f"{index:02d}_{beat['id']}-raw.wav"
        hash_path = output / f"{index:02d}_{beat['id']}.sha256"
        certified_hash = hash_path.read_text().strip() if hash_path.exists() else ""
        beat_changed = certified_hash != beat_hashes[beat_key]
        cached_wav = CERTIFIED_CACHE / f"{beat_hashes[beat_key]}.wav"
        cached_raw = CERTIFIED_CACHE / f"{beat_hashes[beat_key]}-raw.wav"
        if beat_changed and cached_wav.exists() and cached_raw.exists():
            # Une phrase déjà certifiée par Whisper est déterministe et prime
            # sur une nouvelle génération aléatoire du même texte.
            import shutil
            shutil.copy2(cached_wav, path)
            shutil.copy2(cached_raw, raw_path)
            hash_path.write_text(beat_hashes[beat_key]+"\n",encoding="utf-8")
            certified_hash = beat_hashes[beat_key]
            beat_changed = False
        if voice_changed or beat_changed or not path.exists() or not raw_path.exists():
            if path.exists(): path.unlink()
            if raw_path.exists(): raw_path.unlink()
            if hash_path.exists(): hash_path.unlink()
            is_hook = beat.get("id") == "hook"
            # Le moteur refuse parfois les fragments très courts. Une page reste
            # donc une unité vocale complète ; la clarté est assurée par les
            # paramètres stables et le contrôle Whisper renforcé.
            # Le CTA porte deux intentions distinctes : implication personnelle,
            # puis action. Les générer séparément évite que le moteur précipite
            # la seconde phrase et crée une chute artificielle.
            clauses = (re.split(r"(?<=\?)\s+", spoken_texts[beat_key])
                       if beat.get("id") == "cta" else [spoken_texts[beat_key]])
            clauses = [clause for clause in clauses if clause]
            generated=[]
            role = prosody_for(beat.get("id", ""))
            for clause_index,clause in enumerate(clauses,1):
                clause_path=output/f"{path.stem}-part{clause_index}.wav"
                # Même point de départ aléatoire pour toutes les pages : la
                # prosodie change selon le rôle, jamais l'identité de la voix.
                mx.random.seed(VOICE_SEED)
                generate_audio(
                    text=clause, model=model, ref_audio=str(reference),
                    lang_code="fr", speed=role["speed"], output_path=str(output),
                    file_prefix=clause_path.stem, join_audio=True, exaggeration=role["exaggeration"],
                    cfg_weight=role["cfg_weight"],
                    temperature=VOICE_CONFIG["temperature"],
                    top_p=VOICE_CONFIG["top_p"], min_p=VOICE_CONFIG["min_p"],
                    repetition_penalty=VOICE_CONFIG["repetition_penalty"], verbose=False,
                )
                generated.append(clause_path)
            if len(generated)==1: os.replace(generated[0],path)
            else: join_clauses(generated,path, pause_seconds=.20)
            for clause_path in generated: clause_path.unlink(missing_ok=True)
            if is_hook:
                slowed = output / f"{path.stem}-slowed.wav"
                subprocess.run([str(_ffmpeg()), "-y", "-loglevel", "error", "-i", str(path),
                                "-filter:a", f"atempo={HOOK_CONFIG['post_atempo']}",
                                "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(slowed)], check=True)
                os.replace(slowed, path)
            os.replace(path, raw_path)
        elif not raw_path.exists():
            # Première migration vers la chaîne de débit contrôlé : conserver
            # l'original pour que le réglage ne puisse jamais se cumuler.
            os.replace(path, raw_path)
        if voice_changed or beat_changed or tempo_changed or not path.exists():
            raw_duration = _wav(raw_path)[2]
            tempo = calibrated_atempo(spoken_texts[beat_key], raw_duration, beat.get("id", ""))
            subprocess.run([str(_ffmpeg()), "-y", "-loglevel", "error", "-i", str(raw_path),
                            "-filter:a", f"atempo={tempo:.6f},{SEGMENT_LEVEL_FILTER}",
                            "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(path)], check=True)
        # L'empreinte n'est écrite qu'après la création complète du WAV. Une
        # interruption ne peut donc plus certifier par erreur un ancien segment.
        hash_path.write_text(beat_hashes[beat_key]+"\n",encoding="utf-8")
        paths.append(path)
        durations.append(_wav(path)[2])

    expected_paths = set(paths)
    for stale in output.glob("[0-9][0-9]_*.wav"):
        if stale not in expected_paths and "slowed" not in stale.name and "-raw" not in stale.name:
            stale.unlink()

    speech_durations = list(durations)
    speech_rates = [
        round(_spoken_word_count(spoken_texts[key]) * 60.0 / max(duration, .01), 1)
        for key, duration in zip(beat_keys, speech_durations)
    ]
    post_pauses = [0.0 for _ in durations]

    params, _, _ = _wav(paths[0])
    incompatible = [path.name for path in paths if _wav(path)[0][:3] != params[:3]]
    if incompatible:
        raise RuntimeError("Contrôle audio refusé : formats WAV incohérents — " + ", ".join(incompatible))
    sample_size = params.nchannels * params.sampwidth
    silence = b"\0" * (round(PAUSE * params.framerate) * sample_size)
    chunks: list[bytes] = []
    for index, path in enumerate(paths):
        _, data, _ = _wav(path)
        chunks.append(data)
        if index < len(paths) - 1:
            beat_id = spec["beats"][index].get("id")
            # Les respirations sont identiques entre plateformes. Aucun recalage
            # de vitesse global ne doit changer le timbre, la diction ou le débit.
            # Les respirations structurantes durent exactement 0,9 seconde.
            # Les autres raccords conservent une micro-pause naturelle.
            pause = PAGE_SWITCH_HOLD if beat_id in {"hook", "question", "nuance"} else PAUSE
            # La question doit rester visible au moins quatre secondes, comme
            # prévu par les trois chartes. Le complément est une latence de
            # lecture sur la page, sans ralentir la voix ni rallonger tous les
            # changements de page.
            if beat_id == "question":
                pause = max(pause, 4.0 - speech_durations[index])
            chunks.append(b"\0" * (round(pause * params.framerate) * sample_size))
            durations[index] += pause
            post_pauses[index] = pause
    joined = output / "voice.wav"
    with wave.open(str(joined), "wb") as handle:
        handle.setparams(params)
        handle.writeframes(b"".join(chunks))
    targets = {"tiktok": (32.0, 45.0), "reels": (35.0, 48.0), "shorts": (38.0, 52.0)}
    low, high = targets.get(spec.get("platform"), (0.0, 60.0))
    actual = _wav(joined)[2]
    if actual > high:
        raise RuntimeError(f"Voix refusée : {actual:.2f} s dépasse la cible {high:.0f} s. Le script doit être resserré sans accélérer la voix.")
    if actual < low:
        raise RuntimeError(f"Voix refusée : {actual:.2f} s est sous la cible {low:.0f} s. Le script doit être enrichi sans ralentissement artificiel.")
    # Final speech mastering: remove rumble, improve consonant presence and keep
    # a stable social-video loudness without altering the narration timing.
    mastered = output / "voice-mastered.wav"
    subprocess.run([str(_ffmpeg()), "-y", "-loglevel", "error", "-i", str(joined),
                    "-filter:a", MASTERING_FILTER, "-ar", str(params.framerate), "-ac", str(params.nchannels),
                    "-sample_fmt", "s16", str(mastered)], check=True)
    os.replace(mastered, joined)
    (output / "timing.json").write_text(
        json.dumps({"audio": str(joined), "durations": durations,
                    "speech_durations": speech_durations, "speech_rates_wpm": speech_rates,
                    "post_pauses": post_pauses}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    config_path.write_text(json.dumps(cache_config, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    args = parser.parse_args()
    generate(args.spec, args.output, args.reference)


if __name__ == "__main__":
    main()
