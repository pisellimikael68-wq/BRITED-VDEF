---
id: immobilier_deficit_foncier
titre: Les travaux d'un bien locatif se déduisent de votre salaire
domaine: immobilier
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 9
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [déficit foncier, travaux déductibles, revenus fonciers, régime réel]
resume: >-
  Quand les charges d'un bien loué nu dépassent les loyers, le déficit
  s'impute sur le revenu global dans la limite de 10 700 € par an. C'est l'un
  des rares dispositifs qui réduit l'impôt sur le salaire sans plafonnement des
  niches fiscales.
sources:
  - type: texte_legal
    ref: CGI, article 156, I, 3° (imputation du déficit foncier)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041465003
    consulte_le: 2026-07-27
  - type: bofip
    ref: BOI-RFPI-BASE-30-20
    url: https://bofip.impots.gouv.fr/doctrine/BOI-RFPI-BASE-30-20
    consulte_le: 2026-07-27
chiffres:
  - cle: Plafond d'imputation annuelle sur le revenu global
    valeur: "10 700"
    unite: "€"
    source: 0
  - cle: Report de l'excédent sur les revenus fonciers
    valeur: "10"
    unite: "ans"
    source: 0
  - cle: Engagement de location après imputation
    valeur: "3"
    unite: "ans"
    source: 0
  - cle: Plafond majoré pour travaux de rénovation énergétique
    valeur: "21 400"
    unite: "€"
    source: 0
    a_verifier: true
    commentaire: dispositif temporaire, vérifier s'il est encore en vigueur pour l'année concernée
relations:
  complete_par:
    - immobilier_plus_value_duree_detention
  alternative_a:
    - location_meublee_micro_bic
  regi_par:
    - impot_revenu_tranche_marginale
erreurs_frequentes:
  - Croire que tous les travaux sont déductibles. Les travaux de construction, reconstruction ou agrandissement ne le sont pas.
  - Croire que les intérêts d'emprunt s'imputent sur le revenu global. Ils ne s'imputent que sur les revenus fonciers.
  - Oublier l'obligation de louer le bien trois ans après l'imputation, sous peine de remise en cause.
  - Appliquer le dispositif à une location meublée, qui relève des BIC et non des revenus fonciers.
questions_clients:
  - Mes travaux vont-ils réduire mes impôts ?
  - Quelle différence entre entretien et rénovation ?
  - Et si je revends avant trois ans ?
a_ne_pas_dire:
  - Ne pas présenter le déficit foncier comme applicable au meublé : il ne concerne que la location nue.
  - Ne pas citer le plafond majoré sans avoir vérifié qu'il est encore applicable.
---

## Le mécanisme

Un bien loué nu relève des revenus fonciers. Au régime réel, toutes les charges
sont déductibles : entretien, réparation, amélioration, taxe foncière,
assurance, intérêts d'emprunt.

Lorsque ces charges dépassent les loyers, le **déficit** s'impute sur le revenu
global — salaires compris — dans la limite de 10 700 € par an. L'excédent, et
la part correspondant aux intérêts d'emprunt, se reportent dix ans sur les seuls
revenus fonciers.

## Ce qui se joue vraiment

C'est un des rares mécanismes qui réduit l'impôt sur le salaire et qui échappe
au plafonnement global des niches fiscales, parce qu'il ne s'agit pas d'une
réduction d'impôt mais d'une charge réelle.

Pour un contribuable en tranche à 41 %, 10 700 € de déficit représentent environ
4 400 € d'impôt en moins, plus l'effet sur les prélèvements sociaux des revenus
fonciers.

## Le point de vigilance

Deux limites. La nature des travaux d'abord : entretien, réparation et
amélioration sont déductibles, la construction, la reconstruction et
l'agrandissement ne le sont pas, et la frontière est régulièrement contestée.

L'engagement ensuite : le bien doit rester loué jusqu'au 31 décembre de la
troisième année suivant l'imputation. Une vente ou une reprise anticipée
entraîne la remise en cause.
scripts/_journal.jsonl
scripts/credit_immobilier/credit_capacite_emprunt__multi__a1.md
scripts/credit_immobilier/credit_capacite_emprunt__multi__a2.md
scripts/credit_immobilier/credit_capacite_emprunt__multi__a3.md
scripts/credit_immobilier/credit_capacite_emprunt__multi__a4.md
scripts/immobilier/immobilier_deficit_foncier__multi__a1.md
scripts/immobilier/immobilier_deficit_foncier__multi__a2.md
scripts/immobilier/immobilier_deficit_foncier__multi__a3.md
scripts/immobilier/immobilier_deficit_foncier__multi__a4.md
scripts/livret_a/livret_a_plafonds__multi__a1.md
scripts/livret_a/livret_a_plafonds__multi__a2.md
scripts/livret_a/livret_a_plafonds__multi__a3.md
scripts/livret_a/livret_a_plafonds__multi__a4.md
scripts/location_meublee/location_meublee_micro_bic__multi__a1.md
scripts/location_meublee/location_meublee_micro_bic__multi__a2.md
scripts/location_meublee/location_meublee_micro_bic__multi__a3.md
scripts/location_meublee/location_meublee_micro_bic__multi__a4.md
