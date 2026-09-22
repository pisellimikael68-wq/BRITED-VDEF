"""
BRITED Editorial Types

Ce fichier définit le langage officiel du moteur éditorial BRITED.

Tous les modèles, repositories et engines utilisent ces Enums.

Aucune logique métier ne doit être ajoutée ici.
"""

from enum import Enum


# ==========================================================
# ÉDITORIAL ANGLES
# ==========================================================

class EditorialAngle(Enum):
    EXPLANATION = "explanation"
    QUESTION = "question"
    MYTH = "myth"
    MISTAKE = "mistake"
    COMPARISON = "comparison"
    FAQ = "faq"
    STORY = "story"
    CASE_STUDY = "case_study"
    ALERT = "alert"
    EXPERT = "expert"
    REGULATION = "regulation"
    TRUE_FALSE = "true_false"
    TIMELINE = "timeline"
    STEP_BY_STEP = "step_by_step"
    DEEP_DIVE = "deep_dive"


# ==========================================================
# HOOKS
# ==========================================================

class HookCategory(Enum):
    QUESTION = "question"
    MYTH = "myth"
    STATISTIC = "statistic"
    AUTHORITY = "authority"
    STORY = "story"
    SURPRISE = "surprise"
    MISTAKE = "mistake"
    CURIOSITY = "curiosity"
    FEAR = "fear"
    OPPORTUNITY = "opportunity"
    CONTRAST = "contrast"
    PROJECTION = "projection"


# ==========================================================
# HOOK OBJECTIVES
# ==========================================================

class HookObjective(Enum):
    EDUCATE = "educate"
    ATTRACT = "attract"
    CORRECT_BELIEF = "correct_belief"
    CREATE_CURIOSITY = "create_curiosity"
    BUILD_AUTHORITY = "build_authority"
    START_STORY = "start_story"


# ==========================================================
# ÉMOTIONS
# ==========================================================

class Emotion(Enum):
    CURIOSITY = "curiosity"
    SURPRISE = "surprise"
    REASSURANCE = "reassurance"
    FEAR = "fear"
    CONFIDENCE = "confidence"
    HOPE = "hope"
    URGENCY = "urgency"
    SECURITY = "security"
    INSPIRATION = "inspiration"


# ==========================================================
# PERSUASION
# ==========================================================

class Persuasion(Enum):
    AUTHORITY = "authority"
    SOCIAL_PROOF = "social_proof"
    LOGIC = "logic"
    STORYTELLING = "storytelling"
    CONTRAST = "contrast"
    SCARCITY = "scarcity"
    RECIPROCITY = "reciprocity"
    SIMPLICITY = "simplicity"


# ==========================================================
# CTA
# ==========================================================

class CTAObjective(Enum):
    SAVE = "save"
    SHARE = "share"
    COMMENT = "comment"
    FOLLOW = "follow"
    CONTACT = "contact"
    NEWSLETTER = "newsletter"
    DOWNLOAD = "download"
    APPOINTMENT = "appointment"


# ==========================================================
# TRANSITIONS
# ==========================================================

class TransitionType(Enum):
    PEDAGOGY = "pedagogy"
    STORY = "story"
    CONTRAST = "contrast"
    QUESTION = "question"
    SUMMARY = "summary"
    EXAMPLE = "example"
    WARNING = "warning"


# ==========================================================
# STORY PATTERNS
# ==========================================================

class StoryPattern(Enum):
    PROBLEM_SOLUTION = "problem_solution"
    BEFORE_AFTER = "before_after"
    FALSE_BELIEF = "false_belief"
    FAQ = "faq"
    STEP_BY_STEP = "step_by_step"
    CASE_STUDY = "case_study"
    TIMELINE = "timeline"
    COMPARISON = "comparison"


# ==========================================================
# OPENINGS
# ==========================================================

class OpeningType(Enum):
    QUESTION = "question"
    STORY = "story"
    STATISTIC = "statistic"
    MYTH = "myth"
    SHOCK = "shock"
    QUOTE = "quote"


# ==========================================================
# CLOSINGS
# ==========================================================

class ClosingType(Enum):
    SUMMARY = "summary"
    CTA = "cta"
    PROJECTION = "projection"
    KEY_TAKEAWAY = "key_takeaway"
    QUESTION = "question"


# ==========================================================
# ANALOGIES
# ==========================================================

class AnalogyType(Enum):
    EVERYDAY_LIFE = "everyday_life"
    SPORT = "sport"
    HEALTH = "health"
    TRAVEL = "travel"
    COOKING = "cooking"
    CONSTRUCTION = "construction"
    NATURE = "nature"
    BUSINESS = "business"


# ==========================================================
# CONTENT INTENSITY
# ==========================================================

class ContentIntensity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


# ==========================================================
# PEDAGOGY LEVEL
# ==========================================================

class PedagogyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    
