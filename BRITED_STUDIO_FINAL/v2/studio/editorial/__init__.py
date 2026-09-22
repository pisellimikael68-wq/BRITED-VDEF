from v2.studio.editorial.editorial_types import (
    EditorialAngle,
    Emotion,
    HookCategory,
    HookObjective,
    Persuasion,
)

from v2.studio.editorial.playbook.models import Hook


HOOKS = [

    Hook(

        id="myth_001",

        title="Idée reçue sur l'assurance-vie",

        text="La plupart des Français pensent que l'assurance-vie sert uniquement en cas de décès.",

        category=HookCategory.MYTH,

        objective=HookObjective.CORRECT_BELIEF,

        emotion=Emotion.SURPRISE,

        persuasion=Persuasion.LOGIC,

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

    Hook(

        id="faq_001",

        title="Question d'introduction",

        text="Savez-vous réellement comment fonctionne une assurance-vie ?",

        category=HookCategory.QUESTION,

        objective=HookObjective.CREATE_CURIOSITY,

        emotion=Emotion.CURIOSITY,

        persuasion=Persuasion.AUTHORITY,

        intensity=6,

        suitable_angles=[
            EditorialAngle.FAQ,
            EditorialAngle.EXPLANATION,
        ],

        suitable_formats=[
            "carousel",
        ],

        suitable_levels=[
            "beginner",
        ],

        suitable_platforms=[
            "instagram",
        ],

        tags=[
            "assurance_vie",
        ],

    ),

]
