from pydantic import BaseModel, ConfigDict


class LLMResponse(BaseModel):
    """
    Classe de base de toutes les réponses structurées
    renvoyées par le LLM.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_assignment=True,
    )
    