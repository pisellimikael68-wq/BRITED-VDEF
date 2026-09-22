from __future__ import annotations

import json
import threading
import uuid
from datetime import date, datetime
from pathlib import Path


class ProductionQueue:
    def __init__(self, store, runner):
        self.store, self.runner = store, runner
        self.path = store.data / "production_queue.json"
        self.lock = threading.Lock()

    def load(self) -> dict:
        if not self.path.exists(): return {"jobs": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, value: dict) -> None:
        self.path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def enqueue(self, day: date, slot: int, *, generate=True, render=True) -> dict:
        with self.lock:
            value = self.load()
            existing = next((j for j in value["jobs"] if j["date"] == day.isoformat() and j["slot"] == slot and j["status"] in ("queued", "running")), None)
            if existing: return existing
            job = {"id": uuid.uuid4().hex[:12], "date": day.isoformat(), "slot": slot,
                   "generate": generate, "render": render, "status": "queued", "attempts": 0,
                   "created_at": datetime.now().isoformat(timespec="seconds"), "error": "", "manifest": ""}
            value["jobs"].append(job); self.save(value); return job

    def retry(self, job_id: str) -> dict:
        with self.lock:
            value = self.load(); job = next(j for j in value["jobs"] if j["id"] == job_id)
            if job["status"] not in ("failed", "blocked"): raise ValueError("Cette tâche ne nécessite pas de reprise")
            job.update(status="queued", error=""); self.save(value); return job

    def run_pending(self) -> list[dict]:
        completed = []
        while True:
            with self.lock:
                value = self.load(); job = next((j for j in value["jobs"] if j["status"] == "queued"), None)
                if not job: return completed
                job["status"] = "running"; job["attempts"] += 1; job["started_at"] = datetime.now().isoformat(timespec="seconds"); self.save(value)
            try:
                manifest = self.runner(self.store, date.fromisoformat(job["date"]), job["slot"], generate_missing=job["generate"], render=job["render"])
                content = json.loads(manifest.read_text(encoding="utf-8"))
                status = "blocked" if content.get("status") == "blocked" else content.get("status", "scripts_ready")
                error = "; ".join(w for i in content.get("items", []) for w in i.get("warnings", []))
            except Exception as exc:
                message = str(exc)
                if "Aucune publication prévue" in message:
                    # Une date vide est un résultat normal du calendrier, pas
                    # une panne nécessitant l'intervention de l'utilisateur.
                    status, error, manifest = "no_content", "", None
                else:
                    status, error, manifest = "failed", message, None
            with self.lock:
                value = self.load(); saved = next(j for j in value["jobs"] if j["id"] == job["id"])
                saved.update(status=status, error=error, completed_at=datetime.now().isoformat(timespec="seconds"),
                             manifest=str(manifest.relative_to(self.store.root)) if manifest else "")
                self.save(value); completed.append(saved.copy())
