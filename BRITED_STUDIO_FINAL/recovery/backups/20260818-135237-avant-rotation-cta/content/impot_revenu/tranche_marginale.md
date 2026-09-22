---
id: impot_revenu_tranche_marginale
titre: Passer dans la tranche supérieure ne fait jamais perdre d'argent
domaine: impot_revenu
type: notion
statut: valide
difficulte: debutant
potentiel_viral: 10
cree_le: 2026-07-27
revise_le: 2026-07-27
alias:
  - tranche marginale d'imposition
  - TMI
  - changer de tranche
  - barème progressif
resume: >-
  L'idée qu'une augmentation peut faire baisser le revenu net est fausse. Le
  barème français est progressif par tranches : seule la fraction du revenu qui
  dépasse le seuil est taxée au taux supérieur, jamais la totalité.
sources:
  - type: texte_legal
    ref: CGI, article 197
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047620877
    consulte_le: 2026-07-27
  - type: bofip
    ref: BOI-IR-LIQ-20-20-10
    url: https://bofip.impots.gouv.fr/doctrine/BOI-IR-LIQ-20-20-10
    consulte_le: 2026-07-27
  - type: administration
    ref: DGFiP — simulateur officiel de l'impôt sur le revenu
    url: https://www.impots.gouv.fr/simulateurs
    consulte_le: 2026-07-27
chiffres:
  - cle: Taux des tranches du barème
    valeur: "0, 11, 30, 41 et 45"
    unite: "%"
    source: 0
  - cle: Seuils du barème 2026 (revenus 2025)
    valeur: "11 600 / 29 579 / 84 577 / 181 917"
    unite: "€ par part"
    source: 0
    valide_du: 2026-01-01
    valide_au: 2026-12-31
    commentaire: revalorisés de 0,9 % par la loi de finances 2026, vérifiés le 2026-07-27
  - cle: Impôt supplémentaire sur 1 000 € gagnés en tranche à 30 %
    valeur: "300"
    unite: "€"
    source: 0
    commentaire: il reste donc 700 € nets, jamais moins qu'avant
relations:
  prerequis_de:
    - per_deduction_versements
    - fiscalite_quotient_familial
    - compte_titres_pfu
    - location_meublee_micro_bic
erreurs_frequentes:
  - Croire qu'un revenu supplémentaire est taxé en totalité au taux de la nouvelle tranche. Seule la fraction qui dépasse le seuil l'est.
  - Refuser une augmentation ou des heures supplémentaires « pour ne pas changer de tranche ». Mathématiquement, le net augmente toujours.
  - Confondre taux marginal et taux moyen. Un foyer en tranche à 30 % paie en réalité bien moins de 30 % de ses revenus.
  - Confondre le barème de l'impôt, qui ne comporte aucun effet de seuil défavorable, et les prestations sociales sous condition de ressources, qui en comportent de réels.
  - Croire que le taux du prélèvement à la source est la tranche marginale. C'est un taux moyen.
questions_clients:
  - Si j'accepte cette augmentation, est-ce que je vais y perdre ?
  - Mes heures supplémentaires vont-elles me faire changer de tranche ?
  - Pourquoi mon taux de prélèvement à la source est-il différent de ma tranche ?
a_ne_pas_dire:
  - Ne jamais citer de seuil de tranche sans avoir vérifié le barème de l'année en cours : ils sont revalorisés chaque année.
  - Ne pas confondre les taux du barème avec le taux du prélèvement forfaitaire unique.
---

## Le mécanisme

Le barème de l'article 197 du CGI découpe le revenu imposable en tranches
successives. Chaque tranche a son propre taux, et ce taux ne s'applique **qu'à
la part du revenu comprise dans cette tranche**.

Une personne dont le revenu dépasse de 500 € le seuil d'entrée dans la tranche
à 30 % ne paie pas 30 % de tout son revenu. Elle paie 30 % de ces 500 €, soit
150 €, et le reste de son revenu continue d'être taxé aux taux inférieurs.

## Ce qui se joue vraiment

C'est probablement l'idée reçue la plus coûteuse en France, parce qu'elle
pousse des gens à refuser des augmentations, des heures supplémentaires ou une
promotion.

La règle vaut pour l'impôt : **gagner plus laisse plus net**. Sur 1 000 €
supplémentaires en tranche à 30 %, l'impôt monte de 300 € et il reste 700 €. Il
n'existe aucun seuil du barème au franchissement duquel le net diminue.

Une nuance importante, en revanche, qui n'a rien à voir avec le barème : les
prestations sociales, elles, comportent de véritables effets de seuil. Prime
d'activité, aides au logement, bourses ou tarifs sociaux se calculent sur des
plafonds de ressources, et un revenu supplémentaire peut en faire perdre le
bénéfice. C'est de là que vient la confusion — et dans ce cas précis, la perte
est réelle.

## Le point de vigilance

Taux marginal et taux moyen sont deux choses différentes. Un foyer en tranche
à 30 % ne paie pas 30 % de ses revenus : les premières tranches restent taxées
à 0 % et 11 %. Le taux réellement supporté est presque toujours très inférieur
au taux marginal, et c'est ce taux moyen que reflète le prélèvement à la
source.
FILE:content/impot_revenu/decote.md
