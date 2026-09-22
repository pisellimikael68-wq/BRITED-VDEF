from v2.knowledge.compiler.rule_seed import (
    RuleSeed,
)


class SeedStatementPolicy:
    """
    Produit le statement canonique d'un RuleSeed.

    Aucune reformulation n'est effectuée.

    Le statement est simplement le fragment primaire
    normalisé afin de garantir un résultat
    parfaitement déterministe.
    """

    def build(
        self,
        seed: RuleSeed,
    ) -> str:

        return self._normalize(
            seed.primary_content
        )

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:
        """
        Normalisation légère.

        Aucun mot n'est modifié.
        """

        return " ".join(
            value.strip()
            .replace("’", "'")
            .replace("\u00a0", " ")
            .replace("\n", " ")
            .replace("\t", " ")
            .split()
        )
    