from v2.studio.engines.planning_engine import PlanningEngine
from v2.studio.models.campaign import Campaign
from v2.studio.models.planning import Planning


class CampaignEngine:
    """
    Orchestre la génération d'une campagne éditoriale.
    """

    def __init__(self):

        self.planning_engine = PlanningEngine()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        campaign: Campaign,
    ) -> Planning:

        campaign.validate()

        planning = self.planning_engine.generate(
            family=campaign.scope.families[0],
            weeks=campaign.duration_weeks,
            posts_per_week=3,
        )

        return planning
    
    