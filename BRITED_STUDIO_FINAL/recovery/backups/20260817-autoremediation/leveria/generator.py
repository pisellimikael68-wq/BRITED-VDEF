from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import threading
import time
from pathlib import Path

from .audit import audit_script
from .prompts import brief
from .review_agents import review_script, save_review
from .store import Store
from .usage import record_api_usage


_LOCKS: dict[str, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()


def next_version(folder: Path, concept_id: str, platform: str, angle: int) -> Path:
    base = f"{concept_id}__{platform}__a{angle}"
    direct = folder / f"{base}.md"
    if not direct.exists():
        return direct
    version = 2
    while (folder / f"{base}__v{version}.md").exists():
        version += 1
    return folder / f"{base}__v{version}.md"


def _call_openai(prompt: str, key: str) -> str:
    model = os.environ.get("BRITED_MODEL", "gpt-5-mini")
    request_body = {"model": model, "input": prompt,
                    "reasoning": {"effort": "low"}, "max_output_tokens": 5000}
    request = urllib.request.Request("https://api.openai.com/v1/responses",
        data=json.dumps(request_body).encode(), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                data = json.load(response)
            record_api_usage(data, "generation", model)
            break
        except urllib.error.HTTPError as error:
            if 400 <= error.code < 500 and error.code != 429:
                raise RuntimeError(f"API OpenAI : erreur {error.code}") from None
            last_error = error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = error
        if attempt < 2:
            time.sleep((attempt + 1) * 2)
    else:
        raise RuntimeError(f"API OpenAI temporairement indisponible après 3 tentatives : {type(last_error).__name__}")
    return data.get("output_text") or "".join(
        block.get("text", "") for item in data.get("output", []) for block in item.get("content", [])
        if block.get("type") == "output_text"
    )


def generate(store: Store, publication_id: str) -> dict:
    with _LOCKS_GUARD:
        lock = _LOCKS.setdefault(publication_id, threading.Lock())
    if not lock.acquire(blocking=False):
        raise RuntimeError("Cette publication est déjà en cours de génération")
    try:
        return _generate(store, publication_id)
    finally:
        lock.release()


def _generate(store: Store, publication_id: str) -> dict:
    publication = store.publication(publication_id)
    concept = next(c for c in store.concepts() if c.id == publication["concept_id"])
    source = ""
    if concept.source_path:
        source = (store.root / concept.source_path).read_text(encoding="utf-8", errors="ignore")
    if not source.strip():
        raise RuntimeError("Source conceptuelle absente : génération bloquée pour éviter une erreur factuelle")
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Clé OpenAI absente. Ajoutez-la uniquement dans le fichier .env local.")
    policy = json.loads((store.data / "editorial_policy.json").read_text(encoding="utf-8")) if (store.data / "editorial_policy.json").exists() else {}
    angle = int(publication.get("angle_index", 0)) + 1
    prompt = brief(publication["platform"], concept.titre, concept.id, source, policy) + f"\nANGLE ÉDITORIAL : variante n°{angle}. Traite un angle distinct des variantes précédentes tout en restant strictement dans la fiche source.\n"
    text = _call_openai(prompt, key)
    if not text or "SOURCE INSUFFISANTE" in text:
        raise RuntimeError("La génération a été bloquée faute de source suffisante")
    folder = store.scripts / concept.domaine
    folder.mkdir(parents=True, exist_ok=True)
    angle = publication.get("angle_index", 0) + 1
    target = next_version(folder, concept.id, publication["platform"], angle)
    threshold = float(policy.get("automation", {}).get("script_score_threshold", 9.5))
    attempts = int(policy.get("automation", {}).get("maximum_rewrites", 3))
    review = None
    for attempt in range(1, attempts + 1):
        target.write_text(text.strip() + "\n", encoding="utf-8")
        review = review_script(source, text, publication["platform"], threshold=threshold)
        if review.passed:
            break
        if attempt < attempts:
            feedback = "\n".join(review.errors + review.recommendations)
            text = _call_openai(prompt + f"\n\nVERSION REFUSÉE À CORRIGER :\n{text}\n\nÉCARTS À CORRIGER SANS AJOUTER DE FAITS :\n{feedback}\n\nCorrige tous les écarts dans le budget de mots. Ne transforme pas une fiche source riche en inventaire exhaustif : le script doit être complet sur son angle central, pas sur tous les sous-thèmes connexes. Si une phrase secondaire ouvre un mécanisme distinct impossible à expliquer complètement dans la durée, supprime cette digression. Préserve la règle centrale, sa condition, l'exception indispensable pour ne pas induire en erreur et l'exemple. Rends le script Markdown complet corrigé.", key)
    assert review is not None
    relative = str(target.relative_to(store.root))
    review_path = save_review(store.root, publication_id, relative, review)
    if review.passed:
        store.auto_validate_script(relative, publication_id, review_path, review.overall)
        status = "script_certifie_auto"
    else:
        status = "a_corriger"
        store.update_publication(publication_id, script_path=relative, statut=status, review_path=review_path)
    return {"path": relative, "review": review.json(), "review_path": review_path, "status": status,
            "automatic_validation": review.passed, "human_validation_required": False, "published": False}
