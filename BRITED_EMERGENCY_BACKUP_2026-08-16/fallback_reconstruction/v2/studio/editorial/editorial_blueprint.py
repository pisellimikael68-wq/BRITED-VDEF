"""
BRITED Editorial Blueprint

Représente le plan éditorial complet d'une publication.

Tous les composants sont sélectionnés avant la génération du script.
"""

from dataclasses import dataclass

from v2.models.knowledge_models import Topic
from v2.studio.editorial.playbook.models import (
    Analogy,
    CTA,
    Hook,
    Transition,
)


@dataclass(frozen=True)
class EditorialBlueprint:
    """
    Plan éditorial complet d'une publication.
    """

    topic: Topic

    hook: Hook

    transition: Transition | None

    analogy: Analogy | None

    cta: CTA
    