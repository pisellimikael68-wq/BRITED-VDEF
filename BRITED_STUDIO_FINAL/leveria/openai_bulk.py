from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import urllib.request
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .audit import audit_script
from .cta import cta_instruction, cta_mode
from .generator import next_version
from .performance import score_script
from .prompts import brief
from .review_agents import AGENTS, ReviewResult, save_review
from .format_adapter import adapt_beats, beats_from_markdown
from .store import Store
from .usage import record_api_usage

try:
    import certifi
    TLS_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    TLS_CONTEXT = ssl.create_default_context()


TERMINAL = {"completed", "failed", "expired", "cancelled"}


def _load_env(root: Path) -> None:
    path = root / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip().strip('"').strip("'"))


def _request(url: str, key: str, *, body: bytes | None = None, content_type: str = "application/json") -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=body,
        method="POST" if body is not None else "GET",
        headers={"Authorization": f"Bearer {key}", "Content-Type": content_type},
    )
    with urllib.request.urlopen(request, timeout=300, context=TLS_CONTEXT) as response:
        return json.load(response)


def _upload(path: Path, key: str) -> dict[str, Any]:
    boundary = "----brited-" + uuid.uuid4().hex
    raw = path.read_bytes()
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"purpose\"\r\n\r\nbatch\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\n"
        "Content-Type: application/jsonl\r\n\r\n"
    ).encode() + raw + f"\r\n--{boundary}--\r\n".encode()
    return _request("https://api.openai.com/v1/files", key, body=body, content_type=f"multipart/form-data; boundary={boundary}")


def _output_text(data: dict[str, Any]) -> str:
    if data.get("output_text"):
        return str(data["output_text"])
    return "".join(
        str(block.get("text", ""))
        for item in data.get("output", [])
        for block in item.get("content", [])
        if block.get("type") == "output_text"
    )


class BulkScripts:
    """Six-month resumable script generation through OpenAI Batch.

    A batch result is only a draft. Deterministic checks and the independent
    13-agent certification remain mandatory before Store validation.
    """

    def __init__(self, root: Path):
        self.root = root.resolve()
        _load_env(self.root)
        self.store = Store(self.root)
        self.folder = self.root / "data" / "openai_bulk"
        self.folder.mkdir(parents=True, exist_ok=True)
        self.state_path = self.folder / "state.json"

    def load(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return {"status": "idle", "phases": [], "drafts": {}, "blocked": {}}
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def save(self, value: dict[str, Any]) -> None:
        temporary = self.state_path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.state_path)

    def _prompt(self, publication: dict[str, Any]) -> str:
        concept = next(c for c in self.store.concepts() if c.id == publication["concept_id"])
        source = (self.root / concept.source_path).read_text(encoding="utf-8", errors="ignore")
        if not source.strip():
            raise ValueError(f"Source absente : {concept.id}")
        policy_path = self.root / "data" / "editorial_policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        angle = int(publication.get("angle_index", 0)) + 1
        prompt = brief(publication["platform"], concept.titre, concept.id, source, policy)
        prompt += f"\nANGLE ÉDITORIAL : variante n°{angle}. Traite un angle distinct tout en restant strictement dans la fiche source.\n"
        mode = publication.get("cta_mode") or cta_mode(publication["date"], int(publication["slot"]))
        prompt += "\nCTA IMPOSÉ PAR LE CALENDRIER : " + cta_instruction(publication["platform"], mode) + "\n"
        prompt += "\nRends uniquement le script Markdown complet, sans commentaire avant ni après.\n"
        return prompt

    def _source(self, publication: dict[str, Any]) -> str:
        concept = next(c for c in self.store.concepts() if c.id == publication["concept_id"])
        return (self.root / concept.source_path).read_text(encoding="utf-8", errors="ignore")

    def _submit(self, phase: str, rows: list[tuple[str, str]], state: dict[str, Any]) -> dict[str, Any]:
        model = os.environ.get("BRITED_MODEL", "gpt-5-mini")
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        jsonl = self.folder / f"{phase}-{stamp}.jsonl"
        mapping: dict[str, str] = {}
        with jsonl.open("w", encoding="utf-8") as handle:
            for index, (publication_id, prompt) in enumerate(rows, 1):
                custom_id = f"{phase}-{index:04d}"
                mapping[custom_id] = publication_id
                handle.write(json.dumps({
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/responses",
                    "body": {"model": model, "input": prompt, "reasoning": {"effort": "low"},
                             "max_output_tokens": 5000 if phase != "certification" else 3000, "store": False},
                }, ensure_ascii=False) + "\n")
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        uploaded = _upload(jsonl, key)
        batch = _request("https://api.openai.com/v1/batches", key, body=json.dumps({
            "input_file_id": uploaded["id"], "endpoint": "/v1/responses", "completion_window": "24h",
            "metadata": {"project": "BRITED", "phase": phase},
        }).encode())
        state["active"] = {"phase": phase, "batch_id": batch["id"], "input_file_id": uploaded["id"],
                           "jsonl": str(jsonl.relative_to(self.root)), "mapping": mapping}
        state["status"] = f"{phase}_submitted"
        state["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self.save(state)
        return state

    def _poll_active(self, state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
        active = state.get("active", {})
        if not active.get("batch_id"):
            return state, None
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        batch = _request(f"https://api.openai.com/v1/batches/{active['batch_id']}", key)
        active["remote_status"] = batch.get("status")
        active["request_counts"] = batch.get("request_counts", {})
        active["output_file_id"] = batch.get("output_file_id")
        active["error_file_id"] = batch.get("error_file_id")
        state["checked_at"] = datetime.now().isoformat(timespec="seconds")
        self.save(state)
        return state, batch

    def _download_active(self, state: dict[str, Any]) -> list[dict[str, Any]]:
        active = state["active"]
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        request = urllib.request.Request(f"https://api.openai.com/v1/files/{active['output_file_id']}/content",
                                         headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(request, timeout=300, context=TLS_CONTEXT) as response:
            raw = response.read().decode("utf-8")
        output = self.folder / f"{active['phase']}-output-{active['batch_id']}.jsonl"
        output.write_text(raw, encoding="utf-8")
        return [json.loads(line) for line in raw.splitlines() if line.strip()]

    def _write_draft(self, publication_id: str, text: str) -> dict[str, Any]:
        publication = self.store.publication(publication_id)
        concept = next(c for c in self.store.concepts() if c.id == publication["concept_id"])
        text = self._normalize_draft(text, publication)
        folder = self.store.scripts / concept.domaine
        folder.mkdir(parents=True, exist_ok=True)
        target = next_version(folder, concept.id, publication["platform"], int(publication.get("angle_index", 0)) + 1)
        target.write_text(text.strip() + "\n", encoding="utf-8")
        relative = str(target.relative_to(self.root))
        audit = audit_script(text, publication["platform"])
        performance = score_script(text, publication["platform"])
        errors = list(audit.errors) + list(audit.warnings)
        errors.extend(f"{key} : {value:g}/10" for key, value in performance.get("criteria", {}).items() if float(value) != 10.0)
        ready = audit.ok and not audit.warnings and performance.get("overall") == 10.0
        self.store.update_publication(publication_id, script_path=relative, statut="a_certifier" if ready else "a_corriger")
        return {"path": relative, "preflight_ready": ready, "errors": list(dict.fromkeys(errors)), "performance": performance}

    def _normalize_draft(self, text: str, publication: dict[str, Any]) -> str:
        """Apply lossless structural repairs before deterministic auditing.

        This never invents editorial facts: it synchronizes duplicated narration,
        restores the mandatory disclaimer and reuses official URLs already present
        in the concept source.
        """
        value = text.strip()
        table_narration: list[str] = []
        for line in value.splitlines():
            cells = [cell.strip() for cell in line.split("|")]
            if len(cells) >= 6 and cells[1].isdigit():
                table_narration.append(cells[3])
        if table_narration:
            narration = " ".join(part for part in table_narration if part).strip()
            replacement = "## Narration continue\n\n" + narration + "\n"
            if re.search(r"## Narration continue\s*.*?(?=\n## |\Z)", value, re.S | re.I):
                value = re.sub(r"## Narration continue\s*.*?(?=\n## |\Z)", replacement.rstrip(), value,
                               count=1, flags=re.S | re.I)
            else:
                value += "\n\n" + replacement
        disclaimer = ("Contenu pédagogique général. Ne constitue ni un conseil juridique, fiscal ou financier "
                      "personnalisé, ni une recommandation d'investissement.")
        if not re.search(r"information générale|contenu pédagogique|ne constitue pas", value, re.I):
            if re.search(r"## Légende\s*", value, re.I):
                value = re.sub(r"(## Légende\s*)", r"\1\n" + disclaimer + "\n", value, count=1, flags=re.I)
            else:
                value += "\n\n## Légende\n\n" + disclaimer
        source = self._source(publication)
        hosts = ("legifrance.gouv.fr", "bofip.impots.gouv.fr", "service-public.fr", "amf-france.org",
                 "insee.fr", "economie.gouv.fr", "ecb.europa.eu", "banque-france.fr", "impots.gouv.fr",
                 "anil.org", "urssaf.fr", "notaires.fr", "eur-lex.europa.eu")
        all_urls = re.findall(r"https?://[^\s)>]+", source, re.I)
        official_urls = list(dict.fromkeys(url.rstrip(".,;:") for url in all_urls
                                           if any(host in url.casefold() for host in hosts)))
        if source_urls := official_urls:
            if not any(host in value.casefold() for host in hosts):
                addition = "\n".join(f"- {url}" for url in source_urls[:3])
                if re.search(r"## Sources\s*", value, re.I):
                    value = re.sub(r"(## Sources\s*)", r"\1\n" + addition + "\n", value, count=1, flags=re.I)
                else:
                    value += "\n\n## Sources\n\n" + addition
        return value.strip() + "\n"

    def submit_generation(self, start: date, end: date) -> dict[str, Any]:
        state = self.load()
        if state.get("status") not in {"idle", "generation_ingested", "complete", "failed"}:
            return state
        validations = self.store.validations()
        selected = []
        for publication in self.store.calendar().get("publications", []):
            if publication.get("platform") not in {"reels", "shorts"}:
                continue
            if not (start.isoformat() <= publication.get("date", "") <= end.isoformat()):
                continue
            relative = publication.get("script_path", "")
            validation = validations.get(relative, {}) if relative else {}
            if validation.get("validated") and float(validation.get("score", 0)) == 10.0 and float(validation.get("threshold", 0)) == 10.0:
                continue
            selected.append(publication)
        model = os.environ.get("BRITED_MODEL", "gpt-5-mini")
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        jsonl = self.folder / f"generation-{stamp}.jsonl"
        mapping: dict[str, str] = {}
        with jsonl.open("w", encoding="utf-8") as handle:
            for index, publication in enumerate(selected, 1):
                custom_id = f"generation-{index:04d}"
                mapping[custom_id] = publication["id"]
                request = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/responses",
                    "body": {
                        "model": model,
                        "input": self._prompt(publication),
                        "reasoning": {"effort": "low"},
                        "max_output_tokens": 5000,
                        "store": False,
                    },
                }
                handle.write(json.dumps(request, ensure_ascii=False) + "\n")
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("Clé OpenAI absente")
        uploaded = _upload(jsonl, key)
        batch = _request(
            "https://api.openai.com/v1/batches",
            key,
            body=json.dumps({
                "input_file_id": uploaded["id"],
                "endpoint": "/v1/responses",
                "completion_window": "24h",
                "metadata": {"project": "BRITED", "phase": "generation-six-months"},
            }).encode(),
        )
        state.update({
            "status": "generation_submitted",
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "range": {"start": start.isoformat(), "end": end.isoformat()},
            "model": model,
            "generation": {"batch_id": batch["id"], "input_file_id": uploaded["id"], "jsonl": str(jsonl.relative_to(self.root)), "mapping": mapping},
            "summary": {"requested": len(selected), "drafted": 0, "preflight_ready": 0, "blocked": 0, "certified": 0},
        })
        self.save(state)
        return state

    def status(self) -> dict[str, Any]:
        state = self.load()
        if state.get("active", {}).get("batch_id"):
            return self._poll_active(state)[0]
        phase = state.get("generation", {})
        batch_id = phase.get("batch_id")
        if not batch_id:
            return state
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        batch = _request(f"https://api.openai.com/v1/batches/{batch_id}", key)
        state["generation"]["remote_status"] = batch.get("status")
        state["generation"]["request_counts"] = batch.get("request_counts", {})
        state["generation"]["output_file_id"] = batch.get("output_file_id")
        state["generation"]["error_file_id"] = batch.get("error_file_id")
        state["checked_at"] = datetime.now().isoformat(timespec="seconds")
        if batch.get("status") in TERMINAL:
            state["status"] = "generation_ready" if batch.get("status") == "completed" else "failed"
        self.save(state)
        return state

    def ingest_generation(self) -> dict[str, Any]:
        state = self.status()
        if state.get("status") != "generation_ready":
            return state
        output_file_id = state["generation"].get("output_file_id")
        if not output_file_id:
            raise RuntimeError("Fichier de sortie Batch absent")
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        request = urllib.request.Request(
            f"https://api.openai.com/v1/files/{output_file_id}/content",
            headers={"Authorization": f"Bearer {key}"},
        )
        with urllib.request.urlopen(request, timeout=300, context=TLS_CONTEXT) as response:
            raw = response.read().decode("utf-8")
        output_path = self.folder / "generation-output.jsonl"
        output_path.write_text(raw, encoding="utf-8")
        mapping = state["generation"]["mapping"]
        drafts = state.setdefault("drafts", {})
        blocked = state.setdefault("blocked", {})
        for line in raw.splitlines():
            item = json.loads(line)
            publication_id = mapping.get(item.get("custom_id", ""))
            if not publication_id:
                continue
            if item.get("error") or int(item.get("response", {}).get("status_code", 500)) >= 400:
                blocked[publication_id] = str(item.get("error") or item.get("response", {}).get("body", {}).get("error", "Erreur Batch"))
                continue
            body = item["response"]["body"]
            record_api_usage(body, "batch_generation", state.get("model", "gpt-5-mini"))
            text = _output_text(body).strip()
            drafts[publication_id] = self._write_draft(publication_id, text)
        summary = state["summary"]
        summary["drafted"] = len(drafts)
        summary["preflight_ready"] = sum(bool(value.get("preflight_ready")) for value in drafts.values())
        summary["blocked"] = len(blocked) + sum(not bool(value.get("preflight_ready")) for value in drafts.values())
        state["status"] = "generation_ingested"
        state["generation"]["output"] = str(output_path.relative_to(self.root))
        state["ingested_at"] = datetime.now().isoformat(timespec="seconds")
        self.save(state)
        return state

    def submit_corrections(self) -> dict[str, Any]:
        state = self.load()
        round_number = int(state.get("correction_round", 0)) + 1
        policy = json.loads((self.root / "data" / "editorial_policy.json").read_text(encoding="utf-8"))
        max_rounds = int(policy.get("automation", {}).get("maximum_remediation_cycles", 10))
        if round_number > max_rounds:
            state["status"] = "blocked"
            self.save(state)
            return state
        rows: list[tuple[str, str]] = []
        for publication_id, draft in state.get("drafts", {}).items():
            if draft.get("certified") or draft.get("preflight_ready"):
                continue
            publication = self.store.publication(publication_id)
            text = (self.root / draft["path"]).read_text(encoding="utf-8")
            feedback = "\n- ".join(draft.get("errors", []) or ["Certification sémantique inférieure à 10/10"])
            prompt = self._prompt(publication) + (
                "\n\nVERSION REFUSÉE :\n" + text +
                "\n\nÉCARTS BLOQUANTS À CORRIGER :\n- " + feedback +
                "\n\nCorrige tous les écarts sans ajouter de faits ni supprimer une condition, une exception, un chiffre, "
                "un exemple nécessaire ou une source. La narration continue doit être strictement identique à la "
                "concaténation des cellules Narration. Reprends au moins une URL officielle fournie dans la fiche "
                "source. Respecte strictement le budget de mots de la plateforme. Évite toute formulation absolue "
                "(toujours, jamais, forcément, automatiquement) sauf si la source officielle l'établit sans exception. "
                "Chaque phrase doit être naturelle, complète et immédiatement compréhensible à l'oral. Supprime toute "
                "mention interne ou marque de production. Rends uniquement le script Markdown complet corrigé."
            )
            rows.append((publication_id, prompt))
        if not rows:
            return self.submit_certification()
        state["correction_round"] = round_number
        return self._submit("correction", rows, state)

    def ingest_corrections(self) -> dict[str, Any]:
        state = self.load()
        state, batch = self._poll_active(state)
        if not batch or batch.get("status") != "completed":
            return state
        mapping = state["active"]["mapping"]
        for item in self._download_active(state):
            publication_id = mapping.get(item.get("custom_id", ""))
            if not publication_id:
                continue
            if item.get("error") or int(item.get("response", {}).get("status_code", 500)) >= 400:
                state["drafts"][publication_id]["errors"] = [str(item.get("error") or "Erreur Batch correction")]
                continue
            body = item["response"]["body"]
            record_api_usage(body, "batch_correction", state.get("model", "gpt-5-mini"))
            state["drafts"][publication_id] = self._write_draft(publication_id, _output_text(body).strip())
        state.pop("active", None)
        state["status"] = "correction_ingested"
        self._refresh_summary(state)
        self.save(state)
        return state

    def _review_prompt(self, publication_id: str, script: str) -> str:
        publication = self.store.publication(publication_id)
        source = self._source(publication)
        return f"""Tu es le comité de certification BRITED indépendant.
Plateforme : {publication['platform']}
SOURCE DE VÉRITÉ :
{source}

SCRIPT :
{script}

AGENTS :
{json.dumps(AGENTS, ensure_ascii=False, indent=2)}

Retourne uniquement un JSON de forme {{"agents": {{identifiant: {{"score": nombre, "passed": booléen, "findings": [texte]}}}}, "recommendations": [texte]}}.
Règles absolues : chaque agent doit juger indépendamment. 10/10 signifie publiable sans aucune amélioration précise identifiable. 9,9 ou moins bloque. Une note inférieure à 10 exige un finding concret et localisable. Aucune moyenne ne compense une faiblesse. Vérifie mot à mot faits, chiffres, articles, conditions, exceptions, exemple, sources, cohérence question-réponse, français naturel, pédagogie d'un non-spécialiste, rétention, confiance professionnelle, densité et correspondance des pictogrammes. Findings ne contient jamais une qualité. Pour certifier : chaque score exactement 10, passed true, findings vide et recommendations vide."""

    def submit_certification(self) -> dict[str, Any]:
        state = self.load()
        rows = []
        for publication_id, draft in state.get("drafts", {}).items():
            if draft.get("preflight_ready") and not draft.get("certified"):
                rows.append((publication_id, self._review_prompt(publication_id, (self.root / draft["path"]).read_text(encoding="utf-8"))))
        if not rows:
            state["status"] = "complete" if all(x.get("certified") for x in state.get("drafts", {}).values()) else "blocked"
            self._refresh_summary(state); self.save(state); return state
        return self._submit("certification", rows, state)

    def ingest_certification(self) -> dict[str, Any]:
        state = self.load()
        state, batch = self._poll_active(state)
        if not batch or batch.get("status") != "completed":
            return state
        mapping = state["active"]["mapping"]
        for item in self._download_active(state):
            publication_id = mapping.get(item.get("custom_id", ""))
            if not publication_id:
                continue
            draft = state["drafts"][publication_id]
            publication = self.store.publication(publication_id)
            script = (self.root / draft["path"]).read_text(encoding="utf-8")
            audit = audit_script(script, publication["platform"])
            performance = score_script(script, publication["platform"])
            errors = list(audit.errors) + list(audit.warnings)
            recommendations: list[str] = []
            agents: dict[str, dict[str, Any]] = {}
            body = item.get("response", {}).get("body", {})
            if item.get("error") or int(item.get("response", {}).get("status_code", 500)) >= 400:
                errors.append(str(item.get("error") or "Erreur Batch certification"))
            else:
                record_api_usage(body, "batch_certification", state.get("model", "gpt-5-mini"))
                try:
                    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", _output_text(body).strip(), flags=re.I | re.S)
                    payload = json.loads(raw)
                    payload_agents = payload.get("agents", {})
                    for agent_id, label in AGENTS.items():
                        value = payload_agents.get(agent_id, {})
                        score = max(0.0, min(10.0, float(value.get("score", 0))))
                        findings = [str(x) for x in value.get("findings", [])]
                        passed = bool(value.get("passed")) and score == 10.0 and not findings
                        agents[agent_id] = {"label": label, "score": score, "passed": passed, "findings": findings}
                        if not passed:
                            errors.extend(f"{agent_id} : {finding}" for finding in findings or [f"note {score:g}/10"])
                    recommendations = [str(x) for x in payload.get("recommendations", [])]
                except (ValueError, TypeError, json.JSONDecodeError) as exc:
                    errors.append(f"Rapport de certification inexploitable : {type(exc).__name__}")
            scores = [value["score"] for value in agents.values()]
            overall = round(sum(scores) / len(scores), 2) if scores else 0.0
            passed = bool(audit.ok and not audit.warnings and performance.get("overall") == 10.0 and
                          len(agents) == len(AGENTS) and all(x["passed"] for x in agents.values()) and not recommendations)
            result = ReviewResult(passed, 10.0, overall, agents,
                                  {"audit": audit.json(), "performance": performance},
                                  tuple(dict.fromkeys(errors)), tuple(dict.fromkeys(recommendations)),
                                  datetime.now().isoformat(timespec="seconds"), state.get("model", "gpt-5-mini") + ":batch")
            review_path = save_review(self.root, publication_id, draft["path"], result)
            if passed:
                self.store.auto_validate_script(draft["path"], publication_id, review_path, 10.0)
                draft.update(certified=True, review_path=review_path, errors=[])
            else:
                draft.update(certified=False, preflight_ready=False, review_path=review_path,
                             errors=list(dict.fromkeys(errors + recommendations)))
                self.store.update_publication(publication_id, statut="a_corriger", review_path=review_path)
        state.pop("active", None)
        state["status"] = "certification_ingested"
        self._refresh_summary(state); self.save(state)
        return state

    def _refresh_summary(self, state: dict[str, Any]) -> None:
        drafts = state.get("drafts", {})
        state["summary"].update({
            "drafted": len(drafts),
            "preflight_ready": sum(bool(x.get("preflight_ready")) for x in drafts.values()),
            "blocked": len(state.get("blocked", {})) + sum(not x.get("preflight_ready") and not x.get("certified") for x in drafts.values()),
            "certified": sum(bool(x.get("certified")) for x in drafts.values()),
        })

    def advance(self) -> dict[str, Any]:
        state = self.load()
        policy = json.loads((self.root / "data" / "editorial_policy.json").read_text(encoding="utf-8"))
        max_rounds = int(policy.get("automation", {}).get("maximum_remediation_cycles", 10))
        status = state.get("status", "idle")
        if status in {"generation_submitted", "generation_ready"}:
            state = self.ingest_generation()
            if state.get("status") == "generation_ingested":
                return self.submit_corrections()
            return state
        if status == "correction_submitted":
            state = self.ingest_corrections()
            if state.get("status") == "correction_ingested":
                if any(not x.get("preflight_ready") for x in state.get("drafts", {}).values()) and int(state.get("correction_round", 0)) < max_rounds:
                    return self.submit_corrections()
                return self.submit_certification()
            return state
        if status == "certification_submitted":
            state = self.ingest_certification()
            if state.get("status") == "certification_ingested":
                if all(x.get("certified") for x in state.get("drafts", {}).values()):
                    state["status"] = "complete"; self._refresh_summary(state); self.save(state); return state
                if int(state.get("correction_round", 0)) < max_rounds:
                    return self.submit_corrections()
                state["status"] = "blocked"; self.save(state)
            return state
        if status == "blocked" and int(state.get("correction_round", 0)) < max_rounds:
            return self.submit_corrections()
        if status in {"generation_ingested", "correction_ingested"}:
            return self.submit_corrections()
        if status == "certification_ingested":
            return self.submit_certification()
        return state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("submit-generation", "status", "ingest-generation", "advance"))
    parser.add_argument("--root", required=True)
    parser.add_argument("--start", default=date.today().isoformat())
    parser.add_argument("--end", default="2027-02-19")
    args = parser.parse_args()
    bulk = BulkScripts(Path(args.root))
    if args.command == "submit-generation":
        value = bulk.submit_generation(date.fromisoformat(args.start), date.fromisoformat(args.end))
    elif args.command == "ingest-generation":
        value = bulk.ingest_generation()
    elif args.command == "advance":
        value = bulk.advance()
    else:
        value = bulk.status()
    print(json.dumps({"status": value.get("status"), "summary": value.get("summary"), "generation": {k: v for k, v in value.get("generation", {}).items() if k != "mapping"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
