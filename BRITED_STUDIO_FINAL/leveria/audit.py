from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, asdict

from .compliance import check
from .formats import get_format


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


def audit_script(text: str, platform: str) -> Audit:
    words = re.findall(r"\b[\wÀ-ÿ]+(?:['’\-][\wÀ-ÿ]+)*\b", text)
    narration = text
    marker = re.search(r"## Narration continue\s*(.*?)(?=\n## |\Z)", text, re.S | re.I)
    if marker:
        narration = marker.group(1)
        words = re.findall(r"\b[\wÀ-ÿ]+(?:['’\-][\wÀ-ÿ]+)*\b", narration)
    seconds = round(len(words) / (160 / 60) + 4, 1)  # Estimation, jamais une durée mesurée.
    fmt = get_format(platform)
    errors: list[str] = []
    warnings: list[str] = []
    if not fmt.target_seconds_min <= seconds <= fmt.target_seconds_max:
        warnings.append(f"Durée indicative {seconds} s hors cible 60–65 s à 160 mots/minute et 4 s de pauses : lecture chronométrée nécessaire")
    compliance = check(text)
    errors.extend(compliance.errors)
    warnings.extend(compliance.warnings)
    if not re.search(r"exemple|imagin|suppos|€|euros?|%", narration, re.I):
        warnings.append("Aucun exemple concret ou chiffré détecté")
    found_beats = [match.casefold() for match in re.findall(r"\|\s*\d+\s*\|\s*([^|]+)", text)]
    if found_beats:
        expected = [beat.id for beat in fmt.beats]
        def identifier(value: str) -> str:
            folded = unicodedata.normalize("NFKD", value.casefold())
            return re.sub(r"[^a-z]", "", "".join(char for char in folded if not unicodedata.combining(char)))
        normalized = [identifier(value) for value in found_beats]
        cursor = 0
        for beat in expected:
            needle = identifier(beat)
            try:
                cursor = next(i + 1 for i in range(cursor, len(normalized)) if needle in normalized[i])
            except StopIteration:
                errors.append(f"Beat obligatoire absent ou mal ordonné : {beat}")
                break
        table_narration = []
        for line in text.splitlines():
            cells = [cell.strip() for cell in line.split("|")]
            if len(cells) >= 6 and cells[1].isdigit():
                table_narration.append(cells[3])
        if marker and table_narration:
            compact = lambda value: re.sub(r"\s+", " ", value).strip()
            if compact(" ".join(table_narration)) != compact(narration):
                errors.append("Narration continue différente de la concaténation des beats")
    if fmt.id in ("tiktok", "reels") and not re.search(r"\?", narration[:500]):
        warnings.append("Question interactive absente du début")
    forbidden_spoken_labels = re.findall(r"(?:^|[.!?]\s+)(?:La\s+)?(Court|Règle|Question|Réponse)\s*:", narration, re.I)
    if forbidden_spoken_labels:
        errors.append("Libellé de fabrication interdit dans la narration : " + ", ".join(dict.fromkeys(forbidden_spoken_labels)))
    if re.search(r"(?:<=|>=|≤|≥)", narration):
        errors.append("Narration orale : les opérateurs doivent être écrits en français naturel (inférieur ou égal, supérieur ou égal)")
    if fmt.id == "shorts":
        spoken_sentences = [part.strip(" «»\n\t") for part in re.split(r"[.!?]+", narration) if part.strip()]
        oversized = [len(re.findall(r"\b[\wÀ-ÿ€%'-]+\b", sentence)) for sentence in spoken_sentences]
        if oversized and max(oversized) > 35:
            errors.append(f"Face caméra : phrase trop longue pour un souffle naturel ({max(oversized)} mots, maximum 35)")
        hook = spoken_sentences[0] if spoken_sentences else ""
        hook_words = len(re.findall(r"\b[\wÀ-ÿ€%'-]+\b", hook))
        if hook_words > 18:
            errors.append(f"Hook trop long pour arrêter le défilement ({hook_words} mots, maximum 18)")
        generic_opening = re.match(
            r"(?:aujourd['’]hui|dans cette vidéo|nous allons voir|je vais vous expliquer|parlons de|il faut savoir que|saviez-vous que)\b",
            hook,
            re.I,
        )
        if generic_opening:
            errors.append("Hook générique ou professoral : commencer directement par un enjeu concret pour le spectateur")
        if re.match(r"(?:commencer|verser|placer|mettre)\b", hook, re.I):
            errors.append("Hook ambigu hors contexte : nommer dès les premiers mots ce qui est commencé, versé, placé ou réparti")
        opening_lines = [line.strip(" «»\n\t") for line in narration.splitlines() if line.strip()]
        if len(opening_lines) >= 2 and opening_lines[1].endswith("?"):
            errors.append("Valeur retardée : la deuxième phrase reformule une question au lieu d'apporter la réponse")
        if re.search(r"\b(?:vous|cela|ça)\s+impose\s*\?", narration, re.I):
            errors.append("Question orale maladroite : préciser « est-ce imposable ? » ou « cela déclenche-t-il un impôt ? »")
        teaching_phrases = re.findall(
            r"\b(?:dans un premier temps|dans un second temps|premièrement|deuxièmement|nous allons|il convient de|en effet|par conséquent)\b",
            narration,
            re.I,
        )
        if teaching_phrases:
            errors.append("Ton de cours détecté dans la narration : " + ", ".join(dict.fromkeys(value.casefold() for value in teaching_phrases)))
        if not re.search(r"\b(?:concrètement|imagine|imaginez|supposons|projetez-vous|prenons (?:ton|votre|un (?:cas|exemple))|par exemple|en pratique|autrement dit|cela signifie)\b", narration, re.I):
            errors.append("Pédagogie grand public : aucun exemple ou passage concret n'aide à retenir la règle")
        audience_projection = re.search(
            r"\b(?:imagine|imaginez|supposons|mets-toi|mettez-vous|projetez-vous)\b[^.!?]{0,180}\b(?:tu|ton|ta|tes|vous|votre|vos)\b|"
            r"\bprenons\s+(?:ton|ta|tes|votre|un exemple[^.!?]{0,80}\b(?:tu|ton|ta|tes|vous|votre|vos)\b)|"
            r"\bsi\s+(?:tu|vous)\b[^.!?]{0,180}|"
            r"\b(?:ton|ta|tes)\b[^.!?]{0,180}",
            narration,
            re.I,
        )
        if not audience_projection:
            errors.append("Personnalité face caméra : l'exemple ne projette pas explicitement le spectateur dans la situation")
        practical_narration = re.sub(
            r"Vous souhaitez faire le point sur votre situation\s*\?\s*Prenez rendez[-‑ ]vous via le lien dans ma bio\.?",
            "",
            narration,
            flags=re.I,
        )
        practical_action = re.search(
            r"\b(?:explique|expliquez|mettez|vérifie|compare|conserve|garde|déclare|signale|simule|calcule|demande|lis|regarde|note|retrouve|rassemble|fais préciser|fais vérifier|fais les|ouvre|vérifiez|comparez|conservez|gardez|déclarez|signalez|simulez|calculez|demandez|lisez|regardez|notez|assurez-vous|faites correspondre|faites préciser)\b",
            practical_narration,
            re.I,
        )
        if not practical_action:
            errors.append("Valeur concrète : aucun réflexe pratique précis et immédiatement utilisable avant le CTA")
        technical_explanations = {
            "soulte": r"(?:somme|argent|montant).{0,45}(?:ajout|reçu|versé)|(?:ajout|reçu|versé).{0,45}(?:somme|argent|montant)",
            "abattement": r"(?:réduction|part|montant).{0,55}(?:non impos|exonér|retir)|(?:non impos|exonér).{0,55}(?:part|montant)",
            "assiette": r"base.{0,20}(?:calcul|impos)",
            "quote-part": r"(?:part|portion).{0,35}(?:calcul|correspond)",
            "usufruit": r"droit.{0,45}(?:utilis|revenu|habit)",
            "nue-propriété": r"propriét.{0,45}(?:sans|usufruit|utilis)",
            "pfu": r"(?:prélèvement forfaitaire unique|flat.?tax)",
        }
        unexplained = [term for term, explanation in technical_explanations.items()
                       if re.search(rf"\b{re.escape(term)}\b", narration, re.I)
                       and not re.search(explanation, narration, re.I)]
        if unexplained:
            errors.append("Pédagogie grand public : terme technique non expliqué simplement : " + ", ".join(unexplained))
    assurance_after_eight = (
        re.search(r"assurance[- ]vie", narration, re.I)
        and re.search(r"(?:huit|8)\s+ans", narration, re.I)
        and re.search(r"abattement|quatre mille six cents|4\s*600", narration, re.I)
    )
    if assurance_after_eight:
        if not re.search(r"neuf mille deux cents|9\s*200", narration, re.I):
            errors.append("Assurance-vie après huit ans : l'abattement de 9 200 € du couple marié ou pacsé imposé ensemble est absent")
        if not (re.search(r"capital", narration, re.I) and re.search(r"gains?", narration, re.I)):
            errors.append("Rachat d'assurance-vie : la distinction entre capital et gains doit être explicitée")
    financial_contract_types = (
        "assurance-vie", "assurance vie", "contrat de capitalisation", "per", "plan d'épargne retraite",
        "pea", "plan d'épargne en actions", "compte-titres", "compte titres",
    )
    if any(re.search(rf"\b{re.escape(contract_type)}\b", text, re.I) for contract_type in financial_contract_types):
        vague_contract = re.search(r"\b(?:ton|votre|ce|le) contrat\b(?!\s+(?:d['’]assurance[- ]vie|de capitalisation))", narration, re.I)
        vague_investment = re.search(r"\b(?:ton|votre|ce|le) placement\b", narration, re.I)
        if vague_contract or vague_investment:
            errors.append("Série Finance : la nature exacte du contrat ou du produit doit être précisée dans la même phrase")
    score = max(0.0, round(10 - len(errors) * 2 - len(warnings) * .5, 1))
    return Audit(not errors, score, len(words), seconds, tuple(errors), tuple(warnings))
