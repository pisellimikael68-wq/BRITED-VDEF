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

_PRESENTATION_UNIQUE = "Format validé le 11 septembre 2026 : vidéo de 60 à 65 secondes, cible 63 secondes. Préparer environ 150 à 165 mots prononcés, nombres développés, à un débit naturel autour de 160 mots/minute avec des pauses. Ce budget est indicatif : chronométrer la lecture puis le montage final, jingle compris. Si un jingle est ajouté, déduire sa durée du budget de parole ; ne pas accélérer artificiellement. Un texte seul ne garantit pas la durée réelle ni une rémunération TikTok. Le script YouTube Shorts certifié reste la source éditoriale commune. Chaque destination reçoit toutefois un rendu 9:16 autonome, recomposé dans ses propres zones sûres : Instagram/Facebook Reels, TikTok et YouTube Shorts. Question ou promesse immédiatement compréhensible ; réponse directe et entière ; une explication autonome, un exemple et la réserve indispensable ; respiration de 0,9 seconde aux changements structurants ; CTA strictement conforme au calendrier."

PRESENTATION_PAR_PLATEFORME = {
    "tiktok": _PRESENTATION_UNIQUE,
    "reels": _PRESENTATION_UNIQUE,
    "shorts": _PRESENTATION_UNIQUE,
}

PRINCIPES_VISUELS = (
    "9:16 en 1080 × 1920, univers chaud et neutre, aucune mention BRITED dans la vidéo.",
    "Texte central grand, condensé et lisible ; aucun libellé interne Hook, Règle ou domaine.",
    "Toutes les pages de contenu utilisent un corps typographique de référence de 46 px ; l'adaptation aux textes denses est bornée à 40 px minimum, soit un écart maximal de 6 px. Les titres, pastilles et CTA constituent des niveaux hiérarchiques distincts.",
    "Mots révélés progressivement par fondu fluide, parfaitement synchronisés avec la voix.",
    "Transitions de page fluides ; respiration structurante de 0,9 seconde.",
    "La concision ne supprime jamais la règle centrale, sa condition d'application, l'exception indispensable, l'exemple utile ni les sources.",
    "Un sujet trop dense est resserré sur un angle autonome ou scindé en mini-série pour respecter 60–65 secondes sans supprimer ses conditions indispensables.",
    "Un schéma composé de pictogrammes sélectionnés dans la bibliothèque vectorielle locale, présentable, diversifié et cohérent par page, jamais sur le texte, jamais superposé à un autre visuel, jamais coupé ; un contrôle géométrique et sémantique indépendant est bloquant.",
    "Barre de durée uniquement en bas ; aucune barre haute, aucun crayon jaune, aucun demi-cercle.",
    "Question entièrement affichée et lue avant toute réponse ; réponse sur la page suivante.",
    "Dernière page uniquement après la narration, sans synthèse supplémentaire.",
    "Tous les tirets grammaticaux utilisent le caractère ASCII '-' compatible avec la police ; aucun tiret insécable ou exotique.",
    "Les choix OUI et NON apparaissent uniquement dans leurs deux cases : ils ne sont ni ajoutés à la question ni prononcés.",
    "Un même beat n'est jamais coupé sur deux pages ; police, hauteur du cadre et centrage s'adaptent automatiquement.",
    "Dans la narration, écrire et prononcer 'article' en toutes lettres, jamais l'abréviation 'art.'.",
    "Clôture conforme au calendrier : discussion, enregistrement, abonnement ou contact discret. Préserver exactement le texte validé et adapter le visuel au sens ; aucun calendrier ni bouton de rendez-vous imposé aux conclusions communautaires.",
    "La clôture conserve exactement la même structure sur Instagram, TikTok et YouTube ; seuls ses accents prennent la couleur de la série.",
    "La piste audio est débruitée puis retranscrite localement phrase par phrase avec Whisper Large Turbo ; toute perte d'un terme porteur de sens, répétition, hallucination, microcoupure, bruit résiduel, écrêtage ou rupture bloque et régénère uniquement le segment concerné.",
    "Tous les nombres et références sont prononcés comme des nombres français complets et naturels, jamais chiffre par chiffre ; l'affichage conserve les chiffres.",
    "À l'écran, tous les nombres, montants, pourcentages et dates utilisent une forme compacte : chiffres arabes, symbole € à la place du mot euros, K€ lorsque cela améliore la lisibilité, % pour les taux et JJ/MM/AAAA pour les dates. La narration orale reste rédigée en français naturel.",
    "À l'écran, 'inférieur ou égal' s'écrit =< selon la convention BRITED ; à l'oral, cette relation est toujours prononcée intégralement 'inférieur ou égal'.",
    "Une seule empreinte vocale et une seule configuration d'intonation sont utilisées ; la narration et le contenu certifiés sont communs, mais chaque plateforme possède son propre fichier rendu et sa propre empreinte.",
    "Instagram et Facebook utilisent un rendu Reels avec composition recentrée pour le fil, la grille du profil et les commandes de l'application ; TikTok utilise un rendu dédié qui évite sa colonne d'actions et sa légende ; YouTube Shorts conserve son rendu de référence.",
    "Le contrôle de diffusion refuse tout fichier dont le profil visuel ne correspond pas à la destination et interdit de réutiliser l'empreinte YouTube sur Instagram ou TikTok.",
    "La page de réponse utilise une carte chaude adaptative et hiérarchisée : verdict appuyé, précisions dans des modules distincts, texte complet centré géométriquement et aucun encadré disproportionné. Les qualités des personnes sont explicites : par exemple PARTENAIRE DE PACS, jamais le seul sigle PACS lorsqu'il désigne une personne.",
    "La vidéo regimes_changement__shorts (1).mp4 validée est la référence vocale absolue de toutes les vidéos et plateformes : même voix ElevenLabs, même intonation, mêmes fluctuations et même courbe d'énergie page par page.",
    "Face caméra : débit naturel indicatif autour de 160 mots/minute, variations selon le sens. Ajuster à la lecture chronométrée et à la durée du jingle éventuel ; aucune accélération forcée pour tenir le format.",
    "Tout identifiant de page composé, par exemple regle_exemple ou exemple_fiscal, doit être rattaché à son rôle vocal canonique. Un rôle inconnu bloque la production et ne peut jamais revenir silencieusement au débit par défaut.",
    "Le contrôle final vérifie la compréhension et la durée réelle du montage entre 60 et 65 secondes, sans imposer un débit uniforme.",
    "Le texte affiché doit reprendre toutes les informations de la narration de sa page. Seuls les nombres, dates, pourcentages et symboles sont compactés selon la charte ; aucune proposition informative ne peut être omise ou remplacée par une notation télégraphique.",
    "Toute règle financière ou fiscale conditionnée par l'ancienneté d'un contrat doit nommer la nature exacte du contrat et rappeler explicitement la durée requise dans la réponse orale et à l'écran. Pour l'abattement annuel de l'assurance-vie, la mention contrat d'assurance-vie de plus de 8 ans est obligatoire sur la page de réponse.",
    "Pour cette séquence d'assurance-vie, la formulation obligatoire est : 'Si la part de gains retirée dépasse l'abattement, seul l'excédent est imposable. Pour les versements depuis le 27/09/2017, le taux de 7,5 % s'applique dans la limite du seuil global de 150 K€ de primes, tous contrats confondus ; au-delà, 12,8 % peut s'appliquer.' À l'oral, les nombres et la date sont prononcés en français naturel.",
    "La durée finale doit être vérifiée entre 60 et 65 secondes. Si elle ne peut être respectée sans perdre une condition essentielle, reprendre le sous-angle ; ne pas certifier une durée non mesurée.",
    "Le contrôle final préserve le débit naturel du locuteur et refuse les accélérations artificielles ou les conditions devenues inaudibles. Le ton reste conversationnel, chaleureux, assuré et jamais institutionnel.",
    "Resserrer les formulations et les répétitions pour tenir le format en conservant la règle, ses conditions, les chiffres utiles et les risques. Parle comme à un ami en le vouvoyant : vous, votre, vos. Une situation familière, une seule idée, un exemple concret avec les chiffres utiles, une explication de ce que cela change pour lui et une conclusion utile. Pas de dialogue fictif à deux voix, pas de témoignage inventé, pas de tic systématique comme imaginez ou vous voyez.",
    "Deux contrôles indépendants de formulation sont obligatoires : lecture phrase par phrase, puis contre-vérification finale de la compréhension, du sérieux professionnel et de la cohérence question-réponse.",
    "Les libellés internes ou télégraphiques tels que Court :, Règle :, Question : et Réponse : sont interdits dans la narration.",
    "Sur la clôture, la question, le bouton, la mention de bio et le calendrier sont centrés géométriquement et conservent leurs positions verrouillées.",
)

INTERDITS = (
    "crayon jaune", "barre de progression en haut", "dessin coupé",
    "pictogramme sur le texte", "nom de l'application", "nom du domaine",
    "libellé Hook", "libellé Règle", "publication automatique",
    "tiret insécable", "oui/non répété dans la question", "beat coupé sur deux pages",
    "abréviation art. prononcée", "CTA oral différent du CTA visuel", "bruit audio parasite",
    "nombre prononcé chiffre par chiffre", "débit différent selon la plateforme", "phrase ambiguë ou télégraphique",
    "information essentielle supprimée pour tenir la durée", "plusieurs règles principales dans une seule vidéo",
    "débit uniforme et artificiel", "intonation de réponse différente du CTA",
    "montant écrit en toutes lettres à l'écran", "mot euros à l'écran", "date écrite en toutes lettres à l'écran",
)


def presentation_plateforme(platform: str) -> str:
    return PRESENTATION_PAR_PLATEFORME[platform.casefold()]
