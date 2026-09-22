"""
BRITED Editorial Playbook

Hook Engine

Sélectionne le Hook le plus adapté au contexte éditorial.
"""

from v2.studio.editorial.editorial_types import EditorialAngle
from v2.studio.editorial.playbook.models import Hook
from v2.studio.editorial.playbook.repositories.hooks import HOOKS


class HookEngine:
    """
    Sélectionne le meilleur Hook parmi le référentiel.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def select(
        self,
        angle: EditorialAngle,
        platform: str = "instagram",
        level: str = "beginner",
    ) -> Hook:
        """
        Retourne le Hook le plus adapté.
        """

        candidates = [

            hook

            for hook in HOOKS

            if angle in hook.suitable_angles

        ]

        if candidates:
            return candidates[0]

        return HOOKS[0]
    