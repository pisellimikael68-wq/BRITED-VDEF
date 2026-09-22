---
id: succession_bareme_droits
titre: Le barème des droits de succession en ligne directe
domaine: succession
type: regime_fiscal
statut: valide
difficulte: debutant
potentiel_viral: 9
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
  - droits de succession
  - combien on paie sur un héritage
  - barème succession enfant
resume: >-
  Après l'abattement de 100 000 € par parent et par enfant, la part taxable est
  soumise à un barème progressif qui monte de 5 % à 45 %. Les premières tranches
  sont douces : c'est au-delà de 552 324 € par enfant que le taux marginal
  atteint 45 %.
sources:
  - type: texte_legal
    ref: CGI, article 777 (tarif des droits de mutation à titre gratuit)
  - type: texte_legal
    ref: CGI, article 779, I (abattement en ligne directe)
  - type: bofip
    ref: BOI-ENR-DMTG-10-50-20 (tarifs et abattements)
    url: https://bofip.impots.gouv.fr/doctrine/BOI-ENR-DMTG-10-50-20
    consulte_le: 2026-07-29
chiffres:
  - cle: Abattement par parent et par enfant
    valeur: "100 000"
    unite: "€"
    source: 1
  - cle: Taux de la première tranche (jusqu'à 8 072 €)
    valeur: "5"
    unite: "%"
    source: 0
  - cle: Taux marginal le plus élevé en ligne directe
    valeur: "45"
    unite: "%"
    source: 0
  - cle: Seuil d'entrée dans la tranche à 45 %
    valeur: "1 805 677"
    unite: "€"
    source: 0
    commentaire: par part taxable après abattement
relations:
  regi_par:
    - donation_abattement_100000
  complete_par:
    - succession_reserve_hereditaire
erreurs_frequentes:
  - Croire que le taux affiché s'applique à tout l'héritage. Le barème est progressif par tranches : seule la fraction qui dépasse chaque seuil est taxée au taux supérieur.
  - Croire que le conjoint survivant paie des droits. Il en est totalement exonéré depuis la loi TEPA de 2007, de même que le partenaire de PACS.
  - Oublier que l'abattement est calculé par parent. Deux parents, c'est deux abattements de 100 000 € pour le même enfant.
  - Confondre l'abattement de 100 000 € en ligne directe avec celui, bien plus faible, applicable entre frères et sœurs, neveux ou tiers.
questions_clients:
  - Combien vont payer mes enfants sur ma succession ?
  - Est-ce que mon conjoint devra payer des droits ?
  - À partir de quel montant les droits deviennent-ils vraiment lourds ?
a_ne_pas_dire:
  - Ne jamais donner un taux unique « les droits de succession, c'est 20 % ». Le barème est progressif et le taux effectif dépend du montant.
  - Ne pas présenter la transmission comme un moyen d'échapper à l'impôt. Le sujet est l'anticipation, pas l'évitement.
---

## Le mécanisme

Les droits de succession ne se calculent pas sur le patrimoine du défunt mais
sur **la part reçue par chaque héritier**, après application de son abattement
personnel.

Pour un enfant, cet abattement est de 100 000 € par parent (CGI, art. 779, I).
Ce qui dépasse entre dans un barème progressif par tranches (CGI, art. 777) :
5 % sur les premiers milliers d'euros, puis 10 %, 15 %, 20 % sur une très large
tranche intermédiaire, puis 30 %, 40 % et enfin 45 %.

La tranche à 20 % est la plus importante en pratique : elle couvre l'essentiel
des successions ordinaires. Les taux de 40 % et 45 % ne concernent que les parts
individuelles supérieures à plusieurs centaines de milliers d'euros.

## Ce qui se joue vraiment

Le barème étant **progressif et par héritier**, deux leviers réduisent la
facture sans aucun montage : augmenter le nombre de bénéficiaires, et étaler
dans le temps.

Une succession de 600 000 € reçue par un enfant unique est bien plus taxée que
la même somme partagée entre trois enfants : chacun consomme son propre
abattement puis remonte le barème depuis le bas.

## Le point de vigilance

Le conjoint survivant et le partenaire de PACS sont **totalement exonérés** de
droits de succession. Cette exonération ne s'étend pas au concubin, qui est
traité comme un tiers — avec le taux le plus défavorable du barème.

Les donations consenties depuis moins de quinze ans sont réintégrées dans le
calcul (rappel fiscal de l'article 784) : elles consomment l'abattement et
poussent la part taxable vers les tranches hautes.
FILE:content/succession/reserve_hereditaire.md
