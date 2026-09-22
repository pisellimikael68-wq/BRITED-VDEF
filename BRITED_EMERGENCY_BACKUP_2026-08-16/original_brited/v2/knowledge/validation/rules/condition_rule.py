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


class ConditionRule(ValidationRule):
    """
    Vérifie que chaque règle possède
    au moins une condition d'application.
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

            if rule.conditions:
                continue

            report.add(
                ValidationIssue(
                    code="CONDITION_MISSING",
                    title="Condition absente",
                    description=(
                        "La règle ne possède aucune "
                        "condition d'application."
                    ),
                    severity=ValidationSeverity.WARNING,
                    rule_index=index,
                )
            )
            