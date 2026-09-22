---
id: sci_is_ou_ir
titre: Une SCI qui passe à l'IS a cinq ans pour changer d'avis, et une seule fois
domaine: sci
type: enveloppe
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [SCI, société civile immobilière, SCI à l'IS, option IS, renonciation option IS]
resume: >-
  Une SCI est par défaut translucide : les associés sont imposés directement.
  L'option pour l'impôt sur les sociétés permet d'amortir le bien. Contrairement
  à une idée répandue, elle n'est pas immédiatement irrévocable : la loi de
  finances 2019 permet d'y renoncer jusqu'au cinquième exercice suivant. Mais la
  renonciation est définitive et a un coût fiscal.
sources:
  - type: texte_legal
    ref: CGI, article 239, 1, alinéa 3 (droit de renonciation)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037988649/
    consulte_le: 2026-07-27
  - type: bofip
    ref: BOI-IS-CHAMP-20-20-30, § 20, 40 et 60 (renonciation à l'option pour l'IS)
    url: https://bofip.impots.gouv.fr/doctrine/BOI-IS-CHAMP-20-20-30
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 221 bis (atténuation en cas de cessation)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037987801/
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: CGI, article 8, 1° (régime des sociétés de personnes)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000025842591/
    consulte_le: 2026-07-27
chiffres:
  - cle: Délai pour renoncer à l'option IS
    valeur: "jusqu'au cinquième exercice suivant celui de l'option"
    source: 0
    commentaire: droit ouvert par l'article 50 de la loi de finances 2019, applicable aux exercices clos à compter du 31 décembre 2018
  - cle: Caractère de l'option passé ce délai
    valeur: "irrévocable"
    source: 1
  - cle: Possibilité de réoption après renonciation
    valeur: "aucune, définitivement"
    source: 1
    commentaire: BOI-IS-CHAMP-20-20-30 § 60
  - cle: Délai pour exercer l'option initiale
    valeur: "avant la fin du troisième mois de l'exercice concerné"
    source: 1
  - cle: Nombre minimum d'associés
    valeur: "2"
    source: 3
  - cle: Régime par défaut
    valeur: "impôt sur le revenu, revenus fonciers"
    source: 3
relations:
  regi_par:
    - impot_revenu_tranche_marginale
  complete_par:
    - indivision_regle_unanimite
    - transmission_cout_inaction
erreurs_frequentes:
  - Croire que l'option pour l'IS est irrévocable dès le premier jour. Elle ne le devient qu'à défaut de renonciation avant le cinquième exercice suivant.
  - Croire que renoncer est neutre. La renonciation produit les effets d'une cessation d'entreprise : imposition immédiate des plus-values latentes, sauf atténuation de l'article 221 bis.
  - Croire qu'on peut faire des allers-retours. Une société qui a renoncé ne peut plus jamais réopter pour l'IS.
  - Opter pour l'IS pour l'amortissement sans mesurer la plus-value à la revente, calculée sur la valeur nette comptable.
  - Croire que la SCI est un outil de défiscalisation. C'est un outil de détention et de transmission, fiscalement neutre par défaut.
questions_clients:
  - Faut-il créer une SCI pour acheter à deux ?
  - SCI à l'IR ou à l'IS ?
  - On a opté pour l'IS l'an dernier, peut-on revenir en arrière ?
a_ne_pas_dire:
  - Ne pas dire que l'option IS est irrévocable sans préciser le délai de renonciation de cinq exercices, sous peine de dissuader à tort.
  - Ne pas présenter la renonciation comme une simple formalité : elle a un coût fiscal immédiat.
  - Ne pas présenter la SCI comme un moyen d'échapper à l'impôt.
---

## Le mécanisme

Une SCI est par défaut **translucide** : elle ne paie pas d'impôt, ses résultats
sont imposés entre les mains des associés, dans la catégorie des revenus
fonciers, au prorata de leurs parts.

L'option pour l'impôt sur les sociétés change tout : la SCI devient
contribuable, peut déduire l'amortissement du bien, mais l'associé est imposé
une seconde fois lorsqu'il se distribue des dividendes. Elle s'exerce avant la
fin du troisième mois de l'exercice concerné.

## Ce qui se joue vraiment

On lit partout que cette option est irrévocable. C'était vrai avant 2019.
L'article 50 de la loi de finances pour 2019 a ouvert un droit de renonciation,
et le BOFiP l'énonce sans ambiguïté : l'option est révocable **jusqu'au
cinquième exercice suivant celui au titre duquel elle a été exercée**. Ce n'est
qu'à défaut de renonciation dans ce délai qu'elle devient définitive.

Concrètement, une société qui opte au titre de l'exercice clos fin 2025 peut
encore renoncer jusqu'à fin février 2030, la renonciation prenant effet pour
l'exercice 2030.

Deux limites, toutefois, qui font que ce droit ne s'utilise pas à la légère.
La renonciation produit les effets d'une **cessation d'entreprise** : les
plus-values latentes deviennent immédiatement imposables, sauf à bénéficier de
l'atténuation de l'article 221 bis, qui suppose de ne pas modifier les écritures
comptables et que l'imposition reste possible ensuite. Et surtout, une société
qui a renoncé **ne peut plus jamais réopter** pour l'IS.

## Le point de vigilance

Le vrai piège n'est donc pas l'irrévocabilité immédiate, c'est l'amortissement.
À l'IS, la plus-value de revente se calcule sur la valeur nette comptable,
c'est-à-dire le prix d'achat diminué de tous les amortissements déjà déduits.
Un bien amorti vingt ans se revend avec une plus-value taxable bien plus élevée
qu'à l'IR, où les abattements pour durée de détention finissent par exonérer.

L'IS convient à une logique de conservation longue et de réinvestissement. L'IR
convient à une logique de revente. Le délai de cinq exercices laisse le temps de
constater qu'on s'est trompé — pas celui de revenir gratuitement en arrière.
