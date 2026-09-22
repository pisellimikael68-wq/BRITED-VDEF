from time import perf_counter

from v2.knowledge.validation.rules import (
    ValidationRule,
)
from v2.knowledge.validation.validation_registry import (
    VALIDATION_RULES,
)
from v2.knowledge.validation.validation_report import (
    ValidationReport,
)


class Validator:
    """
    Exécute une série de règles de validation
    sur un chapitre compilé.
    """

    def __init__(
        self,
        rules: list[ValidationRule] | None = None,
    ) -> None:
        """
        Initialise le validateur.

        Si aucune liste de règles n'est fournie,
        les règles déclarées dans le ValidationRegistry
        sont automatiquement instanciées.
        """

        self.rules = (
            rules
            if rules is not None
            else [
                rule_class()
                for rule_class in VALIDATION_RULES
            ]
        )

    def validate(
        self,
        knowledge,
    ) -> ValidationReport:
        """
        Exécute toutes les règles de validation
        et retourne un rapport.
        """

        report = ValidationReport()

        start_time = perf_counter()

        for rule in self.rules:
            rule.validate(
                knowledge,
                report,
            )

        end_time = perf_counter()

        report.executed_rules = len(self.rules)
        report.execution_time = end_time - start_time

        return report
    