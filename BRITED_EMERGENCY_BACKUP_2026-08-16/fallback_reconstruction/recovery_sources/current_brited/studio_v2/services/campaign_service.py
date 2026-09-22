"""
BRITED Studio Campaign Service

Service utilisé par l'interface Streamlit.
"""

from v2.studio.engines.campaign_generator import CampaignGenerator
from v2.studio.models.campaign import Campaign
from v2.studio.models.campaign_bundle import CampaignBundle


class CampaignService:

    def __init__(self):

        self.generator = CampaignGenerator()

    def create(
        self,
        campaign: Campaign,
    ) -> CampaignBundle:

        return self.generator.generate(campaign)

        