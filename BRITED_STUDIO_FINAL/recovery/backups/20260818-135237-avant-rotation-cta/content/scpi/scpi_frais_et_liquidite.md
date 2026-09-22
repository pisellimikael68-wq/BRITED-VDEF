---
id: scpi_frais_et_liquidite
titre: Une SCPI met plusieurs années à rembourser ses frais d'entrée
domaine: scpi
type: enveloppe
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [SCPI, pierre-papier, société civile de placement immobilier]
resume: >-
  Les SCPI permettent d'investir dans l'immobilier locatif sans gestion, mais
  leurs frais de souscription élevés et l'absence de liquidité garantie en font
  un placement de long terme. Les revenus sont des revenus fonciers, imposés au
  barème.
sources:
  - type: texte_legal
    ref: Code monétaire et financier, articles L214-114 et suivants
    url: https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072026/LEGISCTA000027764105
    consulte_le: 2026-07-27
  - type: administration
    ref: AMF — investir en SCPI
    url: https://www.amf-france.org/fr/espace-epargnants/comprendre-les-produits-financiers/panorama-des-produits/scpi
    consulte_le: 2026-07-27
chiffres:
  - cle: Frais de souscription usuels
    valeur: "8 à 12"
    unite: "%"
    source: 1
    a_verifier: true
    commentaire: ordre de grandeur, à vérifier sur la note d'information de la SCPI citée
  - cle: Délai de jouissance avant premiers revenus
    valeur: "3 à 6"
    unite: "mois"
    source: 1
    a_verifier: true
  - cle: Imposition des revenus
    valeur: "barème de l'impôt sur le revenu + 17,2 % de prélèvements sociaux"
    source: 0
  - cle: Garantie de revente des parts
    valeur: "aucune"
    source: 0
relations:
  alternative_a:
    - location_meublee_micro_bic
    - etf_replication_indicielle
  regi_par:
    - impot_revenu_tranche_marginale
erreurs_frequentes:
  - Comparer le rendement affiché d'une SCPI au rendement net d'un autre placement. Le taux de distribution est brut de fiscalité et ne tient pas compte des frais d'entrée.
  - Croire que les parts se revendent à tout moment. La liquidité dépend de l'existence d'un acheteur, et le marché secondaire peut se gripper.
  - Oublier que les revenus sont fonciers : imposés au barème, ils sont lourdement taxés dans les tranches hautes.
  - Investir sur un horizon court. Les frais d'entrée ne sont amortis qu'après plusieurs années de distribution.
questions_clients:
  - Les SCPI, c'est de l'immobilier sans les soucis ?
  - Puis-je récupérer mon argent quand je veux ?
  - Combien ça rapporte vraiment après impôt ?
a_ne_pas_dire:
  - Ne jamais citer une SCPI nommément : ce serait une recommandation d'investissement.
  - Ne pas présenter le capital comme garanti : la valeur des parts peut baisser.
  - Ne pas reprendre un taux de distribution sans préciser qu'il est brut et non garanti.
---

## Le mécanisme

Une SCPI collecte l'épargne de nombreux associés pour acquérir et gérer un
patrimoine immobilier locatif. L'associé perçoit une quote-part des loyers,
sans aucune gestion à assumer.

Ces revenus sont des **revenus fonciers** : imposés au barème progressif, plus
17,2 % de prélèvements sociaux.

## Ce qui se joue vraiment

Le taux de distribution affiché est brut. Pour un contribuable en tranche à
30 %, une distribution de 5 % tombe à environ 2,6 % net. Et ce calcul ignore
encore les frais de souscription, qui représentent plusieurs années de revenus
et ne sont récupérés qu'à la revente, si le prix de part a suivi.

C'est ce qui fait de la SCPI un placement de long terme : sortir au bout de
trois ans revient presque toujours à perdre de l'argent, même si la SCPI a
bien distribué.

## Le point de vigilance

La liquidité n'est pas garantie. Revendre suppose de trouver un acheteur, et
en période de retournement du marché immobilier, les demandes de retrait
peuvent s'accumuler sans contrepartie. Ce n'est pas un défaut caché : c'est la
nature même du produit, et l'AMF le rappelle explicitement.
