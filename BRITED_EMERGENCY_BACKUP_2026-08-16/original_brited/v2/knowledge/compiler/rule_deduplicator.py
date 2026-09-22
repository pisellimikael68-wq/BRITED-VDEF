from collections.abc import Iterable

from v2.knowledge.compiler.canonical_fingerprint import (
    CanonicalRuleFingerprintBuilder,
)
from v2.knowledge.compiler.canonical_models import (
    CanonicalRule,
)


class RuleDeduplicator:
    """
    Déduplique des règles canoniques de manière
    entièrement déterministe.

    Deux règles sont considérées comme identiques
    uniquement lorsque leur fingerprint canonique
    est identique.

    Le fingerprint ne dépend pas de l'identifiant
    documentaire de la règle.

    Lorsque plusieurs règles identiques possèdent
    des identifiants différents, la règle dont
    l'identifiant est lexicographiquement le plus
    petit est conservée.

    Aucune similarité textuelle et aucun appel LLM
    n'interviennent.
    """

    def deduplicate(
        self,
        rules: Iterable[CanonicalRule],
    ) -> list[CanonicalRule]:
        """
        Retourne les règles canoniques uniques dans
        un ordre stable.
        """

        unique_by_fingerprint: dict[
            str,
            CanonicalRule,
        ] = {}

        for rule in rules:

            fingerprint = (
                CanonicalRuleFingerprintBuilder.build(
                    rule
                )
            )

            existing = unique_by_fingerprint.get(
                fingerprint
            )

            if existing is None:

                unique_by_fingerprint[
                    fingerprint
                ] = rule

                continue

            unique_by_fingerprint[
                fingerprint
            ] = self._select_stable_rule(
                existing,
                rule,
            )

        return sorted(
            unique_by_fingerprint.values(),
            key=self._sort_key,
        )

    @staticmethod
    def _select_stable_rule(
        first: CanonicalRule,
        second: CanonicalRule,
    ) -> CanonicalRule:
        """
        Sélectionne un représentant stable lorsque
        deux règles ont le même fingerprint.
        """

        if second.id < first.id:
            return second

        return first

    @staticmethod
    def _sort_key(
        rule: CanonicalRule,
    ) -> tuple[str, str, str, str, str]:
        """
        Clé de tri stable.
        """

        return (
            rule.family,
            rule.chapter,
            rule.rule_type,
            rule.statement,
            rule.id,
        )