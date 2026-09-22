from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import date, timedelta
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
        self.root = root
        self.data = root / "data"
        self.content = root / "content"
        self.scripts = root / "scripts"
        self.production = root / "production"
        for folder in (self.data, self.content, self.scripts, self.production):
            folder.mkdir(parents=True, exist_ok=True)

    @property
    def calendar_path(self) -> Path:
        return self.data / "calendrier.json"

    def concepts(self) -> list[Concept]:
        catalog_path = self.data / "concepts_recuperes.json"
        if catalog_path.exists():
            raw = json.loads(catalog_path.read_text(encoding="utf-8"))
            return [Concept(**item) for item in raw]
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
        return json.loads(self.calendar_path.read_text(encoding="utf-8"))

    def save_calendar(self, value: dict[str, Any]) -> None:
        self.calendar_path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def build_calendar(self, start: date, days: int = 30) -> dict[str, Any]:
        concepts = self.concepts()
        if not concepts:
            raise ValueError("Aucun concept récupéré")
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
        by_id = {concept.id: concept for concept in concepts}
        for offset in range(days):
            day = start + timedelta(days=offset)
            for slot in (1, 2):
                recovered_ids = recovered_order.get(day.isoformat(), [])
                concept_id = recovered_ids[slot - 1] if len(recovered_ids) >= slot else concepts[(offset * 2 + slot - 1) % len(concepts)].id
                concept = by_id.get(concept_id) or Concept(concept_id, "divers", recovered_titles.get(concept_id, humanize(concept_id)), "finance")
                for platform in PLATFORMS:
                    aliases = (platform, "instagram") if platform == "reels" else (platform, "youtube") if platform == "shorts" else (platform,)
                    existing_script = ""
                    for alias in aliases:
                        candidates = sorted(self.scripts.rglob(f"{concept.id}__{alias}__a{slot}.md"))
                        if candidates:
                            existing_script = str(candidates[0].relative_to(self.root)); break
                    publications.append({
                        "id": f"{day.isoformat()}:{platform}:{concept.id}:{slot-1}",
                        "date": day.isoformat(), "slot": slot,
                        "heure": "10:00" if slot == 1 else "17:00",
                        "platform": platform, "concept_id": concept.id,
                        "titre": recovered_titles.get(concept.id, concept.titre), "serie": concept.serie,
                        "statut": "script_valide" if existing_script else "a_ecrire", "script_path": existing_script, "note": "",
                        "angle_index": slot - 1,
                    })
        value = {"publications": publications, "warnings": [], "generated_at": date.today().isoformat()}
        self.save_calendar(value)
        return value

    def scripts_index(self) -> list[dict[str, Any]]:
        result = []
        for path in sorted(self.scripts.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            result.append({"path": str(path.relative_to(self.root)), "name": path.name,
                           "validated": "A_CORRIGER" not in path.name and "BROUILLON" not in path.name,
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

    def state(self) -> dict[str, Any]:
        concepts = self.concepts()
        calendar = self.calendar()
        return {
            "version": "3.0-reconstruction", "localOnly": True,
            "concepts": [asdict(item) for item in concepts],
            "calendar": calendar, "scripts": self.scripts_index(),
            "series": SERIES, "platforms": PLATFORM_LABELS,
            "recovery": {"concepts": len(concepts), "completeSources": sum(item.recovered for item in concepts),
                         "missingSources": sum(not item.recovered for item in concepts),
                         "calendarEvidenceEntries": len(json.loads((self.data / "calendrier_recupere.json").read_text(encoding="utf-8")).get("publications", [])) if (self.data / "calendrier_recupere.json").exists() else 0},
        }
