from abc import ABC, abstractmethod

from v2.knowledge.validation.validation_report import (
    ValidationReport,
)


class ValidationRule(ABC):
    """
    Contrat commun à toutes les règles
    de validation.
    """

    @abstractmethod
    def validate(
        self,
        knowledge,
        report: ValidationReport,
    ) -> None:
        """
        Analyse le chapitre et enrichit
        le rapport de validation.
        """
        ...
        