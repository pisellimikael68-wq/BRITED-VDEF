---
id: ifi_seuil_declenchement
titre: L'IFI se déclenche à 1,3 million mais se calcule dès 800 000 €
domaine: ifi
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [IFI, impôt sur la fortune immobilière, ISF]
resume: >-
  L'IFI ne frappe que le patrimoine immobilier net. Il se déclenche au-delà de
  1 300 000 €, mais le barème s'applique alors dès 800 000 €. La résidence
  principale bénéficie d'un abattement de 30 %.
sources:
  - type: texte_legal
    ref: CGI, article 964 (champ d'application)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036364476
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 977 (barème)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036364746
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 973 (abattement résidence principale)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000036364513
    consulte_le: 2026-07-27
chiffres:
  - cle: Seuil de déclenchement
    valeur: "1 300 000"
    unite: "€"
    source: 0
  - cle: Début effectif du barème une fois le seuil franchi
    valeur: "800 000"
    unite: "€"
    source: 1
  - cle: Abattement sur la résidence principale
    valeur: "30"
    unite: "%"
    source: 2
  - cle: Date d'appréciation du patrimoine
    valeur: "1er janvier"
    source: 0
relations:
  s_applique_a:
    - immobilier_plus_value_residence_principale
    - sci_is_ou_ir
    - scpi_frais_et_liquidite
  alternative_a:
    - or_fiscalite_metaux_precieux
  complete_par:
    - demembrement_bareme_669
erreurs_frequentes:
  - Croire que l'IFI porte sur tout le patrimoine. Les placements financiers, l'assurance-vie en unités de compte non immobilières et les liquidités en sont exclus.
  - Oublier de déduire les dettes. L'IFI porte sur le patrimoine immobilier NET, capital restant dû des crédits déduit.
  - Croire qu'en dépassant 1 300 000 € on n'est taxé que sur l'excédent. Le barème repart à 800 000 €.
  - Oublier l'abattement de 30 % sur la résidence principale, qui fait souvent passer sous le seuil.
questions_clients:
  - Mon appartement me rend-il redevable de l'IFI ?
  - Mon crédit compte-t-il ?
  - Ma résidence principale est-elle comptée en totalité ?
a_ne_pas_dire:
  - Ne pas laisser croire que l'IFI concerne l'épargne financière : il ne vise que l'immobilier.
---

## Le mécanisme

L'IFI vise le patrimoine **immobilier net** du foyer fiscal, apprécié au
1er janvier. Sont déduites les dettes affectées aux biens imposables,
notamment le capital restant dû des crédits.

Le seuil d'assujettissement est de 1 300 000 €. Mais une fois franchi, le
barème progressif de l'article 977 s'applique **à partir de 800 000 €**, ce qui
crée un effet de seuil brutal.

## Ce qui se joue vraiment

L'abattement de 30 % sur la résidence principale est le paramètre le plus
décisif pour un patrimoine moyen. Une résidence principale de 900 000 € n'entre
dans l'assiette que pour 630 000 €. Beaucoup de foyers qui se croient concernés
ne le sont pas.

## Le point de vigilance

L'endettement change tout. Un patrimoine immobilier de 1 500 000 € financé par
400 000 € de crédit restant dû se situe sous le seuil. C'est la raison pour
laquelle l'IFI se calcule chaque année et non une fois pour toutes.
