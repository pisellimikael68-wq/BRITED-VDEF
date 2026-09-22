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


class LegalReferenceRule(ValidationRule):
    """
    Vérifie que chaque règle possède
    au moins une référence légale.
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

            if rule.legal_references:
                continue

            report.add(
                ValidationIssue(
                    code="LEGAL_REFERENCE_MISSING",
                    title="Référence légale absente",
                    description=(
                        "La règle ne possède aucune "
                        "référence légale."
                    ),
                    severity=ValidationSeverity.ERROR,
                    rule_index=index,
                )
            )
            