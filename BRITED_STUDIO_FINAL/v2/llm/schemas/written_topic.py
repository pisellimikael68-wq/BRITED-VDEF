from pydantic import Field, field_validator

from .base import LLMResponse


class WrittenTopicSchema(LLMResponse):
    """
    Réponse structurée renvoyée par le LLM.
    """

    title: str

    summary: str = ""

    description: str

    keywords: list[str] = Field(default_factory=list)

    vocabulary: list[str] = Field(default_factory=list)

    examples: list[str] = Field(default_factory=list)

    legal_sources: list[str] = Field(default_factory=list)

    @field_validator("keywords", mode="before")
    @classmethod
    def normalize_keywords(cls, value):
        return cls._normalize_list(value)

    @field_validator("vocabulary", mode="before")
    @classmethod
    def normalize_vocabulary(cls, value):
        return cls._normalize_list(value)

    @field_validator("examples", mode="before")
    @classmethod
    def normalize_examples(cls, value):
        return cls._normalize_list(value)

    @field_validator("legal_sources", mode="before")
    @classmethod
    def normalize_legal_sources(cls, value):
        return cls._normalize_list(value)

    @staticmethod
    def _normalize_list(value) -> list[str]:

        if value is None:
            return []

        if not isinstance(value, list):
            return [str(value)]

        normalized: list[str] = []

        for item in value:

            if isinstance(item, str):
                normalized.append(item)
                continue

            if isinstance(item, dict):

                if "term" in item and "definition" in item:
                    normalized.append(
                        f"{item['term']} : {item['definition']}"
                    )
                    continue

                if "description" in item:
                    normalized.append(str(item["description"]))
                    continue

                if "example" in item:
                    normalized.append(str(item["example"]))
                    continue

                if "reference" in item and "description" in item:
                    normalized.append(
                        f"{item['reference']} : {item['description']}"
                    )
                    continue

                if "reference" in item:
                    normalized.append(str(item["reference"]))
                    continue

                normalized.append(
                    " - ".join(str(v) for v in item.values())
                )
                continue

            normalized.append(str(item))

        return normalized
    