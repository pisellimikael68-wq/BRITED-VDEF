"""
BRITED Topic Template

Copiez ce modèle pour créer un nouveau Topic.

Tous les Topics de la Knowledge Base doivent
respecter cette structure.
"""

from v2.models.knowledge_models import Topic


TOPIC_TEMPLATE = Topic(

    # ==========================================================
    # IDENTITÉ
    # ==========================================================

    id="",

    title="",

    pillar="",

    family="",

    # ==========================================================
    # DESCRIPTION
    # ==========================================================

    description="",

    objective="",

    difficulty="Débutant",

    priority=10,

    # ==========================================================
    # CONTENU
    # ==========================================================

    keywords=[

    ],

    misconceptions=[

    ],

    client_questions=[

    ],

    common_mistakes=[

    ],

    analogies=[

    ],

    # ==========================================================
    # PÉDAGOGIE
    # ==========================================================

    key_points=[

    ],

    examples=[

    ],

    vocabulary=[

    ],

    # ==========================================================
    # ÉDITORIAL
    # ==========================================================

    recommended_formats=[

    ],

    # ==========================================================
    # RÉFÉRENCES
    # ==========================================================

    legal_sources=[

    ],

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    related_topics=[

    ],

)
