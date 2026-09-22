from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class SeedCompiledRuleSchema(BaseModel):
    """
    Enrichissement d'un RuleSeed.

    Les éléments déterministes (statement,
    rule_type, severity et conditions)
    sont calculés hors LLM.

    Le LLM complète uniquement les informations
    difficiles à inférer automatiquement.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    required_elements: list[str] = Field(
        default_factory=list,
    )

    forbidden_interpretations: list[str] = Field(
        default_factory=list,
    )

    legal_references: list[str] = Field(
        default_factory=list,
    )
    