---
id: location_meublee_micro_bic
titre: Louer meublé change complètement la fiscalité des loyers
domaine: location_meublee
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias:
  - LMNP
  - micro-BIC
  - location meublée non professionnelle
resume: >-
  Les loyers d'un meublé relèvent des BIC et non des revenus fonciers. Le
  régime micro-BIC applique un abattement forfaitaire sur les recettes, très
  supérieur à celui du micro-foncier applicable au nu.
sources:
  - type: texte_legal
    ref: CGI, article 50-0 (régime micro-BIC)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047982540
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 32 (micro-foncier, location nue)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041464595
    consulte_le: 2026-07-27
  - type: bofip
    ref: BOI-BIC-CHAMP-40-20
    url: https://bofip.impots.gouv.fr/doctrine/BOI-BIC-CHAMP-40-20
    consulte_le: 2026-07-27
chiffres:
  - cle: Abattement micro-foncier, location nue
    valeur: "30"
    unite: "%"
    source: 1
  - cle: Abattement micro-BIC, meublé classique
    valeur: "50"
    unite: "%"
    source: 0
    a_verifier: true
    commentaire: les taux et seuils des meublés de tourisme ont été modifiés récemment, vérifier la catégorie exacte
  - cle: Seuil du régime micro-BIC, meublé classique
    valeur: "77 700"
    unite: "€"
    source: 0
    a_verifier: true
relations:
  regi_par:
    - impot_revenu_tranche_marginale
  alternative_a:
    - scpi_frais_et_liquidite
    - immobilier_plus_value_residence_principale
    - compte_titres_pfu
  complete_par:
    - sci_is_ou_ir
erreurs_frequentes:
  - Croire que meublé et nu relèvent du même régime. Le meublé est un BIC, le nu un revenu foncier : deux fiscalités distinctes.
  - Rester au micro par défaut alors que le régime réel, qui permet d'amortir le bien, est souvent plus favorable dès qu'il y a un crédit.
  - Confondre location meublée classique et meublé de tourisme : les taux et seuils diffèrent et ont changé récemment.
  - Oublier que le statut impose des obligations déclaratives propres, dont l'immatriculation de l'activité.
questions_clients:
  - Vaut-il mieux louer meublé ou vide ?
  - Dois-je créer une société pour louer en meublé ?
  - Le micro ou le réel ?
a_ne_pas_dire:
  - Ne pas énoncer les taux et seuils des meublés de tourisme sans vérification : ils ont été modifiés récemment et diffèrent du meublé classique.
  - Ne pas présenter l'amortissement comme un gain définitif : il est réintégré dans le calcul de la plus-value depuis les évolutions récentes.
---

## Le mécanisme

Louer un logement vide produit des **revenus fonciers**. Le louer meublé produit
des **bénéfices industriels et commerciaux**. Ce n'est pas une nuance
administrative : les deux régimes n'ont ni les mêmes abattements, ni les mêmes
charges déductibles, ni les mêmes obligations.

En micro, l'abattement forfaitaire du meublé classique est nettement supérieur
à celui de la location nue.

## Ce qui se joue vraiment

Le micro n'est pourtant pas toujours le bon choix. Le régime réel permet de
déduire les charges effectives et surtout d'**amortir** le bien, c'est-à-dire
d'en déduire chaque année une fraction de la valeur. Dès qu'il existe un crédit
et des travaux, le réel efface souvent la totalité du revenu imposable pendant
plusieurs années, là où le micro laisse la moitié des loyers taxable.

Le choix se fait donc au cas par cas, en comparant charges réelles et
abattement forfaitaire.

## Le point de vigilance

La catégorie exacte du bien détermine tout. Meublé classique, meublé de
tourisme classé et meublé de tourisme non classé n'ont ni les mêmes taux ni les
mêmes seuils, et ces paramètres ont été modifiés récemment. Aucun chiffre ne
doit être diffusé sans avoir identifié la catégorie et vérifié le texte en
vigueur.
