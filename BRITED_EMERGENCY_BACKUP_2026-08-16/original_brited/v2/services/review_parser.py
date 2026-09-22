import re

from v2.models.content_models import Review


def _extract_section(title: str, text: str) -> str:
    pattern = rf"#\s*{re.escape(title)}\s*(.*?)(?=\n# |\Z)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return ""

    return match.group(1).strip()


def _extract_score(section: str) -> int:
    if not section:
        return 0

    # Cas : Score : 30/30
    match = re.search(
        r"Score\s*:\s*(\d+)\s*/\s*\d+",
        section,
        re.IGNORECASE,
    )

    if match:
        return int(match.group(1))

    # Cas : Score : 30
    match = re.search(
        r"Score\s*:\s*(\d+)",
        section,
        re.IGNORECASE,
    )

    if match:
        return int(match.group(1))

    # Cas : 30/30 ou 20/20 ou 10/10
    matches = re.findall(
        r"(\d+)\s*/\s*\d+",
        section,
        re.IGNORECASE,
    )

    if matches:
        return int(matches[-1])

    # Pour la section globale "# Score" contenant juste "97"
    match = re.search(
        r"^\s*(\d+)\s*$",
        section,
        re.MULTILINE,
    )

    if match:
        return int(match.group(1))

    return 0


def _extract_list(title: str, text: str) -> list[str]:
    section = _extract_section(title, text)

    if not section:
        return []

    items = []

    for line in section.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("-"):
            line = line[1:].strip()

        items.append(line)

    return items


def parse_review(text: str) -> Review:
    review = Review(score=0)

    review.score = _extract_score(
        _extract_section("Score", text)
    )

    review.patrimonial_score = _extract_score(
        _extract_section("Patrimonial", text)
    )

    review.pedagogy_score = _extract_score(
        _extract_section("Pédagogie", text)
    )

    review.instagram_score = _extract_score(
        _extract_section("Instagram", text)
    )

    review.hook_score = _extract_score(
        _extract_section("Hook", text)
    )

    review.cta_score = _extract_score(
        _extract_section("CTA", text)
    )

    review.compliance_score = _extract_score(
        _extract_section("Compliance", text)
    )

    review.strengths = _extract_list(
        "Points forts",
        text,
    )

    review.weaknesses = _extract_list(
        "Faiblesses",
        text,
    )

    rewrite = _extract_section(
        "Réécriture nécessaire",
        text,
    ).lower()

    review.rewrite_needed = (
        "oui" in rewrite
        or "yes" in rewrite
        or "nécessaire" in rewrite
    ) and "aucune" not in rewrite

    review.rewrite_instructions = _extract_list(
        "Instructions de réécriture",
        text,
    )

    return review
