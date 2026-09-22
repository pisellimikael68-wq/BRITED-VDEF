from dataclasses import dataclass

from v2.knowledge.validation.validation_severity import (
    ValidationSeverity,
)


@dataclass(frozen=True)
class ValidationIssue:
    """
    Représente une anomalie détectée
    lors de la validation d'un chapitre.
    """

    code: str

    title: str

    description: str

    severity: ValidationSeverity

    rule_index: int | None = None
    