from dataclasses import dataclass, field


@dataclass(
    frozen=True
)
class RuleSeed:
    """
    Noyau documentaire déterministe d'une règle métier.

    Le primary_anchor définit l'identité stable
    de la règle.

    Les supporting_anchors apportent uniquement
    du contexte documentaire complémentaire.
    """

    source_id: str

    primary_anchor: str

    primary_content: str

    supporting_anchors: list[str] = field(
        default_factory=list
    )

    supporting_contents: list[str] = field(
        default_factory=list
    )

    @property
    def stable_id(
        self,
    ) -> str:

        return (
            f"{self.source_id}"
            f"::{self.primary_anchor}"
        )
    