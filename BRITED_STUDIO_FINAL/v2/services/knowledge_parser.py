from v2.models.content_models import Knowledge


def parse_knowledge(raw_text: str) -> Knowledge:

    knowledge = Knowledge()

    current_section = None

    section_map = {
        "définitions": "definitions",
        "definitions": "definitions",

        "règles": "rules",
        "regles": "rules",

        "fiscalité": "taxation",
        "fiscalite": "taxation",

        "erreurs": "mistakes",
        "erreurs fréquentes": "mistakes",

        "idées reçues": "misconceptions",
        "idees recues": "misconceptions",

        "questions fréquentes": "frequently_asked_questions",
        "questions frequentes": "frequently_asked_questions",

        "analogies": "analogies",

        "exemples": "examples",
        "cas pratiques": "examples",

        "références": "references",
        "references": "references",
    }

    for line in raw_text.splitlines():

        clean = line.strip()

        if not clean:
            continue

        title = clean.lower().replace("#", "").strip()

        if title in section_map:

            current_section = section_map[title]
            continue

        if clean.startswith("-") and current_section:

            value = clean.lstrip("-").strip()

            getattr(
                knowledge,
                current_section
            ).append(value)

    return knowledge
