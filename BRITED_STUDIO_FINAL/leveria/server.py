from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import threading
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from .audit import audit_script
from .generator import generate
from .daily import run as run_daily
from .store import Store
from .performance import score_script
from .scheduler import Scheduler
from .queue import ProductionQueue
from .script_batch import ScriptBatch
from .distribution import NativeDistribution
from .connections import PlatformConnections


ROOT = Path(os.environ.get("BRITED_ROOT", Path(__file__).resolve().parents[1])).resolve()
STORE = Store(ROOT)
QUEUE = ProductionQueue(STORE, run_daily)
BATCH = ScriptBatch(STORE)
DISTRIBUTION = NativeDistribution(ROOT)
CONNECTIONS = PlatformConnections(ROOT)
WEB = Path(__file__).with_name("web")


def safe_web_target(request_path: str) -> Path | None:
    """Resolve a public asset without ever leaving the dedicated web folder."""
    path = urlparse(request_path).path
    relative = "index.html" if path in ("/", "/index.html") else unquote(path.lstrip("/"))
    target = (WEB / relative).resolve()
    return target if WEB.resolve() in target.parents and target.is_file() else None


def load_env() -> None:
    path = ROOT / ".env"
    if not path.exists(): return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        print("[BRITED]", fmt % args)

    def send_json(self, code: int, value: object) -> None:
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def body(self) -> dict:
        size = int(self.headers.get("Content-Length", "0"))
        if size > 1_048_576:
            raise ValueError("Requête trop volumineuse")
        return json.loads(self.rfile.read(size) or b"{}")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path); path = parsed.path
        if path == "/api/final-scripts":
            day = parse_qs(parsed.query).get("date", [date.today().isoformat()])[0]
            try:
                return self.send_json(200, STORE.final_scripts(day))
            except ValueError as error:
                return self.send_json(400, {"error": str(error)})
        if path == "/api/editorial-plan":
            return self.send_json(200, STORE.face_camera_launch_plan())
        if path == "/api/shooting-library":
            query = parse_qs(parsed.query)
            start = query.get("start", [date.today().isoformat()])[0]
            try:
                days = int(query.get("days", ["14"])[0])
                return self.send_json(200, STORE.shooting_library(start, days))
            except ValueError as error:
                return self.send_json(400, {"error": str(error)})
        if path == "/api/state": return self.send_json(200, STORE.state())
        if path == "/api/scripts/batch/status":
            usage_path = ROOT / "data" / "api_usage.json"
            usage = json.loads(usage_path.read_text(encoding="utf-8")) if usage_path.exists() else {"total": {"calls": 0, "input_tokens": 0, "output_tokens": 0}}
            return self.send_json(200, {"batch": BATCH.load(), "apiUsage": usage})
        if path == "/api/health": return self.send_json(200, {"ok": True, "root": str(ROOT), "localOnly": True})
        if path == "/api/connections": return self.send_json(200, CONNECTIONS.status())
        if path.startswith("/files/"):
            # La page publique n'expose aucun fichier du dépôt. Les anciens
            # aperçus restent locaux mais ne sont jamais servis par HTTP.
            return self.send_json(404, {"error": "Fichier non exposé"})
        target = safe_web_target(self.path)
        if target is None:
            return self.send_json(404, {"error": "Page absente"})
        body = target.read_bytes(); self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "text/plain")
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        try:
            if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
                return self.send_json(415, {"error": "Format JSON requis"})
            origin = self.headers.get("Origin", "")
            if origin and origin not in ("http://127.0.0.1:8766", "http://localhost:8766"):
                return self.send_json(403, {"error": "Origine refusée"})
            payload = self.body()
            if self.path == "/api/calendar/build":
                value = STORE.build_calendar(date.fromisoformat(payload.get("start", date.today().isoformat())), int(payload.get("days", 30)))
                return self.send_json(200, value)
            if self.path == "/api/generate":
                return self.send_json(200, generate(STORE, str(payload["publicationId"])))
            if self.path == "/api/audit":
                publication = STORE.publication(str(payload["publicationId"]))
                script_path = publication.get("script_path", "")
                if not script_path: raise ValueError("Aucun script associé")
                text = (ROOT / script_path).read_text(encoding="utf-8")
                result = audit_script(text, publication["platform"])
                return self.send_json(200, {**result.json(), "performance": score_script(text, publication["platform"])})
            if self.path == "/api/script/read":
                return self.send_json(200, STORE.read_script(str(payload["publicationId"]), str(payload.get("path", ""))))
            if self.path == "/api/script/save":
                return self.send_json(200, STORE.save_script_revision(str(payload["publicationId"]), str(payload["text"])))
            if self.path == "/api/calendar/update":
                return self.send_json(200, STORE.update_calendar_entry(str(payload["publicationId"]), dict(payload.get("changes", {}))))
            if self.path == "/api/manifest/read":
                return self.send_json(200, STORE.manifest(str(payload["path"])))
            if self.path == "/api/heritage/search":
                return self.send_json(200, STORE.search_heritage(str(payload.get("query", "")), str(payload.get("kind", "conversation")), int(payload.get("offset", 0)), min(100, int(payload.get("limit", 50)))))
            if self.path == "/api/production/day":
                return self.send_json(200, STORE.production_day(str(payload["date"])))
            if self.path == "/api/scripts/batch":
                configured = json.loads((ROOT / "data/automation.json").read_text(encoding="utf-8"))
                allowed = list(configured.get("script_generation_platforms", ["reels", "shorts"]))
                requested = [str(item) for item in payload.get("platforms", allowed) if str(item) in allowed]
                if not requested: raise ValueError("Aucune plateforme autorisée pour la génération en série")
                return self.send_json(200, BATCH.prepare(date.fromisoformat(payload["start"]), int(payload.get("days", 7)), requested))
            if self.path == "/api/pilot":
                platform = str(payload["platform"])
                if platform not in ("tiktok", "reels", "shorts"): raise ValueError("Plateforme pilote inconnue")
                manifest = run_daily(STORE, date.fromisoformat(payload["date"]), int(payload["slot"]),
                                     generate_missing=False, render=True, platforms=[platform])
                return self.send_json(200, {"manifest": str(manifest.relative_to(ROOT)), "data": STORE.manifest(str(manifest.relative_to(ROOT)))})
            if self.path == "/api/backup":
                return self.send_json(200, STORE.backup(str(payload.get("label", "manual"))))
            if self.path == "/api/video/approve":
                return self.send_json(200, STORE.approve_video(str(payload["path"]), str(payload["publicationId"])))
            if self.path == "/api/distribution/prepare":
                return self.send_json(200, DISTRIBUTION.prepare(str(payload["path"])))
            if self.path == "/api/connections/save":
                return self.send_json(200, CONNECTIONS.save_public_setup(
                    str(payload["platform"]), dict(payload.get("values", {}))))
            if self.path == "/api/status":
                item = STORE.update_publication(str(payload["publicationId"]), statut=str(payload["status"]))
                return self.send_json(200, item)
            if self.path == "/api/validate":
                publication = STORE.publication(str(payload["publicationId"]))
                script_path = publication.get("script_path", "")
                if not script_path:
                    raise ValueError("Aucun script à valider")
                return self.send_json(200, STORE.validate_script(script_path, publication["id"]))
            if self.path == "/api/daily":
                job = QUEUE.enqueue(date.fromisoformat(payload["date"]), int(payload["slot"]),
                                    generate=bool(payload.get("generate", False)), render=bool(payload.get("render", False)))
                threading.Thread(target=QUEUE.run_pending, name=f"brited-job-{job['id']}", daemon=True).start()
                return self.send_json(200, next(x for x in QUEUE.load()["jobs"] if x["id"] == job["id"]))
            if self.path == "/api/queue/retry":
                job = QUEUE.retry(str(payload["jobId"])); threading.Thread(target=QUEUE.run_pending, name=f"brited-retry-{job['id']}", daemon=True).start()
                return self.send_json(200, next(x for x in QUEUE.load()["jobs"] if x["id"] == job["id"]))
            return self.send_json(404, {"error": "Action inconnue"})
        except (ValueError, KeyError, RuntimeError) as error:
            self.send_json(400, {"error": str(error)})
        except Exception as error:
            self.send_json(500, {"error": f"Erreur interne : {error}"})


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--port", type=int, default=8766); parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args(); load_env()
    policy_path = STORE.data / "editorial_policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8")) if policy_path.exists() else {}
    # Une nouvelle ligne éditoriale ne retire pas les validations historiques.
    # Les nouvelles générations conservent tous leurs contrôles habituels.
    if not policy.get("conversation_format", {}).get("preserve_existing_validated_versions", False):
        STORE.reconcile_certifications()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    def scheduled_run(day, slot):
        config_path = STORE.data / "automation.json"
        config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
        QUEUE.enqueue(day, slot, generate=bool(config.get("generate_missing_scripts", True)),
                      render=bool(config.get("render_validated_scripts", False)))
        return QUEUE.run_pending()
    def scheduled_preflight(start, days):
        config_path = STORE.data / "automation.json"
        config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
        platforms = list(config.get("script_generation_platforms", ["reels", "shorts"]))
        return BATCH.prepare(start, days, platforms)
    scheduler = Scheduler(STORE, scheduled_run, scheduled_preflight)
    scheduler.start()
    url = f"http://127.0.0.1:{args.port}"
    print(f"BRITED Studio local : {url}\nDonnées : {ROOT}")
    if not args.no_open: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__ == "__main__": main()
