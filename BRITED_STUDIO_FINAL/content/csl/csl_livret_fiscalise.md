---
id: csl_livret_fiscalise
titre: Un livret bancaire n'a pas de plafond, mais il est imposé
domaine: csl
type: enveloppe
statut: valide
difficulte: debutant
potentiel_viral: 7
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [compte sur livret, CSL, livret bancaire, super livret]
resume: >-
  Le compte sur livret est un produit d'épargne libre : pas de plafond, taux
  fixé par la banque, disponibilité totale. Contrepartie, les intérêts sont
  soumis au prélèvement forfaitaire unique de 30 %, ce que les taux
  promotionnels affichés font souvent oublier.
sources:
  - type: texte_legal
    ref: CGI, article 200 A (prélèvement forfaitaire unique)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041464718
    consulte_le: 2026-07-27
  - type: administration
    ref: Service-public.fr — comptes d'épargne bancaire
    url: https://www.service-public.fr/particuliers/vosdroits/F2365
    consulte_le: 2026-07-27
chiffres:
  - cle: Plafond de versements
    valeur: "aucun"
    source: 1
  - cle: Imposition des intérêts
    valeur: "30"
    unite: "%"
    source: 0
  - cle: Rendement net d'un taux brut de 3 %
    valeur: "2,1"
    unite: "%"
    source: 0
    commentaire: après prélèvement forfaitaire unique de 30 %
relations:
  alternative_a:
    - livret_a_plafonds
    - ldds_plafond_et_don
  regi_par:
    - compte_titres_pfu
erreurs_frequentes:
  - Comparer le taux d'un livret bancaire à celui du Livret A sans corriger de la fiscalité. Les deux ne sont pas comparables bruts.
  - Se laisser attirer par un taux promotionnel sans regarder sa durée, souvent limitée à quelques mois.
  - Croire que le taux boosté s'applique à l'ensemble du dépôt et pour toute l'année.
  - Utiliser un livret bancaire comme placement de long terme, alors qu'il ne sert qu'à loger une trésorerie excédentaire.
questions_clients:
  - Ce super livret à 4 %, c'est intéressant ?
  - Faut-il déclarer les intérêts ?
  - Que faire quand mon Livret A est plein ?
a_ne_pas_dire:
  - Ne citer aucune banque ni offre promotionnelle nommément.
  - Ne pas présenter un taux brut sans indiquer le taux net après fiscalité.
---

## Le mécanisme

Le compte sur livret est un produit d'épargne bancaire ordinaire. Sa
rémunération est fixée librement par l'établissement, il n'a pas de plafond, et
les fonds restent disponibles.

Ses intérêts ne bénéficient d'aucune exonération : ils supportent le
prélèvement forfaitaire unique de 30 %, sauf option pour le barème.

## Ce qui se joue vraiment

C'est l'écart entre le taux affiché et le taux perçu. Un livret annoncé à 3 %
brut rapporte 2,1 % net. Comparé à un Livret A exonéré, la comparaison ne peut
donc jamais se faire sur les taux bruts.

S'y ajoutent les taux promotionnels : un taux élevé porte fréquemment sur les
seuls premiers mois et sur un montant plafonné, avant de retomber sur un taux
de base beaucoup plus faible. Le rendement moyen sur douze mois est souvent
très éloigné du chiffre affiché.

## Le point de vigilance

Le livret bancaire n'a d'intérêt qu'une fois les livrets réglementés saturés,
et pour une trésorerie destinée à être utilisée à court terme. Sur un horizon
long, sa fiscalité et son rendement en font le placement le moins efficace de
la gamme.
### content/compte_titres/pfu_flat_tax.md
