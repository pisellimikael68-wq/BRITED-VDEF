from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Serie:
    id: str
    label: str
    couleur_secondaire: str
    pictogramme: str


SERIES = (
    Serie("fiscalite", "Fiscalité", "#6F4E37", "pourcentage"),
    Serie("immobilier", "Immobilier", "#C96F4A", "maison"),
    Serie("juridique", "Juridique", "#D99A2B", "balance"),
    Serie("finance", "Finance", "#2457D6", "courbe"),
)

PRESENTATION_PAR_PLATEFORME = {
    "tiktok": "38 à 42 secondes. Hook avant 3 secondes ; question binaire fixe avec OUI/NON ; réponse sur la page suivante ; changements utiles toutes les 2 à 4 secondes ; dernière page « Le saviez-vous ? » puis commenter, partager et s'abonner.",
    "reels": "28 à 40 secondes. Situation reconnaissable dès 2 secondes ; carton-question TikTok avec choix visibles ; réponse distincte ; priorité à l'enregistrement et au partage ; CTA enregistrer, partager et s'abonner.",
    "shorts": "40 à 58 secondes. Question recherchée ou promesse avant 2 secondes ; réponse directe sans attente ; explication autonome ; exemple complet ; abonnement discret.",
}

PRINCIPES_VISUELS = (
    "9:16 en 1080 × 1920, univers chaud et neutre, aucune mention BRITED dans la vidéo.",
    "Texte central grand, condensé et lisible ; aucun libellé interne Hook, Règle ou domaine.",
    "Mots révélés progressivement par fondu fluide, parfaitement synchronisés avec la voix.",
    "Transitions de page fluides ; respiration jusqu'à deux secondes lorsque la compréhension l'exige.",
    "Un schéma ou pictogramme pédagogique par page, jamais sur le texte, jamais coupé.",
    "Barre de durée uniquement en bas ; aucune barre haute, aucun crayon jaune, aucun demi-cercle.",
    "Question entièrement affichée et lue avant toute réponse ; réponse sur la page suivante.",
    "Dernière page uniquement après la narration, sans synthèse supplémentaire.",
)

INTERDITS = (
    "crayon jaune", "barre de progression en haut", "dessin coupé",
    "pictogramme sur le texte", "nom de l'application", "nom du domaine",
    "libellé Hook", "libellé Règle", "publication automatique",
)


def presentation_plateforme(platform: str) -> str:
    return PRESENTATION_PAR_PLATEFORME[platform.casefold()]
