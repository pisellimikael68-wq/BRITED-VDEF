---
id: etf_replication_indicielle
titre: Un ETF n'est pas un placement, c'est un contenant
domaine: etf
type: enveloppe
statut: valide
difficulte: debutant
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [ETF, tracker, gestion passive, fonds indiciel]
resume: >-
  Un ETF réplique un indice plutôt que de chercher à le battre. Ses frais de
  gestion sont très inférieurs à ceux d'un fonds actif, écart qui se cumule
  année après année. Le risque de perte en capital reste entier.
sources:
  - type: administration
    ref: AMF — les ETF, fonctionnement et risques
    url: https://www.amf-france.org/fr/espace-epargnants/comprendre-les-produits-financiers/panorama-des-produits/etf
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: Directive UCITS 2009/65/CE
    url: https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32009L0065
    consulte_le: 2026-07-27
chiffres:
  - cle: Frais annuels typiques d'un ETF sur grand indice
    valeur: "0,05 à 0,40"
    unite: "%"
    source: 0
    a_verifier: true
    commentaire: ordre de grandeur, à vérifier sur le DIC du produit cité
  - cle: Frais annuels typiques d'un fonds actif
    valeur: "1,5 à 2,5"
    unite: "%"
    source: 0
    a_verifier: true
  - cle: Éligibilité au PEA
    valeur: "possible si le fonds est UCITS et respecte les quotas européens"
    source: 1
relations:
  complete_par:
    - actions_dividende_et_propriete
  s_applique_a:
    - pea_exoneration_5ans
  alternative_a:
    - scpi_frais_et_liquidite
erreurs_frequentes:
  - Croire qu'un ETF est moins risqué qu'une action. Il est diversifié, mais son capital n'est pas garanti et il baisse quand l'indice baisse.
  - Comparer deux ETF sur le seul nom de l'indice, sans regarder les frais, la méthode de réplication ni la devise.
  - Croire que tous les ETF sont éligibles au PEA. Seuls ceux respectant les contraintes européennes le sont.
  - Négliger l'effet des frais sur longue durée : un écart annuel de 1,5 % ampute une part considérable du capital final sur vingt ans.
questions_clients:
  - Un ETF, c'est risqué ?
  - Quelle différence avec un fonds classique ?
  - Puis-je en mettre dans mon PEA ?
a_ne_pas_dire:
  - Ne jamais citer un ETF ou un émetteur nommément : ce serait une recommandation d'investissement.
  - Ne pas présenter la diversification comme une absence de risque.
---

## Le mécanisme

Un ETF est un fonds coté qui réplique un indice. Il ne cherche pas à
sélectionner les meilleures valeurs : il achète l'indice tel quel. C'est ce qui
explique des frais de gestion très inférieurs à ceux d'un fonds géré
activement.

## Ce qui se joue vraiment

L'écart de frais paraît anodin sur un an et devient considérable sur vingt.
Chaque point de pourcentage prélevé annuellement est retiré du capital qui
aurait continué à produire des intérêts composés. C'est un effet cumulatif, pas
additif, et c'est l'argument central de la gestion passive.

## Le point de vigilance

Un ETF ne réduit pas le risque de marché. Il le diversifie sur un indice, ce
qui élimine le risque lié à une entreprise unique mais laisse entier le risque
de baisse générale. Un ETF sur un indice actions peut perdre une part
importante de sa valeur, et le capital n'est jamais garanti.
