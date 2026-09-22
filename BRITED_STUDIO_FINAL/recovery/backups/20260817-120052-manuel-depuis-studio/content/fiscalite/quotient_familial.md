---
id: fiscalite_quotient_familial
titre: Un enfant ne réduit pas l'impôt du même montant pour tout le monde
domaine: fiscalite
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [quotient familial, parts fiscales, demi-part, plafonnement]
resume: >-
  Le quotient familial divise le revenu imposable par un nombre de parts avant
  application du barème. L'avantage qui en résulte est plafonné par demi-part,
  ce qui le rend décroissant à mesure que le revenu augmente.
sources:
  - type: texte_legal
    ref: CGI, article 194 (nombre de parts)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041464700
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 197, I, 2 (plafonnement)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047620877
    consulte_le: 2026-07-27
  - type: administration
    ref: Service-public.fr — quotient familial
    url: https://www.service-public.fr/particuliers/vosdroits/F2702
    consulte_le: 2026-07-27
chiffres:
  - cle: Parts pour un couple marié ou pacsé sans enfant
    valeur: "2"
    source: 0
  - cle: Parts pour chacun des deux premiers enfants
    valeur: "0,5"
    source: 0
  - cle: Parts à partir du troisième enfant
    valeur: "1"
    source: 0
  - cle: Plafond de l'avantage par demi-part, imposition 2026
    valeur: "1 807"
    unite: "€"
    source: 1
    valide_du: 2026-01-01
    valide_au: 2026-12-31
    commentaire: 1 791 € en 2025, revalorisé de 0,9 %, vérifié le 2026-07-27
relations:
  complete_par:
    - impot_revenu_tranche_marginale
  s_applique_a:
    - regimes_communaute_par_defaut
  varie_selon:
    - protection_sociale_invalidite
erreurs_frequentes:
  - Croire qu'un enfant fait économiser un montant fixe. L'économie dépend du taux marginal et s'arrête au plafond.
  - Oublier le saut du troisième enfant, qui apporte une part entière et non une demi-part.
  - Croire que le rattachement d'un enfant majeur est toujours favorable. Le versement d'une pension déductible peut l'être davantage.
  - Confondre quotient familial et quotient conjugal, qui produisent tous deux un effet mais obéissent à des règles différentes.
questions_clients:
  - Combien un enfant fait-il gagner sur les impôts ?
  - Mon fils étudiant, je le rattache ou je déduis une pension ?
  - Pourquoi mon voisin économise-t-il plus que moi avec le même nombre d'enfants ?
a_ne_pas_dire:
  - Ne pas citer de montant de plafond sans vérifier la loi de finances de l'année d'imposition concernée.
---

## Le mécanisme

Le quotient familial divise le revenu imposable du foyer par un nombre de parts
avant d'appliquer le barème, puis multiplie l'impôt obtenu par ce même nombre.
Comme le barème est progressif, la division fait tomber le revenu dans des
tranches plus basses et réduit l'impôt.

L'avantage qui en résulte est cependant **plafonné par demi-part**.

## Ce qui se joue vraiment

L'économie n'est donc pas la même pour tous. Pour un foyer en tranche à 11 %,
la demi-part d'un enfant rapporte peu. Pour un foyer en tranche à 41 %, elle
rapporte beaucoup plus — jusqu'à ce que le plafond intervienne et fige
l'avantage.

Autrement dit, l'avantage croît avec le revenu puis se bloque net. C'est ce qui
explique que deux familles avec le même nombre d'enfants n'économisent pas la
même chose.

## Le point de vigilance

Le troisième enfant apporte une part entière et non une demi-part : le gain est
sensiblement plus important que pour les deux premiers.

Pour un enfant majeur étudiant, le rattachement au foyer n'est pas toujours le
meilleur choix. Verser une pension alimentaire déductible peut se révéler plus
favorable lorsque le plafonnement du quotient est déjà atteint. Les deux
options se simulent, elles ne se devinent pas.
FILE:content/fiscalite/controle_fiscal.md
