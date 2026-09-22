---
id: produits_structures_barriere
titre: La protection d'un produit structuré n'est pas une garantie
domaine: produits_structures
type: enveloppe
statut: valide
difficulte: avance
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [produit structuré, autocall, barrière de protection, fonds à formule]
resume: >-
  Un produit structuré promet un rendement conditionnel assorti d'une barrière
  de protection. Tant que le sous-jacent reste au-dessus, le capital est
  préservé. En dessous, la perte est intégrale et proportionnelle à la baisse.
sources:
  - type: administration
    ref: AMF — produits structurés, recommandations et mises en garde
    url: https://www.amf-france.org/fr/espace-epargnants/comprendre-les-produits-financiers/panorama-des-produits/produits-structures
    consulte_le: 2026-07-27
  - type: administration
    ref: ACPR — commercialisation des produits structurés
    url: https://acpr.banque-france.fr
    consulte_le: 2026-07-27
chiffres:
  - cle: Protection du capital en dessous de la barrière
    valeur: "aucune"
    source: 0
  - cle: Nature du risque sous la barrière
    valeur: "perte proportionnelle à la baisse du sous-jacent"
    source: 0
  - cle: Risque supplémentaire porté par l'investisseur
    valeur: "défaut de l'émetteur"
    source: 0
relations:
  complete_par:
    - obligations_risque_de_taux
    - actions_dividende_et_propriete
erreurs_frequentes:
  - Confondre barrière de protection et garantie en capital. La protection disparaît intégralement si la barrière est franchie.
  - Ignorer le risque de défaut de l'émetteur, qui s'ajoute au risque de marché et n'est couvert par aucune barrière.
  - Croire que le rendement affiché est acquis. Il est conditionnel, et l'année sans versement ne se rattrape pas toujours.
  - Négliger l'illiquidité : la revente avant l'échéance se fait au prix de marché, souvent défavorable.
questions_clients:
  - Mon capital est-il garanti ?
  - Que se passe-t-il si l'indice baisse beaucoup ?
  - Puis-je sortir avant l'échéance ?
a_ne_pas_dire:
  - Ne jamais employer le mot « garanti » pour un produit à barrière.
  - Ne citer aucun produit ni émetteur nommément.
  - Toujours mentionner le risque de perte en capital et le risque émetteur.
---

## Le mécanisme

Un produit structuré combine un placement obligataire et des instruments
dérivés pour offrir un rendement conditionnel, adossé à un sous-jacent —
souvent un indice boursier.

La **barrière de protection** fonctionne par tout ou rien. Tant que le
sous-jacent reste au-dessus du niveau défini à l'échéance, le capital est
remboursé intégralement. S'il passe en dessous, la protection cesse
entièrement : l'investisseur subit la totalité de la baisse.

## Ce qui se joue vraiment

C'est un effet de seuil, pas un amortisseur. Avec une barrière à -40 %, une
baisse de 39 % laisse le capital intact et une baisse de 41 % fait perdre 41 %.
La différence entre les deux scénarios tient à deux points d'indice.

Le mot « protection » est ce qui induit en erreur : il suggère un filet, alors
qu'il s'agit d'une condition.

## Le point de vigilance

L'investisseur porte aussi le **risque de défaut de l'émetteur**. Si
l'établissement qui a émis le produit fait faillite, ni la barrière ni la
formule ne s'appliquent. C'est un risque distinct du risque de marché, souvent
absent des présentations commerciales, et sur lequel l'AMF appelle
régulièrement à la vigilance.
