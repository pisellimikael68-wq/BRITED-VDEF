---
id: succession_conjoint_exoneration
titre: Le conjoint survivant ne paie aucun droit de succession
domaine: succession
type: regime_fiscal
statut: valide
difficulte: debutant
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias:
  - droits de succession conjoint
  - veuf veuve impôt
  - loi TEPA succession
resume: >-
  Depuis 2007, le conjoint marié survivant et le partenaire de PACS sont
  totalement exonérés de droits de succession, sans plafond. Le concubin,
  lui, est taxé à 60 %.
sources:
  - type: texte_legal
    ref: CGI, article 796-0 bis
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006305556
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 777 (barème des droits de succession)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041464745
    consulte_le: 2026-07-27
  - type: bofip
    ref: BOI-ENR-DMTG-10-50-20
    url: https://bofip.impots.gouv.fr/doctrine/BOI-ENR-DMTG-10-50-20
    consulte_le: 2026-07-27
chiffres:
  - cle: Droits de succession dus par le conjoint marié
    valeur: "0"
    unite: "€"
    source: 0
  - cle: Droits de succession dus par le partenaire de PACS
    valeur: "0"
    unite: "€"
    source: 0
    commentaire: exonération conditionnée à la présence d'un testament
  - cle: Taux applicable entre concubins
    valeur: "60"
    unite: "%"
    source: 1
relations:
  complete_par:
    - transmission_cout_inaction
    - indivision_regle_unanimite
  prerequis_de:
    - donation_abattement_100000
erreurs_frequentes:
  - Croire que le PACS suffit à hériter. Le partenaire pacsé est exonéré de droits, mais il n'est pas héritier légal : sans testament, il ne reçoit rien.
  - Croire que le concubin est traité comme un conjoint. Il est taxé à 60 %, le taux applicable aux personnes non parentes.
  - Croire que l'exonération dispense de régler la succession : elle porte sur les droits, pas sur la liquidation.
questions_clients:
  - Mon conjoint devra-t-il payer des droits sur la maison ?
  - Le PACS protège-t-il autant que le mariage ?
  - Ma compagne peut-elle rester dans le logement si je décède ?
a_ne_pas_dire:
  - Ne jamais laisser entendre que le PACS équivaut au mariage en matière successorale. La différence, sans testament, est totale.
---

## Le mécanisme

L'article 796-0 bis du CGI, issu de la loi TEPA de 2007, exonère totalement de
droits de succession le conjoint survivant et le partenaire lié par un PACS.
L'exonération est **sans plafond** : elle porte sur l'intégralité de ce que le
survivant recueille.

## Ce qui se joue vraiment

L'exonération fiscale et la qualité d'héritier sont deux choses différentes, et
c'est là que se situe le piège.

Le conjoint marié est héritier de plein droit. Le partenaire de PACS ne l'est
pas : il est exonéré de droits, mais il ne reçoit rien s'il n'a pas été
institué légataire par testament. Un couple pacsé sans testament laisse donc le
survivant sans droit sur le patrimoine du défunt, alors même qu'il n'aurait
rien payé.

Le concubin, lui, cumule les deux désavantages : il n'hérite pas, et s'il reçoit
quelque chose par testament, il est taxé à 60 %.

## Le point de vigilance

Sur une maison de 300 000 € transmise à une compagne non pacsée par testament,
les droits atteignent environ 180 000 €. Dans la majorité des cas, elle doit
vendre le bien pour payer l'impôt sur ce bien.
FILE:content/succession/bareme_droits.md
