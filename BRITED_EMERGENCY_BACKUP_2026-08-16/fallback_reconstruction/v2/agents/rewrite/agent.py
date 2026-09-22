from v2.core.base_agent import BaseAgent
from v2.core.context import BritedContext
from v2.services.script_parser import parse_script

class RewriteAgent(BaseAgent):

    @property
    def category(self) -> str:
        return "Quality"

    def run(self, context: BritedContext) -> BritedContext:

        script = context.script
        review = context.review

        prompt = f"""
Tu es RewriteAgent.

Tu dois améliorer le script Instagram suivant.

Sujet :
{context.subject}

Angle retenu :
{context.selected_angle.title}

Description de l'angle :
{context.selected_angle.description}

IMPORTANT :

IMPORTANT

Tu n'es PAS l'auteur du script.

Tu es son éditeur.

Ta mission est uniquement de l'améliorer.

Tu ne dois jamais :

- changer le sujet ;
- changer l'angle ;
- changer la promesse du titre ;
- ajouter de nouvelles notions patrimoniales ;
- remplacer le cas concret par un autre.

Tu dois uniquement :

- améliorer le hook ;
- améliorer la fluidité ;
- améliorer la pédagogie ;
- améliorer le CTA ;
- corriger les remarques du ReviewAgent.

Le lecteur doit avoir l'impression de lire le même script, mais en mieux.

Si tu modifies le sujet ou l'angle, ta réponse est considérée comme incorrecte.

SCRIPT ORIGINAL

Le texte ci-dessous est le script de référence.

Tu dois le corriger.

Tu ne dois jamais le remplacer par un autre.

Toute ta réponse doit rester fidèle à ce script.

Titre :
{script.title}

Hook :
{script.hook}

Script :
{script.body}

CTA :
{script.cta}

Le ReviewAgent a donné les remarques suivantes.

Points forts :
{review.strengths}

Faiblesses :
{review.weaknesses}

Réécris le script en corrigeant les faiblesses.

Conserve les points forts.

Réponds exactement avec :

# Titre

# Hook

# Script 60 secondes

# CTA
"""

        result = self.openai.ask(prompt)

        print("\n========== REWRITE ==========\n")
        print(result)
        print("\n=============================\n")

        context.script = parse_script(result)

        return context