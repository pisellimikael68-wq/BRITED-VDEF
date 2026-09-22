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


class ForbiddenInterpretationRule(ValidationRule):
    """
    Vérifie que chaque règle possède
    des interprétations interdites.

    Une issue de test temporaire est ajoutée
    afin de vérifier le fonctionnement
    du niveau de sévérité INFO.
    """

    def validate(
        self,
        knowledge,
        report: ValidationReport,
    ) -> None:
        """
        Ajoute temporairement une issue INFO,
        puis vérifie les interprétations interdites
        de chaque règle du corpus.
        """

        for index, rule in enumerate(
            knowledge.rules,
            start=1,
        ):
            if rule.forbidden_interpretations:
                continue

            report.add(
                ValidationIssue(
                    code="FORBIDDEN_INTERPRETATION_MISSING",
                    title="Interprétation interdite absente",
                    description=(
                        "La règle ne contient aucune "
                        "interprétation interdite."
                    ),
                    severity=ValidationSeverity.INFO,
                    rule_index=index,
                )
            )
