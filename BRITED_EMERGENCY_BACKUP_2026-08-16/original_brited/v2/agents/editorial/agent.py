from v2.core.base_agent import BaseAgent
from v2.core.context import BritedContext

from v2.doctrine.editorial import EDITORIAL_GUIDELINES

from v2.services.editorial_parser import parse_editorial
from v2.services.editorial_contract_builder import (
    build_editorial_contract,
)


class EditorialAgent(BaseAgent):

    @property
    def category(self) -> str:
        return "Editorial"

    def run(self, context: BritedContext) -> BritedContext:

        prompt = f"""
Tu es EditorialAgent.

{EDITORIAL_GUIDELINES}

========================================
MISSION
========================================

Tu es le Directeur Éditorial de BRITED.

Tu ne rédiges jamais le contenu.

Tu définis la stratégie éditoriale qui sera ensuite appliquée
par les autres agents.

Tu t'appuies uniquement sur :

- la doctrine BRITED ;
- les connaissances patrimoniales ;
- le sujet demandé.

========================================
SUJET
========================================

{context.subject}

========================================
CONNAISSANCES LEVERIA
========================================

{context.raw_knowledge}

========================================
OBJECTIF
========================================

Définis la meilleure stratégie éditoriale.

Réponds exactement sous cette structure :

Audience :

Objectif :

Message clé :

Ton :

Émotion :

Complexité :

Format :

CTA :

Points à éviter :
"""

        result = self.openai.ask(prompt)

        print("\n========== EDITORIAL ==========\n")
        print(result)
        print("\n===============================\n")

        context.editorial = parse_editorial(result)

        context.editorial_contract = build_editorial_contract(
            context.editorial
        )

        return context
    