# BRITED Topic Standard

Chaque Topic représente une unité de connaissance exploitable par tous les agents.

Un Topic ne décrit qu'une seule idée.

Il doit être suffisamment riche pour permettre :

- à Leveria de comprendre le sujet ;
- à AngleAgent de proposer plusieurs angles ;
- à Writer de produire plusieurs scripts ;
- à ReviewAgent de contrôler la qualité.

---

# Structure

Chaque Topic contient :

- id
- title
- pillar
- family
- description
- objective
- difficulty
- priority
- keywords
- misconceptions
- client_questions
- common_mistakes
- analogies
- recommended_formats
- legal_sources

---

# Règles

## id

- unique
- en snake_case
- stable dans le temps

Exemple :

assurance_vie_definition

---

## title

Court.

Compréhensible.

Maximum 80 caractères.

---

## description

Décrit le sujet.

Une phrase.

---

## objective

Une seule idée pédagogique.

Jamais plusieurs objectifs.

---

## difficulty

Valeurs autorisées :

- Débutant
- Intermédiaire
- Expert

---

## priority

De 1 à 10.

10 = sujet majeur.

---

## keywords

5 à 15 mots-clés.

---

## misconceptions

2 à 5 idées reçues.

Toujours formulées comme un particulier pourrait les exprimer.

---

## client_questions

2 à 5 questions réelles.

Écrites avec les mots des clients.

---

## common_mistakes

2 à 5 erreurs fréquentes.

---

## analogies

0 à 3 analogies pédagogiques.

---

## recommended_formats

Formats Instagram recommandés.

Exemples :

- Idée reçue
- Cas pratique
- Question client
- Storytelling
- Comparaison
- Carrousel
- FAQ

---

## legal_sources

Articles de loi, BOFiP, doctrine, etc.

Uniquement si utiles.