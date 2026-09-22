from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


PLATFORMS = ("tiktok", "reels", "shorts")
PLATFORM_LABELS = {"tiktok": "TikTok", "reels": "Instagram", "shorts": "YouTube Shorts"}
SERIES = {
    "fiscalite": {"label": "Fiscalité", "color": "#6F4E37", "icon": "％"},
    "immobilier": {"label": "Immobilier", "color": "#C96F4A", "icon": "⌂"},
    "juridique": {"label": "Juridique", "color": "#D99A2B", "icon": "§"},
    "finance": {"label": "Finance", "color": "#2457D6", "icon": "↗"},
}


DOMAIN_SERIES = {
    "regimes_matrimoniaux": "juridique", "donation": "juridique",
    "societes_civiles": "juridique", "gouvernance_familiale": "juridique",
    "immobilier": "immobilier", "location_meublee": "immobilier", "sci": "immobilier",
    "scpi": "immobilier", "opci": "immobilier",
    "fiscalite": "fiscalite", "fiscalite_internationale": "fiscalite",
    "impot_revenu": "fiscalite", "ifi": "fiscalite",
    "assurance_vie": "finance", "pea": "finance", "per": "finance",
    "etf": "finance", "obligations": "finance", "compte_titres": "finance",
    "produits_structures": "finance", "culture_financiere": "finance",
}


def classify_series(domaine: str, concept_id: str, fallback: str = "finance") -> str:
    value = f"{domaine} {concept_id}".casefold()
    if any(word in value for word in ("immobilier", "location", "sci", "scpi", "opci", "foncier", "pinel", "malraux", "lmnp", "lmp")):
        return "immobilier"
    if any(word in value for word in ("regimes_matrimoniaux", "donation", "succession", "demembrement", "pacs", "concubin", "reserve_hereditaire", "gouvernance_familiale")):
        return "juridique"
    if any(word in value for word in ("fiscalite", "impot", "ifi", "pfu", "abattement", "declaration", "plus_value", "990i", "152500", "2086")):
        return "fiscalite"
    return fallback if fallback in SERIES else "finance"


@dataclass(frozen=True)
class Concept:
    id: str
    domaine: str
    titre: str
    serie: str
    source_path: str = ""
    recovered: bool = True


def humanize(value: str) -> str:
    return value.replace("_", " ").strip().capitalize()


class Store:
    def __init__(self, root: Path):
        self.root = root.resolve()
        root = self.root
        self.data = root / "data"
        self.content = root / "content"
        self.scripts = root / "scripts"
        self.production = root / "production"
        for folder in (self.data, self.content, self.scripts, self.production):
            folder.mkdir(parents=True, exist_ok=True)

    @property
    def calendar_path(self) -> Path:
        return self.data / "calendrier.json"

    @property
    def validations_path(self) -> Path:
        return self.data / "validations.json"

    def validations(self) -> dict[str, dict[str, Any]]:
        if not self.validations_path.exists():
            return {}
        return json.loads(self.validations_path.read_text(encoding="utf-8"))

    def reconcile_certifications(self) -> dict[str, int]:
        """Invalidate obsolete certifications while preserving their complete history."""
        from .audit import audit_script
        values = self.validations()
        calendar = self.calendar()
        publications = calendar.get("publications", [])
        current_by_path = {item.get("script_path", ""): item for item in publications if item.get("script_path")}
        checked = invalidated = 0
        changed = False
        for relative, record in values.items():
            if not record.get("validated"):
                continue
            target = self.root / relative
            publication = current_by_path.get(relative)
            platform = publication.get("platform") if publication else ("reels" if "__instagram__" in relative else "shorts" if "__youtube__" in relative else "tiktok")
            checked += 1
            errors = ["Fichier certifié introuvable"] if not target.is_file() else list(audit_script(target.read_text(encoding="utf-8"), platform).errors)
            if errors:
                record.update(validated=False, previous_validation=True, stale=True,
                              invalidated_at=datetime.now().isoformat(timespec="seconds"),
                              invalidation_reason=errors)
                if publication:
                    publication["statut"] = "a_corriger"
                invalidated += 1; changed = True
        if changed:
            self.validations_path.write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            self.calendar_path.write_text(json.dumps(calendar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"checked": checked, "invalidated": invalidated,
                "current_certified": sum(bool(item.get("script_path") and values.get(item.get("script_path"), {}).get("validated")) for item in publications)}

    def certification_health(self, publications: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        from .audit import audit_script
        publications = publications if publications is not None else self.calendar().get("publications", [])
        values = self.validations(); by_platform: dict[str, dict[str, int]] = {}
        authored = validated = certified = inconsistent = 0
        for publication in publications:
            platform = publication.get("platform", "unknown")
            counters = by_platform.setdefault(platform, {"scheduled": 0, "authored": 0, "certified": 0})
            counters["scheduled"] += 1
            relative = publication.get("script_path", ""); target = self.root / relative if relative else None
            if not relative or not target or not target.is_file():
                continue
            authored += 1; counters["authored"] += 1
            is_validated = bool(values.get(relative, {}).get("validated")); validated += int(is_validated)
            audit_ok = audit_script(target.read_text(encoding="utf-8"), platform).ok
            if is_validated and audit_ok:
                certified += 1; counters["certified"] += 1
            elif is_validated and not audit_ok:
                inconsistent += 1
        return {"authored": authored, "validated": validated, "certified": certified,
                "inconsistent": inconsistent, "by_platform": by_platform}

    def validate_script(self, path: str, publication_id: str) -> dict[str, Any]:
        target = (self.root / path).resolve()
        if self.root not in target.parents or not target.is_file():
            raise ValueError("Script introuvable")
        publication = self.publication(publication_id)
        from .audit import audit_script
        audit = audit_script(target.read_text(encoding="utf-8"), publication["platform"])
        if not audit.ok:
            raise ValueError("Validation refusée : le script ne passe pas les contrôles")
        values = self.validations()
        values[path] = {"publication_id": publication_id, "validated": True,
                        "validated_at": date.today().isoformat(), "audit": audit.json()}
        self.validations_path.write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.update_publication(publication_id, statut="script_valide", script_path=path)
        return values[path]

    def auto_validate_script(self, path: str, publication_id: str, review_path: str, score: float) -> dict[str, Any]:
        if score < 9.5:
            raise ValueError("Certification automatique refusée sous 9,5/10")
        target = (self.root / path).resolve()
        review = (self.root / review_path).resolve()
        if self.root not in target.parents or not target.is_file() or self.root not in review.parents or not review.is_file():
            raise ValueError("Script ou rapport de contrôle introuvable")
        report = json.loads(review.read_text(encoding="utf-8"))
        if not report.get("passed") or not report.get("agents") or not all(item.get("passed") for item in report["agents"].values()):
            raise ValueError("Le comité automatique n'a pas unanimement validé le script")
        values = self.validations()
        values[path] = {"publication_id": publication_id, "validated": True, "mode": "automatic_committee",
                        "score": score, "threshold": 9.5, "review_path": review_path,
                        "validated_at": datetime.now().isoformat(timespec="seconds")}
        self.validations_path.write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.update_publication(publication_id, statut="script_certifie_auto", script_path=path, review_path=review_path)
        return values[path]

    def concepts(self) -> list[Concept]:
        catalog_path = self.data / "concepts_recuperes.json"
        if catalog_path.exists():
            raw = json.loads(catalog_path.read_text(encoding="utf-8"))
            result = []
            for item in raw:
                value = {key: item.get(key) for key in ("id", "domaine", "titre", "serie", "source_path", "recovered")}
                value["serie"] = classify_series(value.get("domaine") or "", value.get("id") or "", value.get("serie") or "finance")
                path = self.root / (value.get("source_path") or "")
                valid = False
                if path.is_file():
                    match = re.search(r"(?m)^id:\s*([^\s]+)", path.read_text(encoding="utf-8", errors="ignore"))
                    valid = bool(match and match.group(1) == value["id"])
                if not valid:
                    value["source_path"] = ""
                    value["recovered"] = False
                result.append(Concept(**value))
            return result
        concepts: list[Concept] = []
        for path in sorted(self.content.glob("*/*.md")):
            domaine, concept_id = path.parent.name, path.stem
            text = path.read_text(encoding="utf-8", errors="ignore")
            title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            concepts.append(Concept(
                concept_id, domaine,
                title_match.group(1).strip() if title_match else humanize(concept_id),
                DOMAIN_SERIES.get(domaine, "finance"), str(path.relative_to(self.root)), True,
            ))
        return concepts

    def calendar(self) -> dict[str, Any]:
        if not self.calendar_path.exists():
            return {"publications": [], "warnings": ["Calendrier à reconstruire"]}
        value = json.loads(self.calendar_path.read_text(encoding="utf-8"))
        validations = self.validations()
        for publication in value.get("publications", []):
            path = publication.get("script_path", "")
            if publication.get("statut") == "script_valide" and not validations.get(path, {}).get("validated"):
                publication["statut"] = "en_attente_validation" if path else "a_ecrire"
        return value

    def save_calendar(self, value: dict[str, Any]) -> None:
        self._write_json_atomic(self.calendar_path, value)

    def _write_json_atomic(self, path: Path, value: object) -> None:
        """Write important state without ever exposing a half-written JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)

    def backup(self, label: str = "manual") -> dict[str, Any]:
        """Create a local, recoverable snapshot of the editorial state."""
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = self.root / "recovery" / "backups" / f"{stamp}-{re.sub(r'[^a-z0-9_-]+', '-', label.casefold())}"
        target.mkdir(parents=True, exist_ok=False)
        copied: list[str] = []
        for relative in ("data", "scripts", "content", "production"):
            source = self.root / relative
            if source.exists():
                shutil.copytree(source, target / relative)
                copied.append(relative)
        manifest = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "label": label,
            "folders": copied,
            "source": str(self.root),
        }
        self._write_json_atomic(target / "backup.json", manifest)
        return {**manifest, "path": str(target.relative_to(self.root))}

    def build_calendar(self, start: date, days: int = 180) -> dict[str, Any]:
        if self.calendar_path.exists():
            archive = self.root / "recovery" / "calendar_versions"
            archive.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            shutil.copy2(self.calendar_path, archive / f"calendrier-{stamp}.json")
        concepts = self.concepts()
        certified = [item for item in concepts if item.recovered and item.source_path and (self.root / item.source_path).is_file()]
        if not certified:
            raise ValueError("Aucun concept certifié et exploitable")
        publications: list[dict[str, Any]] = []
        recovered_path = self.data / "calendrier_recupere.json"
        recovered = json.loads(recovered_path.read_text(encoding="utf-8")).get("publications", []) if recovered_path.exists() else []
        recovered_order: dict[str, list[str]] = {}
        recovered_titles: dict[str, str] = {}
        for item in recovered:
            day_key, concept_id = item.get("date", ""), item.get("concept_id", "")
            recovered_titles[concept_id] = item.get("titre", humanize(concept_id))
            if concept_id and concept_id not in recovered_order.setdefault(day_key, []):
                recovered_order[day_key].append(concept_id)
        by_id = {concept.id: concept for concept in certified}
        angle_counts: dict[str, int] = {}
        for offset in range(days):
            day = start + timedelta(days=offset)
            for slot in (1, 2):
                recovered_ids = recovered_order.get(day.isoformat(), [])
                recovered_id = recovered_ids[slot - 1] if len(recovered_ids) >= slot else ""
                concept = by_id.get(recovered_id) or certified[(offset * 2 + slot - 1) % len(certified)]
                angle_counts[concept.id] = angle_counts.get(concept.id, 0) + 1
                angle_index = angle_counts[concept.id] - 1
                for platform in PLATFORMS:
                    aliases = (platform, "instagram") if platform == "reels" else (platform, "youtube") if platform == "shorts" else (platform,)
                    existing_script = ""
                    for alias in aliases:
                        candidates = sorted(self.scripts.rglob(f"{concept.id}__{alias}__a{angle_index + 1}.md"))
                        if candidates:
                            existing_script = str(candidates[0].relative_to(self.root)); break
                    is_validated = bool(existing_script and self.validations().get(existing_script, {}).get("validated"))
                    publications.append({
                        "id": f"{day.isoformat()}:{platform}:{concept.id}:{slot-1}",
                        "date": day.isoformat(), "slot": slot,
                        "heure": "10:00" if slot == 1 else "17:00",
                        "platform": platform, "concept_id": concept.id,
                        "titre": concept.titre, "serie": concept.serie,
                        "statut": "script_valide" if is_validated else "en_attente_validation" if existing_script else "a_ecrire", "script_path": existing_script, "note": "",
                        "angle_index": angle_index,
                    })
        value = {"publications": publications, "warnings": [], "generated_at": date.today().isoformat()}
        self.save_calendar(value)
        return value

    def scripts_index(self) -> list[dict[str, Any]]:
        result = []
        validations = self.validations()
        for path in sorted(self.scripts.rglob("*.md")):
            if "__" not in path.stem or path.name.startswith("CHARTE_"):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            relative = str(path.relative_to(self.root))
            result.append({"path": relative, "name": path.name,
                           "validated": bool(validations.get(relative, {}).get("validated")),
                           "words": len(re.findall(r"\b[\wÀ-ÿ'-]+\b", text))})
        return result

    def publication(self, publication_id: str) -> dict[str, Any]:
        for item in self.calendar().get("publications", []):
            if item.get("id") == publication_id:
                return item
        raise KeyError(publication_id)

    def update_publication(self, publication_id: str, **changes: Any) -> dict[str, Any]:
        calendar = self.calendar()
        for item in calendar.get("publications", []):
            if item.get("id") == publication_id:
                item.update(changes)
                self.save_calendar(calendar)
                return item
        raise KeyError(publication_id)

    def script_versions(self, publication_id: str) -> list[dict[str, Any]]:
        publication = self.publication(publication_id)
        aliases = (publication["platform"], "instagram") if publication["platform"] == "reels" else (publication["platform"], "youtube") if publication["platform"] == "shorts" else (publication["platform"],)
        validations = self.validations()
        paths = [path for alias in aliases for path in self.scripts.rglob(f"{publication['concept_id']}__{alias}__a{publication.get('angle_index', 0)+1}*.md")]
        return [{"path": str(path.relative_to(self.root)), "name": path.name,
                 "validated": bool(validations.get(str(path.relative_to(self.root)), {}).get("validated")),
                 "modified": path.stat().st_mtime}
                for path in sorted(set(paths), key=lambda item: item.stat().st_mtime, reverse=True)]

    def manifest(self, relative: str) -> dict[str, Any]:
        target = (self.root / relative).resolve()
        if self.root not in target.parents or not target.is_file() or target.name != "manifest.json":
            raise ValueError("Manifeste introuvable")
        value = json.loads(target.read_text(encoding="utf-8")); value["path"] = str(target.relative_to(self.root))
        for item in value.get("items", []):
            for key in ("video", "script"):
                raw = item.get(key, "")
                if raw:
                    path = Path(raw)
                    item[key] = str(path.relative_to(self.root)) if path.is_absolute() and self.root in path.parents else raw
        return value

    def approve_video(self, manifest_path: str, publication_id: str) -> dict[str, Any]:
        target = (self.root / manifest_path).resolve()
        value = self.manifest(manifest_path)
        item = next((x for x in value.get("items", []) if x.get("publication_id") == publication_id), None)
        if not item or item.get("status") not in ("awaiting_approval", "approved"):
            raise ValueError("Vidéo non disponible pour validation")
        item["status"] = "approved"; item["human_approved"] = True
        value.pop("path", None); value["publish_locked"] = True
        value["status"] = "approved" if all(x.get("status") == "approved" for x in value.get("items", [])) else "awaiting_approval"
        target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.update_publication(publication_id, statut="video_validee")
        return self.manifest(manifest_path)

    def heritage(self) -> dict[str, Any]:
        path = self.data / "history.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"summary": {}, "conversation_messages": [], "subject_bank": [], "artifacts": []}

    def search_heritage(self, query: str = "", kind: str = "conversation", offset: int = 0, limit: int = 50) -> dict[str, Any]:
        data = self.heritage(); key = {"conversation":"conversation_messages", "subjects":"subject_bank", "artifacts":"artifacts"}.get(kind, "conversation_messages")
        rows = data.get(key, []); needle = query.casefold().strip()
        if needle: rows = [row for row in rows if needle in json.dumps(row, ensure_ascii=False).casefold()]
        total = len(rows); return {"kind":kind,"query":query,"total":total,"offset":offset,"limit":limit,"items":rows[offset:offset+limit]}

    def production_day(self, day: str) -> dict[str, Any]:
        publications = [item.copy() for item in self.calendar().get("publications", []) if item.get("date") == day]
        validations = self.validations()
        for item in publications:
            relative = item.get("script_path", "")
            target = self.root / relative if relative else None
            item["script_text"] = target.read_text(encoding="utf-8") if target and target.is_file() else ""
            item["validation"] = validations.get(relative, {})
            review_path = item.get("review_path") or item["validation"].get("review_path", "")
            review_target = self.root / review_path if review_path else None
            item["review"] = json.loads(review_target.read_text(encoding="utf-8")) if review_target and review_target.is_file() else {}
        publications.sort(key=lambda item: (int(item.get("slot", 0)), PLATFORMS.index(item["platform"])))
        return {"date": day, "publications": publications,
                "summary": {"total": len(publications), "scripts": sum(bool(item["script_text"]) for item in publications),
                            "certified": sum(bool(item["validation"].get("validated")) for item in publications),
                            "videos": sum(item.get("statut") in ("video_prete", "video_validee") for item in publications)}}

    def read_script(self, publication_id: str, path: str = "") -> dict[str, Any]:
        publication = self.publication(publication_id)
        relative = path or publication.get("script_path", "")
        if not relative:
            return {"publication": publication, "path": "", "text": "", "versions": self.script_versions(publication_id)}
        target = (self.root / relative).resolve()
        if self.root not in target.parents or not target.is_file():
            raise ValueError("Script introuvable")
        return {"publication": publication, "path": relative,
                "text": target.read_text(encoding="utf-8"),
                "validated": bool(self.validations().get(relative, {}).get("validated")),
                "versions": self.script_versions(publication_id)}

    def save_script_revision(self, publication_id: str, text: str) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Le script ne peut pas être vide")
        publication = self.publication(publication_id)
        concept = next(item for item in self.concepts() if item.id == publication["concept_id"])
        from .generator import next_version
        folder = self.scripts / concept.domaine
        folder.mkdir(parents=True, exist_ok=True)
        target = next_version(folder, concept.id, publication["platform"], publication.get("angle_index", 0) + 1)
        target.write_text(text.strip() + "\n", encoding="utf-8")
        relative = str(target.relative_to(self.root))
        self.update_publication(publication_id, script_path=relative, statut="en_attente_validation")
        return self.read_script(publication_id)

    def update_calendar_entry(self, publication_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        allowed = {"date", "slot", "heure", "concept_id", "titre", "serie", "note"}
        clean = {key: value for key, value in changes.items() if key in allowed}
        if "slot" in clean:
            clean["slot"] = int(clean["slot"])
            if clean["slot"] not in (1, 2):
                raise ValueError("Créneau invalide")
            clean["heure"] = "10:00" if clean["slot"] == 1 else "17:00"
        if "concept_id" in clean:
            concept = next((item for item in self.concepts() if item.id == clean["concept_id"]), None)
            if concept is None:
                raise ValueError("Concept inconnu")
            clean.update({"titre": concept.titre, "serie": concept.serie,
                          "script_path": "", "statut": "a_ecrire"})
        return self.update_publication(publication_id, **clean)

    def state(self) -> dict[str, Any]:
        concepts = self.concepts()
        calendar = self.calendar()
        from .charte import PRINCIPES_VISUELS, SERIES as CHARTER_SERIES
        from .formats import FORMATS
        charter = {
            "version": "derniere_version_validee",
            "cadence": {"publications_par_jour": 2, "jours_par_semaine": 7,
                        "creneaux": ["10:00", "17:00"]},
            "series": {item.id: {"nom": item.label, "couleur": item.couleur_secondaire,
                                  "pictogramme": item.pictogramme} for item in CHARTER_SERIES},
            "principes_visuels": list(PRINCIPES_VISUELS),
            "plateformes": {key: {"duree_cible_secondes": [fmt.target_seconds_min, fmt.target_seconds_max],
                                    "duree_max_secondes": fmt.hard_maximum_seconds,
                                    "structure": [beat.id for beat in fmt.beats],
                                    "priorite": fmt.priority} for key, fmt in FORMATS.items()},
            "garde_fous": ["Aucune publication automatique", "Validation humaine obligatoire pour chaque vidéo",
                            "Certification automatique des scripts : 6 agents à 9,5/10 minimum",
                            "Un script validé n'est jamais écrasé", "Source absente = génération bloquée",
                            "Contrôle des mots et de la synchronisation avant aperçu"],
        }
        complete = sum(bool(item.recovered and item.source_path and (self.root / item.source_path).is_file()) for item in concepts)
        automation_path = self.data / "automation.json"
        automation = json.loads(automation_path.read_text(encoding="utf-8")) if automation_path.exists() else {}
        queue_path = self.data / "production_queue.json"
        queue = json.loads(queue_path.read_text(encoding="utf-8")) if queue_path.exists() else {"jobs": []}
        batch_path = self.data / "script_batch.json"
        script_batch = json.loads(batch_path.read_text(encoding="utf-8")) if batch_path.exists() else {"status": "idle", "summary": {"total": 0, "certified": 0, "blocked": 0, "pending": 0}, "items": []}
        requirements_path = self.data / "requirements.json"
        requirements = json.loads(requirements_path.read_text(encoding="utf-8")) if requirements_path.exists() else []
        policy_path = self.data / "editorial_policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8")) if policy_path.exists() else {}
        heritage_path = self.data / "history.json"
        heritage_summary = json.loads(heritage_path.read_text(encoding="utf-8")).get("summary", {}) if heritage_path.exists() else {}
        usage_path = self.data / "api_usage.json"
        api_usage = json.loads(usage_path.read_text(encoding="utf-8")) if usage_path.exists() else {"total": {"calls": 0, "input_tokens": 0, "output_tokens": 0}, "days": {}}
        reviews = []
        for path in sorted((self.data / "reviews").glob("*.json")) if (self.data / "reviews").exists() else []:
            try:
                review = json.loads(path.read_text(encoding="utf-8"))
                reviews.append({"path": str(path.relative_to(self.root)), "publication_id": review.get("publication_id"),
                                "passed": review.get("passed", False), "overall": review.get("overall", 0),
                                "agents": review.get("agents", {})})
            except (OSError, json.JSONDecodeError):
                continue
        manifests = []
        manifest_ready = 0
        manifest_blocked = 0
        for path in sorted(self.production.rglob("manifest*.json"), reverse=True)[:50]:
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            statuses = [item.get("status") for item in value.get("items", [])]
            manifest_ready += statuses.count("awaiting_approval")
            manifest_blocked += statuses.count("blocked")
            manifests.append({"path": str(path.relative_to(self.root)), "date": value.get("date"),
                              "slot": value.get("slot"), "locked": value.get("publish_locked", True),
                              "items": len(value.get("items", [])), "status": value.get("status", "unknown"),
                              "ready": statuses.count("awaiting_approval"), "blocked": statuses.count("blocked")})
        publications = calendar.get("publications", [])
        certification_health = self.certification_health(publications)
        dates = sorted({item.get("date") for item in publications if item.get("date")})
        jobs = queue.get("jobs", [])
        blocked_jobs = [item for item in jobs if item.get("status") in ("blocked", "failed")]
        ready_jobs = [item for item in jobs if item.get("status") == "ready_for_review"]
        runtime_checks = {
            "calendar_complete": len(publications) == 1080 and len(dates) == 180,
            "sources_safe": all(item.recovered and item.source_path for item in concepts if any(p.get("concept_id") == item.id for p in publications)),
            "publication_locked": automation.get("publish") is False and automation.get("human_approval_required") is True,
            "scheduler_configured": {(item.get("slot"), item.get("time")) for item in automation.get("runs", [])} == {(1, "10:00"), (2, "17:00")},
            "queue_healthy": not blocked_jobs,
            "certifications_consistent": certification_health["inconsistent"] == 0,
        }
        last_backup = None
        backups = sorted((self.root / "recovery" / "backups").glob("*/backup.json"), reverse=True) if (self.root / "recovery" / "backups").exists() else []
        if backups:
            try: last_backup = json.loads(backups[0].read_text(encoding="utf-8")) | {"path": str(backups[0].parent.relative_to(self.root))}
            except (OSError, json.JSONDecodeError): pass
        return {
            "version": "BRITED Studio · dernière version reconstruite", "localOnly": True,
            "concepts": [asdict(item) for item in concepts],
            "calendar": calendar, "scripts": self.scripts_index(),
            "series": SERIES, "platforms": PLATFORM_LABELS,
            "charter": charter,
            "automation": automation,
            "queue": queue,
            "scriptBatch": script_batch,
            "requirements": requirements,
            "editorialPolicy": policy,
            "heritageSummary": heritage_summary,
            "apiUsage": api_usage,
            "reviews": reviews,
            "manifests": manifests,
            "operations": {"runtimeChecks": runtime_checks, "blockedJobs": len(blocked_jobs) + manifest_blocked,
                           "readyForReview": max(len(ready_jobs), manifest_ready), "lastBackup": last_backup,
                           "certificationHealth": certification_health,
                           "calendarStart": dates[0] if dates else None, "calendarEnd": dates[-1] if dates else None},
            "recovery": {"concepts": len(concepts), "completeSources": complete,
                         "missingSources": len(concepts) - complete,
                         "calendarEvidenceEntries": len(json.loads((self.data / "calendrier_recupere.json").read_text(encoding="utf-8")).get("publications", [])) if (self.data / "calendrier_recupere.json").exists() else 0},
        }
