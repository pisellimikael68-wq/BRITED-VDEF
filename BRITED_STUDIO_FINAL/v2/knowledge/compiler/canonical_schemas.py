from typing import Literal

from pydantic import BaseModel, Field


class CanonicalRuleSchema(BaseModel):
    """
    Règle métier normalisée sémantiquement.
    """

    source_rule_ids: list[str] = Field(
        default_factory=list
    )

    canonical_name: str

    rule_type: Literal[
        "formula",
        "tax_rate",
        "threshold",
        "sensitive_date",
        "condition",
        "exception",
        "legal_rule",
        "definition",
        "other",
    ]

    severity: Literal[
        "critical",
        "high",
        "standard",
    ]

    concepts: list[str] = Field(
        default_factory=list
    )

    conditions: list[str] = Field(
        default_factory=list
    )

    constraints: list[str] = Field(
        default_factory=list
    )

    legal_references: list[str] = Field(
        default_factory=list
    )


class CanonicalKnowledgeSchema(BaseModel):
    """
    Sortie du Semantic Rule Canonicalizer.
    """

    rules: list[CanonicalRuleSchema] = Field(
        default_factory=list
    )
    