from v2.agents.models import PlannedFamily


class ArchitectAgent:
    """
    Responsable de la conception
    pédagogique d'une famille.
    """

    def design(
        self,
        family_name: str,
    ) -> PlannedFamily:

        return PlannedFamily(
            pillar="epargne",
            name=family_name,
        )
    