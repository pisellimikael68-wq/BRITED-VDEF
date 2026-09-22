"""
BRITED Campaign Serializer

Conversion entre CampaignSnapshot et JSON.
"""

import json
from dataclasses import asdict
from pathlib import Path

from v2.studio.models.campaign_snapshot import (
    CampaignSnapshot,
    ScriptSnapshot,
)


class CampaignSerializer:

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(
        self,
        snapshot: CampaignSnapshot,
        path: Path,
    ) -> None:

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(

                asdict(snapshot),

                file,

                indent=4,

                ensure_ascii=False,

            )

    # ==========================================================
    # LOAD
    # ==========================================================

    def load(
        self,
        path: Path,
    ) -> CampaignSnapshot:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        scripts = [

            ScriptSnapshot(**script)

            for script in data["scripts"]

        ]

        return CampaignSnapshot(

            name=data["name"],

            family=data["family"],

            weeks=data["weeks"],

            scripts=scripts,

        )

        