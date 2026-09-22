---
id: immobilier_revenus_fonciers_micro
titre: "Micro-foncier ou réel : le seuil qui décide"
domaine: immobilier
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
  - micro foncier
  - régime réel foncier
  - déficit foncier
resume: >-
  En location nue, le micro-foncier applique un abattement forfaitaire de 30 %
  jusqu'à 15 000 € de loyers. Le régime réel déduit les charges effectives et
  ouvre le déficit foncier, imputable sur le revenu global dans une limite
  annuelle.
sources:
  - type: texte_legal
    ref: CGI, article 32 (régime micro-foncier)
  - type: texte_legal
    ref: CGI, article 31 (charges déductibles des revenus fonciers)
  - type: texte_legal
    ref: CGI, article 156, I, 3° (imputation du déficit foncier)
  - type: bofip
    ref: BOI-RFPI-BASE-30-20 (charges déductibles)
    url: https://bofip.impots.gouv.fr/doctrine/BOI-RFPI-BASE-30-20
    consulte_le: 2026-07-29
chiffres:
  - cle: Plafond de loyers du micro-foncier
    valeur: "15 000"
    unite: "€"
    source: 0
    commentaire: revenus bruts fonciers annuels du foyer
  - cle: Abattement forfaitaire du micro-foncier
    valeur: "30"
    unite: "%"
    source: 0
  - cle: Plafond annuel d'imputation du déficit foncier sur le revenu global
    valeur: "10 700"
    unite: "€"
    source: 2
  - cle: Durée d'engagement de location après imputation d'un déficit
    valeur: "3"
    unite: "ans"
    source: 2
relations:
  complete_par:
    - location_meublee_reel_amortissement
    - immobilier_dpe_location
erreurs_frequentes:
  - Rester au micro-foncier par défaut alors que les charges réelles dépassent 30 % des loyers, ce qui est courant dès qu'il y a un emprunt.
  - Croire que les intérêts d'emprunt créent du déficit imputable sur le revenu global. La fraction de déficit provenant des intérêts ne s'impute que sur les revenus fonciers.
  - Croire que l'option pour le réel se révoque librement. Elle engage pour trois ans.
  - Oublier que l'imputation d'un déficit sur le revenu global impose de continuer à louer le bien pendant trois ans, sous peine de remise en cause.
questions_clients:
  - Dois-je choisir le micro-foncier ou le réel ?
  - Pourquoi mes travaux ne réduisent pas mon impôt autant que prévu ?
  - Le déficit foncier réduit-il mes impôts sur mon salaire ?
a_ne_pas_dire:
  - Ne jamais dire au spectateur quel régime choisir. Comparer les deux sur un cas fictif chiffré reste permis.
  - Ne pas présenter le déficit foncier comme une niche : c'est la déduction de charges réellement supportées.
---

## Le mécanisme

La location nue relève des revenus fonciers, avec deux régimes.

Le **micro-foncier** s'applique de plein droit si les revenus fonciers bruts du
foyer ne dépassent pas 15 000 € : un abattement de 30 % couvre forfaitairement
toutes les charges, sans justificatif ni comptabilité.

Le **régime réel** déduit les charges effectives listées à l'article 31 :
intérêts d'emprunt, travaux d'entretien et de réparation, taxe foncière, primes
d'assurance, frais de gestion, provisions de copropriété.

## Ce qui se joue vraiment

L'arbitrage se ramène à une comparaison : les charges réelles dépassent-elles
30 % des loyers ? Dès qu'il y a un crédit en cours ou des travaux, la réponse
est presque toujours oui.

Quand les charges dépassent les loyers, le régime réel produit un **déficit
foncier**. Celui-ci s'impute sur le revenu global — salaires compris — dans la
limite de 10 700 € par an, le surplus étant reportable sur les revenus fonciers
des dix années suivantes.

## Le point de vigilance

Une distinction technique change tout : la part du déficit provenant des
**intérêts d'emprunt** ne s'impute jamais sur le revenu global. Elle reste
cantonnée aux revenus fonciers. Seules les autres charges — travaux au premier
chef — ouvrent l'imputation sur le salaire.

Et l'imputation n'est pas définitive tant qu'une condition n'est pas tenue : le
bien doit rester loué jusqu'au 31 décembre de la troisième année suivante. Une
vente ou une reprise pour usage personnel entraîne la remise en cause de
l'avantage.
