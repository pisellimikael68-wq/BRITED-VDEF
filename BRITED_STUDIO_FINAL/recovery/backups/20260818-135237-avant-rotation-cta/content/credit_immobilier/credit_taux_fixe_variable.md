---
id: credit_taux_fixe_variable
titre: Taux fixe, variable, ou mixte
domaine: credit_immobilier
type: notion
statut: valide
difficulte: intermediaire
potentiel_viral: 7
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- taux fixe ou variable
- taux capé
- crédit à taux révisable
resume: Le taux fixe fige la mensualité et le coût total pour toute la durée du prêt. Le taux variable
  suit un indice de référence et n'est acceptable qu'assorti d'un plafond de variation. Le choix porte
  sur la répartition du risque de taux, pas sur une prévision.
sources:
- type: texte_legal
  ref: Code de la consommation, article L. 313-25 (mentions de l'offre de prêt)
- type: texte_legal
  ref: Code de la consommation, article L. 313-46 (information annuelle en cas de taux variable)
- type: administration
  ref: Banque de France — taux d'usure et crédit immobilier
  url: https://www.banque-france.fr
  consulte_le: 2026-07-29
chiffres:
- cle: Durée de validité minimale d'une offre de prêt
  valeur: '30'
  unite: jours
  source: 0
- cle: Délai de réflexion obligatoire avant acceptation
  valeur: '10'
  unite: jours
  source: 0
relations:
  complete_par:
  - credit_remboursement_anticipe
  - credit_assurance_emprunteur_lemoine
  alternative_a:
  - credit_remboursement_anticipe
  regi_par:
  - credit_capacite_emprunt
erreurs_frequentes:
- Accepter un taux variable non capé. Sans plafond de variation, la mensualité ou la durée peuvent augmenter
  sans limite contractuelle.
- Comparer un taux fixe et un taux variable sur le seul taux de départ, alors que le second est par construction
  plus bas à l'origine.
- Croire que le cap protège la mensualité. Selon le contrat, la variation joue sur la durée du prêt plutôt
  que sur la mensualité, ce qui déplace le risque au lieu de le supprimer.
- Ignorer le taux annuel effectif global, seul indicateur qui intègre assurance, frais de dossier et garantie.
questions_clients:
- Faut-il prendre un taux fixe ou variable ?
- Qu'est-ce qu'un taux capé plus un ?
- Puis-je passer d'un taux variable à un taux fixe ?
a_ne_pas_dire:
- Ne jamais dire au spectateur quel type de taux prendre, ni anticiper l'évolution des taux. Comparer
  les deux sur un emprunt fictif reste permis.
- Ne pas présenter le taux variable comme moins cher — il est seulement moins cher au départ, en échange
  d'un risque transféré à l'emprunteur.
---

## Le mécanisme

Un crédit à **taux fixe** conserve le même taux pendant toute sa durée. La
mensualité et le coût total sont connus dès la signature. La banque supporte
intégralement le risque d'évolution des taux.

Un crédit à **taux variable** est indexé sur un indice de référence, révisé
périodiquement. Le taux de départ est plus bas, mais le risque d'évolution est
transféré à l'emprunteur.

Le **taux capé** est un taux variable assorti d'un plafond de variation, en
général exprimé en points par rapport au taux initial. Un « capé +1 » ne peut
dépasser le taux d'origine augmenté d'un point.

Les formules **mixtes** appliquent un taux fixe pendant les premières années,
puis basculent en variable.

## Ce qui se joue vraiment

Le choix n'est pas un pari sur l'évolution des taux, que personne ne connaît. Il
porte sur la question de savoir **qui porte le risque** et si l'emprunteur a les
moyens de l'absorber.

Un ménage dont le taux d'effort est déjà tendu n'a pas de marge pour une
mensualité qui augmente : le taux fixe achète une certitude, et cette certitude
a un prix, visible dans l'écart de taux de départ.

Un investisseur disposant d'une épargne de sécurité et d'un horizon court peut
raisonnablement accepter un variable capé.

## Le point de vigilance

Le mécanisme d'ajustement compte autant que le cap. Certains contrats font
varier la **mensualité**, d'autres la **durée** du prêt. Un contrat qui allonge
la durée protège le budget mensuel mais peut prolonger l'emprunt de plusieurs
années, avec un coût total nettement supérieur — et la durée d'allongement est
elle-même souvent plafonnée, ce qui fait resurgir la hausse de mensualité.

Enfin, le seul chiffre comparable d'une offre à l'autre est le taux annuel
effectif global, qui intègre l'assurance emprunteur, les frais de dossier et la
garantie. Comparer deux taux nominaux ne compare rien.
