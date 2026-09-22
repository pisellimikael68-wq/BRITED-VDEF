from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, asdict
from typing import Any


CAPACITY = {
    "tiktok": {"regular": 22, "question": 19, "reponse": 15, "regle": 28, "nuance": 26, "cta": 18},
    "reels": {"regular": 22, "question": 19, "reponse": 15, "regle": 28, "nuance": 26, "cta": 18},
    "shorts": {"regular": 26, "question": 22, "reponse": 18, "cta": 22},
}

CANONICAL_APPOINTMENT_CTA = (
    "Vous souhaitez faire le point sur votre situation ? "
    "Prenez rendez-vous via le lien dans ma bio."
)


def words(text: str) -> list[str]:
    return re.findall(r"\S+", text.strip())


def normalized(text: str) -> str:
    value = text.replace("‑", "-").replace("‐", "-").replace("‒", "-")
    value = re.sub(r"\b(?:art|Art)\.\s*(?=\d)", "article ", value)
    return " ".join(words(value))


def beats_from_markdown(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    aliases = {"idee_utile": "regle", "reponse_explicite": "reponse",
               "question_interactive": "question", "exemple_concret": "exemple",
               "nuance_essentielle": "nuance", "cloture_en_boucle": "cta"}
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[- :|]+$", line):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 5 and cells[0].isdigit():
                beat_id = cells[1].casefold().replace("é", "e").replace("è", "e").replace("ô", "o")
                beat_id = re.sub(r"[^a-z]+", "_", beat_id).strip("_")
                narration = normalized(cells[2])
                # Les choix existent déjà dans les deux boutons visuels. Ils ne
                # doivent jamais être répétés dans la question, ni être lus.
                if aliases.get(beat_id, beat_id) == "question":
                    narration = re.sub(r"(?:[,;:]?\s*(?:oui\s*(?:/|ou)\s*non)\s*[.!?]?)$", "", narration, flags=re.I).strip()
                rows.append({"id": aliases.get(beat_id, beat_id), "label": cells[1],
                             "narration": narration, "visual": normalized(cells[3]), "screen_text": normalized(cells[4])})
    return rows


def digest(text: str) -> str:
    return hashlib.sha256(normalized(text).encode("utf-8")).hexdigest()


def split_text(text: str, maximum: int) -> list[str]:
    """Split on the best nearby punctuation without changing a single token."""
    tokens = words(text)
    if len(tokens) <= maximum:
        return [normalized(text)]
    chunks: list[str] = []
    cursor = 0
    minimum = max(7, round(maximum * .58))
    while len(tokens) - cursor > maximum:
        upper = cursor + maximum
        candidates = [i for i in range(cursor + minimum, upper + 1)
                      if tokens[i - 1].endswith((".", "!", "?", ";", ":", ","))]
        cut = candidates[-1] if candidates else upper
        chunks.append(" ".join(tokens[cursor:cut])); cursor = cut
    if cursor < len(tokens):
        chunks.append(" ".join(tokens[cursor:]))
    return chunks


def font_size(word_count: int, role: str) -> int:
    base = 46 if role in ("question", "reponse") else 43
    return max(32, base - max(0, word_count - 13) // 2)


@dataclass(frozen=True)
class AdaptationReport:
    passed: bool
    platform: str
    source_hash: str
    adapted_hash: str
    source_beats: int
    adapted_pages: int
    splits: int
    exact_text_preserved: bool
    minimum_font_size: int
    cta_normalized: bool
    warnings: tuple[str, ...]

    def json(self) -> dict[str, Any]:
        return asdict(self)


def adapt_beats(beats: list[dict[str, str]], platform: str) -> tuple[list[dict[str, Any]], AdaptationReport]:
    limits = CAPACITY.get(platform, CAPACITY["tiktok"])
    adapted: list[dict[str, Any]] = []
    original = " ".join(beat.get("narration", "") for beat in beats)
    minimum_font = 99
    warnings: list[str] = []
    cta_normalized = False
    comparison_beats: list[str] = []
    for beat_index, beat in enumerate(beats):
        beat_id = beat.get("id", "regle")
        role = beat_id if beat_id in limits else "regular"
        source_narration = normalized(beat.get("narration", ""))
        # Keep the approved CTA, including community questions, unchanged.
        comparison_beats.append(source_narration)
        # Règle commune validée : un beat cohérent reste sur une seule page.
        # La typographie et les cadres s'adaptent à la densité ; le moteur ne
        # crée plus jamais une page isolée pour la fin d'une phrase ou un article.
        chunks = [source_narration]
        for part_index, chunk in enumerate(chunks):
            page_role = role
            if role == "question" and part_index < len(chunks) - 1: page_role = "regular"
            if role == "reponse" and part_index > 0: page_role = "regular"
            if role == "cta" and part_index < len(chunks) - 1: page_role = "regular"
            size = font_size(len(words(chunk)), page_role)
            minimum_font = min(minimum_font, size)
            # La narration reste optimisee pour une diction francaise naturelle,
            # tandis que le texte affiche conserve la notation editoriale compacte
            # certifiee (chiffres, €, K€, %, dates). Un beat coherent n'etant plus
            # scinde, le texte ecran source peut etre preserve sans ambiguite.
            source_screen_text = normalized(beat.get("screen_text", ""))
            page_screen_text = source_screen_text or chunk
            adapted.append({**beat, "id": f"{beat_id}_{part_index + 1}" if len(chunks) > 1 else beat_id,
                            "source_beat_id": beat_id, "source_beat_index": beat_index,
                            "part": part_index + 1, "parts": len(chunks), "page_role": page_role,
                            "narration": chunk, "font_size": size,
                            "screen_text": page_screen_text})
    recomposed = " ".join(page["narration"] for page in adapted)
    exact = normalized(" ".join(comparison_beats)) == normalized(recomposed)
    literal_exact = normalized(original) == normalized(recomposed)
    if minimum_font < 34: warnings.append("Densité élevée : police proche du minimum de sécurité")
    report = AdaptationReport(exact, platform, digest(original), digest(recomposed), len(beats), len(adapted),
                              len(adapted) - len(beats), literal_exact, minimum_font if adapted else 0,
                              cta_normalized, tuple(warnings))
    if not report.passed:
        raise ValueError("L'agent de format a modifié ou perdu des mots : rendu bloqué")
    return adapted, report
