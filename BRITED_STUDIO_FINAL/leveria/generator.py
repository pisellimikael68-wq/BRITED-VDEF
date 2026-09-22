from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
import threading
import time
from pathlib import Path

from .audit import audit_script
from .performance import score_script
from .prompts import brief
from .review_agents import review_script, save_review
from .store import Store
from .usage import record_api_usage
from .cta import cta_instruction, cta_mode
from .local_llm import LocalAIUnavailable, call_local

try:
    import certifi
    TLS_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    TLS_CONTEXT = ssl.create_default_context()


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
            with urllib.request.urlopen(request, timeout=300, context=TLS_CONTEXT) as response:
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
    policy = json.loads((store.data / "editorial_policy.json").read_text(encoding="utf-8")) if (store.data / "editorial_policy.json").exists() else {}
    automation_path = store.data / "automation.json"
    automation = json.loads(automation_path.read_text(encoding="utf-8")) if automation_path.exists() else {}
    angle = int(publication.get("angle_index", 0)) + 1
    prompt = brief(publication["platform"], concept.titre, concept.id, source, policy) + f"\nANGLE ÉDITORIAL : variante n°{angle}. Traite un angle distinct des variantes précédentes tout en restant strictement dans la fiche source.\n"
    mode = (cta_mode(publication["date"], int(publication["slot"]))
            if policy.get("cta_rotation", {}).get("strategy") == "community_first"
            else publication.get("cta_mode") or cta_mode(publication["date"], int(publication["slot"])))
    prompt += "\nCTA IMPOSÉ PAR LE CALENDRIER : " + cta_instruction(publication["platform"], mode) + "\n"
    prior_review_path = publication.get("review_path", "")
    if prior_review_path:
        prior = store.root / prior_review_path
        if prior.is_file():
            try:
                prior_payload = json.loads(prior.read_text(encoding="utf-8"))
                prior_errors = [str(value) for value in prior_payload.get("errors", [])]
            except (OSError, json.JSONDecodeError):
                prior_errors = []
            if prior_errors:
                prompt += "\nÉCHECS DE LA VERSION PRÉCÉDENTE À CORRIGER IMPÉRATIVEMENT :\n- " + "\n- ".join(prior_errors) + "\n"
    external_ai = automation.get("external_ai", {})
    prefer_external = bool(external_ai.get("prefer_for_strict_certification", False))
    provider = ""
    key = ""
    if prefer_external:
        if not bool(external_ai.get("enabled", False)):
            raise RuntimeError("Certification stricte externe demandée mais moteur externe désactivé")
        if not bool(external_ai.get("manual_approval_granted", False)):
            raise RuntimeError("Certification stricte externe bloquée : autorisation absente")
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("Certification stricte externe autorisée mais clé absente")
        text = _call_openai(prompt, key)
        provider = "openai"
    else:
        try:
            text, local_model = call_local(store.root, prompt)
            provider = f"ollama:{local_model}"
        except LocalAIUnavailable as local_error:
            if not bool(external_ai.get("enabled", False)):
                raise RuntimeError(f"Script absent : mode zéro token actif, mais {local_error}. Aucun appel OpenAI n'a été effectué.") from None
            if not bool(external_ai.get("manual_approval_granted", False)):
                raise RuntimeError("Secours OpenAI bloqué : autorisation ponctuelle absente. Aucun token consommé.") from None
            key = os.environ.get("OPENAI_API_KEY", "").strip()
            if not key:
                raise RuntimeError("Secours OpenAI autorisé mais clé absente. Aucun appel n'a été effectué.") from None
            text = _call_openai(prompt, key)
            provider = "openai"
    if not text or "SOURCE INSUFFISANTE" in text:
        raise RuntimeError("La génération a été bloquée faute de source suffisante")
    folder = store.scripts / concept.domaine
    folder.mkdir(parents=True, exist_ok=True)
    angle = publication.get("angle_index", 0) + 1
    target = next_version(folder, concept.id, publication["platform"], angle)
    threshold = float(policy.get("automation", {}).get("script_score_threshold", 10.0))
    attempts = int(policy.get("automation", {}).get("maximum_rewrites", 3))
    review = None
    for attempt in range(1, attempts + 1):
        target.write_text(text.strip() + "\n", encoding="utf-8")
        preflight = audit_script(text, publication["platform"])
        performance = score_script(text, publication["platform"])
        preflight_errors = list(preflight.errors) + list(preflight.warnings)
        if performance.get("overall") != 10.0:
            preflight_errors.extend(
                f"{criterion} : {score:g}/10"
                for criterion, score in performance.get("criteria", {}).items()
                if float(score) != 10.0
            )
        # Ne pas mobiliser le comité sémantique sur une version qui échoue
        # déjà à une mesure objective. Cela accélère fortement les lots longs
        # et empêche un modèle critique de contredire un dépassement mesuré.
        if preflight_errors and attempt < attempts:
            feedback = "\n".join(dict.fromkeys(preflight_errors))
            correction_prompt = prompt + f"\n\nVERSION REFUSÉE À CORRIGER :\n{text}\n\nÉCARTS OBJECTIFS À CORRIGER :\n{feedback}\n\nRends uniquement le script Markdown complet corrigé. Vise 60–65 secondes avec une lecture naturelle, sans sacrifier les conditions ; utilise le budget de mots comme repère et ne recopie jamais la source brute."
            if provider.startswith("ollama:"):
                text, _ = call_local(store.root, correction_prompt)
            else:
                text = _call_openai(correction_prompt, key)
            continue
        review = review_script(source, text, publication["platform"], threshold=threshold, root=store.root)
        if review.passed:
            break
        if attempt < attempts:
            feedback = "\n".join(review.errors + review.recommendations)
            correction_prompt = prompt + f"\n\nVERSION REFUSÉE À CORRIGER :\n{text}\n\nÉCARTS À CORRIGER SANS AJOUTER DE FAITS :\n{feedback}\n\nCorrige automatiquement tous les écarts en visant 60–65 secondes ; le budget de mots reste un repère à vérifier à voix haute. La narration continue doit être recopiée strictement à l'identique de la concaténation des cellules Narration du tableau, ponctuation comprise. Ne transforme pas une fiche source riche en inventaire exhaustif : le script doit être complet sur un seul angle central, pas sur tous les sous-thèmes connexes. Réduis d'abord les répétitions, amorces et formulations longues. Si une phrase secondaire ouvre une seconde règle impossible à expliquer complètement dans la durée, retire uniquement cette digression et réserve-la à une mini-série. Ne retire jamais la règle centrale, sa condition d'application, l'exception indispensable, les chiffres déterminants, l'exemple utile ni les sources. Si la durée ne peut pas être respectée sans perte de pertinence ou de sécurité juridique et fiscale, refuse la version au lieu de l'appauvrir. Rends le script Markdown complet corrigé."
            if provider.startswith("ollama:"):
                text, _ = call_local(store.root, correction_prompt)
            else:
                text = _call_openai(correction_prompt, key)
    assert review is not None
    relative = str(target.relative_to(store.root))
    review_path = save_review(store.root, publication_id, relative, review)
    if review.passed:
        store.auto_validate_script(relative, publication_id, review_path, review.overall)
        status = "script_certifie_auto"
    else:
        status = "a_corriger"
        store.update_publication(publication_id, script_path=relative, statut=status, review_path=review_path)
    return {"path": relative, "review": review.json(), "review_path": review_path, "status": status, "provider": provider,
            "automatic_validation": review.passed, "human_validation_required": False, "published": False}
