from v2.models.editorial_models import EditorialStrategy


def parse_editorial(text: str) -> EditorialStrategy:

    strategy = EditorialStrategy()

    current = None

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        lower = line.lower()

        if lower.startswith("audience"):
            current = "audience"
            continue

        if lower.startswith("objectif"):
            current = "objective"
            continue

        if lower.startswith("message"):
            current = "key_message"
            continue

        if lower.startswith("ton"):
            current = "tone"
            continue

        if lower.startswith("émotion") or lower.startswith("emotion"):
            current = "emotion"
            continue

        if lower.startswith("complexité") or lower.startswith("complexite"):
            current = "complexity"
            continue

        if lower.startswith("format"):
            current = "format"
            continue

        if lower.startswith("cta"):
            current = "cta_strategy"
            continue

        if (
            lower.startswith("à éviter")
            or lower.startswith("a éviter")
            or lower.startswith("a eviter")
            or lower.startswith("points à éviter")
        ):
            current = "forbidden_points"
            continue

        if current == "audience":
            strategy.audience += line + "\n"

        elif current == "objective":
            strategy.objective += line + "\n"

        elif current == "key_message":
            strategy.key_message += line + "\n"

        elif current == "tone":
            strategy.tone += line + "\n"

        elif current == "emotion":
            strategy.emotion += line + "\n"

        elif current == "complexity":
            strategy.complexity += line + "\n"

        elif current == "format":
            strategy.format += line + "\n"

        elif current == "cta_strategy":
            strategy.cta_strategy += line + "\n"

        elif current == "forbidden_points":

            strategy.forbidden_points.append(
                line.lstrip("-• ").strip()
            )

    strategy.audience = strategy.audience.strip()
    strategy.objective = strategy.objective.strip()
    strategy.key_message = strategy.key_message.strip()
    strategy.tone = strategy.tone.strip()
    strategy.emotion = strategy.emotion.strip()
    strategy.complexity = strategy.complexity.strip()
    strategy.format = strategy.format.strip()
    strategy.cta_strategy = strategy.cta_strategy.strip()

    return strategy
