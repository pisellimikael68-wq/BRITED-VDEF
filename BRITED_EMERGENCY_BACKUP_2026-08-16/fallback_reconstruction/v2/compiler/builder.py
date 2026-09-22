from dataclasses import MISSING, fields

from v2.models.knowledge_models import Topic

from .models import RawChapter, RawTopic


def build_topic(
    raw: RawTopic,
    chapter: RawChapter,
) -> Topic:
    """
    Transforme un RawTopic en Topic BRITED.
    Les champs inconnus sont automatiquement remplis
    avec leur valeur par défaut.
    """

    values = {}

    # -----------------------------
    # Champs obligatoires provenant
    # du Markdown
    # -----------------------------

    values["id"] = raw.id
    values["title"] = raw.title
    values["pillar"] = chapter.pillar
    values["family"] = chapter.family
    values["chapter"] = chapter.chapter

    values["difficulty"] = raw.difficulty
    values["priority"] = raw.priority
    values["editorial_order"] = raw.editorial_order

    # -----------------------------
    # Complète automatiquement tous
    # les autres champs du dataclass
    # -----------------------------

    for field in fields(Topic):

        if field.name in values:
            continue

        if field.default is not MISSING:
            values[field.name] = field.default
            continue

        if field.default_factory is not MISSING:
            values[field.name] = field.default_factory()
            continue

        # Champs obligatoires sans valeur
        values[field.name] = ""

    return Topic(**values)
