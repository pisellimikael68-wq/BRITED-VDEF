from v2.knowledge.validation.rules.validation_rule import (
    ValidationRule,
)
from v2.knowledge.validation.validation_issue import (
    ValidationIssue,
)
from v2.knowledge.validation.validation_report import (
    ValidationReport,
)
from v2.knowledge.validation.validation_severity import (
    ValidationSeverity,
)


class RequiredElementRule(ValidationRule):
    """
    Vérifie que chaque règle possède
    des éléments obligatoires.
    """

    def validate(
        self,
        knowledge,
        report: ValidationReport,
    ) -> None:

        for index, rule in enumerate(
            knowledge.rules,
            start=1,
        ):

            if rule.required_elements:
                continue

            report.add(
                ValidationIssue(
                    code="REQUIRED_ELEMENTS_MISSING",
                    title="Éléments obligatoires absents",
                    description=(
                        "La règle ne contient aucun "
                        "élément obligatoire."
                    ),
                    severity=ValidationSeverity.INFO,
                    rule_index=index,
                )
            )
