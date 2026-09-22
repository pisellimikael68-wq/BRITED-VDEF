from __future__ import annotations

import argparse
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
from .store import Store, PLATFORMS
from .format_adapter import adapt_beats, beats_from_markdown


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
    selected.sort(key=lambda item: PLATFORMS.index(item["platform"]))
    if not selected: raise RuntimeError("Aucune publication prévue pour ce créneau")
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
        audit = audit_script(text, publication["platform"])
        if not audit.ok:
            items.append({"publication_id": publication["id"], "platform": publication["platform"],
                          "title": publication["titre"], "script": str(script_path), "status": "blocked",
                          "audit": audit.json(), "warnings": list(audit.errors)})
            continue
        platform_dir = destination / publication["platform"]; platform_dir.mkdir(parents=True, exist_ok=True)
        source_beats = pages(text)
        adapted_beats, adaptation = adapt_beats(source_beats, publication["platform"])
        spec = {"publication_id": publication["id"], "platform": publication["platform"],
                "concept_id": publication["concept_id"], "title": publication["titre"],
                "header": publication["titre"], "serie": publication.get("serie", "finance"),
                "narration": narration(text), "source_beats": source_beats, "beats": adapted_beats,
                "format_adaptation": adaptation.json(),
                "disclaimer": "Information générale • pas un conseil personnalisé"}
        spec_path = platform_dir / "spec.json"
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (platform_dir / "format-adaptation.json").write_text(json.dumps(adaptation.json(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        status = "ready_for_render"
        if render:
            voice = store.root / "video_pipeline/generate_voice_local.py"
            renderer = store.root / "video_pipeline/render_social.py"
            if not voice.exists() or not renderer.exists():
                warnings.append("Modules vidéo absents"); status = "blocked"
            else:
                audio_python = Path("/Users/Shared/BRITED-Audio/bin/python")
                if not audio_python.exists(): audio_python = Path(sys.executable)
                voice_dir = platform_dir / "voice"
                try:
                    subprocess.run([str(audio_python), str(voice), str(spec_path), str(voice_dir)], check=True, cwd=store.root)
                    video_path = platform_dir / f"{publication['concept_id']}__{publication['platform']}.mp4"
                    subprocess.run([sys.executable, str(renderer), str(spec_path), str(video_path), "--timing", str(voice_dir / "timing.json")], check=True, cwd=store.root)
                    verifier = store.root / "video_pipeline/verify_video_words.py"
                    quality = store.root / "video_pipeline/verify_video_quality.py"
                    if verifier.exists(): subprocess.run([sys.executable, str(verifier), str(spec_path), str(voice_dir / "timing.json"), str(video_path)], check=True, cwd=store.root)
                    if quality.exists(): subprocess.run([sys.executable, str(quality), str(spec_path), str(voice_dir / "timing.json"), str(video_path)], check=True, cwd=store.root)
                    quality_path = video_path.with_suffix('.quality-check.json')
                    if quality_path.exists(): actual_duration = json.loads(quality_path.read_text(encoding="utf-8")).get("expected_duration")
                    video = str(video_path); status = "awaiting_approval"
                except Exception as error:
                    warnings.append(f"Production ou contrôle vidéo refusé : {error}"); status = "blocked"
        items.append({"publication_id": publication["id"], "platform": publication["platform"],
                      "title": publication["titre"], "script": str(script_path), "video": video,
                      "duration": actual_duration or audit.seconds, "status": status, "audit": audit.json(), "warnings": warnings,
                      "validation": validation, "review_path": validation.get("review_path", ""),
                      "quality_report": str(video_path.with_suffix('.quality-check.json')) if video and video_path.with_suffix('.quality-check.json').exists() else "",
                      "word_report": str(video_path.with_suffix('.word-check.json')) if video and video_path.with_suffix('.word-check.json').exists() else ""})
    suffix = "-pilot-" + "-".join(platforms) if platforms else ""
    manifest = destination / f"manifest{suffix}.json"
    manifest_status = "blocked" if any(item.get("status") == "blocked" for item in items) else ("awaiting_approval" if render else "scripts_ready")
    manifest.write_text(json.dumps({"date": day.isoformat(), "slot": slot, "status": manifest_status,
        "publish_locked": True, "items": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in items:
        if item.get("status") == "awaiting_approval":
            store.update_publication(item["publication_id"], statut="video_prete", manifest_path=str(manifest.relative_to(store.root)))
    return manifest


def approve(manifest: Path) -> None:
    data = json.loads(manifest.read_text(encoding="utf-8")); data["status"] = "approved"
    data["publish_locked"] = True  # Approval never grants publication rights.
    data["approved_for_publication_workflow"] = True
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
