from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from v2.studio.models.brand_strategy import BrandStrategy


# ==========================================================
# ENUMS
# ==========================================================

class CampaignType(Enum):
    EVERGREEN = "evergreen"
    SEASONAL = "seasonal"
    PRODUCT = "product"
    EVENT = "event"
    THEMATIC = "thematic"


class CampaignIntent(Enum):
    EDUCATE = "educate"
    ACQUIRE = "acquire"
    AUTHORITY = "authority"
    CONVERT = "convert"
    RETENTION = "retention"


class CampaignStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# ==========================================================
# OBJECTS
# ==========================================================

@dataclass(frozen=True)
class CampaignGoal:
    title: str
    description: str
    target_value: Optional[int] = None
    metric: Optional[str] = None


@dataclass(frozen=True)
class CampaignScope:
    families: list[str] = field(default_factory=list)
    chapters: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)


# ==========================================================
# CAMPAIGN
# ==========================================================

@dataclass(frozen=True)
class Campaign:

    id: str

    name: str

    description: str

    strategy: BrandStrategy

    campaign_type: CampaignType

    intent: CampaignIntent

    goal: CampaignGoal

    scope: CampaignScope

    duration_weeks: int

    priority: int = 5

    status: CampaignStatus = CampaignStatus.DRAFT

    version: int = 1

    def validate(self):

        if not self.id:
            raise ValueError("Campaign.id is required.")

        if not self.name:
            raise ValueError("Campaign.name is required.")

        if self.duration_weeks <= 0:
            raise ValueError("duration_weeks must be > 0.")

        if not (
            self.scope.families
            or self.scope.chapters
            or self.scope.topics
        ):
            raise ValueError(
                "Campaign scope cannot be empty."
            )

        self.strategy.validate()
        