---
id: fonds_investissement_frais
titre: Les frais d'un fonds ne se voient jamais sur votre relevé
domaine: fonds_investissement
type: enveloppe
statut: valide
difficulte: debutant
potentiel_viral: 9
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [OPCVM, SICAV, FCP, frais de gestion, fonds actif]
resume: >-
  Les frais de gestion d'un fonds sont prélevés directement sur la valeur de la
  part, jour après jour. Ils n'apparaissent donc sur aucune ligne de relevé, ce
  qui les rend indolores — et durablement coûteux.
sources:
  - type: administration
    ref: AMF — les frais des placements collectifs
    url: https://www.amf-france.org/fr/espace-epargnants/comprendre-les-produits-financiers/panorama-des-produits/opcvm
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: Code monétaire et financier, articles L214-1 et suivants
    url: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000006157031
    consulte_le: 2026-07-27
chiffres:
  - cle: Mode de prélèvement des frais de gestion
    valeur: "déduits quotidiennement de la valeur liquidative"
    source: 0
  - cle: Document où les frais sont obligatoirement indiqués
    valeur: "document d'informations clés (DIC)"
    source: 0
  - cle: Effet d'un écart de frais de 1,5 % par an sur trente ans
    valeur: "plus d'un tiers du capital final"
    source: 0
    a_verifier: true
    commentaire: ordre de grandeur mathématique, à recalculer selon l'hypothèse de rendement retenue
relations:
  alternative_a:
    - etf_replication_indicielle
  complete_par:
    - culture_interets_composes
  s_applique_a:
    - assurance_vie_abattement_8ans
erreurs_frequentes:
  - Croire qu'un fonds sans frais d'entrée est un fonds peu coûteux. Les frais de gestion annuels pèsent bien davantage sur la durée.
  - Comparer des performances passées sans vérifier si elles sont nettes ou brutes de frais.
  - Ignorer les frais du contrat qui abrite le fonds, qui s'ajoutent à ceux du fonds lui-même.
  - Chercher les frais sur son relevé : ils n'y figurent pas, ils sont déjà déduits de la valeur affichée.
questions_clients:
  - Combien me coûte vraiment mon fonds ?
  - Pourquoi mon fonds fait moins bien que son indice ?
  - Où voit-on les frais ?
a_ne_pas_dire:
  - Ne citer aucun fonds ni société de gestion nommément.
  - Ne pas laisser entendre qu'un fonds à frais faibles est nécessairement plus performant.
---

## Le mécanisme

Les frais de gestion d'un placement collectif ne sont pas facturés : ils sont
prélevés en continu sur l'actif du fonds. La valeur liquidative publiée est
donc déjà nette de frais.

Conséquence pratique : aucune ligne de relevé ne les mentionne. Le seul
document qui les indique est le document d'informations clés, que presque
personne ne lit.

## Ce qui se joue vraiment

Cette invisibilité est ce qui les rend coûteux. Un point et demi de frais
annuels ne coûte pas 1,5 % : il ampute chaque année la totalité de la
croissance qu'aurait produite cette somme sur toute la durée restante. Sur
trente ans, l'effet cumulé représente une part considérable du capital final.

Le même mécanisme explique pourquoi un fonds indiciel actif sous-performe
presque toujours son indice : l'indice n'a pas de frais.

## Le point de vigilance

Les frais se superposent. Un fonds logé dans un contrat d'assurance-vie
supporte les frais du fonds **et** ceux du contrat. Un mandat de gestion en
ajoute un troisième niveau. Le coût total ne se lit sur aucun document unique
et doit être additionné à la main.
