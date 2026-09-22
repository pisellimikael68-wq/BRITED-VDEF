from __future__ import annotations

import re
from dataclasses import dataclass


OFFICIAL = ("legifrance.gouv.fr", "bofip.impots.gouv.fr", "service-public.fr", "service-public.gouv.fr",
            "amf-france.org", "insee.fr", "economie.gouv.fr", "ecb.europa.eu",
            "banque-france.fr", "impots.gouv.fr", "anil.org", "urssaf.fr",
            "notaires.fr", "eur-lex.europa.eu")
OFFICIAL_CITATIONS = (
    r"\bcode civil\b[^\n]{0,80}\barticle\s+[0-9]",
    r"\b(?:code général des impôts|CGI)\b[^\n]{0,80}\b(?:article|art\.)?\s*[0-9]",
    r"\bcode monétaire et financier\b[^\n]{0,80}\barticle\s+[LRD]?[0-9]",
    r"\bcode de la consommation\b[^\n]{0,80}\barticle\s+[LRD]?[0-9]",
    r"\bBOFiP\b[^\n]{0,100}\bBOI-[A-Z0-9-]+",
)
FORBIDDEN = (
    r"rendement garanti", r"sans risque", r"je vous conseille", r"je te conseille",
    r"vous devez investir", r"tu dois investir", r"contactez[- ]moi",
    r"\bBRITED\b", r"\bLeveria\b", r"\bLevéria\b",
)


@dataclass(frozen=True)
class ComplianceResult:
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def check(text: str, source: str = "") -> ComplianceResult:
    errors: list[str] = []
    warnings: list[str] = []
    combined = text + "\n" + source
    has_official_url = any(host in combined.casefold() for host in OFFICIAL)
    has_official_citation = any(re.search(pattern, combined, re.I) for pattern in OFFICIAL_CITATIONS)
    if not has_official_url and not has_official_citation:
        errors.append("Aucune source officielle reconnue")
    for expression in FORBIDDEN:
        if re.search(expression, text, re.I):
            errors.append(f"Formulation interdite détectée : {expression}")
    narration_match = re.search(r"## Narration continue\s*(.*?)(?=\n## |\Z)", text, re.S | re.I)
    editorial_text = narration_match.group(1) if narration_match else text
    assertive_text = re.sub(r"[^.!?]*\?", "", editorial_text)
    if re.search(r"\b(?:toujours|jamais|forcément|automatiquement)\b", assertive_text, re.I):
        warnings.append("Formulation absolue à vérifier dans son contexte")
    if not re.search(r"information générale|contenu pédagogique|ne constitue pas", text, re.I):
        warnings.append("Mention pédagogique absente")
    return ComplianceResult(not errors, tuple(errors), tuple(warnings))


def disclaimer_for(platform: str) -> str:
    return "Contenu pédagogique général. Ne constitue ni un conseil juridique, fiscal ou financier personnalisé, ni une recommandation d'investissement."
