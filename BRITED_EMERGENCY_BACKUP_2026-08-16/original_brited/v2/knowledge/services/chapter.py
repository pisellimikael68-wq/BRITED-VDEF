from dataclasses import dataclass
from datetime import datetime

from v2.knowledge.services.chapter_status import ChapterStatus


@dataclass(frozen=True)
class Chapter:
    """
    Représente un chapitre du corpus compilé.

    Cet objet est utilisé par BRITED Studio
    pour piloter la production du corpus.
    """

    family: str

    name: str

    status: ChapterStatus

    rules: int

    legal_references: int

    source_anchors: int

    compiled_at: datetime | None = None
    