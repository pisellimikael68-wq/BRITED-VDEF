"""
BRITED Editorial Playbook

Hooks Repository

Contient l'ensemble des Hooks éditoriaux utilisés par le HookEngine.
"""

from v2.studio.editorial.playbook.models import Hook

from v2.studio.editorial.editorial_types import (
    EditorialAngle,
    Emotion,
    HookCategory,
    HookObjective,
    Persuasion,
)

# ==========================================================
# HOOKS
# ==========================================================

HOOKS: list[Hook] = [

    # ======================================================
    # MYTH
    # ======================================================

    Hook(

        id="myth_001",

        title="Assurance-vie ≠ assurance décès",

        text="La plupart des Français pensent que l'assurance-vie sert uniquement en cas de décès.",

        category=HookCategory.MYTH,

        objective=HookObjective.CORRECT_BELIEF,

        emotion=Emotion.SURPRISE,

        persuasion=Persuasion.AUTHORITY,

        intensity=8,

        suitable_angles=[
            EditorialAngle.MYTH,
        ],

        suitable_formats=[
            "carousel",
            "reel",
        ],

        suitable_levels=[
            "beginner",
        ],

        suitable_platforms=[
            "instagram",
            "linkedin",
        ],

        tags=[
            "assurance_vie",
        ],
    ),

    # ======================================================
    # QUESTION
    # ======================================================

    Hook(

        id="question_001",

        title="Comprendre l'assurance-vie",

        text="Savez-vous réellement comment fonctionne une assurance-vie ?",

        category=HookCategory.QUESTION,

        objective=HookObjective.CREATE_CURIOSITY,

        emotion=Emotion.CURIOSITY,

        persuasion=Persuasion.LOGIC,

        intensity=6,

        suitable_angles=[
            EditorialAngle.QUESTION,
            EditorialAngle.EXPLANATION,
            EditorialAngle.FAQ,
        ],

        suitable_formats=[
            "carousel",
            "reel",
        ],

        suitable_levels=[
            "beginner",
        ],

        suitable_platforms=[
            "instagram",
            "linkedin",
        ],

        tags=[
            "assurance_vie",
        ],
    ),

]
