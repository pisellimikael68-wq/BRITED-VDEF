from dataclasses import dataclass, field


@dataclass(slots=True)
class RawTopic:
    """
    Représente une ligne lue dans un fichier Markdown.
    """

    id: str
    title: str
    editorial_order: int
    difficulty: str
    priority: int


@dataclass(slots=True)
class RawChapter:
    """
    Représente un chapitre Markdown complet.
    """

    pillar: str
    family: str
    chapter: str

    topics: list[RawTopic] = field(default_factory=list)
    