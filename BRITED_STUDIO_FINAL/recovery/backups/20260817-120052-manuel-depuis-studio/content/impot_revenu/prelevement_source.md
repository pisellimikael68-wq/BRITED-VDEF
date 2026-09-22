---
id: impot_revenu_prelevement_source
titre: Taux personnalisé, neutre ou individualisé
domaine: impot_revenu
type: notion
statut: valide
difficulte: debutant
potentiel_viral: 8
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- prélèvement à la source
- taux neutre
- taux individualisé
resume: Le prélèvement à la source propose trois taux. Le personnalisé est celui du foyer, le neutre masque
  la situation fiscale à l'employeur, l'individualisé répartit la charge entre conjoints selon leurs revenus
  respectifs. Aucun ne change le montant final de l'impôt.
sources:
- type: texte_legal
  ref: CGI, article 204 H (détermination du taux de prélèvement)
- type: texte_legal
  ref: CGI, article 204 M (taux individualisé des conjoints)
- type: texte_legal
  ref: CGI, article 204 J (modulation du prélèvement)
- type: administration
  ref: impots.gouv.fr — gérer mon prélèvement à la source
  url: https://www.impots.gouv.fr
  consulte_le: 2026-07-29
chiffres:
- cle: Nombre d'options de taux offertes au contribuable
  valeur: '3'
  source: 0
- cle: Délai de prise en compte d'un changement de situation familiale
  valeur: '60'
  unite: jours
  source: 2
  commentaire: délai de déclaration du changement à l'administration
relations:
  complete_par:
  - impot_revenu_decote
  - impot_revenu_pension_alimentaire
  s_applique_a:
  - impot_revenu_tranche_marginale
erreurs_frequentes:
- Croire que le taux individualisé réduit l'impôt du couple. Il ne change que la répartition entre les
  deux conjoints, pas le total dû par le foyer.
- Croire que le taux neutre est plus avantageux. Il ignore la situation familiale et conduit souvent à
  un prélèvement plus élevé, régularisé ensuite.
- Oublier de déclarer un changement de situation. Naissance, mariage, divorce ou décès doivent être signalés
  dans les soixante jours pour que le taux s'ajuste.
- Croire que le prélèvement à la source solde l'impôt. Il n'est qu'un acompte: la déclaration annuelle
    reste due et produit un solde ou un remboursement.
questions_clients:
- Mon employeur voit-il combien je gagne par ailleurs ?
- Faut-il choisir le taux individualisé quand on gagne beaucoup moins que son conjoint ?
- Pourquoi j'ai un solde à payer alors que je suis prélevé chaque mois ?
a_ne_pas_dire:
- Ne jamais dire au spectateur quelle option de taux retenir. Illustrer les trois options sur un couple
  fictif reste permis.
- Ne pas laisser croire que le prélèvement à la source a supprimé la déclaration de revenus.
---

## Le mécanisme

Le prélèvement à la source ne modifie ni le barème ni le montant de l'impôt. Il
en change seulement le calendrier de paiement, et le taux appliqué chaque mois.

Le **taux personnalisé** est calculé par l'administration à partir de la
dernière déclaration du foyer. C'est l'option par défaut.

Le **taux neutre** correspond à celui d'un célibataire sans personne à charge,
appliqué au seul salaire connu de l'employeur. Il sert à ne pas révéler la
situation fiscale du foyer.

Le **taux individualisé** répartit la charge entre les deux conjoints
proportionnellement à leurs revenus personnels, au lieu d'appliquer le même taux
aux deux.

## Ce qui se joue vraiment

Le taux individualisé est le plus mal compris. Il ne fait **aucune économie** :
le foyer paie exactement la même chose, mais celui qui gagne moins est prélevé à
un taux plus faible, et celui qui gagne plus à un taux plus élevé.

Son intérêt est donc entièrement relationnel : il évite qu'un conjoint aux
revenus modestes supporte, sur son bulletin de paie, un taux calculé sur les
revenus de l'autre.

Le taux neutre, lui, a un coût réel. Ignorant les enfants et la situation
familiale, il prélève généralement davantage. L'excédent est restitué, mais un
an plus tard.

## Le point de vigilance

Le prélèvement à la source est un **acompte**, pas un solde. La déclaration
annuelle reste obligatoire, et c'est elle qui fixe l'impôt réellement dû —
notamment parce que les réductions et crédits d'impôt ne sont pas intégrés au
taux.

Un changement de situation — mariage, PACS, naissance, divorce, décès — doit
être déclaré dans les soixante jours. À défaut, le taux reste calé sur une
situation périmée pendant des mois.
FILE:content/impot_revenu/pension_alimentaire.md
