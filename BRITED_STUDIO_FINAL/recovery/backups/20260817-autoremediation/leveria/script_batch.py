from __future__ import annotations

import json
import threading
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from .generator import generate
from .audit import audit_script


class ScriptBatch:
    """Progressive, resumable script preparation independent from video rendering."""

    def __init__(self, store):
        self.store = store
        self.path = store.data / "script_batch.json"
        self.lock = threading.Lock()
        state = self.load()
        if state.get("status") == "running":
            for item in state.get("items", []):
                if item.get("status") == "running":
                    item["status"] = "pending"
                    item["error"] = ""
            state["resumed_at"] = datetime.now().isoformat(timespec="seconds")
            self._summary(state)
            self.save(state)
            threading.Thread(target=self._run, name="brited-script-batch-resume", daemon=True).start()

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"status": "idle", "items": [], "summary": {"total": 0, "certified": 0, "blocked": 0, "pending": 0}}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"status": "invalid", "items": [], "summary": {"total": 0, "certified": 0, "blocked": 0, "pending": 0}}

    def save(self, value: dict[str, Any]) -> None:
        temporary = self.path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.path)

    def prepare(self, start: date, days: int, platforms: list[str]) -> dict[str, Any]:
        with self.lock:
            current = self.load()
            if current.get("status") == "running":
                if current.get("start") == start.isoformat() and int(current.get("days", 0)) == int(days) and current.get("platforms") == platforms:
                    return current
                raise RuntimeError("Une préparation de scripts est déjà en cours ; le nouveau lot attendra la prochaine fenêtre")
            end = start + timedelta(days=max(1, days) - 1)
            selected = [p for p in self.store.calendar().get("publications", [])
                        if start.isoformat() <= p.get("date", "") <= end.isoformat() and p.get("platform") in platforms]
            items = []
            validations = self.store.validations()
            for publication in selected:
                relative = publication.get("script_path", "")
                certified = bool(relative and validations.get(relative, {}).get("validated"))
                if certified:
                    candidate = self.store.root / relative
                    certified = bool(candidate.is_file() and audit_script(candidate.read_text(encoding="utf-8"), publication["platform"]).ok)
                items.append({"publication_id": publication["id"], "date": publication["date"], "slot": publication["slot"],
                              "platform": publication["platform"], "title": publication["titre"],
                              "status": "certified" if certified else "pending", "path": relative if certified else "", "error": ""})
            state = {"status": "running", "started_at": datetime.now().isoformat(timespec="seconds"),
                     "start": start.isoformat(), "days": days, "platforms": platforms,
                     "remediation_round": 0, "maximum_remediation_rounds": 1, "items": items}
            self._summary(state); self.save(state)
        threading.Thread(target=self._run, name="brited-script-batch", daemon=True).start()
        return self.load()

    def _summary(self, state: dict[str, Any]) -> None:
        items = state.get("items", [])
        state["summary"] = {"total": len(items), "certified": sum(x["status"] == "certified" for x in items),
                            "blocked": sum(x["status"] == "blocked" for x in items),
                            "pending": sum(x["status"] in ("pending", "running") for x in items)}

    def _run(self) -> None:
        while True:
            with self.lock:
                state = self.load()
                item = next((x for x in state.get("items", []) if x.get("status") == "pending"), None)
                if item is None:
                    blocked = [x for x in state.get("items", []) if x.get("status") == "blocked"]
                    remediation_round = int(state.get("remediation_round", 0))
                    maximum_rounds = int(state.get("maximum_remediation_rounds", 1))
                    if blocked and remediation_round < maximum_rounds:
                        for blocked_item in blocked:
                            blocked_item.update(status="pending", error="")
                        state["remediation_round"] = remediation_round + 1
                        state["remediation_started_at"] = datetime.now().isoformat(timespec="seconds")
                        self._summary(state); self.save(state)
                        continue
                    state["status"] = "blocked" if any(x.get("status") == "blocked" for x in state.get("items", [])) else "complete"
                    state["completed_at"] = datetime.now().isoformat(timespec="seconds")
                    self._summary(state); self.save(state); return
                item["status"] = "running"; self._summary(state); self.save(state)
                publication_id = item["publication_id"]
            try:
                result = generate(self.store, publication_id)
                status = "certified" if result.get("automatic_validation") else "blocked"
                path = result.get("path", "")
                review_path = result.get("review_path", "")
                findings = [str(value) for value in result.get("review", {}).get("errors", [])]
                error = "" if status == "certified" else " · ".join(findings[:3]) or "Certification inférieure à 9,5/10"
            except Exception as exc:
                status, path, review_path, error = "blocked", "", "", str(exc)
            with self.lock:
                state = self.load(); saved = next(x for x in state["items"] if x["publication_id"] == publication_id)
                saved.update(status=status, path=path, review_path=review_path, error=error,
                             completed_at=datetime.now().isoformat(timespec="seconds"))
                self._summary(state); self.save(state)
