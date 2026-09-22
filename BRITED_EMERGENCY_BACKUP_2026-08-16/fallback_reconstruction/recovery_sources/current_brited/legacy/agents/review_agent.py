from legacy.services.openai_service import ask_model


def review_script(subject: str, script: str):

    prompt = f"""
Tu es le Review Agent de BRITED.

Mission :
Évaluer un script Instagram patrimonial.

Sujet :
{subject}

Script :
{script}

Évalue strictement :

- Rigueur juridique /15
- Vulgarisation /15
- Rétention /10
- Potentiel de partage /10

Si le score est inférieur à 46/50, propose une version améliorée.

Format obligatoire :

# Score qualité /50

# Points forts

# Points faibles

# Version améliorée si nécessaire
"""

    return ask_model(prompt)
