from v2.core.base_agent import BaseAgent
from v2.core.context import BritedContext

from v2.doctrine.editorial import EDITORIAL_GUIDELINES
from v2.services.script_parser import parse_script


class WriterAgent(BaseAgent):

    @property
    def category(self) -> str:
        return "Creative"

    def run(self, context: BritedContext) -> BritedContext:

        if context.knowledge is None:
            raise ValueError("Knowledge manquante dans le contexte.")

        if context.selected_angle is None:
            raise ValueError("Aucun angle sélectionné.")

        if context.editorial_contract is None:
            raise ValueError("Contrat éditorial manquant.")

        knowledge = context.knowledge
        angle = context.selected_angle
        contract = context.editorial_contract

        prompt = f"""
Tu es WriterAgent.

Tu es le rédacteur officiel de BRITED.

========================================
DOCTRINE ÉDITORIALE BRITED
========================================

{EDITORIAL_GUIDELINES}

========================================
MISSION
========================================

Tu appliques strictement le contrat éditorial.

Tu n'inventes jamais la stratégie.

Tu ne modifies jamais les contraintes imposées.

Tu utilises uniquement :

- le contrat éditorial ;
- les connaissances patrimoniales ;
- l'angle retenu.

========================================
SUJET
========================================

{context.subject}

========================================
CONTRAT ÉDITORIAL
========================================

Audience :
{contract.audience}

Objectif :
{contract.objective}

Message clé :
{contract.key_message}

Ton :
{contract.tone}

Format :
{contract.format}

CTA :
{contract.cta}

========================================
ANGLE RETENU
========================================

Titre :
{angle.title}

Description :
{angle.description}

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

Rédige le meilleur script Instagram possible.

Le contenu doit :

- respecter intégralement le contrat éditorial ;
- respecter la doctrine BRITED ;
- être exact sur le plan patrimonial ;
- être très pédagogique ;
- être fluide à l'oral ;
- être crédible ;
- être facilement mémorisable ;
- être adapté à un Reel d'environ 60 secondes.

Tu ne modifies jamais :

- le public visé ;
- le ton ;
- le format demandé ;
- le CTA demandé.

Tu peux uniquement améliorer :

- le hook ;
- les exemples ;
- le storytelling ;
- les analogies ;
- la pédagogie.

Ne jamais :

- inventer une règle fiscale ;
- inventer une règle juridique ;
- donner un conseil personnalisé ;
- promettre un résultat ;
- faire de prospection.

========================================
FORMAT DE RÉPONSE
========================================

Réponds exactement sous cette forme :

# Titre

# Hook

# Script 60 secondes

# CTA
"""

        result = self.openai.ask(prompt)

        context.script = parse_script(result)

        return context