from legacy.services.openai_service import ask_model


def choose_angle(subject: str, knowledge: str):
    prompt = f"""
Tu es l'Angle Agent de BRITED.

Ta mission : trouver le meilleur angle Instagram pour une vidéo patrimoniale.

Sujet :
{subject}

Connaissances Leveria :
{knowledge}

Tu ne rédiges pas la vidéo.

Tu dois proposer 5 angles, puis choisir le meilleur.

Critères :
- curiosité
- peur de l'erreur
- valeur pédagogique
- potentiel de partage
- simplicité

Format obligatoire :

# 5 angles possibles

## Angle 1
...

## Angle 2
...

## Angle 3
...

## Angle 4
...

## Angle 5
...

# Angle retenu

...

# Pourquoi cet angle est le meilleur

...
"""
    return ask_model(prompt)

