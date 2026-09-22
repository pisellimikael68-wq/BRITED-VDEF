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


class SourceAnchorRule(ValidationRule):
    """
    Vérifie que chaque règle possède
    au moins une ancre de source.
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

            if rule.source_anchors:
                continue

            report.add(
                ValidationIssue(
                    code="SOURCE_ANCHOR_MISSING",
                    title="Ancre de source absente",
                    description=(
                        "La règle ne possède aucune "
                        "ancre de source."
                    ),
                    severity=ValidationSeverity.ERROR,
                    rule_index=index,
                )
            )
            