from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class LocalAIUnavailable(RuntimeError):
    pass


_STARTED_SERVERS: list[subprocess.Popen] = []


def _ollama_binary() -> Path | None:
    candidates = (
        Path("/Applications/Ollama.app/Contents/Resources/ollama"),
        Path("/usr/local/bin/ollama"),
        Path("/opt/homebrew/bin/ollama"),
    )
    return next((path for path in candidates if path.is_file()), None)


def _start_server(endpoint: str) -> bool:
    binary = _ollama_binary()
    if binary is None or not endpoint.startswith("http://127.0.0.1:11434"):
        return False
    process = subprocess.Popen(
        [str(binary), "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL, start_new_session=True,
    )
    _STARTED_SERVERS.append(process)
    for _ in range(30):
        try:
            with urllib.request.urlopen(endpoint + "/api/tags", timeout=1):
                return True
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(.2)
    return False


def local_config(root: Path) -> dict[str, Any]:
    path = root / "data" / "automation.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("local_ai", {})


def call_local(root: Path, prompt: str, *, json_output: bool | dict[str, Any] = False) -> tuple[str, str]:
    config = local_config(root)
    if not config.get("enabled"):
        raise LocalAIUnavailable("IA locale désactivée")
    endpoint = str(config.get("endpoint", "http://127.0.0.1:11434")).rstrip("/")
    model = str(config.get("model") or config.get("recommended_model_for_8gb") or "qwen3:1.7b")
    body: dict[str, Any] = {
        "model": model, "prompt": "/no_think\n" + prompt, "stream": False, "think": False,
        # Garder un contexte borné sur Mac portable. Un rapport JSON du comité
        # contient dix agents et exige davantage de sortie qu'un script court ;
        # un plafond trop bas produisait parfois un JSON tronqué.
        "options": {"temperature": 0.2, "num_ctx": 8192,
                    "num_predict": 2000 if json_output else 1200},
    }
    if json_output:
        body["format"] = json_output if isinstance(json_output, dict) else "json"
    request = urllib.request.Request(endpoint + "/api/generate", data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            payload = json.load(response)
    except TimeoutError:
        raise LocalAIUnavailable("IA locale : délai maximal de 4 minutes dépassé") from None
    except (urllib.error.URLError, OSError):
        if not _start_server(endpoint):
            raise LocalAIUnavailable("serveur Ollama impossible à démarrer") from None
        try:
            with urllib.request.urlopen(request, timeout=240) as response:
                payload = json.load(response)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise LocalAIUnavailable(f"IA locale indisponible après redémarrage : {type(exc).__name__}") from exc
    except (urllib.error.HTTPError, json.JSONDecodeError) as exc:
        raise LocalAIUnavailable(f"IA locale indisponible : {type(exc).__name__}") from exc
    text = str(payload.get("response", "")).strip()
    # Certains modèles Qwen exposent encore un bloc de réflexion malgré
    # think=False. Il ne doit jamais entrer dans un script ou un rapport.
    text = re.sub(r"(?is)^.*?</think>\s*", "", text).strip()
    text = re.sub(r"(?is)<think>.*?</think>\s*", "", text).strip()
    if not text:
        raise LocalAIUnavailable("IA locale : réponse vide")
    return text, model
