import hashlib
import re
import unicodedata

from v2.knowledge.compiler.models import (
    CompiledRule,
)


class RuleFingerprintBuilder:
    """
    Construit une empreinte déterministe pour une règle compilée.

    L'empreinte repose sur la structure métier extraite
    et non sur l'identifiant libre produit par le LLM.
    """

    @classmethod
    def build(
        cls,
        *,
        family: str,
        chapter: str,
        rule: CompiledRule,
    ) -> str:

        components = [
            cls._normalize(family),
            cls._normalize(chapter),
            cls._normalize(rule.rule_type.value),
        ]

        required_elements = sorted(
            {
                cls._normalize(value)
                for value in rule.required_elements
                if cls._normalize(value)
            }
        )

        conditions = sorted(
            {
                cls._normalize(value)
                for value in rule.conditions
                if cls._normalize(value)
            }
        )

        components.extend(required_elements)
        components.extend(conditions)

        canonical_value = "|".join(
            components
        )

        return hashlib.sha256(
            canonical_value.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:

        value = unicodedata.normalize(
            "NFKD",
            value.lower(),
        )

        value = "".join(
            character
            for character in value
            if not unicodedata.combining(character)
        )

        value = re.sub(
            r"[^a-z0-9]+",
            "_",
            value,
        )

        value = re.sub(
            r"_+",
            "_",
            value,
        )

        return value.strip("_")
    