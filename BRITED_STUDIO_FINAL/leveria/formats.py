from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Beat:
    id: str
    label: str
    intent: str
    seconds_min: float
    seconds_max: float


@dataclass(frozen=True)
class PlatformFormat:
    id: str
    label: str
    target_seconds_min: float
    target_seconds_max: float
    hard_maximum_seconds: float
    beats: tuple[Beat, ...]
    priority: str

    def word_budget(self, words_per_minute: int = 160) -> tuple[int, int]:
        return (round((self.target_seconds_min - 4) * words_per_minute / 60),
                round((self.target_seconds_max - 4) * words_per_minute / 60))


REELS = PlatformFormat(
    "reels", "Instagram / Facebook Reels", 60, 65, 65,
    (
        Beat("hook", "Hook", "Situation vécue reconnaissable dans les deux premières secondes.", 2, 3),
        Beat("question", "Question", "Carton complet et choix OUI/NON avant la réponse.", 2, 3),
        Beat("reponse", "Réponse", "Réponse explicite sur une page séparée.", 1, 2),
        Beat("regle", "Règle", "Une seule idée utile avec sa condition d'application.", 5, 7),
        Beat("exemple", "Exemple", "Situation simple et enregistrable.", 7, 10),
        Beat("nuance", "Nuance", "Limite juridique ou fiscale essentielle.", 3, 5),
        Beat("cta", "Clôture", "Idée utile ou invitation adaptée au calendrier, sans obligation commerciale.", 3, 4),
    ), "partage privé, enregistrement et complétion",
)

# Le fond éditorial est commun, mais TikTok conserve un rendu autonome afin de
# respecter ses zones d'interface et son cadrage de consultation.
TIKTOK = PlatformFormat(
    "tiktok", "TikTok", 
    60, 65, 65,
    REELS.beats, "rétention mobile et zones d'interface TikTok",
)

SHORTS = PlatformFormat(
    "shorts", "Face caméra · script unique", 60, 65, 65,
    (
        Beat("hook", "Accroche", "Une phrase vive que Mikael peut dire naturellement face caméra.", 2, 5),
        Beat("reponse", "Réponse", "La réponse immédiate, franche et conversationnelle.", 3, 8),
        Beat("regle", "Explication", "La règle expliquée comme à un ami, sans langage récité.", 8, 25),
        Beat("exemple", "Exemple", "Un cas concret facile à raconter et à comprendre.", 8, 25),
        Beat("nuance", "Point de vigilance", "La réserve indispensable, formulée calmement.", 4, 15),
        Beat("cta", "Conclusion", "Une conclusion naturelle et un CTA non agressif.", 3, 8),
    ), "naturel face caméra, crédibilité et clarté patrimoniale",
)

FORMATS = {item.id: item for item in (TIKTOK, REELS, SHORTS)}


def get_format(platform: str) -> PlatformFormat:
    aliases = {"instagram": "reels", "youtube": "shorts", "youtube_shorts": "shorts"}
    key = aliases.get(platform.casefold(), platform.casefold())
    if key not in FORMATS:
        raise KeyError(f"plateforme inconnue : {platform!r}")
    return FORMATS[key]
