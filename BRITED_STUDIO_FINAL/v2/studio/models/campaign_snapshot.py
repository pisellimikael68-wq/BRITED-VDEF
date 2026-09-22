"""
BRITED Campaign Snapshot

Représentation persistante d'une campagne.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScriptSnapshot:
    """
    Représentation persistante d'un script.
    """

    topic_id: str

    title: str

    content: str

    status: str = "ready"


@dataclass(frozen=True)
class CampaignSnapshot:
    """
    Version sauvegardée d'une campagne.
    """

    name: str

    family: str

    weeks: int

    scripts: list[ScriptSnapshot] = field(default_factory=list)

    