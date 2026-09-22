from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

from .audit import audit_script
from .generator import generate
from .store import Store, PLATFORMS, certified_by_reference_evidence
from .format_adapter import adapt_beats, beats_from_markdown
from .cta import cta_mode


REFERENCE_VALIDATIONS = {
    "tiktok": "design-system/VALIDATION_YOUTUBE_VISUEL_A_V7.json",
    "reels": "design-system/VALIDATION_YOUTUBE_VISUEL_A_V7.json",
    "shorts": "design-system/VALIDATION_YOUTUBE_VISUEL_A_V7.json",
}


def voice_cache_matches_active_provider(store: Store, voice_dir: Path) -> bool:
    """Refuse un cache audio créé avec un moteur ou une voix désormais obsolète."""
    provider_path = store.root / "config/voice-provider.json"
    cache_path = voice_dir / "voice-config.json"
    if not provider_path.is_file() or not cache_path.is_file():
        return False
    try:
        active = json.loads(provider_path.read_text(encoding="utf-8"))
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return False
    provider = active.get("active_provider", "local")
    if cached.get("provider", "local") != provider:
        return False
    if provider == "elevenlabs":
        return (
            cached.get("voice_id") == active.get("voice_id")
            and cached.get("model_id") == active.get("model_id")
            and cached.get("voice_settings") == active.get("voice_settings")
        )
    return True


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validated_visual_reference(store: Store, platform: str) -> dict[str, Any]:
    relative = REFERENCE_VALIDATIONS[platform]
    path = store.root / relative
    if not path.is_file():
        raise RuntimeError(f"Charte vidéo validée absente pour {platform}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "validated":
        raise RuntimeError(f"Charte vidéo non validée pour {platform}")
    video = store.root / str(payload.get("reference_video", ""))
    if not video.is_file():
        raise RuntimeError(f"Vidéo de référence validée absente pour {platform}")
    expected_hash = payload.get("reference_sha256", "")
    actual_hash = file_sha256(video)
    if not expected_hash or expected_hash != actual_hash:
        raise RuntimeError(f"Empreinte de la référence vidéo invalide pour {platform}")
    return {"validation": relative, "reference_video": str(video.relative_to(store.root)),
            "reference_sha256": actual_hash, "renderer": payload.get("renderer", ""),
            "delivery_profile": platform, "master_reference_platform": payload.get("platform")}


def consolidate_pilot_manifests(destination: Path, day: date, slot: int) -> Path | None:
    """Construit le manifeste de créneau dès que les trois pilotes sont verts."""
    manifests = [destination / f"manifest-pilot-{platform}.json" for platform in PLATFORMS]
    if not all(path.exists() for path in manifests):
        return None
    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in manifests]
    if not all(data.get("status") == "awaiting_approval" and
               all(item.get("status") == "awaiting_approval" for item in data.get("items", []))
               for data in payloads):
        return None
    items = [item for data in payloads for item in data.get("items", [])]
    items.sort(key=lambda item: PLATFORMS.index(item["platform"]))
    target = destination / "manifest.json"
    target.write_text(json.dumps({"date": day.isoformat(), "slot": slot,
        "status": "awaiting_approval", "publish_locked": True, "items": items,
        "consolidated_from_certified_pilots": True}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def narration(text: str) -> str:
    match = re.search(r"## Narration continue\s*(.*?)(?=\n## |\Z)", text, re.S | re.I)
    return (match.group(1) if match else text).strip()


def pages(text: str) -> list[dict[str, str]]:
    return beats_from_markdown(text)


def run(store: Store, day: date, slot: int, *, generate_missing: bool = False, render: bool = False,
        platforms: list[str] | None = None) -> Path:
    if slot not in (1, 2): raise ValueError("Le créneau doit être 1 ou 2")
    selected = [p for p in store.calendar().get("publications", []) if p.get("date") == day.isoformat() and int(p.get("slot", 0)) == slot]
    if platforms:
        selected = [p for p in selected if p.get("platform") in platforms]
    if not selected: raise RuntimeError("Aucune publication prévue pour ce créneau")
    linked_publications = list(selected)
    # Shorts reste la source éditoriale commune, mais chaque destination reçoit
    # un rendu autonome et contrôlé dans ses propres zones sûres.
    if platforms is None:
        shorts = next((item for item in selected if item.get("platform") == "shorts"), None)
        if shorts is None:
            raise RuntimeError("Script YouTube Shorts source absent pour ce créneau")
        by_platform = {item.get("platform"): item for item in selected}
        selected = []
        for delivery_platform in ("shorts", "reels", "tiktok"):
            linked = by_platform.get(delivery_platform, shorts)
            selected.append({**shorts, "id": linked.get("id", shorts["id"]),
                "platform": delivery_platform,
                "distribution_source_platform": "shorts",
                "source_publication_id": shorts["id"]})
    else:
        selected.sort(key=lambda item: {"shorts": 0, "reels": 1, "tiktok": 2}.get(item["platform"], 99))
    destination = store.production / day.isoformat() / f"slot-{slot}"
    destination.mkdir(parents=True, exist_ok=True)
    items: list[dict[str, Any]] = []
    for publication in selected:
        current_relative = publication.get("script_path", "")
        current_validated = bool(current_relative and store.validations().get(current_relative, {}).get("validated"))
        if generate_missing and (not current_relative or not current_validated):
            try:
                generate(store, publication["id"]); publication = store.publication(publication["id"])
            except Exception as error:
                items.append({"publication_id": publication["id"], "platform": publication["platform"],
                              "title": publication["titre"], "status": "blocked",
                              "warnings": [f"Génération impossible : {error}"]})
                continue
        script_path = store.root / publication.get("script_path", "")
        warnings: list[str] = []
        video = ""
        actual_duration = None
        if not publication.get("script_path") or not script_path.is_file():
            items.append({"publication_id": publication["id"], "platform": publication["platform"],
                          "title": publication["titre"], "status": "blocked", "warnings": ["Script natif validé absent"]})
            continue
        relative_script = str(script_path.relative_to(store.root))
        validation = store.validations().get(relative_script, {})
        if not validation.get("validated"):
            items.append({"publication_id": publication["id"], "platform": publication["platform"],
                          "title": publication["titre"], "script": relative_script,
                          "status": "blocked", "warnings": ["Validation humaine du script absente"]})
            continue
        text = script_path.read_text(encoding="utf-8")
        # Le script et la narration sont ceux de Shorts pour les trois rendus ;
        # seul le profil de composition change selon la destination.
        audit = audit_script(text, "shorts")
        reference_evidence_ok = certified_by_reference_evidence(
            store.root, script_path, "shorts", validation, list(audit.errors)
        )
        if not audit.ok and not reference_evidence_ok:
            items.append({"publication_id": publication["id"], "platform": publication["platform"],
                          "title": publication["titre"], "script": str(script_path), "status": "blocked",
                          "audit": audit.json(), "warnings": list(audit.errors)})
            continue
        try:
            visual_reference = validated_visual_reference(store, publication["platform"])
        except RuntimeError as error:
            items.append({"publication_id": publication["id"], "platform": publication["platform"],
                          "title": publication["titre"], "script": relative_script,
                          "status": "blocked", "warnings": [str(error)]})
            continue
        platform_dir = destination / publication["platform"]; platform_dir.mkdir(parents=True, exist_ok=True)
        source_beats = pages(text)
        adapted_beats, adaptation = adapt_beats(source_beats, "shorts")
        spec = {"publication_id": publication["id"], "platform": publication["platform"],
                "concept_id": publication["concept_id"], "title": publication["titre"],
                "header": publication["titre"], "serie": publication.get("serie", "finance"),
                "narration": narration(text), "source_beats": source_beats, "beats": adapted_beats,
                "format_adaptation": adaptation.json(),
                # La page de réponse future hiérarchise automatiquement le
                # verdict et les précisions sans modifier le script certifié.
                "answer_design": "adaptive_sections_v2",
                "cta_mode": publication.get("cta_mode") or cta_mode(day, slot),
                "disclaimer": "Information générale • pas un conseil personnalisé"}
        spec_path = platform_dir / "spec.json"
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (platform_dir / "format-adaptation.json").write_text(json.dumps(adaptation.json(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        status = "ready_for_render"
        if render:
            # Le routeur choisit le moteur vocal officiellement activé. Il
            # conserve la voix locale certifiée tant qu'un aperçu ElevenLabs
            # n'a pas été explicitement validé et activé.
            voice = store.root / "video_pipeline/generate_voice.py"
            renderer = store.root / "video_pipeline/render_social_visual_a.py"
            if not voice.exists() or not renderer.exists():
                warnings.append("Modules vidéo absents"); status = "blocked"
            else:
                audio_python = Path("/Users/Shared/BRITED-Audio/bin/python")
                if not audio_python.exists(): audio_python = Path(sys.executable)
                own_voice_dir = platform_dir / "voice"
                shared_voice_dir = destination / "shorts" / "voice"
                voice_dir = (shared_voice_dir if publication["platform"] != "shorts"
                             and (shared_voice_dir / "timing.json").exists() else own_voice_dir)
                try:
                    oral = store.root / "video_pipeline/verify_voice_content.py"
                    existing_timing = voice_dir / "timing.json"
                    existing_check = voice_dir / "voice.voice-content-check.json"
                    cache_matches_provider = voice_cache_matches_active_provider(store, voice_dir)
                    if not cache_matches_provider:
                        # The cached reports describe the previous waveform and must
                        # never validate audio made with another provider or voice.
                        for stale_report in (
                            existing_check,
                            voice_dir / "voice.audio-check.json",
                        ):
                            stale_report.unlink(missing_ok=True)
                    cached_timing = (
                        json.loads(existing_timing.read_text(encoding="utf-8"))
                        if existing_timing.exists() else {}
                    )
                    cached_check = (
                        json.loads(existing_check.read_text(encoding="utf-8"))
                        if existing_check.exists() else {}
                    )
                    voice_config_path = voice_dir / "voice-config.json"
                    cached_voice_config = (
                        json.loads(voice_config_path.read_text(encoding="utf-8"))
                        if voice_config_path.exists() else {}
                    )
                    # Un cache vocal n'est réutilisable que s'il décrit toutes
                    # les pages du spec courant. Cela empêche notamment qu'un
                    # ancien rendu à six pages fasse disparaître silencieusement
                    # une nouvelle clôture située en page sept.
                    cache_matches_current_spec = (
                        len(cached_timing.get("durations", [])) == len(spec["beats"])
                        and len(cached_timing.get("speech_durations", [])) == len(spec["beats"])
                        and len(cached_check.get("pages", [])) == len(spec["beats"])
                        and cached_voice_config.get("spec_sha256") == file_sha256(spec_path)
                    )
                    existing_audio_valid = (
                        existing_timing.exists()
                        and existing_check.exists()
                        and cache_matches_provider
                        and cache_matches_current_spec
                        and cached_check.get("passed") is True
                    )
                    for voice_attempt in range(3):
                        if existing_audio_valid:
                            break
                        subprocess.run([str(audio_python), str(voice), str(spec_path), str(voice_dir)], check=True, cwd=store.root)
                        if not oral.exists(): break
                        try:
                            subprocess.run([str(audio_python), str(oral), str(spec_path), str(voice_dir / "timing.json")], check=True, cwd=store.root)
                            break
                        except subprocess.CalledProcessError:
                            report_path=voice_dir/"voice.voice-content-check.json"
                            report=json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
                            failed={page.get("beat") for page in report.get("pages",[]) if not page.get("passed")}
                            existing_audio_valid = False
                            if voice_attempt==2 or not failed: raise
                            # Seules les phrases réellement refusées sont
                            # invalidées puis recréées ; jamais les segments sains.
                            for index,beat in enumerate(spec["beats"],1):
                                if beat["id"] not in failed: continue
                                for suffix in (".wav","-raw.wav",".sha256"):
                                    (voice_dir/f"{index:02d}_{beat['id']}{suffix}").unlink(missing_ok=True)
                    video_path = platform_dir / f"{publication['concept_id']}__{publication['platform']}.mp4"
                    subprocess.run([sys.executable, str(renderer), str(spec_path), str(video_path), "--timing", str(voice_dir / "timing.json")], check=True, cwd=store.root)
                    verifier = store.root / "video_pipeline/verify_video_words.py"
                    quality = store.root / "video_pipeline/verify_video_quality.py"
                    if verifier.exists(): subprocess.run([sys.executable, str(verifier), str(spec_path), str(voice_dir / "timing.json"), str(video_path)], check=True, cwd=store.root)
                    if quality.exists(): subprocess.run([sys.executable, str(quality), str(spec_path), str(voice_dir / "timing.json"), str(video_path)], check=True, cwd=store.root)
                    trace_path = video_path.with_suffix('.render-trace.json')
                    if not trace_path.exists():
                        raise RuntimeError("Preuve du profil visuel absente")
                    trace = json.loads(trace_path.read_text(encoding="utf-8"))
                    features = trace.get("features", {})
                    if (features.get("delivery_profile") != publication["platform"] or
                            not features.get("platform_specific_composition")):
                        raise RuntimeError(f"Cadrage {publication['platform']} non certifié")
                    instagram_audit = store.root / "video_pipeline/audit_instagram.py"
                    if publication["platform"] == "reels" and instagram_audit.exists():
                        subprocess.run([sys.executable, str(instagram_audit), str(video_path)], check=True, cwd=store.root)
                    quality_path = video_path.with_suffix('.quality-check.json')
                    if quality_path.exists(): actual_duration = json.loads(quality_path.read_text(encoding="utf-8")).get("expected_duration")
                    video = str(video_path); status = "awaiting_approval"
                except Exception as error:
                    warnings.append(f"Production ou contrôle vidéo refusé : {error}"); status = "blocked"
        item={"publication_id": publication["id"], "platform": publication["platform"],
                      "title": publication["titre"], "script": str(script_path), "video": video,
                      "script_sha256": file_sha256(script_path), "spec_sha256": file_sha256(spec_path),
                      "video_sha256": file_sha256(Path(video)) if video and Path(video).is_file() else "",
                      "visual_reference": visual_reference,
                      "reference_evidence_accepted": reference_evidence_ok,
                      "duration": actual_duration or audit.seconds, "status": status, "audit": audit.json(), "warnings": warnings,
                      "validation": validation, "review_path": validation.get("review_path", ""),
                      "quality_report": str(video_path.with_suffix('.quality-check.json')) if video and video_path.with_suffix('.quality-check.json').exists() else "",
                      "word_report": str(video_path.with_suffix('.word-check.json')) if video and video_path.with_suffix('.word-check.json').exists() else ""}
        destinations = {"reels": ["instagram", "facebook"],
                        "tiktok": ["tiktok"], "shorts": ["youtube"]}
        item["distribution_destinations"] = destinations[publication["platform"]]
        item["delivery_profile"] = publication["platform"]
        item["shared_identical_video"] = False
        if publication["platform"] == "reels":
            item["facebook_delivery_mode"] = "instagram_crosspost"
        items.append(item)
    suffix = "-pilot-" + "-".join(platforms) if platforms else ""
    manifest = destination / f"manifest{suffix}.json"
    manifest_status = "blocked" if any(item.get("status") == "blocked" for item in items) else ("awaiting_approval" if render else "scripts_ready")
    manifest.write_text(json.dumps({"date": day.isoformat(), "slot": slot, "status": manifest_status,
        "publish_locked": True, "items": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if platforms and render:
        consolidate_pilot_manifests(destination, day, slot)
    for item in items:
        if item.get("status") == "awaiting_approval":
            store.update_publication(item["publication_id"], statut="video_prete", manifest_path=str(manifest.relative_to(store.root)))
    return manifest


def approve(manifest: Path) -> None:
    data = json.loads(manifest.read_text(encoding="utf-8")); data["status"] = "approved"
    data["publish_locked"] = True  # Approval never grants publication rights.
    data["approved_for_publication_workflow"] = True
    for item in data.get("items", []):
        if item.get("status") == "awaiting_approval":
            item["status"] = "approved"
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(prog="BRITED quotidien")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--slot", type=int, required=True, choices=(1, 2))
    parser.add_argument("--date", dest="day", type=date.fromisoformat, default=date.today())
    parser.add_argument("--generate", action="store_true", help="Générer les scripts natifs manquants")
    parser.add_argument("--render", action="store_true", help="Créer voix et vidéos après validation des scripts")
    parser.add_argument("--platform", action="append", choices=PLATFORMS, help="Limiter à une plateforme (mode pilote)")
    parser.add_argument("--approve", type=Path, help="Approuver un manifeste déjà contrôlé (publication toujours verrouillée)")
    args = parser.parse_args()
    if args.approve:
        approve(args.approve)
        print(args.approve)
        return
    manifest = run(Store(args.root.resolve()), args.day, args.slot,
                   generate_missing=args.generate, render=args.render, platforms=args.platform)
    print(manifest)


if __name__ == "__main__":
    main()
