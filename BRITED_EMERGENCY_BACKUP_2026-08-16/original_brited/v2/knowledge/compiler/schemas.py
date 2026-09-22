from typing import Literal

from pydantic import BaseModel, Field


class CompiledRuleSchema(BaseModel):
    """
    Règle extraite par le Knowledge Compiler.
    """

    id: str

    statement: str

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

    source_anchors: list[str] = Field(
        default_factory=list
    )

    conditions: list[str] = Field(
        default_factory=list
    )

    required_elements: list[str] = Field(
        default_factory=list
    )

    forbidden_interpretations: list[str] = Field(
        default_factory=list
    )

    legal_references: list[str] = Field(
        default_factory=list
    )


class CompiledKnowledgeSchema(BaseModel):
    """
    Sortie structurée du Knowledge Compiler.
    """

    rules: list[CompiledRuleSchema] = Field(
        default_factory=list
    )
    