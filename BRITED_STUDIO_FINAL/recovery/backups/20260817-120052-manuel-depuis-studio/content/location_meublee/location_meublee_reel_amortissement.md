---
id: location_meublee_reel_amortissement
titre: Le régime réel et l'amortissement
domaine: location_meublee
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- LMNP réel
- amortissement location meublée
- micro-BIC ou réel
resume: Au régime réel, le loueur en meublé déduit ses charges réelles et amortit le bien, ce qui efface
  souvent la totalité du résultat imposable pendant des années. C'est le mécanisme qui distingue vraiment
  la location meublée de la location nue.
sources:
- type: texte_legal
  ref: CGI, article 39 (charges déductibles et amortissements)
- type: texte_legal
  ref: CGI, article 50-0 (régime micro-BIC)
- type: texte_legal
  ref: CGI, article 155, IV (loueur en meublé professionnel ou non professionnel)
- type: bofip
  ref: BOI-BIC-CHAMP-40-20 (location meublée)
  url: https://bofip.impots.gouv.fr/doctrine/BOI-BIC-CHAMP-40-20
  consulte_le: 2026-07-29
chiffres:
- cle: Durée d'amortissement usuelle du gros œuvre
  valeur: 30 à 50
  unite: ans
  source: 0
  commentaire: par composants, selon la nature de l'élément
- cle: Part du prix non amortissable
  valeur: le terrain
  source: 0
relations:
  regi_par:
  - location_meublee_micro_bic
  complete_par:
  - immobilier_revenus_fonciers_micro
  - immobilier_plus_value_duree_detention
  alternative_a:
  - immobilier_deficit_foncier
erreurs_frequentes:
- Croire que l'amortissement peut créer un déficit. L'amortissement du bien ne peut pas augmenter ou créer un déficit: la
    fraction non utilisée est reportée sans limite de durée.
- Amortir le prix d'achat entier. La quote-part de terrain n'est pas amortissable et doit être isolée.
- Choisir le micro-BIC par confort alors que les charges réelles et l'amortissement dépassent l'abattement
  forfaitaire.
- Croire que le régime réel est irréversible ou inaccessible sans comptable. Il suppose une comptabilité
  commerciale, mais reste ouvert sur option.
questions_clients:
- Pourquoi je ne paie pas d'impôt sur mes loyers meublés ?
- Faut-il un comptable pour le LMNP ?
- Micro-BIC ou réel, comment savoir ?
a_ne_pas_dire:
- Ne pas présenter l'amortissement comme une exonération définitive — il réduit le résultat imposable
  année après année, il ne supprime pas l'impôt sur la plus-value de cession.
- Ne jamais dire au spectateur quel régime fiscal adopter. Comparer micro-BIC et réel sur un bien fictif
  reste permis.
---

## Le mécanisme

La location meublée relève des bénéfices industriels et commerciaux, pas des
revenus fonciers. Cette qualification ouvre l'accès aux règles comptables de
l'entreprise, et notamment à l'**amortissement**.

Le bien est décomposé en composants — gros œuvre, façade, toiture,
installations, agencements — chacun amorti sur sa propre durée. Chaque année,
une fraction de la valeur est déduite du résultat, sans aucune sortie de
trésorerie.

S'y ajoutent les charges réelles : intérêts d'emprunt, taxe foncière, charges de
copropriété, assurance, frais de gestion, travaux.

## Ce qui se joue vraiment

Le cumul charges plus amortissement absorbe très souvent la totalité des loyers.
Le résultat imposable tombe à zéro et le bailleur encaisse des loyers sans
impôt sur le revenu ni prélèvements sociaux dessus, parfois pendant dix ou
quinze ans.

C'est la différence de nature avec la location nue, où l'amortissement n'existe
pas : à loyer identique, le bailleur nu est imposé et le bailleur meublé ne
l'est pas.

## Le point de vigilance

L'amortissement ne peut pas créer de déficit. La fraction qui excède le résultat
est mise en report et s'utilisera les années suivantes — l'avantage est différé,
jamais perdu, mais il ne remonte pas contre les autres revenus.

Le régime réel exige une comptabilité commerciale : bilan, compte de résultat,
liasse fiscale. C'est un coût annuel réel, à mettre en face de l'économie
d'impôt attendue avant de choisir.
