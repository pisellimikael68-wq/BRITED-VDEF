from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .audit import audit_script
from .generator import generate
from .daily import run as run_daily
from .store import Store


ROOT = Path(os.environ.get("BRITED_ROOT", Path(__file__).resolve().parents[1])).resolve()
STORE = Store(ROOT)
WEB = Path(__file__).with_name("web")


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
        self.end_headers(); self.wfile.write(body)

    def body(self) -> dict:
        size = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(size) or b"{}")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/state": return self.send_json(200, STORE.state())
        if path == "/api/health": return self.send_json(200, {"ok": True, "root": str(ROOT), "localOnly": True})
        if path.startswith("/files/"):
            relative = unquote(path[len("/files/"):])
            target = (ROOT / relative).resolve()
            if ROOT not in target.parents or not target.is_file(): return self.send_json(404, {"error": "Fichier absent"})
            body = target.read_bytes(); self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        target = WEB / ("index.html" if path in ("/", "/index.html") else path.lstrip("/"))
        if not target.is_file(): return self.send_json(404, {"error": "Page absente"})
        body = target.read_bytes(); self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "text/plain")
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        try:
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
                return self.send_json(200, result.json())
            if self.path == "/api/status":
                item = STORE.update_publication(str(payload["publicationId"]), statut=str(payload["status"]))
                return self.send_json(200, item)
            if self.path == "/api/daily":
                manifest = run_daily(STORE, date.fromisoformat(payload["date"]), int(payload["slot"]),
                                     generate_missing=bool(payload.get("generate", False)), render=bool(payload.get("render", False)))
                return self.send_json(200, json.loads(manifest.read_text(encoding="utf-8")))
            return self.send_json(404, {"error": "Action inconnue"})
        except (ValueError, KeyError, RuntimeError) as error:
            self.send_json(400, {"error": str(error)})
        except Exception as error:
            self.send_json(500, {"error": f"Erreur interne : {error}"})


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--port", type=int, default=8766); parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args(); load_env()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{args.port}"
    print(f"BRITED Studio local : {url}\nDonnées : {ROOT}")
    if not args.no_open: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__ == "__main__": main()
