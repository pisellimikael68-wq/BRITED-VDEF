---
id: ifi_dettes_deductibles
titre: Quelles dettes réduisent l'IFI
domaine: ifi
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 7
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- passif IFI
- dettes déductibles IFI
- réduire son IFI
resume: 'L''IFI se calcule sur la valeur nette du patrimoine immobilier : les dettes affectées à des biens
  taxables sont déductibles. Mais la liste est limitative, les prêts in fine sont retraités et un plafonnement
  s''applique aux gros patrimoines.'
sources:
- type: texte_legal
  ref: CGI, article 974 (dettes déductibles de l'assiette de l'IFI)
- type: texte_legal
  ref: CGI, article 964 (assiette de l'IFI)
- type: texte_legal
  ref: CGI, article 979 (plafonnement de l'IFI)
- type: bofip
  ref: BOI-PAT-IFI-20-30 (passif déductible)
  url: https://bofip.impots.gouv.fr/doctrine/BOI-PAT-IFI-20-30
  consulte_le: 2026-07-29
chiffres:
- cle: Seuil d'assujettissement à l'IFI
  valeur: 1 300 000
  unite: €
  source: 1
  commentaire: valeur nette du patrimoine immobilier au 1er janvier
- cle: Plafonnement de l'IFI par rapport aux revenus
  valeur: '75'
  unite: '%'
  source: 2
- cle: Abattement sur la résidence principale
  valeur: '30'
  unite: '%'
  source: 1
relations:
  regi_par:
  - ifi_seuil_declenchement
  complete_par:
  - holding_animatrice
  s_applique_a:
  - sci_is_ou_ir
erreurs_frequentes:
- Croire que toutes les dettes sont déductibles. Seules celles affectées à des actifs immobiliers taxables
  le sont, à l'exclusion notamment de certains prêts familiaux.
- Déduire l'intégralité d'un prêt in fine. Il est retraité comme s'il s'amortissait, pour éviter de maintenir
  artificiellement un passif constant.
- Oublier l'abattement de 30 % sur la résidence principale, qui réduit l'assiette avant même le calcul
  du passif.
- Croire que le seuil de 1 300 000 € est un abattement. Une fois franchi, le barème s'applique à partir
  de 800 000 €.
questions_clients:
- Mon crédit immobilier réduit-il mon IFI ?
- La résidence principale compte-t-elle dans l'IFI ?
- Un prêt familial est-il déductible ?
a_ne_pas_dire:
- Ne jamais calculer l'IFI réel du spectateur. Un exemple sur un patrimoine fictif, avec des montants
  ronds, reste permis.
- Ne pas suggérer de monter un passif artificiel pour réduire l'assiette — c'est précisément ce que les
  dispositifs anti-abus visent.
---

## Le mécanisme

L'IFI porte sur la valeur **nette** du patrimoine immobilier au 1er janvier :
actifs taxables moins dettes déductibles.

Encore faut-il que la dette soit déductible au sens de l'article 974 : elle doit
exister au 1er janvier, être à la charge personnelle du redevable, et surtout
être **affectée** à un actif immobilier compris dans l'assiette.

Un crédit qui a financé la résidence principale est déductible, mais dans la
même proportion que le bien est taxable — l'abattement de 30 % réduisant
l'assiette, il réduit aussi la fraction de dette admise.

## Ce qui se joue vraiment

Le législateur a fermé plusieurs voies d'optimisation qui existaient sous l'ISF.

Le **prêt in fine** est retraité : il est déduit comme s'il s'amortissait
linéairement sur sa durée. Un emprunt sans amortissement ne permet donc plus de
maintenir indéfiniment un passif au niveau du capital emprunté.

Les **prêts entre proches** et les prêts consentis par une société contrôlée
sont encadrés, voire écartés, pour éviter la création d'un passif de complaisance.

Un **mécanisme de plafonnement du passif** s'applique aux patrimoines importants
lorsque l'endettement dépasse une forte proportion de la valeur des biens.

## Le point de vigilance

Le seuil de 1 300 000 € n'est pas un abattement mais un déclencheur. Une fois
franchi, le barème progressif s'applique à partir de 800 000 €, ce qui crée un
effet de seuil marqué au passage.

Le plafonnement de l'article 979 limite la somme de l'IFI et de l'impôt sur le
revenu à 75 % des revenus de l'année précédente. C'est un mécanisme de
protection réel pour les patrimoines importants à faibles revenus, et il est
sous-utilisé faute d'être connu.
