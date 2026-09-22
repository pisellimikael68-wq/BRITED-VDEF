---
id: per_sortie_capital_rente
titre: Sortir en capital ou en rente
domaine: per
type: strategie
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
  - sortie du PER
  - PER capital ou rente
  - récupérer son PER à la retraite
resume: >-
  Le PER individuel permet, à la retraite, de sortir en capital, en rente, ou en
  combinant les deux. La fiscalité diffère radicalement selon le choix, et selon
  que les versements ont été déduits ou non à l'entrée.
sources:
  - type: texte_legal
    ref: Code monétaire et financier, article L. 224-5 (modalités de liquidation du PER)
  - type: texte_legal
    ref: Code monétaire et financier, article L. 224-4 (cas de déblocage anticipé)
  - type: texte_legal
    ref: CGI, article 158, 5 (imposition des pensions et rentes)
  - type: texte_legal
    ref: CGI, article 163 quatervicies (déduction des versements)
chiffres:
  - cle: Nombre de compartiments du PER
    valeur: "3"
    source: 0
    commentaire: versements volontaires, épargne salariale, versements obligatoires
  - cle: Abattement applicable aux pensions et rentes viagères à titre gratuit
    valeur: "10"
    unite: "%"
    source: 2
relations:
  regi_par:
    - per_deduction_versements
  complete_par:
    - retraite_releve_carriere
erreurs_frequentes:
  - Croire que le PER se dénoue obligatoirement en rente. Depuis la loi PACTE, la sortie en capital est possible pour les versements volontaires et l'épargne salariale.
  - Oublier que la sortie en capital des versements déduits est imposée au barème de l'impôt sur le revenu, sans abattement de 10 %, ce qui peut faire changer de tranche l'année de la sortie.
  - Croire que les plus-values suivent le même régime que le capital versé. Elles relèvent du prélèvement forfaitaire, distinctement.
  - Ignorer qu'un capital peut être fractionné sur plusieurs années pour lisser la progressivité de l'impôt.
questions_clients:
  - Vaut-il mieux prendre mon PER en une fois ou en rente ?
  - Vais-je être imposé sur tout d'un coup ?
  - Puis-je récupérer mon PER avant la retraite ?
a_ne_pas_dire:
  - Ne jamais dire au spectateur quelle modalité de sortie retenir : l'arbitrage dépend de sa tranche marginale, de son espérance de vie et de ses autres revenus. Illustrer les deux sorties sur un cas fictif chiffré reste permis.
  - Ne pas présenter la déduction à l'entrée comme un gain définitif : c'est un report d'imposition, pas une exonération.
---

## Le mécanisme

Le PER individuel se dénoue à la retraite — ou à l'achat de la résidence
principale, ou dans l'un des cas d'accident de la vie prévus par le code
monétaire et financier.

Trois sorties sont possibles pour les versements volontaires : capital en une
fois, capital fractionné, rente viagère. Elles peuvent se combiner.

La fiscalité dépend d'un choix fait bien plus tôt : celui d'avoir déduit ou non
les versements du revenu imposable à l'entrée.

## Ce qui se joue vraiment

Si les versements ont été déduits, la sortie en capital réintègre ces sommes au
barème de l'impôt sur le revenu, **sans l'abattement de 10 %** applicable aux
pensions. Les plus-values, elles, subissent le prélèvement forfaitaire.

Le risque est un effet de seuil brutal : 80 000 € récupérés en une fois peuvent
faire basculer une tranche marginale de 11 % à 41 % l'année de la sortie. Le
fractionnement sur plusieurs exercices existe précisément pour ça.

Si les versements n'ont pas été déduits, la logique s'inverse : le capital versé
ressort en franchise d'impôt, seules les plus-values sont taxées.

## Le point de vigilance

La rente viagère est en principe sans retour. Une fois le contrat liquidé en
rente, le capital n'appartient plus à l'épargnant : il est converti en un droit à
percevoir un revenu jusqu'au décès. Selon les options choisies, il peut ne rien
rester aux héritiers.

Seules les rentes d'un montant très faible peuvent, dans les conditions fixées
par la réglementation, être servies sous forme de capital.

C'est l'arbitrage central et il n'a pas de bonne réponse universelle : la rente
protège contre le risque de vivre très longtemps, le capital protège la
transmission.
