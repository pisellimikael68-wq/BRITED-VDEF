import re

from v2.knowledge.compiler.models import (
    RuleSeverity,
    RuleType,
)
from v2.knowledge.compiler.rule_seed import (
    RuleSeed,
)


class SeedSeverityPolicy:
    """
    Politique déterministe d'attribution de la sévérité.

    La sévérité représente le risque métier
    associé à une mauvaise restitution d'une règle.

    Aucun appel LLM.
    """

    CRITICAL_TYPES = {
        RuleType.FORMULA,
        RuleType.TAX_RATE,
        RuleType.SENSITIVE_DATE,
    }

    HIGH_TYPES = {
        RuleType.THRESHOLD,
        RuleType.CONDITION,
        RuleType.EXCEPTION,
        RuleType.LEGAL_RULE,
    }

    CRITICAL_PATTERNS = (
        r"\b\d+(?:[.,]\d+)?\s*%",
        r"\b\d{1,3}(?:\s\d{3})+\s*€?",
        r"\b\d{1,3}(?:\s\d{3})+\s*euros?",
        r"\b\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}",
        r"\b31 décembre\b",
    )

    HIGH_PATTERNS = (
        r"\bdoit\b",
        r"\bsous réserve\b",
        r"\bà condition\b",
        r"\bsauf\b",
        r"\buniquement\b",
        r"\bexclusivement\b",
    )

    def classify(
        self,
        *,
        seed: RuleSeed,
        rule_type: RuleType,
    ) -> RuleSeverity:

        text = self._normalize(
            seed.primary_content
        )

        if rule_type in self.CRITICAL_TYPES:
            return RuleSeverity.CRITICAL

        if self._matches_any(
            text,
            self.CRITICAL_PATTERNS,
        ):
            return RuleSeverity.CRITICAL

        if rule_type in self.HIGH_TYPES:
            return RuleSeverity.HIGH

        if self._matches_any(
            text,
            self.HIGH_PATTERNS,
        ):
            return RuleSeverity.HIGH

        return RuleSeverity.STANDARD

    @staticmethod
    def _matches_any(
        text: str,
        patterns: tuple[str, ...],
    ) -> bool:

        return any(
            re.search(
                pattern,
                text,
            )
            is not None
            for pattern in patterns
        )

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:

        return " ".join(
            value.lower()
            .replace("’", "'")
            .replace("\n", " ")
            .split()
        )
    