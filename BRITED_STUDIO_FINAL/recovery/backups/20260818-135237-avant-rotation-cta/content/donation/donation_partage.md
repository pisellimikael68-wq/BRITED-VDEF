---
id: donation_partage
titre: La donation-partage fige les valeurs et évite la dispute au décès
domaine: donation
type: strategie
statut: valide
difficulte: intermediaire
potentiel_viral: 9
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [donation-partage, rapport des donations, partage anticipé]
resume: >-
  Une donation simple est réévaluée au décès, ce qui déséquilibre le partage si
  les biens ont évolué différemment. La donation-partage fige les valeurs au
  jour de l'acte, à condition que tous les héritiers réservataires y
  participent.
sources:
  - type: texte_legal
    ref: Code civil, article 1075 (donation-partage)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006436124
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: Code civil, article 1078 (évaluation figée au jour de l'acte)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006436137
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: Code civil, article 860 (rapport des donations simples)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006433072
    consulte_le: 2026-07-27
chiffres:
  - cle: Date d'évaluation en donation-partage
    valeur: "jour de l'acte"
    source: 1
  - cle: Date d'évaluation d'une donation simple
    valeur: "jour du décès"
    source: 2
  - cle: Condition de l'effet de figement
    valeur: "participation de tous les héritiers réservataires"
    source: 1
  - cle: Forme obligatoire
    valeur: "acte notarié"
    source: 0
relations:
  complete_par:
    - donation_abattement_100000
    - demembrement_bareme_669
  prerequis_de:
    - gouvernance_familiale_pacte
erreurs_frequentes:
  - Croire qu'une donation simple règle définitivement le partage. Elle est réévaluée au décès, ce qui peut tout rouvrir.
  - Omettre un héritier réservataire, ce qui fait perdre l'effet de figement des valeurs.
  - Croire que la donation-partage échappe aux droits de donation. Elle suit le régime fiscal ordinaire, abattements compris.
  - Attribuer des lots très inégaux sans soulte, ce qui ramène le déséquilibre au moment du décès.
questions_clients:
  - Quelle différence avec une donation classique ?
  - Faut-il que tous mes enfants soient d'accord ?
  - Et si un bien prend beaucoup de valeur après ?
a_ne_pas_dire:
  - Ne pas présenter la donation-partage comme un avantage fiscal : elle est civile, pas fiscale.
---

## Le mécanisme

Une donation simple n'est pas définitive dans ses effets. Au décès du donateur,
elle est **rapportée** à la succession pour la valeur du bien **au jour du
décès**, afin de vérifier l'égalité entre héritiers.

La donation-partage fonctionne autrement : elle attribue immédiatement des lots
et, si tous les héritiers réservataires y participent, les valeurs sont
**figées au jour de l'acte**.

## Ce qui se joue vraiment

L'écart apparaît avec le temps. Un parent donne un appartement de 200 000 € à
l'un et 200 000 € de titres à l'autre. Vingt ans plus tard, l'appartement en
vaut 400 000, les titres 250 000.

En donation simple, le partage se refait sur ces valeurs actualisées et le
premier enfant doit compenser. En donation-partage, chacun garde ce qu'il a
reçu : la question ne se pose pas.

C'est ce qui en fait moins un outil fiscal qu'un outil de **paix familiale** —
elle supprime la source de contentieux la plus fréquente entre frères et sœurs.

## Le point de vigilance

L'effet de figement suppose que **tous** les héritiers réservataires soient
présents à l'acte et reçoivent un lot. Un enfant oublié, et la donation-partage
retombe au régime de la donation simple avec réévaluation. L'acte notarié est
obligatoire.
FILE:content/donation/don_familial_790g.md
