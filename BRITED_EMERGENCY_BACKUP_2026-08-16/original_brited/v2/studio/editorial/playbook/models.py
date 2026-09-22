from dataclasses import dataclass, field

from v2.studio.editorial.editorial_types import (
    AnalogyType,
    CTAObjective,
    Emotion,
    EditorialAngle,
    HookCategory,
    HookObjective,
    Persuasion,
    TransitionType,
)


# ==========================================================
# HOOK
# ==========================================================

@dataclass(frozen=True)
class Hook:
    id: str
    title: str
    text: str

    category: HookCategory
    objective: HookObjective
    emotion: Emotion
    persuasion: Persuasion

    intensity: int

    suitable_angles: list[EditorialAngle] = field(default_factory=list)
    suitable_formats: list[str] = field(default_factory=list)
    suitable_levels: list[str] = field(default_factory=list)
    suitable_platforms: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)


# ==========================================================
# CTA
# ==========================================================

@dataclass(frozen=True)
class CTA:
    id: str
    title: str
    text: str

    objective: CTAObjective
    emotion: Emotion
    intensity: int

    suitable_formats: list[str] = field(default_factory=list)
    suitable_platforms: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


# ==========================================================
# TRANSITION
# ==========================================================

@dataclass(frozen=True)
class Transition:
    id: str
    text: str

    transition_type: TransitionType
    emotion: Emotion

    suitable_angles: list[EditorialAngle] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


# ==========================================================
# ANALOGY
# ==========================================================

@dataclass(frozen=True)
class Analogy:
    id: str
    concept: str
    text: str
    explanation: str

    analogy_type: AnalogyType
    level: str

    tags: list[str] = field(default_factory=list)
    