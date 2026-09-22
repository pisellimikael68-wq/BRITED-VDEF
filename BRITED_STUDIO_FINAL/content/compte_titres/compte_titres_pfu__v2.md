---
id: compte_titres_pfu
version: 2
titre: Le PFU de 31,4 % n'est pas toujours le meilleur choix
domaine: compte_titres
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-08-27
alias: [PFU, flat tax, prélèvement forfaitaire unique, compte-titres]
resume: >-
  En 2026, les revenus mobiliers et plus-values de valeurs mobilières sont,
  sauf exception, soumis au PFU de 31,4 %, soit 12,8 % d'impôt sur le revenu
  et 18,6 % de prélèvements sociaux. L'option globale pour le barème progressif
  peut être plus favorable selon le foyer et la nature des revenus.
sources:
  - type: administration_fiscale
    ref: J'ai des valeurs mobilières, comment sont-elles imposées ?
    url: https://www.impots.gouv.fr/particulier/questions/jai-des-valeurs-mobilieres-comment-sont-elles-imposees
    consulte_le: 2026-08-27
  - type: administration_fiscale
    ref: J'ai réalisé une plus-value mobilière, comment est-elle imposée ?
    url: https://www.impots.gouv.fr/particulier/questions/jai-realise-une-plus-value-mobiliere-comment-est-elle-imposee
    consulte_le: 2026-08-27
  - type: administration_fiscale
    ref: Mes valeurs mobilières ouvrent-elles droit à abattement ?
    url: https://www.impots.gouv.fr/particulier/questions/mes-valeurs-mobilieres-ouvrent-elles-droit-abattement
    consulte_le: 2026-08-27
chiffres:
  - cle: Taux global du PFU en 2026
    valeur: "31,4"
    unite: "%"
    source: 0
  - cle: Part d'impôt sur le revenu
    valeur: "12,8"
    unite: "%"
    source: 0
  - cle: Part de prélèvements sociaux
    valeur: "18,6"
    unite: "%"
    source: 0
  - cle: Abattement sur les dividendes éligibles en cas d'option pour le barème
    valeur: "40"
    unite: "%"
    source: 2
relations:
  regi_par:
    - impot_revenu_tranche_marginale
  alternative_a:
    - pea_exoneration_5ans
  s_applique_a:
    - actions_dividende_et_propriete
    - obligations_risque_de_taux
erreurs_frequentes:
  - Croire que le PFU est nécessairement le choix le moins coûteux.
  - Oublier que l'option pour le barème est globale pour les revenus mobiliers et plus-values concernés du foyer.
  - Appliquer l'abattement de 40 % à tous les revenus ou aux prélèvements sociaux : il concerne uniquement les dividendes éligibles imposés au barème et ne réduit pas les prélèvements sociaux.
  - Confondre le compte-titres avec l'assurance-vie ou le PEA, qui suivent leurs régimes propres.
questions_clients:
  - Dois-je cocher la case 2OP pour le barème ?
  - Pourquoi le PFU représente-t-il 31,4 % en 2026 ?
  - L'abattement de 40 % réduit-il aussi les prélèvements sociaux ?
a_ne_pas_dire:
  - Ne pas recommander une option fiscale sans simulation globale du foyer.
---

## Le mécanisme

En 2026, les revenus de valeurs mobilières sont soumis, sauf exception, à un
prélèvement global de 31,4 % : 12,8 % au titre de l'impôt sur le revenu et
18,6 % au titre des prélèvements sociaux. Les plus-values mobilières sont
également soumises au PFU de 31,4 %, sauf option globale pour le barème.

## L'alternative du barème

Le contribuable peut opter, via la case 2OP de sa déclaration, pour le barème
progressif de l'impôt sur le revenu. Cette option concerne globalement les
revenus mobiliers et plus-values entrant dans son périmètre pour le foyer.

Les dividendes éligibles imposés au barème bénéficient d'un abattement de 40 %
pour le calcul de l'impôt sur le revenu. Cet abattement ne réduit pas l'assiette
des prélèvements sociaux, qui restent dus. Une fraction de la CSG peut être
déductible lorsque les revenus sont imposés au barème.

## Exemple pédagogique

Pour 1 000 € de dividendes éligibles :

- PFU : 128 € d'impôt sur le revenu et 186 € de prélèvements sociaux, soit 314 € ;
- barème à 11 % : base imposable de 600 € après l'abattement de 40 %, soit 66 €
  d'impôt, auxquels s'ajoutent 186 € de prélèvements sociaux, soit 252 € avant
  l'effet ultérieur de la CSG déductible.

Cet exemple est volontairement simplifié. Le choix dépend de l'ensemble des
revenus et plus-values concernés, de la tranche du foyer et des règles propres
à chaque revenu.
