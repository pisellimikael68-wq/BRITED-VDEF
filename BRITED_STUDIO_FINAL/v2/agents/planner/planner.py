from v2.agents.models import PlannedFamily
from v2.planning.markdown_plan_loader import MarkdownPlanLoader


class PlannerAgent:
    """
    Responsable de la planification éditoriale.

    Il transforme un plan Markdown en objets métier.
    """

    def __init__(self):

        self.loader = MarkdownPlanLoader()

    def plan(
        self,
        *,
        family: str,
    ) -> PlannedFamily:

        return self.loader.load(family)
    