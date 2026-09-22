---
id: impot_revenu_decote
titre: La décote qui annule l'impôt des revenus modestes
domaine: impot_revenu
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 7
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- décote impôt
- seuil d'imposition
- pourquoi je ne paie pas d'impôt
resume: La décote réduit l'impôt des foyers dont la cotisation reste faible après application du barème.
  Elle explique pourquoi le seuil réel d'entrée dans l'impôt est nettement plus élevé que le début de
  la première tranche.
sources:
- type: texte_legal
  ref: CGI, article 197, I, 4 (décote)
- type: texte_legal
  ref: CGI, article 197, I, 1 (barème progressif)
- type: bofip
  ref: BOI-IR-LIQ-20-30-20 (décote)
  url: https://bofip.impots.gouv.fr/doctrine/BOI-IR-LIQ-20-30-20
  consulte_le: 2026-07-29
chiffres:
- cle: Taux de résorption de la décote
  valeur: 45,25
  unite: '%'
  source: 0
  commentaire: fraction de l'impôt brut retranchée du plafond de décote
- cle: Taux de la première tranche imposable du barème
  valeur: '11'
  unite: '%'
  source: 1
relations:
  regi_par:
  - fiscalite_quotient_familial
  complete_par:
  - impot_revenu_prelevement_source
  s_applique_a:
  - impot_revenu_tranche_marginale
erreurs_frequentes:
- Confondre le seuil de la première tranche et le seuil réel d'imposition. La décote décale ce dernier
  vers le haut, parfois de plusieurs milliers d'euros.
- Croire que la décote est un abattement sur le revenu. Elle s'applique après le calcul de l'impôt, pas
  sur l'assiette.
- Ignorer l'effet de taux marginal implicite: dans la zone de résorption de la décote, chaque euro supplémentaire
    est taxé bien au-delà de 11 %.
- Croire que la décote se demande. Elle est appliquée automatiquement par l'administration.
questions_clients:
- À partir de quel revenu paie-t-on des impôts ?
- Pourquoi une petite augmentation m'a coûté si cher en impôt ?
- Faut-il demander la décote ?
a_ne_pas_dire:
- Ne jamais calculer l'impôt réel du spectateur. Illustrer l'effet de la décote sur un revenu fictif reste
  permis.
- Ne pas donner de seuil chiffré d'entrée dans l'impôt sans préciser l'année et la composition du foyer
  — il est revalorisé chaque année.
---

## Le mécanisme

Le barème progressif ne suffit pas à décrire l'entrée dans l'impôt. Une fois
l'impôt brut calculé, la **décote** de l'article 197, I, 4 en retranche une
fraction lorsque cet impôt reste inférieur à un plafond fixé chaque année.

La décote diminue à mesure que l'impôt brut augmente : elle est égale au plafond
diminué d'une fraction de l'impôt brut. Elle s'éteint donc progressivement, et
non d'un coup.

## Ce qui se joue vraiment

Son effet le plus important est aussi le moins visible : dans la zone où la
décote se résorbe, le **taux marginal réel** est bien supérieur au taux affiché.

Chaque euro de revenu supplémentaire produit à la fois de l'impôt selon le
barème et une réduction de la décote. Un foyer situé dans cette zone peut voir
son impôt augmenter de plusieurs dizaines d'euros pour cent euros de revenu
supplémentaire, alors qu'il se croit dans la tranche à 11 %.

C'est l'explication de la réaction fréquente : « j'ai eu une petite
augmentation et j'y ai perdu ». Le foyer n'y perd jamais en net, mais le taux
de prélèvement sur cette fraction est effectivement très élevé.

## Le point de vigilance

Les montants de la décote sont revalorisés chaque année par la loi de finances.
Tout seuil chiffré doit être daté, faute de quoi il devient faux au premier
janvier suivant.

La décote est appliquée automatiquement : elle ne se demande pas, elle ne se
coche pas. Ce qui se demande, en revanche, ce sont les éléments qui déterminent
le quotient familial et les charges déductibles — et c'est là que les erreurs
de déclaration coûtent réellement.
FILE:content/impot_revenu/prelevement_source.md
