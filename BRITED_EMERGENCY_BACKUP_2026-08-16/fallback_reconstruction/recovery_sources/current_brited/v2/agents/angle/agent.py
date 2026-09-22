from v2.core.base_agent import BaseAgent
from v2.core.context import BritedContext
from v2.doctrine.editorial import EDITORIAL_GUIDELINES
from v2.services.angle_parser import parse_angles


class AngleAgent(BaseAgent):

    @property
    def category(self) -> str:
        return "Creative"

    def run(self, context: BritedContext) -> BritedContext:

        knowledge = context.knowledge
        editorial = context.editorial

        prompt = f"""
Tu es AngleAgent.

{EDITORIAL_GUIDELINES}

========================================
MISSION
========================================

Tu es responsable de la stratégie de contenu.

Tu ne rédiges pas le script.

Tu proposes uniquement les meilleurs angles
pour appliquer la stratégie éditoriale définie.

========================================
SUJET
========================================

{context.subject}

========================================
STRATÉGIE ÉDITORIALE
========================================

Audience :
{editorial.audience}

Objectif :
{editorial.objective}

Message clé :
{editorial.key_message}

Ton :
{editorial.tone}

Émotion :
{editorial.emotion}

Complexité :
{editorial.complexity}

Format :
{editorial.format}

CTA :
{editorial.cta_strategy}

Points à éviter :
{editorial.forbidden_points}

========================================
CONNAISSANCES LEVERIA
========================================

Définitions :

{knowledge.definitions}

Règles :

{knowledge.rules}

Fiscalité :

{knowledge.taxation}

Erreurs fréquentes :

{knowledge.mistakes}

Idées reçues :

{knowledge.misconceptions}

Questions fréquentes :

{knowledge.frequently_asked_questions}

Analogies :

{knowledge.analogies}

Exemples :

{knowledge.examples}

Références :

{knowledge.references}

========================================
OBJECTIF
========================================

Propose exactement 5 angles.

Chaque angle doit :

- être utile ;
- être original ;
- être pédagogique ;
- susciter immédiatement la curiosité ;
- respecter la stratégie éditoriale.

Attribue un score sur 10 à chaque angle.

========================================
FORMAT DE RÉPONSE
========================================

ANGLE 1
Titre :
Description :
Score :

ANGLE 2
Titre :
Description :
Score :

ANGLE 3
Titre :
Description :
Score :

ANGLE 4
Titre :
Description :
Score :

ANGLE 5
Titre :
Description :
Score :
"""

        raw = self.openai.ask(prompt)

        print("\n========== ANGLES ==========\n")
        print(raw)
        print("\n============================\n")

        context.angles = parse_angles(raw)

        if context.angles:
            context.angles.sort(
                key=lambda angle: angle.score,
                reverse=True,
            )

            context.selected_angle = context.angles[0]

        return context
    