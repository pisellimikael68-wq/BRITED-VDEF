from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True, frozen=True)
class SourceDocument:
    """
    Représente un document source du corpus Knowledge.

    Ce modèle décrit la provenance d'un document.
    Il ne contient pas encore le texte extrait.
    """

    id: str
    title: str
    path: Path

    source_type: str
    origin: str

    academic_year: str = ""
    language: str = "fr"

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    def exists(self) -> bool:
        """
        Indique si le fichier source existe réellement.
        """

        return self.path.is_file()


@dataclass(slots=True, frozen=True)
class SourceChunk:
    """
    Représente un fragment textuel extrait d'un document source.
    """

    document_id: str
    text: str

    chunk_index: int

    page_start: int | None = None
    page_end: int | None = None

    metadata: dict[str, str] = field(
        default_factory=dict
    )
    