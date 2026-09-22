from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


PLATFORMS = ("tiktok", "reels", "shorts")
PLATFORM_LABELS = {"tiktok": "TikTok", "reels": "Instagram / Facebook", "shorts": "Script face caméra unique"}
SERIES = {
    "fiscalite": {"label": "Fiscalité", "color": "#6F4E37", "icon": "％"},
    "immobilier": {"label": "Immobilier", "color": "#C96F4A", "icon": "⌂"},
    "juridique": {"label": "Juridique", "color": "#D99A2B", "icon": "§"},
    "finance": {"label": "Finance", "color": "#2457D6", "icon": "↗"},
}


def editorial_diversity(publications: list[dict[str, Any]], window_days: int = 14) -> dict[str, Any]:
    """Measure whether the public learns through a varied editorial journey."""
    rows = sorted((item for item in publications if item.get("platform") == "shorts"),
                  key=lambda item: (str(item.get("date", "")), int(item.get("slot", 0))))
    dates = sorted({str(item.get("date")) for item in rows if item.get("date")})
    missing_windows: list[dict[str, Any]] = []
    required = set(SERIES)
    for index in range(max(0, len(dates) - window_days + 1)):
        selected_dates = set(dates[index:index + window_days])
        present = {str(item.get("serie")) for item in rows if item.get("date") in selected_dates}
        missing = sorted(required - present)
        if missing:
            missing_windows.append({"from": dates[index], "to": dates[index + window_days - 1], "missing": missing})
    repeated_topics = [rows[index].get("concept_id") for index in range(1, len(rows))
                       if rows[index].get("concept_id") == rows[index - 1].get("concept_id")]
    return {"passed": not missing_windows and not repeated_topics,
            "windowDays": window_days, "missingWindows": missing_windows,
            "consecutiveRepeatedTopics": sorted(set(repeated_topics))}


def certified_by_reference_evidence(root: Path, target: Path, platform: str,
                                    record: dict[str, Any], errors: list[str]) -> bool:
    """Verify a measured, human-approved reference without relaxing global limits."""
    if not errors or not all(error.startswith("Script trop long") for error in errors):
        return False
    required = ("script_sha256", "reference_spec", "reference_spec_sha256",
                "quality_report", "word_report", "reference_video")
    if record.get("mode") != "explicit_human_reference_validation" or not all(record.get(key) for key in required):
        return False
    try:
        script_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        spec_path = root / record["reference_spec"]
        quality_path = root / record["quality_report"]
        word_path = root / record["word_report"]
        video_path = root / record["reference_video"]
        if script_hash != record["script_sha256"] or not all(path.is_file() for path in (spec_path, quality_path, word_path, video_path)):
            return False
        if hashlib.sha256(spec_path.read_bytes()).hexdigest() != record["reference_spec_sha256"]:
            return False
        source = target.read_text(encoding="utf-8")
        marker = re.search(r"## Narration continue\s*(.*?)(?=\n## |\Z)", source, re.S | re.I)
        source_narration = " ".join((marker.group(1) if marker else source).split())
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec_narration = " ".join(" ".join(beat.get("narration", "") for beat in spec.get("beats", [])).split())
        quality = json.loads(quality_path.read_text(encoding="utf-8"))
        word = json.loads(word_path.read_text(encoding="utf-8"))
        measured = float(quality.get("expected_duration", 999))
        return bool(source_narration == spec_narration and quality.get("passed") and word.get("passed")
                    and abs(measured - float(record.get("measured_duration_seconds", -1))) < .05)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return False


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

    def editorial_policy_hash(self) -> str:
        policy = self.data / "editorial_policy.json"
        return hashlib.sha256(policy.read_bytes()).hexdigest() if policy.is_file() else ""

    def reconcile_certifications(self) -> dict[str, int]:
        """Invalidate obsolete certifications while preserving their complete history."""
        from .audit import audit_script
        values = self.validations()
        calendar = self.calendar()
        publications = calendar.get("publications", [])
        current_by_path = {item.get("script_path", ""): item for item in publications if item.get("script_path")}
        checked = invalidated = 0
        changed = False
        policy_hash = self.editorial_policy_hash()
        for relative, record in values.items():
            if not record.get("validated"):
                continue
            target = self.root / relative
            publication = current_by_path.get(relative)
            platform = publication.get("platform") if publication else ("reels" if "__instagram__" in relative else "shorts" if "__youtube__" in relative else "tiktok")
            checked += 1
            script_audit = None if not target.is_file() else audit_script(target.read_text(encoding="utf-8"), platform)
            errors = ["Fichier certifié introuvable"] if script_audit is None else list(script_audit.errors) + list(script_audit.warnings)
            if float(record.get("score", 0)) != 10.0 or float(record.get("threshold", 0)) != 10.0:
                errors.append("Ancienne certification inférieure au nouveau seuil strict de 10/10")
            if not policy_hash or record.get("editorial_policy_sha256") != policy_hash:
                errors.append("Certification antérieure à la ligne éditoriale grand public actuellement validée")
            review_path = self.root / str(record.get("review_path", ""))
            if not review_path.is_file():
                errors.append("Rapport de certification 10/10 introuvable")
            else:
                try:
                    report = json.loads(review_path.read_text(encoding="utf-8"))
                    agents = report.get("agents", {})
                    from .review_agents import AGENTS
                    if (not report.get("passed") or set(agents) != set(AGENTS)
                            or not all(item.get("passed") and float(item.get("score", 0)) == 10.0 for item in agents.values())):
                        errors.append("Comité non unanime à 10/10")
                except (OSError, ValueError, TypeError, json.JSONDecodeError):
                    errors.append("Rapport de certification 10/10 illisible")
            legacy_certification = any("nouveau seuil strict" in error or "Comité non unanime" in error or "rapport de certification" in error.casefold() for error in errors)
            if errors and (legacy_certification or not certified_by_reference_evidence(self.root, target, platform, record, errors)):
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
            audit = audit_script(target.read_text(encoding="utf-8"), platform)
            record = values.get(relative, {})
            strict_score = float(record.get("score", 0)) == 10.0 and float(record.get("threshold", 0)) == 10.0
            audit_ok = audit.ok and not audit.warnings and strict_score
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
        if score != 10.0:
            raise ValueError("Certification automatique refusée : score strictement inférieur à 10/10")
        target = (self.root / path).resolve()
        review = (self.root / review_path).resolve()
        if self.root not in target.parents or not target.is_file() or self.root not in review.parents or not review.is_file():
            raise ValueError("Script ou rapport de contrôle introuvable")
        report = json.loads(review.read_text(encoding="utf-8"))
        from .review_agents import AGENTS
        if (not report.get("passed") or set(report.get("agents", {})) != set(AGENTS)
                or not all(item.get("passed") and float(item.get("score", 0)) == 10.0 for item in report["agents"].values())):
            raise ValueError("Le comité automatique n'a pas unanimement validé le script")
        values = self.validations()
        values[path] = {"publication_id": publication_id, "validated": True, "mode": "automatic_committee",
                        "score": score, "threshold": 10.0, "review_path": review_path,
                        "editorial_policy_sha256": self.editorial_policy_hash(),
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
        publications = value.get("publications", [])
        for publication in publications:
            if publication.get("platform") != "tiktok":
                continue
            instagram = next((candidate for candidate in publications
                if candidate.get("platform") == "reels"
                and candidate.get("date") == publication.get("date")
                and candidate.get("slot") == publication.get("slot")
                and candidate.get("concept_id") == publication.get("concept_id")), None)
            if instagram:
                publication["script_path"] = instagram.get("script_path", "")
                publication["review_path"] = instagram.get("review_path", "")
                publication["distribution_source_platform"] = "reels"
                if instagram.get("statut"):
                    publication["statut"] = instagram["statut"]
        for publication in publications:
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
                    from .cta import cta_mode
                    aliases = ("reels", "instagram") if platform in ("reels", "tiktok") else (platform, "youtube") if platform == "shorts" else (platform,)
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
                        "cta_mode": cta_mode(day, slot),
                    })
        diversity = editorial_diversity(publications)
        warnings = [] if diversity["passed"] else ["Diversité éditoriale à corriger avant programmation"]
        value = {"publications": publications, "warnings": warnings,
                 "editorial_diversity": diversity, "generated_at": date.today().isoformat()}
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
        publication = self.canonical_script_publication(publication_id)
        aliases = ("shorts", "youtube", "face_camera")
        validations = self.validations()
        paths = [path for alias in aliases for path in self.scripts.rglob(f"{publication['concept_id']}__{alias}__a{publication.get('angle_index', 0)+1}*.md")]
        return [{"path": str(path.relative_to(self.root)), "name": path.name,
                 "validated": bool(validations.get(str(path.relative_to(self.root)), {}).get("validated")),
                 "modified": path.stat().st_mtime}
                for path in sorted(set(paths), key=lambda item: item.stat().st_mtime, reverse=True)]

    def canonical_script_publication(self, publication_id: str) -> dict[str, Any]:
        """Return the single face-camera script record for a scheduled subject.

        Legacy platform rows remain in the calendar as distribution history, but
        they never create or expose a second editorial script.
        """
        publication = self.publication(publication_id)
        if publication.get("platform") == "shorts":
            return publication
        candidate = next((item for item in self.calendar().get("publications", [])
                          if item.get("platform") == "shorts"
                          and item.get("date") == publication.get("date")
                          and item.get("slot") == publication.get("slot")
                          and item.get("concept_id") == publication.get("concept_id")), None)
        return candidate or publication

    def manifest(self, relative: str) -> dict[str, Any]:
        target = (self.root / relative).resolve()
        is_manifest = target.name == "manifest.json" or (
            target.name.startswith("manifest-pilot-") and target.suffix == ".json"
        )
        if self.root not in target.parents or self.production not in target.parents or not target.is_file() or not is_manifest:
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
        for linked_id in item.get("linked_publication_ids", []):
            if linked_id != publication_id:
                self.update_publication(linked_id, statut="video_validee")
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
            if item.get("platform") in {"tiktok", "reels"}:
                youtube = next((candidate for candidate in publications
                    if candidate.get("platform") == "shorts"
                    and candidate.get("slot") == item.get("slot")
                    and candidate.get("concept_id") == item.get("concept_id")), None)
                if youtube:
                    item["script_path"] = youtube.get("script_path", "")
                    item["review_path"] = youtube.get("review_path", "")
                    item["distribution_source_platform"] = "shorts"
            relative = item.get("script_path", "")
            target = self.root / relative if relative else None
            item["script_text"] = target.read_text(encoding="utf-8") if target and target.is_file() else ""
            item["validation"] = validations.get(relative, {})
            review_path = item.get("review_path") or item["validation"].get("review_path", "")
            review_target = self.root / review_path if review_path else None
            item["review"] = json.loads(review_target.read_text(encoding="utf-8")) if review_target and review_target.is_file() else {}
        publications.sort(key=lambda item: (int(item.get("slot", 0)), PLATFORMS.index(item["platform"])))
        unique_scripts = {item.get("script_path") for item in publications if item.get("script_text")}
        unique_certified = {item.get("script_path") for item in publications if item.get("validation", {}).get("validated")}
        unique_video_sources = {(item.get("slot"), "shorts")
                                for item in publications if item.get("statut") in ("video_prete", "video_validee")}
        return {"date": day, "publications": publications,
                "summary": {"total": len(publications), "scripts": len(unique_scripts),
                            "certified": len(unique_certified), "videos": len(unique_video_sources),
                            "active_charters": 1, "distribution_destinations": 4}}

    def read_script(self, publication_id: str, path: str = "") -> dict[str, Any]:
        publication = self.canonical_script_publication(publication_id)
        publication_id = publication["id"]
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

    def final_scripts(self, day: str) -> dict[str, Any]:
        """Return only scripts that still satisfy the complete 10/10 proof."""
        from .audit import audit_script
        from .review_agents import AGENTS

        try:
            date.fromisoformat(day)
        except ValueError as error:
            raise ValueError("Date invalide") from error
        validations = self.validations()
        policy_hash = self.editorial_policy_hash()
        rows = sorted((item for item in self.calendar().get("publications", [])
                       if item.get("date") == day and item.get("platform") == "shorts"),
                      key=lambda item: int(item.get("slot", 0)))
        scripts: list[dict[str, Any]] = []
        pending = 0
        for item in rows:
            relative = str(item.get("script_path", ""))
            target = self.root / relative if relative else None
            record = validations.get(relative, {})
            review_relative = str(record.get("review_path") or item.get("review_path", ""))
            review_target = self.root / review_relative if review_relative else None
            certified = bool(relative and target and target.is_file() and record.get("validated")
                             and float(record.get("score", 0)) == 10.0
                             and float(record.get("threshold", 0)) == 10.0
                             and policy_hash and record.get("editorial_policy_sha256") == policy_hash
                             and review_target and review_target.is_file())
            report: dict[str, Any] = {}
            if certified:
                try:
                    report = json.loads(review_target.read_text(encoding="utf-8"))
                    agents = report.get("agents", {})
                    certified = bool(
                        report.get("passed") and float(report.get("overall", 0)) == 10.0
                        and set(agents) == set(AGENTS)
                        and not report.get("errors") and not report.get("recommendations")
                        and all(agent.get("passed") and float(agent.get("score", 0)) == 10.0
                                and not agent.get("findings") and not agent.get("recommendations")
                                for agent in agents.values())
                    )
                except (OSError, ValueError, TypeError, json.JSONDecodeError):
                    certified = False
            if certified:
                text = target.read_text(encoding="utf-8")
                audit = audit_script(text, "shorts")
                certified = audit.ok and not audit.errors and not audit.warnings
            if not certified:
                pending += 1
                continue
            match = re.search(r"## Narration continue\s*([\s\S]*?)(?=\n## |$)", text, re.I)
            narration = (match.group(1) if match else "").strip()
            narration = "\n\n".join(line.strip().removeprefix("«").removesuffix("»").strip()
                                      for line in narration.splitlines() if line.strip())
            if narration:
                scripts.append({"id": item["id"], "slot": item.get("slot"),
                                "time": "10 h" if item.get("slot") == 1 else "17 h",
                                "title": item.get("titre", ""), "text": narration,
                                "certified": True, "score": 10.0,
                                "agents": len(AGENTS), "impactValidated": "impact_dynamique" in report.get("agents", {})})
            else:
                pending += 1
        return {"date": day, "scripts": scripts, "ready": len(scripts),
                "scheduled": len(rows), "pending": pending}

    def face_camera_launch_plan(self) -> dict[str, Any]:
        """Expose the editorial path without exposing repository files."""
        path = self.data / "face_camera_launch_plan.json"
        if not path.is_file():
            return {"version": 1, "principle": "", "days": []}
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value.get("days"), list):
            raise ValueError("Programme éditorial invalide")
        ready_by_date = {day["date"]: self.final_scripts(day["date"])["ready"]
                         for day in value["days"] if isinstance(day, dict) and day.get("date")}
        value["days"] = [{**day, "ready": ready_by_date.get(day.get("date"), 0)}
                         for day in value["days"]]
        return value

    def shooting_library(self, start: str, days: int = 14) -> dict[str, Any]:
        """Return a safe, readable filming queue, including clearly labelled drafts."""
        try:
            first_day = date.fromisoformat(start)
        except ValueError as error:
            raise ValueError("Date invalide") from error
        if days < 1 or days > 31:
            raise ValueError("La période doit contenir entre 1 et 31 jours")
        selected = {(first_day + timedelta(days=offset)).isoformat() for offset in range(days)}
        certified_by_id = {
            script["id"]: script
            for day in selected
            for script in self.final_scripts(day)["scripts"]
        }
        rows = sorted((item for item in self.calendar().get("publications", [])
                       if item.get("date") in selected and item.get("platform") == "shorts"),
                      key=lambda item: (item.get("date", ""), int(item.get("slot", 0))))
        scripts: list[dict[str, Any]] = []
        for item in rows:
            certified = certified_by_id.get(item.get("id"))
            if certified:
                scripts.append({**certified, "date": item.get("date"), "status": "final"})
                continue
            relative = str(item.get("script_path", ""))
            target = self.root / relative if relative else None
            text = target.read_text(encoding="utf-8") if target and target.is_file() else ""
            match = re.search(r"## Narration continue\s*([\s\S]*?)(?=\n## |$)", text, re.I)
            narration = (match.group(1) if match else "").strip()
            narration = "\n\n".join(line.strip().removeprefix("«").removesuffix("»").strip()
                                      for line in narration.splitlines() if line.strip())
            scripts.append({"id": item.get("id"), "date": item.get("date"),
                            "slot": item.get("slot"),
                            "time": "10 h" if item.get("slot") == 1 else "17 h",
                            "title": item.get("titre", ""), "text": narration,
                            "status": "draft", "certified": False, "score": None,
                            "agents": 0, "impactValidated": False})
        return {"start": start, "days": days, "scripts": scripts,
                "ready": sum(item["status"] == "final" for item in scripts),
                "drafts": sum(item["status"] == "draft" for item in scripts)}

    def save_script_revision(self, publication_id: str, text: str) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Le script ne peut pas être vide")
        publication = self.canonical_script_publication(publication_id)
        publication_id = publication["id"]
        concept = next(item for item in self.concepts() if item.id == publication["concept_id"])
        from .generator import next_version
        folder = self.scripts / concept.domaine
        folder.mkdir(parents=True, exist_ok=True)
        target = next_version(folder, concept.id, "shorts", publication.get("angle_index", 0) + 1)
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
                                    "priorite": fmt.priority,
                                    **({"destinations_diffusion": ["instagram", "tiktok"]} if key == "reels" else {})}
                               for key, fmt in FORMATS.items() if key != "tiktok"},
            "garde_fous": ["Aucune publication automatique", "Validation humaine obligatoire pour chaque vidéo",
                            "Certification automatique des scripts : tous les agents à 10/10, sans réserve",
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
        openai_bulk_path = self.data / "openai_bulk" / "state.json"
        openai_bulk = json.loads(openai_bulk_path.read_text(encoding="utf-8")) if openai_bulk_path.exists() else {"status": "idle", "summary": {"requested": 0, "drafted": 0, "preflight_ready": 0, "blocked": 0, "certified": 0}}
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
        # Les manifestes pilotes sont des preuves intermédiaires ; une fois
        # consolidés, ils ne doivent pas être comptés comme des sessions
        # supplémentaires à regarder.
        for path in sorted(self.production.rglob("manifest.json"), reverse=True)[:50]:
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
        # Le calendrier historique conserve les trois anciennes déclinaisons.
        # Le site face caméra n'expose toutefois qu'une entrée canonique par
        # sujet : le script `shorts`, désormais commun aux quatre réseaux.
        calendar_for_ui = dict(calendar)
        calendar_for_ui["publications"] = [
            item for item in publications if item.get("platform") == "shorts"
        ]
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
            "calendar": calendar_for_ui, "scripts": self.scripts_index(),
            "series": SERIES, "platforms": PLATFORM_LABELS,
            "charter": charter,
            "automation": automation,
            "queue": queue,
            "scriptBatch": script_batch,
            "openaiBulk": openai_bulk,
            "requirements": requirements,
            "editorialPolicy": policy,
            "editorialDiversity": editorial_diversity(calendar_for_ui.get("publications", [])),
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
