from dataclasses import dataclass

from v2.studio.models.campaign import Campaign
from v2.studio.models.planning import Planning
from v2.studio.models.publication import Publication
from v2.studio.models.script import Script


@dataclass(frozen=True)
class CampaignBundle:
    """
    Représente une campagne éditoriale complète.

    Une campagne =

    - un Campaign
    - un Planning
    - toutes les Publications
    - tous les Scripts
    """

    campaign: Campaign

    planning: Planning

    publications: list[Publication]

    scripts: list[Script]

    