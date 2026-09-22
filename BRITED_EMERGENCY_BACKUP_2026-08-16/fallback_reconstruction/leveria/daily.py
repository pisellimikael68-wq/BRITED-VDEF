from __future__ import annotations

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


def narration(text: str) -> str:
    match = re.search(r"## Narration continue\s*(.*?)(?=\n## |\Z)", text, re.S | re.I)
    return (match.group(1) if match else text).strip()


def pages(text: str) -> list[dict[str, str]]:
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[- :|]+$", line):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 5 and cells[0].isdigit():
                rows.append({"label": cells[1], "narration": cells[2], "visual": cells[3], "screen_text": cells[4]})
    return rows


def run(store: Store, day: date, slot: int, *, generate_missing: bool = False, render: bool = False) -> Path:
    if slot not in (1, 2): raise ValueError("Le créneau doit être 1 ou 2")
    selected = [p for p in store.calendar().get("publications", []) if p.get("date") == day.isoformat() and int(p.get("slot", 0)) == slot]
    selected.sort(key=lambda item: PLATFORMS.index(item["platform"]))
    if not selected: raise RuntimeError("Aucune publication prévue pour ce créneau")
    destination = store.production / day.isoformat() / f"slot-{slot}"
    destination.mkdir(parents=True, exist_ok=True)
    items: list[dict[str, Any]] = []
    for publication in selected:
        if not publication.get("script_path") and generate_missing:
            generate(store, publication["id"]); publication = store.publication(publication["id"])
        script_path = store.root / publication.get("script_path", "")
        warnings: list[str] = []
        video = ""
        if not publication.get("script_path") or not script_path.is_file():
            items.append({"publication_id": publication["id"], "platform": publication["platform"],
                          "title": publication["titre"], "status": "blocked", "warnings": ["Script natif validé absent"]})
            continue
        text = script_path.read_text(encoding="utf-8")
        audit = audit_script(text, publication["platform"])
        if not audit.ok:
            items.append({"publication_id": publication["id"], "platform": publication["platform"],
                          "title": publication["titre"], "script": str(script_path), "status": "blocked",
                          "audit": audit.json(), "warnings": list(audit.errors)})
            continue
        platform_dir = destination / publication["platform"]; platform_dir.mkdir(parents=True, exist_ok=True)
        spec = {"publication_id": publication["id"], "platform": publication["platform"],
                "concept_id": publication["concept_id"], "title": publication["titre"],
                "narration": narration(text), "beats": pages(text),
                "disclaimer": "Information générale • pas un conseil personnalisé"}
        spec_path = platform_dir / "spec.json"
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
                subprocess.run([str(audio_python), str(voice), str(spec_path), str(voice_dir)], check=True, cwd=store.root)
                video_path = platform_dir / f"{publication['concept_id']}__{publication['platform']}.mp4"
                subprocess.run([sys.executable, str(renderer), str(spec_path), str(video_path), "--timing", str(voice_dir / "timing.json")], check=True, cwd=store.root)
                video = str(video_path); status = "awaiting_approval"
        items.append({"publication_id": publication["id"], "platform": publication["platform"],
                      "title": publication["titre"], "script": str(script_path), "video": video,
                      "duration": audit.seconds, "status": status, "audit": audit.json(), "warnings": warnings})
    manifest = destination / "manifest.json"
    manifest.write_text(json.dumps({"date": day.isoformat(), "slot": slot, "status": "awaiting_approval",
        "publish_locked": True, "items": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def approve(manifest: Path) -> None:
    data = json.loads(manifest.read_text(encoding="utf-8")); data["status"] = "approved"
    data["publish_locked"] = True  # Approval never grants publication rights.
    data["approved_for_publication_workflow"] = True
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
