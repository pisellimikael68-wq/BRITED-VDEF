from legacy.services.openai_service import ask_model


def write_script(
    subject: str,
    knowledge: str,
    angle: str,
    review: str | None = None,
):

    prompt = f"""
Tu es le Writer Agent de BRITED.

Mission :
Écrire une vidéo Instagram patrimoniale.

Sujet :
{subject}

Connaissances Leveria :
{knowledge}

Angle choisi :
{angle}

Écris une vidéo Instagram patrimoniale de 60 secondes.

Format obligatoire :

# Titre

# Hook

# Script 60 secondes

# Références juridiques

# Concepts Leveria utilisés
"""

    if review:
        prompt += f"""

Le Review Agent a identifié les améliorations suivantes :

{review}

Améliore le script en tenant compte de ces remarques.

Ne conserve que les bonnes idées.

Ne réécris pas le même script.

L'objectif est d'obtenir un score supérieur ou égal à 46/50.
"""

    return ask_model(prompt)
