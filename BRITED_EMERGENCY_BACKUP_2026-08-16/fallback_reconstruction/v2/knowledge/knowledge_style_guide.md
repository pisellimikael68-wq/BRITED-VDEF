# BRITED Knowledge Style Guide

## Mission

La Knowledge Base BRITED sert à produire automatiquement des contenus patrimoniaux.

Chaque Topic doit être :
- atomique ;
- autonome ;
- pédagogique ;
- exploitable par un moteur IA ;
- juridiquement prudent.

## Règle fondamentale

Un Topic = une seule idée.

Ne jamais mélanger plusieurs notions dans un même Topic.

## Structure

Chaque Topic doit respecter strictement le dataclass Topic défini dans `knowledge_models.py`.

Aucun champ inventé.

Aucun champ obligatoire oublié.

## Taxonomie

Chaque Topic respecte :

Pilier → Famille → Chapitre → Topic

Les valeurs doivent correspondre à la taxonomie officielle.

## Difficulté

Utiliser uniquement :

- Débutant
- Intermédiaire
- Avancé
- Expert

## Priorité

- 10 = indispensable
- 9 = très important
- 8 = important
- 7 = complément
- 6 = niche
- 5 = expert

## Editorial order

L'ordre éditorial doit être croissant.

Pas de doublon.

Pas de trou volontaire.

## Objective

Le champ objective décrit ce que le lecteur comprend ou saura faire après le Topic.

Éviter les formulations vagues comme :
- Présenter...
- Parler de...

Préférer :
- Expliquer...
- Permettre au lecteur de comprendre...
- Clarifier...

## Keywords

Entre 5 et 10 mots-clés.

Pas de phrases.

Pas de ponctuation.

## Key points

Entre 4 et 7 points clés.

Chaque point doit être clair, court et exploitable dans un script.

## Examples

Au moins 2 exemples réalistes.

Les exemples doivent illustrer une vraie situation patrimoniale.

## Vocabulary

Uniquement des termes techniques ou utiles.

Pas de phrases complètes.

## Misconceptions

Les misconceptions sont des croyances fausses.

Elles ne sont pas des erreurs de comportement.

## Common mistakes

Les common_mistakes sont des erreurs d'action ou de décision.

Elles ne sont pas des croyances.

## Client questions

Les client_questions doivent être formulées comme de vraies questions de client.

## Client objections

Les client_objections expriment une résistance ou une hésitation.

## Client fears

Les client_fears expriment une inquiétude.

## Client goals

Les client_goals expriment un objectif patrimonial.

## Client intents

Les client_intents expriment une intention d'action ou de recherche.

## Analogies

Les analogies doivent rendre le sujet plus simple.

Elles doivent être courtes et pédagogiques.

## Expert tips

Les expert_tips doivent apporter une nuance professionnelle.

Ils ne doivent jamais constituer un conseil personnalisé.

## Attention points

Les attention_points signalent des points de vigilance.

Ils doivent rester généraux.

## Legal sources

Les legal_sources doivent être aussi précises que possible.

Ne jamais inventer une référence juridique.

Utiliser si pertinent :
- Code des assurances
- Code civil
- Code général des impôts
- BOFiP
- AMF
- ACPR
- Code monétaire et financier

## Navigation

related_topics, prerequisites et next_topics ne doivent pointer que vers des Topics existants ou explicitement demandés.

En cas de doute, laisser la liste vide.

## Style

Ton professionnel.

Pédagogique.

Clair.

Neutre.

Jamais commercial.

Jamais promotionnel.

Jamais alarmiste.

## Réponse attendue

Répondre uniquement avec du code Python.

Ne jamais ajouter d'introduction.

Ne jamais ajouter de conclusion.

Ne jamais expliquer le code.
