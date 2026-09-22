from dataclasses import dataclass, field
from typing import List


@dataclass
class Knowledge:
    definitions: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)
    taxation: List[str] = field(default_factory=list)
    mistakes: List[str] = field(default_factory=list)

    # NOUVEAU
    misconceptions: List[str] = field(default_factory=list)
    frequently_asked_questions: List[str] = field(default_factory=list)

    analogies: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)


@dataclass
class Angle:
    title: str
    description: str
    score: int


@dataclass
class Script:
    title: str
    hook: str
    body: str
    cta: str
    references: List[str] = field(default_factory=list)


@dataclass
class Review:

    # Score global
    score: int

    # Scores détaillés
    patrimonial_score: int = 0
    pedagogy_score: int = 0
    instagram_score: int = 0
    hook_score: int = 0
    cta_score: int = 0
    compliance_score: int = 0
    credibility_score: int = 0
    virality_score: int = 0

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)

    rewrite_needed: bool = False
    rewrite_instructions: List[str] = field(default_factory=list)


@dataclass
class AngleCandidate:
    title: str
    description: str
    score: int