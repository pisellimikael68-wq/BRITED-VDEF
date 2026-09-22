from __future__ import annotations

import json
import threading
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


class Scheduler:
    """Planificateur local prudent : déclenche uniquement à la minute exacte, jamais au rattrapage."""
    def __init__(self, store, callback, preflight_callback=None):
        self.store, self.callback, self.preflight_callback = store, callback, preflight_callback
        self.state_path = store.data / "automation_state.json"
        self.stop_event = threading.Event()

    def due(self, now: datetime) -> int | None:
        run = self.due_run(now)
        return int(run["slot"]) if run and "slot" in run else None

    def due_run(self, now: datetime) -> dict | None:
        config_path = self.store.data / "automation.json"
        if not config_path.exists(): return None
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not config.get("active", True): return None
        state = json.loads(self.state_path.read_text(encoding="utf-8")) if self.state_path.exists() else {}
        runs = list(config.get("runs", []))
        if config.get("preflight"):
            runs.insert(0, {**config["preflight"], "mode": "preflight"})
        for run in runs:
            hour, minute = map(int, run["time"].split(":"))
            key = f"{now.date().isoformat()}:{run.get('mode', 'slot')}:{run.get('slot', '')}"
            if (now.hour, now.minute) == (hour, minute) and state.get(key) != "done":
                return run
        return None

    def mark(self, now: datetime, slot: int, status: str) -> None:
        state = json.loads(self.state_path.read_text(encoding="utf-8")) if self.state_path.exists() else {}
        state[f"{now.date().isoformat()}:slot:{slot}"] = status
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def mark_run(self, now: datetime, run: dict, status: str) -> None:
        state = json.loads(self.state_path.read_text(encoding="utf-8")) if self.state_path.exists() else {}
        key = f"{now.date().isoformat()}:{run.get('mode', 'slot')}:{run.get('slot', '')}"
        state[key] = status
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def run(self) -> None:
        while not self.stop_event.wait(20):
            now = datetime.now(); run = self.due_run(now)
            if run:
                self.mark_run(now, run, "running")
                try:
                    if run.get("mode") == "preflight":
                        days = int(run.get("days_ahead", 7))
                        if self.preflight_callback:
                            self.preflight_callback(now.date() + timedelta(days=1), days)
                        else:
                            for offset in range(1, days + 1):
                                for slot in (1, 2):
                                    self.callback(now.date() + timedelta(days=offset), slot)
                        message = f"Les scripts des {days} prochains jours sont préparés et certifiés."
                    else:
                        slot = int(run["slot"]); self.callback(now.date(), slot)
                        message = f"Le créneau {slot} a été traité. Ouvrez BRITED Studio uniquement si des vidéos attendent votre validation."
                    self.mark_run(now, run, "done")
                    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "BRITED Studio"'], check=False)
                except Exception as error:
                    self.mark_run(now, run, f"error: {error}")
                    subprocess.run(["osascript", "-e", 'display notification "Une préparation est bloquée : ouvrez BRITED Studio." with title "BRITED Studio"'], check=False)

    def start(self) -> None:
        threading.Thread(target=self.run, name="brited-scheduler", daemon=True).start()
