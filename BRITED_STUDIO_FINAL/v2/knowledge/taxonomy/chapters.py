"""
BRITED Knowledge Taxonomy

Chapitres officiels de la Knowledge Base.

⚠️ Ce référentiel est commun à toutes les familles.
Les moteurs de planning et de génération de campagnes
s'appuient sur cet ordre pédagogique.
"""

from dataclasses import dataclass


# ==========================================================
# CHAPTER
# ==========================================================

@dataclass(frozen=True)
class Chapter:
    id: str
    name: str
    description: str
    order: int


# ==========================================================
# CHAPTERS
# ==========================================================

CHAPTERS = [

    Chapter(
        id="fondamentaux",
        name="Fondamentaux",
        description="Définition, objectifs et utilité.",
        order=1,
    ),

    Chapter(
        id="fonctionnement",
        name="Fonctionnement",
        description="Comprendre les mécanismes et le fonctionnement.",
        order=2,
    ),

    Chapter(
        id="avantages",
        name="Avantages",
        description="Identifier les bénéfices et points forts.",
        order=3,
    ),

    Chapter(
        id="limites",
        name="Limites",
        description="Comprendre les risques, contraintes et inconvénients.",
        order=4,
    ),

    Chapter(
        id="fiscalite",
        name="Fiscalité",
        description="Régime fiscal applicable.",
        order=5,
    ),

    Chapter(
        id="transmission",
        name="Transmission",
        description="Conséquences patrimoniales et successorales.",
        order=6,
    ),

    Chapter(
        id="optimisation",
        name="Optimisation",
        description="Stratégies d'optimisation patrimoniale.",
        order=7,
    ),

    Chapter(
        id="comparaisons",
        name="Comparaisons",
        description="Comparer avec les autres solutions patrimoniales.",
        order=8,
    ),

    Chapter(
        id="erreurs",
        name="Erreurs fréquentes",
        description="Éviter les erreurs les plus courantes.",
        order=9,
    ),

    Chapter(
        id="questions_clients",
        name="Questions clients",
        description="Répondre aux interrogations les plus fréquentes.",
        order=10,
    ),

    Chapter(
        id="cas_pratiques",
        name="Cas pratiques",
        description="Illustrer par des situations concrètes.",
        order=11,
    ),

    Chapter(
        id="actualites",
        name="Actualités",
        description="Évolutions réglementaires, fiscales et jurisprudentielles.",
        order=12,
    ),

]
