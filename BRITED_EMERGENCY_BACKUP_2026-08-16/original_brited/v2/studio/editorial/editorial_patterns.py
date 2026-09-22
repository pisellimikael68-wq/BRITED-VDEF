from dataclasses import dataclass

from v2.studio.editorial.editorial_types import EditorialAngle


# ==========================================================
# PATTERN
# ==========================================================

@dataclass(frozen=True)
class EditorialPattern:
    """
    Décrit la structure éditoriale d'une publication.
    """

    angle: EditorialAngle

    hook_type: str

    structure: list[str]

    objective: str

    cta: str


# ==========================================================
# PATTERNS
# ==========================================================

EDITORIAL_PATTERNS = {

    EditorialAngle.EXPLANATION: EditorialPattern(

        angle=EditorialAngle.EXPLANATION,

        hook_type="question",

        structure=[
            "Définition",
            "Explication",
            "Exemple",
            "À retenir",
        ],

        objective="Faire comprendre un concept.",

        cta="Enregistrez cette publication pour la retrouver plus tard.",
    ),

    EditorialAngle.FAQ: EditorialPattern(

        angle=EditorialAngle.FAQ,

        hook_type="question",

        structure=[
            "Question",
            "Réponse",
            "Exemple",
            "Conclusion",
        ],

        objective="Répondre à une question fréquente.",

        cta="Posez votre question en commentaire.",
    ),

    EditorialAngle.MYTH: EditorialPattern(

        angle=EditorialAngle.MYTH,

        hook_type="idée reçue",

        structure=[
            "Idée reçue",
            "Pourquoi c'est faux",
            "La bonne explication",
            "À retenir",
        ],

        objective="Corriger une idée reçue.",

        cta="Partagez cette publication à quelqu'un qui croit encore cela.",
    ),

    EditorialAngle.MISTAKE: EditorialPattern(

        angle=EditorialAngle.MISTAKE,

        hook_type="erreur",

        structure=[
            "Erreur",
            "Conséquences",
            "Bonne pratique",
            "À retenir",
        ],

        objective="Éviter une erreur fréquente.",

        cta="Enregistrez cette publication pour éviter cette erreur.",
    ),

    EditorialAngle.COMPARISON: EditorialPattern(

        angle=EditorialAngle.COMPARISON,

        hook_type="comparaison",

        structure=[
            "Présentation",
            "Avantages",
            "Inconvénients",
            "Comment choisir",
        ],

        objective="Comparer deux solutions.",

        cta="Lequel choisiriez-vous ?",
    ),

    EditorialAngle.STORY: EditorialPattern(

        angle=EditorialAngle.STORY,

        hook_type="histoire",

        structure=[
            "Contexte",
            "Problème",
            "Solution",
            "Leçon",
        ],

        objective="Créer de l'identification.",

        cta="Cette histoire vous parle ?",
    ),

    EditorialAngle.CASE_STUDY: EditorialPattern(

        angle=EditorialAngle.CASE_STUDY,

        hook_type="cas pratique",

        structure=[
            "Situation",
            "Analyse",
            "Solution",
            "À retenir",
        ],

        objective="Illustrer un cas concret.",

        cta="Souhaitez-vous d'autres cas pratiques ?",
    ),

    EditorialAngle.TRUE_FALSE: EditorialPattern(

        angle=EditorialAngle.TRUE_FALSE,

        hook_type="vrai ou faux",

        structure=[
            "Affirmation",
            "Réponse",
            "Explication",
            "À retenir",
        ],

        objective="Tester les connaissances.",

        cta="Combien de bonnes réponses avez-vous trouvées ?",
    ),

    EditorialAngle.DEEP_DIVE: EditorialPattern(

        angle=EditorialAngle.DEEP_DIVE,

        hook_type="expert",

        structure=[
            "Contexte",
            "Analyse",
            "Nuances",
            "Conclusion",
        ],

        objective="Approfondir un sujet complexe.",

        cta="Abonnez-vous pour plus d'analyses patrimoniales.",
    ),

    EditorialAngle.REGULATION: EditorialPattern(

        angle=EditorialAngle.REGULATION,

        hook_type="actualité réglementaire",

        structure=[
            "Texte",
            "Impact",
            "Conséquences",
            "À retenir",
        ],

        objective="Expliquer une règle juridique.",

        cta="Enregistrez cette fiche.",
    ),

    EditorialAngle.QUESTION: EditorialPattern(

        angle=EditorialAngle.QUESTION,

        hook_type="question",

        structure=[
            "Question",
            "Explication",
            "Exemple",
            "À retenir",
        ],

        objective="Répondre à une interrogation.",

        cta="Posez vos questions en commentaire.",
    ),

}

