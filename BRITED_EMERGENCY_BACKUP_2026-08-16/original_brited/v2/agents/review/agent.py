from v2.core.base_agent import BaseAgent
from v2.core.context import BritedContext

from v2.doctrine.editorial import EDITORIAL_GUIDELINES
from v2.standards.quality import QUALITY_STANDARD
from v2.standards.review import REVIEW_STANDARD

from v2.services.review_parser import parse_review


class ReviewAgent(BaseAgent):

    @property
    def category(self) -> str:
        return "Quality"

    def run(self, context: BritedContext) -> BritedContext:

        if context.script is None:
            raise ValueError("Aucun script à évaluer.")

        script = context.script

        prompt = f"""
Tu es ReviewAgent.

Tu es le Directeur Qualité de BRITED.

========================================
DOCTRINE ÉDITORIALE BRITED
========================================

{EDITORIAL_GUIDELINES}

========================================
STANDARD QUALITÉ BRITED
========================================

{QUALITY_STANDARD}

========================================
STANDARD DE REVIEW
========================================

{REVIEW_STANDARD}

========================================
SCRIPT À ÉVALUER
========================================

Titre :

{script.title}

Hook :

{script.hook}

Script :

{script.body}

CTA :

{script.cta}

========================================
MISSION
========================================

Évalue ce contenu selon les standards BRITED.

Ne réécris pas le contenu.

Ne propose pas une nouvelle version.

Analyse uniquement la qualité du script.

Respecte strictement le format de réponse demandé dans REVIEW_STANDARD.
"""

        result = self.openai.ask(prompt)

        print("\n========== REVIEW RAW ==========\n")
        print(result)
        print("\n===============================\n")

        context.review = parse_review(result)

        return context
    