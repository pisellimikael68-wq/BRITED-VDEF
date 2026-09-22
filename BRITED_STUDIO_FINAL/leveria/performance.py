from __future__ import annotations

import re
from .audit import audit_script
from .formats import get_format


def score_script(text: str, platform: str) -> dict:
    audit = audit_script(text, platform)
    narration_match = re.search(r"## Narration continue\s*(.*?)(?=\n## |\Z)", text, re.S | re.I)
    narration = (narration_match.group(1) if narration_match else text).strip()
    opening = " ".join(narration.split()[:28])
    criteria = {
        "Accroche immédiate": 10.0 if re.search(r"\?|\btu\b|\bton\b|vous|votre|imagin|saviez", opening, re.I) else 7.0,
        "Durée indicative à confirmer à la lecture": 10.0 if not any("Durée indicative" in w for w in audit.warnings) else 7.0,
        "Structure": 10.0 if not any("Beat obligatoire" in e for e in audit.errors) else 5.0,
        "Interaction": 10.0 if re.search(r"\?", opening) else 7.0,
        "Exemple concret": 10.0 if re.search(r"exemple|imagin|suppos|€|euros?|%", narration, re.I) else 6.0,
        "Clarté": 10.0 if audit.ok and not audit.warnings else 0.0,
        "Conclusion utile": 10.0 if not any("réflexe pratique" in e for e in audit.errors) else 6.0,
        "Sécurité éditoriale": 10.0 if audit.ok else max(0.0, 10 - 2 * len(audit.errors)),
    }
    overall = round(sum(criteria.values()) / len(criteria), 1)
    return {"overall": overall, "criteria": criteria, "platform": platform,
            "audit": audit.json(), "ready": audit.ok and not audit.warnings and overall == 10.0 and all(score == 10.0 for score in criteria.values())}
