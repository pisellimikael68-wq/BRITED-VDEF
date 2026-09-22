from v2.knowledge.compiler.canonical_models import (
    CanonicalKnowledge,
    CanonicalRule,
)
from v2.knowledge.compiler.models import (
    CompiledKnowledge,
    CompiledRule,
)


class RuleCanonicalizer:
    """
    Transforme un CompiledKnowledge en représentation
    canonique entièrement déterministe.

    La canonicalisation ne modifie pas le sens métier
    des règles. Elle normalise uniquement :

    - la casse ;
    - les apostrophes ;
    - les espaces ;
    - l'ordre des collections ;
    - les doublons exacts après normalisation.

    Aucun appel LLM n'intervient.
    """

    def canonicalize(
        self,
        knowledge: CompiledKnowledge,
    ) -> CanonicalKnowledge:
        """
        Canonicalise toutes les règles d'un bloc compilé.
        """

        return CanonicalKnowledge(
            source_id=knowledge.source_id,
            family=knowledge.family,
            chapter=knowledge.chapter,
            rules=tuple(
                self._canonicalize_rule(
                    rule=rule,
                    family=knowledge.family,
                    chapter=knowledge.chapter,
                )
                for rule in knowledge.rules
            ),
        )

    def _canonicalize_rule(
        self,
        *,
        rule: CompiledRule,
        family: str,
        chapter: str,
    ) -> CanonicalRule:
        """
        Produit la représentation canonique d'une règle.

        L'identité stable de la CompiledRule est conservée.
        """

        return CanonicalRule(
            id=rule.id,
            family=self._normalize_identifier(
                family
            ),
            chapter=self._normalize_identifier(
                chapter
            ),
            rule_type=rule.rule_type.value,
            statement=self._normalize_text(
                rule.statement
            ),
            keywords=(),
            conditions=self._normalize_collection(
                rule.conditions
            ),
            required_elements=self._normalize_collection(
                rule.required_elements
            ),
            forbidden_interpretations=(
                self._normalize_collection(
                    rule.forbidden_interpretations
                )
            ),
            legal_references=self._normalize_collection(
                rule.legal_references
            ),
        )

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        """
        Normalise une formulation textuelle sans modifier
        son contenu métier.
        """

        normalized = (
            value.strip()
            .lower()
            .replace("’", "'")
            .replace("`", "'")
            .replace("\u00a0", " ")
            .replace("\n", " ")
            .replace("\t", " ")
        )

        return " ".join(
            normalized.split()
        )

    @classmethod
    def _normalize_collection(
        cls,
        values: list[str],
    ) -> tuple[str, ...]:
        """
        Normalise, déduplique et trie une collection.

        Le tri rend le résultat indépendant de l'ordre
        produit par le LLM.
        """

        normalized_values = {
            cls._normalize_text(value)
            for value in values
            if value.strip()
        }

        return tuple(
            sorted(normalized_values)
        )

    @staticmethod
    def _normalize_identifier(
        value: str,
    ) -> str:
        """
        Normalise un identifiant de famille ou chapitre.
        """

        normalized = (
            value.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        return "_".join(
            part
            for part in normalized.split("_")
            if part
        )
    