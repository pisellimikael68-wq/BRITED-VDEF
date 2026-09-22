"""
BRITED Editorial Context

Objet partagé entre tous les moteurs éditoriaux.

Il décrit le contexte dans lequel un contenu est généré.
"""

from dataclasses import dataclass

from v2.studio.editorial.editorial_types import EditorialAngle
from v2.studio.models.brand_strategy import (
    AudienceLevel,
    Platform,
)
from v2.studio.models.publication import (
    ContentFormat,
    PublicationObjective,
)


@dataclass(frozen=True)
class EditorialContext:
    """
    Contexte éditorial utilisé par tous les Engines.
    """

    platform: Platform

    format: ContentFormat

    objective: PublicationObjective

    audience: AudienceLevel

    angle: EditorialAngle

    duration_seconds: int = 60
    