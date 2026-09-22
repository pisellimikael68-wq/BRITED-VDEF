---
id: compte_titres_pfu
titre: La flat tax de 30 % n'est pas toujours le meilleur choix
domaine: compte_titres
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [PFU, flat tax, prélèvement forfaitaire unique, compte-titres]
resume: >-
  Les revenus du capital sont taxés à 30 %, soit 12,8 % d'impôt et 17,2 % de
  prélèvements sociaux. Mais l'option pour le barème progressif reste possible
  et devient favorable dans les tranches basses.
sources:
  - type: texte_legal
    ref: CGI, article 200 A
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041464718
    consulte_le: 2026-07-27
  - type: bofip
    ref: BOI-RPPM-RCM-20-15
    url: https://bofip.impots.gouv.fr/doctrine/BOI-RPPM-RCM-20-15
    consulte_le: 2026-07-27
chiffres:
  - cle: Taux global du PFU
    valeur: "30"
    unite: "%"
    source: 0
  - cle: Part d'impôt sur le revenu
    valeur: "12,8"
    unite: "%"
    source: 0
  - cle: Part de prélèvements sociaux
    valeur: "17,2"
    unite: "%"
    source: 0
  - cle: Abattement sur dividendes en cas d'option pour le barème
    valeur: "40"
    unite: "%"
    source: 0
relations:
  regi_par:
    - impot_revenu_tranche_marginale
  alternative_a:
    - pea_exoneration_5ans
  s_applique_a:
    - actions_dividende_et_propriete
    - obligations_risque_de_taux
    - cryptoactifs_fiscalite_cessions
erreurs_frequentes:
  - Croire que le PFU est obligatoire. L'option pour le barème progressif reste ouverte chaque année.
  - Oublier que l'option pour le barème est globale : elle s'applique à tous les revenus du capital du foyer, pas au choix.
  - Subir le PFU en tranche à 0 % ou 11 %, alors que le barème serait moins coûteux.
  - Confondre le PFU avec la fiscalité de l'assurance-vie ou du PEA, qui ont leurs régimes propres.
questions_clients:
  - Dois-je cocher la case pour le barème ?
  - Pourquoi ma banque a-t-elle prélevé 30 % ?
  - Le PEA est-il concerné par la flat tax ?
a_ne_pas_dire:
  - Ne pas recommander une option fiscale sans préciser qu'elle est globale et dépend de la situation du foyer.
---

## Le mécanisme

Depuis 2018, les revenus du capital — dividendes, intérêts, plus-values de
cession de valeurs mobilières — sont soumis par défaut au prélèvement
forfaitaire unique de 30 %, qui recouvre 12,8 % d'impôt et 17,2 % de
prélèvements sociaux.

Le contribuable peut cependant opter pour l'imposition au barème progressif,
en cochant une case sur sa déclaration.

## Ce qui se joue vraiment

Le PFU est défavorable dans les tranches basses. Un foyer en tranche à 0 % ou
11 % paie 12,8 % d'impôt là où le barème lui coûterait 0 % ou 11 %, avec en
prime un abattement de 40 % sur les dividendes que le PFU ne permet pas.

Le calcul s'inverse à partir de la tranche à 30 %, où le PFU devient
avantageux.

## Le point de vigilance

L'option est **globale et annuelle** : elle s'applique à l'ensemble des revenus
du capital du foyer pour l'année, sans possibilité de la réserver à certains
revenus. Elle se simule avant de se cocher.
### content/actions/dividende_et_propriete.md
