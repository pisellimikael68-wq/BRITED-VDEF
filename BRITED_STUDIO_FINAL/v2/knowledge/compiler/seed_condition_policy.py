from v2.knowledge.compiler.rule_seed import (
    RuleSeed,
)


class SeedConditionPolicy:
    """
    Produit les conditions déterministes lorsqu'elles
    sont déjà présentes dans le RuleSeed.

    À ce stade, la politique est volontairement simple :
    elle ne tente pas d'inférer de nouvelles conditions.
    """

    def build(
        self,
        seed: RuleSeed,
    ) -> list[str]:

        conditions: list[str] = []

        primary = seed.primary_content.lower()

        if "rachat total" in primary:
            conditions.append(
                "Le rachat doit être total."
            )

        if "rachat partiel" in primary:
            conditions.append(
                "Le rachat doit être partiel."
            )

        if "plus de huit ans" in primary:
            conditions.append(
                "Le contrat doit avoir plus de huit ans au moment du rachat."
            )

        if "moins de huit ans" in primary:
            conditions.append(
                "Le contrat doit avoir moins de huit ans au moment du rachat."
            )

        if "27 septembre 2017" in primary:
            conditions.append(
                "Les primes doivent avoir été versées à compter du 27 septembre 2017."
            )

        return conditions
    