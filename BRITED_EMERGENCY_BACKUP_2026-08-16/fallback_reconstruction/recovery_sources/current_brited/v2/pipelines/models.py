from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class GenerationError:
    """
    Représente une erreur survenue lors de la génération
    d'un topic.
    """

    topic_id: str

    message: str

    error_type: str = ""

    chapter: str = ""


@dataclass(slots=True)
class GenerationReport:
    """
    Rapport de génération d'un pipeline.
    """

    generated_files: list[Path] = field(default_factory=list)

    errors: list[GenerationError] = field(default_factory=list)

    skipped: int = 0

    started_at: datetime | None = None

    finished_at: datetime | None = None

    @property
    def generated(self) -> int:
        return len(self.generated_files)

    @property
    def failed(self) -> int:
        return len(self.errors)

    @property
    def duration(self):
        """
        Durée totale de génération.
        """

        if (
            self.started_at is None
            or self.finished_at is None
        ):
            return None

        return self.finished_at - self.started_at

    @property
    def duration_seconds(self) -> float:
        """
        Durée totale en secondes.
        """

        if self.duration is None:
            return 0.0

        return self.duration.total_seconds()

    def _format_duration(self) -> str:
        if self.duration is None:
            return "-"

        total = int(self.duration_seconds)

        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60

        if hours:
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        return f"{minutes:02}:{seconds:02}"

    def __str__(self) -> str:
        lines = [
            "",
            "=" * 60,
            "BRITED REPORT",
            "=" * 60,
            "",
            f"Topics générés : {self.generated}",
            f"Topics ignorés : {self.skipped}",
            f"Topics en erreur : {self.failed}",
            "",
            f"Durée : {self._format_duration()}",
        ]

        if self.errors:
            lines.extend(
                [
                    "",
                    "ERREURS",
                    "-" * 60,
                ]
            )

            for error in self.errors:
                location = error.topic_id

                if error.chapter:
                    location = f"{error.chapter} / {error.topic_id}"

                lines.extend(
                    [
                        location,
                        f"Type : {error.error_type or 'Erreur inconnue'}",
                        f"Message : {error.message}",
                        "",
                    ]
                )

        return "\n".join(lines)
        