from dataclasses import dataclass, field
from typing import Optional

from v2.models.content_models import (
    Knowledge,
    Angle,
    Script,
    Review,
)

from v2.models.editorial_models import (
    EditorialStrategy,
    EditorialContract,
)

from v2.models.editorial_brief import EditorialBrief


@dataclass
class BritedContext:

    subject: str

    # ==========================================
    # Knowledge Engine
    # ==========================================

    editorial_brief: Optional[EditorialBrief] = None

    knowledge: Optional[Knowledge] = None

    raw_knowledge: Optional[str] = None

    # ==========================================
    # Editorial Engine
    # ==========================================

    editorial: Optional[EditorialStrategy] = None

    editorial_contract: Optional[EditorialContract] = None

    # ==========================================
    # Creative Engine
    # ==========================================

    angles: list[Angle] = field(default_factory=list)

    selected_angle: Optional[Angle] = None

    # ==========================================
    # Production
    # ==========================================

    script: Optional[Script] = None

    # ==========================================
    # Quality
    # ==========================================

    review: Optional[Review] = None

    score: int = 0

    iterations: int = 0

    # ==========================================
    # Monitoring
    # ==========================================

    history: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)
    