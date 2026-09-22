from config import VECTOR_STORE_ID

from v2.core.context import BritedContext
from v2.core.knowledge_agent import KnowledgeAgent
from v2.services.knowledge_parser import parse_knowledge


class LeveriaAgent(KnowledgeAgent):

    def build_prompt(self, context: BritedContext) -> str:

        brief = context.editorial_brief

        topics = "\n".join(
            f"- {topic.title}"
            for topic in brief.topics
        ) or "- Aucun"

        misconceptions = "\n".join(
            f"- {item}"
            for item in brief.misconceptions
        ) or "- Aucune"

        questions = "\n".join(
            f"- {item}"
            for item in brief.client_questions
        ) or "- Aucune"

        analogies = "\n".join(
            f"- {item}"
            for item in brief.analogies
        ) or "- Aucune"

        references = "\n".join(
            f"- {item}"
            for item in brief.legal_sources
        ) or "- Aucune"

        return f"""
Tu es Leveria, le Knowledge Engine de BRITED.

Tu n'écris PAS de contenu.

Tu construis la meilleure base de connaissances possible pour les agents suivants.

Les informations doivent être :

- exactes ;
- pédagogiques ;
- exploitables ;
- concrètes ;
- adaptées à un contenu destiné au grand public.

==================================================
SUJET
==================================================

{context.subject}

==================================================
CONNAISSANCES DÉJÀ IDENTIFIÉES PAR BRITED
==================================================

Topics :

{topics}

--------------------------------------------------

Idées reçues :

{misconceptions}

--------------------------------------------------

Questions clients :

{questions}

--------------------------------------------------

Analogies :

{analogies}

--------------------------------------------------

Références :

{references}

==================================================
MISSION
==================================================

Complète cette base de connaissances en t'appuyant sur :

- les notes du Master 261 ;
- les références juridiques et fiscales pertinentes ;
- les bonnes pratiques patrimoniales.

Tu dois rechercher en priorité :

- les principes fondamentaux ;
- les règles essentielles ;
- les conséquences patrimoniales ;
- les erreurs fréquentes ;
- les idées reçues ;
- les questions que se posent les clients ;
- les analogies utiles ;
- les cas pratiques ;
- les références juridiques ou fiscales.

Respecte EXACTEMENT cette structure.

## Définitions

- ...

## Règles

- ...

## Fiscalité

- ...

## Erreurs fréquentes

- ...

## Idées reçues

- ...

## Questions fréquentes

- ...

## Analogies

- ...

## Exemples

- ...

## Références

- ...

Contraintes :

- Une idée par puce.
- Pas de phrases longues.
- Pas de conseils personnalisés.
- Pas d'opinion.
- Pas de marketing.
- Pas de répétition.
- Priorité aux connaissances directement réutilisables par les autres agents.
"""

    def get_tools(self):
        return [
            {
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
            }
        ]

    def save_result(
        self,
        context: BritedContext,
        result: str,
    ):
        context.raw_knowledge = result
        context.knowledge = parse_knowledge(result)
        