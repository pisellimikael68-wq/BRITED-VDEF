"""
BRITED Workspace Storage

Gestion du dossier de travail local.
"""

from pathlib import Path

# ==========================================================
# ROOT
# ==========================================================

WORKSPACE = Path("workspace")

CAMPAIGNS = WORKSPACE / "campaigns"

EXPORTS = WORKSPACE / "exports"

TEMP = WORKSPACE / "temp"


# ==========================================================
# INITIALIZATION
# ==========================================================

def initialize_workspace() -> None:
    """
    Crée automatiquement l'arborescence du Workspace.
    """

    WORKSPACE.mkdir(exist_ok=True)

    CAMPAIGNS.mkdir(exist_ok=True)

    EXPORTS.mkdir(exist_ok=True)

    TEMP.mkdir(exist_ok=True)
    