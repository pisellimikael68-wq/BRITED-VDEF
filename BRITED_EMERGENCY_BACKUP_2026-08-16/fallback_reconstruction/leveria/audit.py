from __future__ import annotations

import re
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Audit:
    ok: bool
    score: float
    words: int
    seconds: float
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    def json(self) -> dict:
        return asdict(self)


LIMITS = {"tiktok": (85, 145), "reels": (70, 135), "shorts": (75, 145)}


def audit_script(text: str, platform: str) -> Audit:
    words = re.findall(r"\b[\wÀ-ÿ€%'-]+\b", text)
    narration = text
    marker = re.search(r"## Narration continue\s*(.*?)(?=\n## |\Z)", text, re.S | re.I)
    if marker:
        narration = marker.group(1)
        words = re.findall(r"\b[\wÀ-ÿ€%'-]+\b", narration)
    seconds = round(len(words) / 2.7, 1)
    low, high = LIMITS.get(platform, LIMITS["tiktok"])
    errors: list[str] = []
    warnings: list[str] = []
    if len(words) < low: errors.append(f"Script trop court : {len(words)} mots (minimum {low})")
    if len(words) > high: errors.append(f"Script trop long : {len(words)} mots (maximum {high})")
    if not re.search(r"https?://|Legifrance|BOFiP|INSEE|AMF", text, re.I):
        errors.append("Aucune source vérifiable détectée")
    if not re.search(r"exemple|imagin|suppos|€|euros?|%", narration, re.I):
        warnings.append("Aucun exemple concret ou chiffré détecté")
    if not re.search(r"abonn|partag|comment|enregistr", narration, re.I):
        warnings.append("Clôture sans appel à l’action")
    if not re.search(r"\?", narration[:400]):
        warnings.append("Aucune question d’implication au début")
    score = max(0.0, round(10 - len(errors) * 2 - len(warnings) * .5, 1))
    return Audit(not errors, score, len(words), seconds, tuple(errors), tuple(warnings))
