from v2.studio.engines.campaign_engine import CampaignEngine

from v2.studio.models.campaign import (
    Campaign,
    CampaignGoal,
    CampaignIntent,
    CampaignScope,
    CampaignStatus,
    CampaignType,
)

from v2.studio.models.brand_strategy import BrandStrategy


def main():

    strategy = BrandStrategy(
        name="Leveria",
        mission="Education patrimoniale",
        vision="Rendre la gestion de patrimoine accessible",
    )

    campaign = Campaign(

        id="assurance_vie_instagram",

        name="Instagram Assurance-vie",

        description="Campagne Instagram Assurance-vie",

        strategy=strategy,

        campaign_type=CampaignType.EVERGREEN,

        intent=CampaignIntent.EDUCATE,

        goal=CampaignGoal(
            title="Eduquer",
            description="Construire une série pédagogique."
        ),

        scope=CampaignScope(
            families=["assurance_vie"]
        ),

        duration_weeks=8,

        status=CampaignStatus.DRAFT,
    )

    engine = CampaignEngine()

    planning = engine.generate(campaign)

    planning.display()


if __name__ == "__main__":
    main()

    