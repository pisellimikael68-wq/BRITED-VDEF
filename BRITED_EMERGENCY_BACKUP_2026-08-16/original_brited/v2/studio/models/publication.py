from dataclasses import dataclass, field

from v2.models.knowledge_models import Topic

from v2.studio.editorial.editorial_types import EditorialAngle
from v2.studio.editorial.editorial_patterns import EditorialPattern


@dataclass
class Publication:
    """
    Représente une publication éditoriale générée à partir d'un Topic.
    """

    # ==========================================================
    # SOURCE
    # ==========================================================

    topic: Topic

    # ==========================================================
    # ÉDITORIAL
    # ==========================================================

    angle: EditorialAngle

    pattern: EditorialPattern

    format: str

    title: str

    hook: str

    objective: str

    structure: list[str] = field(default_factory=list)

    call_to_action: str = ""

    # ==========================================================
    # SCRIPT
    # ==========================================================

    script: str | None = None
    