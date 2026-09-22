from dataclasses import dataclass, field
from enum import StrEnum


class RuleType(StrEnum):
    """
    Types génériques de règles Knowledge.
    """

    FORMULA = "formula"
    TAX_RATE = "tax_rate"
    THRESHOLD = "threshold"
    SENSITIVE_DATE = "sensitive_date"
    CONDITION = "condition"
    EXCEPTION = "exception"
    LEGAL_RULE = "legal_rule"
    DEFINITION = "definition"
    OTHER = "other"


class RuleSeverity(StrEnum):
    """
    Niveau de sensibilité d'une règle.
    """

    CRITICAL = "critical"
    HIGH = "high"
    STANDARD = "standard"


@dataclass(slots=True, frozen=True)
class CompiledRule:
    """
    Règle structurée produite par le Knowledge Compiler.

    Les source_anchors identifient les fragments exacts
    du corpus académique utilisés pour extraire la règle.
    """

    id: str

    statement: str

    rule_type: RuleType

    severity: RuleSeverity = RuleSeverity.STANDARD

    source_anchors: list[str] = field(
        default_factory=list
    )

    conditions: list[str] = field(
        default_factory=list
    )

    required_elements: list[str] = field(
        default_factory=list
    )

    forbidden_interpretations: list[str] = field(
        default_factory=list
    )

    legal_references: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True, frozen=True)
class CompiledKnowledge:
    """
    Résultat de compilation d'un bloc Knowledge.
    """

    source_id: str

    family: str

    chapter: str

    rules: list[CompiledRule] = field(
        default_factory=list
    )

    def critical_rules(self) -> list[CompiledRule]:

        return [
            rule
            for rule in self.rules
            if rule.severity == RuleSeverity.CRITICAL
        ]
    