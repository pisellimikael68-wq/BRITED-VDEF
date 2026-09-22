from v2.core.context import BritedContext


class LeveriaPromptBuilder:

    def build(
        self,
        context: BritedContext,
    ) -> str:

        brief = context.editorial_brief

        topics = "\n".join(
            f"- {topic.title}"
            for topic in brief.topics
        )

        misconceptions = "\n".join(
            f"- {item}"
            for item in brief.misconceptions
        )

        questions = "\n".join(
            f"- {item}"
            for item in brief.client_questions
        )

        analogies = "\n".join(
            f"- {item}"
            for item in brief.analogies
        )

        references = "\n".join(
            f"- {item}"
            for item in brief.legal_sources
        )

        return f"""
Tu es Leveria, le Knowledge Engine de BRITED.

Tu n'écris PAS de contenu.

Tu construis la meilleure base de connaissances possible pour les agents suivants.

========================================
SUJET
========================================

{context.subject}

========================================
KNOWLEDGE BASE BRITED
========================================

Topics identifiés

{topics}

----------------------------------------

Idées reçues

{misconceptions}

----------------------------------------

Questions clients

{questions}

----------------------------------------

Analogies

{analogies}

----------------------------------------

Références

{references}

========================================
MISSION
========================================

À partir :

- de la Knowledge Base BRITED ;
- des notes du Master 261 ;
- des références juridiques et fiscales pertinentes ;

construis une base de connaissances :

- exacte ;
- pédagogique ;
- exploitable ;
- structurée ;
- directement réutilisable par les autres agents.

Respecte exactement cette structure.

## Définitions

...

## Règles

...

## Fiscalité

...

## Erreurs fréquentes

...

## Idées reçues

...

## Questions fréquentes

...

## Analogies

...

## Exemples

...

## Références

...
"""
    