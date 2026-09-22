from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Any


_LOCK = threading.Lock()


def record_api_usage(response: dict[str, Any], purpose: str, model: str) -> None:
    """Persist token counters only; prompts, responses and API keys are never recorded."""
    usage = response.get("usage") or {}
    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    root = Path(os.environ.get("BRITED_ROOT", Path(__file__).resolve().parents[1])).resolve()
    path = root / "data" / "api_usage.json"
    today = datetime.now().date().isoformat()
    with _LOCK:
        try:
            value = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        except (OSError, json.JSONDecodeError):
            value = {}
        total = value.setdefault("total", {"calls": 0, "input_tokens": 0, "output_tokens": 0})
        day = value.setdefault("days", {}).setdefault(today, {"calls": 0, "input_tokens": 0, "output_tokens": 0})
        for bucket in (total, day):
            bucket["calls"] += 1; bucket["input_tokens"] += input_tokens; bucket["output_tokens"] += output_tokens
        purposes = value.setdefault("purposes", {})
        purpose_bucket = purposes.setdefault(purpose, {"calls": 0, "input_tokens": 0, "output_tokens": 0})
        purpose_bucket["calls"] += 1; purpose_bucket["input_tokens"] += input_tokens; purpose_bucket["output_tokens"] += output_tokens
        value["last_call"] = {"at": datetime.now().isoformat(timespec="seconds"), "purpose": purpose,
                              "model": model, "input_tokens": input_tokens, "output_tokens": output_tokens}
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
