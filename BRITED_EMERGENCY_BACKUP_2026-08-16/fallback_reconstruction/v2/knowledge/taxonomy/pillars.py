"""
BRITED Knowledge Taxonomy

Piliers officiels de la connaissance patrimoniale.

⚠️ Ce fichier est considéré comme une référence.
Les piliers ne doivent être modifiés qu'en cas d'évolution majeure
de l'architecture BRITED.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Pillar:
    id: str
    name: str
    description: str
    order: int


PILLARS = [

    Pillar(
        id="epargner",
        name="Épargner",
        description="Constituer et développer une épargne patrimoniale.",
        order=1,
    ),

    Pillar(
        id="investir",
        name="Investir",
        description="Investir dans des actifs financiers ou immobiliers.",
        order=2,
    ),

    Pillar(
        id="transmettre",
        name="Transmettre",
        description="Préparer la transmission du patrimoine.",
        order=3,
    ),

    Pillar(
        id="proteger",
        name="Protéger",
        description="Sécuriser les personnes et le patrimoine.",
        order=4,
    ),

    Pillar(
        id="financer",
        name="Financer",
        description="Optimiser les solutions de financement.",
        order=5,
    ),

    Pillar(
        id="entreprendre",
        name="Entreprendre",
        description="Structurer le patrimoine professionnel.",
        order=6,
    ),

    Pillar(
        id="fiscalite",
        name="Fiscalité",
        description="Comprendre et optimiser la fiscalité patrimoniale.",
        order=7,
    ),

    Pillar(
        id="international",
        name="International",
        description="Traiter les problématiques patrimoniales internationales.",
        order=8,
    ),

]
