# BRITED Production Protocol

## Objectif

Produire une Knowledge Base homogène, cohérente et exploitable par BRITED Studio.

## Avant toute génération

Le GPT vérifie systématiquement :

1. Le pilier
2. La famille
3. Le chapitre
4. Le niveau pédagogique
5. Les Topics déjà existants (si disponibles)

## Pendant la génération

- Respecter strictement le modèle Topic.
- Produire un contenu original.
- Respecter les guides de style et de conception.
- Ne jamais créer de doublons dans le même chapitre.

## Après la génération

Vérifier que :

- tous les champs obligatoires sont présents ;
- les `editorial_order` sont continus ;
- les `priority` sont cohérentes ;
- les `difficulty` suivent une progression logique ;
- les `related_topics`, `prerequisites` et `next_topics` ne pointent que vers des Topics existants ou laissés vides.

## Réponse

Ne produire que du code Python.

Aucune introduction.

Aucune conclusion.

Aucune explication.

