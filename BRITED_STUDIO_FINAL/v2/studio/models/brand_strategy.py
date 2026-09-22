from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class CreatorType(Enum):
    CGP = "cgp"
    PRIVATE_BANK = "private_bank"
    FAMILY_OFFICE = "family_office"
    NOTARY = "notary"
    LAWYER = "lawyer"
    ACCOUNTANT = "accountant"
    REAL_ESTATE = "real_estate"
    OTHER = "other"


class EditorialArchetype(Enum):
    PEDAGOGUE = "pedagogue"
    EXPERT = "expert"
    PREMIUM_ADVISOR = "premium_advisor"
    VULGARIZER = "vulgarizer"
    STRATEGIST = "strategist"
    ACADEMIC = "academic"


class AudienceSegment(Enum):
    YOUNG_ACTIVE = "young_active"
    FAMILY = "family"
    RETIREE = "retiree"
    ENTREPRENEUR = "entrepreneur"
    LIBERAL_PROFESSION = "liberal_profession"
    EXPAT = "expat"
    HNWI = "hnwi"
    GENERAL_PUBLIC = "general_public"


class AudienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Platform(Enum):
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    NEWSLETTER = "newsletter"


@dataclass(frozen=True)
class Identity:
    creator_type: CreatorType
    business_name: Optional[str]
    activity: str
    location: Optional[str] = None


@dataclass(frozen=True)
class EditorialIdentity:
    archetype: EditorialArchetype
    positioning: str
    promise: str
    values: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BusinessGoals:
    notoriety: int = 25
    authority: int = 25
    acquisition: int = 25
    loyalty: int = 25

    def validate(self) -> None:
        total = self.notoriety + self.authority + self.acquisition + self.loyalty
        if total != 100:
            raise ValueError(f"BusinessGoals must total 100, got {total}.")


@dataclass(frozen=True)
class AudienceProfile:
    segments: list[AudienceSegment]
    level: AudienceLevel
    language: str = "fr"


@dataclass(frozen=True)
class ToneProfile:
    pedagogy: int = 90
    expertise: int = 80
    storytelling: int = 60
    emotion: int = 30
    humour: int = 5
    provocation: int = 0

    def validate(self) -> None:
        scores = {
            "pedagogy": self.pedagogy,
            "expertise": self.expertise,
            "storytelling": self.storytelling,
            "emotion": self.emotion,
            "humour": self.humour,
            "provocation": self.provocation,
        }

        for name, value in scores.items():
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be between 0 and 100, got {value}.")


@dataclass(frozen=True)
class PublishingProfile:
    platforms: list[Platform]
    posts_per_week: int
    duration_weeks: int

    def validate(self) -> None:
        if self.posts_per_week <= 0:
            raise ValueError("posts_per_week must be greater than 0.")
        if self.duration_weeks <= 0:
            raise ValueError("duration_weeks must be greater than 0.")
        if not self.platforms:
            raise ValueError("At least one platform is required.")


@dataclass(frozen=True)
class EditorialPreferences:
    preferred_families: list[str] = field(default_factory=list)
    preferred_chapters: list[str] = field(default_factory=list)
    excluded_families: list[str] = field(default_factory=list)
    excluded_chapters: list[str] = field(default_factory=list)
    excluded_topics: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AIProfile:
    avoid_clickbait: bool = True
    always_use_examples: bool = True
    never_give_personal_advice: bool = True
    explain_with_nuance: bool = True
    preferred_length: str = "medium"


@dataclass(frozen=True)
class BrandStrategy:
    id: str
    name: str
    description: str

    identity: Identity
    editorial_identity: EditorialIdentity
    business_goals: BusinessGoals
    audience: AudienceProfile
    tone: ToneProfile
    publishing: PublishingProfile
    preferences: EditorialPreferences = field(default_factory=EditorialPreferences)
    ai_profile: AIProfile = field(default_factory=AIProfile)

    version: int = 1

    def validate(self) -> None:
        if not self.id:
            raise ValueError("BrandStrategy.id is required.")
        if not self.name:
            raise ValueError("BrandStrategy.name is required.")

        self.business_goals.validate()
        self.tone.validate()
        self.publishing.validate()
        