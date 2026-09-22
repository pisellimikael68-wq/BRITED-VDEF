from dataclasses import dataclass


# ==========================================================
# Planner
# ==========================================================


@dataclass(slots=True)
class PlannedTopic:
    """
    Topic produit par le Planner.
    """

    id: str
    title: str
    editorial_order: int


@dataclass(slots=True)
class PlannedChapter:
    """
    Chapitre produit par le Planner.
    """

    name: str
    editorial_order: int
    topics: list[PlannedTopic]


@dataclass(slots=True)
class PlannedFamily:
    """
    Famille complète produite par le Planner.
    """

    name: str
    chapters: list[PlannedChapter]


# ==========================================================
# Writer
# ==========================================================


@dataclass(slots=True)
class WrittenTopic:
    """
    Topic entièrement rédigé par le Writer.
    """

    id: str

    title: str

    summary: str

    description: str

    keywords: list[str]

    vocabulary: list[str]

    examples: list[str]

    legal_sources: list[str]

    # Hash du prompt ayant servi à générer ce fichier.
    # Utilisé pour savoir si une régénération est nécessaire.
    prompt_hash: str | None = None
    