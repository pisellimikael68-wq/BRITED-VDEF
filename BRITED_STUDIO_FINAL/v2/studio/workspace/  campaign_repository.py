"""
BRITED Campaign Repository

Responsable du stockage local des campagnes.
"""

import json
from pathlib import Path

from v2.studio.models.campaign_bundle import CampaignBundle
from v2.studio.workspace.storage import (
    CAMPAIGNS,
    initialize_workspace,
)


class CampaignRepository:

    def __init__(self):

        initialize_workspace()

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(
        self,
        name: str,
        bundle: CampaignBundle,
    ) -> Path:

        path = CAMPAIGNS / f"{name}.json"

        with open(path, "w", encoding="utf-8") as file:

            json.dump(
                bundle,
                file,
                default=lambda o: o.__dict__,
                indent=4,
                ensure_ascii=False,
            )

        return path

    # ==========================================================
    # LIST
    # ==========================================================

    def list_campaigns(
        self,
    ) -> list[str]:

        return sorted(

            file.stem

            for file in CAMPAIGNS.glob("*.json")

        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        name: str,
    ) -> None:

        path = CAMPAIGNS / f"{name}.json"

        if path.exists():

            path.unlink()

            