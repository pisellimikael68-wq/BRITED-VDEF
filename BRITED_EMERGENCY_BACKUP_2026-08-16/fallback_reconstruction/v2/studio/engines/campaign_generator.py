"""
BRITED Campaign Generator

Génère une campagne éditoriale complète.

Pipeline :

Campaign
    ↓
Planning
    ↓
Publications
    ↓
Scripts
    ↓
CampaignBundle
"""

from v2.studio.engines.campaign_engine import CampaignEngine
from v2.studio.engines.publication_engine import PublicationEngine
from v2.studio.engines.script_engine import ScriptEngine

from v2.studio.models.campaign import Campaign
from v2.studio.models.campaign_bundle import CampaignBundle


class CampaignGenerator:

    def __init__(self):

        self.campaign_engine = CampaignEngine()

        self.publication_engine = PublicationEngine()

        self.script_engine = ScriptEngine()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        campaign: Campaign,
    ) -> CampaignBundle:

        planning = self.campaign_engine.generate(
            campaign
        )

        publications = []

        scripts = []

        for week in planning.weeks:

            for topic in week.topics:

                publication = self.publication_engine.generate(
                    topic
                )

                script = self.script_engine.generate(
                    publication
                )

                publications.append(
                    publication
                )

                scripts.append(
                    script
                )

        return CampaignBundle(

            campaign=campaign,

            planning=planning,

            publications=publications,

            scripts=scripts,

        )

        