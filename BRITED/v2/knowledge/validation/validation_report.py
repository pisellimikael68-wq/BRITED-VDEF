from dataclasses import dataclass, field

from v2.knowledge.validation.validation_issue import (
    ValidationIssue,
)

from v2.knowledge.validation.validation_severity import (
    ValidationSeverity,
)


@dataclass
class ValidationReport:
    """
    Rapport de validation d'un chapitre.
    """

    issues: list[ValidationIssue] = field(
        default_factory=list
    )

    # Métadonnées d'exécution
    executed_rules: int = 0
    execution_time: float = 0.0

    def add(
        self,
        issue: ValidationIssue,
    ) -> None:

        self.issues.append(issue)

    @property
    def errors(self) -> list[ValidationIssue]:

        return [
            issue
            for issue in self.issues
            if issue.severity == ValidationSeverity.ERROR
        ]

    @property
    def warnings(self) -> list[ValidationIssue]:

        return [
            issue
            for issue in self.issues
            if issue.severity == ValidationSeverity.WARNING
        ]

    @property
    def infos(self) -> list[ValidationIssue]:

        return [
            issue
            for issue in self.issues
            if issue.severity == ValidationSeverity.INFO
        ]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def issue_count(self) -> int:
        return len(self.issues)

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def info_count(self) -> int:
        return len(self.infos)

    def summary(
        self,
        family: str,
        chapter: str,
    ) -> str:
        """
        Retourne un résumé textuel du rapport de validation.
        """

        return (
            "=== Validation Report ===\n"
            f"Famille             : {family}\n"
            f"Chapitre            : {chapter}\n"
            f"Valide              : {self.is_valid}\n"
            f"Nombre d'issues     : {self.issue_count}\n"
            f"Erreurs             : {self.error_count}\n"
            f"Avertissements      : {self.warning_count}\n"
            f"Informations        : {self.info_count}"
        )
    