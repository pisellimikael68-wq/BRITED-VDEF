---
id: impot_revenu_pension_alimentaire
titre: Déduire une pension versée à un enfant majeur
domaine: impot_revenu
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- pension alimentaire enfant majeur
- déduire aide étudiant
- rattachement ou pension
resume: Un parent qui aide un enfant majeur peut soit le rattacher à son foyer fiscal, soit déduire une
  pension alimentaire plafonnée. Les deux s'excluent, et le meilleur choix dépend de la tranche d'imposition
  du parent.
sources:
- type: texte_legal
  ref: CGI, article 156, II, 2° (déduction des pensions alimentaires)
- type: texte_legal
  ref: CGI, article 196 B (abattement en cas de rattachement d'un enfant majeur)
- type: texte_legal
  ref: Code civil, article 205 (obligation alimentaire)
- type: bofip
  ref: BOI-IR-BASE-20-30-20 (pensions alimentaires versées aux enfants)
  url: https://bofip.impots.gouv.fr/doctrine/BOI-IR-BASE-20-30-20
  consulte_le: 2026-07-29
chiffres:
- cle: Âge à partir duquel l'enfant sort du foyer fiscal de plein droit
  valeur: '18'
  unite: ans
  source: 1
- cle: Âge limite de rattachement de l'enfant majeur poursuivant ses études
  valeur: '25'
  unite: ans
  source: 1
relations:
  regi_par:
  - fiscalite_quotient_familial
  complete_par:
  - impot_revenu_prelevement_source
  alternative_a:
  - fiscalite_quotient_familial
erreurs_frequentes:
- Cumuler rattachement et déduction de pension pour le même enfant. Les deux sont exclusifs l'un de l'autre
  sur une même année.
- Déduire sans pouvoir justifier. La pension doit correspondre à des dépenses réelles et proportionnées
  aux ressources du parent et aux besoins de l'enfant.
- Oublier que la pension déduite par le parent est imposable chez l'enfant qui la reçoit, ce qui peut
  le rendre imposable et lui faire perdre certains droits.
- Croire que le plafond est le même selon que l'enfant est hébergé ou non. Les modalités diffèrent, avec
  un forfait pour le logement et la nourriture.
questions_clients:
- Vaut-il mieux rattacher mon fils étudiant ou déduire une pension ?
- Mon enfant doit-il déclarer ce que je lui verse ?
- Puis-je déduire le loyer que je paie pour ma fille ?
a_ne_pas_dire:
- Ne jamais trancher à la place du spectateur — l'arbitrage dépend de sa tranche marginale et de la composition
  de son foyer. Chiffrer les deux voies sur un cas fictif reste permis.
- Ne pas suggérer de déduire une pension non versée ou surévaluée.
---

## Le mécanisme

À sa majorité, un enfant cesse automatiquement de faire partie du foyer fiscal
de ses parents. Deux voies s'ouvrent alors, et une seule peut être empruntée par
an et par enfant.

Le **rattachement** ramène l'enfant dans le foyer. Il apporte une demi-part ou
une part supplémentaire selon le rang, mais l'avantage qui en résulte est
plafonné, et les revenus de l'enfant deviennent ceux du foyer.

La **déduction d'une pension alimentaire** sort l'enfant du foyer mais permet au
parent de retrancher de son revenu imposable les sommes réellement versées, dans
une limite annuelle par enfant.

## Ce qui se joue vraiment

Le calcul dépend entièrement de la **tranche marginale** du parent.

Une déduction du revenu vaut le montant déduit multiplié par le taux marginal :
elle est d'autant plus intéressante que le parent est fortement imposé. À 41 %,
elle est nettement plus efficace que le plafonnement du quotient familial.

À l'inverse, pour un foyer faiblement imposé, le rattachement l'emporte
généralement.

## Le point de vigilance

La pension déduite chez le parent est **imposable chez l'enfant**. Elle
constitue pour lui un revenu, qui peut le rendre imposable et lui faire perdre
le bénéfice de dispositifs conditionnés aux ressources.

La déduction suppose aussi une réalité : versements traçables, dépenses
proportionnées, obligation alimentaire effective. Un forfait existe pour le
logement et la nourriture de l'enfant hébergé, ce qui dispense de justifier ces
postes — mais pas les autres.
scripts/impot_revenu/impot_revenu_pension_alimentaire__multi__a1.md
scripts/impot_revenu/impot_revenu_prelevement_source__multi__a3.md
scripts/impot_revenu/impot_revenu_decote__multi__a3.md
scripts/impot_revenu/impot_revenu_prelevement_source__multi__a2.md
scripts/impot_revenu/impot_revenu_pension_alimentaire__multi__a4.md
scripts/impot_revenu/impot_revenu_decote__multi__a2.md
scripts/impot_revenu/impot_revenu_tranche_marginale__multi__a2.md
scripts/impot_revenu/impot_revenu_tranche_marginale__multi__a3.md
scripts/impot_revenu/impot_revenu_tranche_marginale__multi__a4.md
scripts/impot_revenu/impot_revenu_tranche_marginale__multi__a1.md
scripts/impot_revenu/impot_revenu_prelevement_source__multi__a1.md
scripts/impot_revenu/impot_revenu_decote__multi__a1.md
scripts/impot_revenu/impot_revenu_pension_alimentaire__multi__a3.md
scripts/impot_revenu/impot_revenu_pension_alimentaire__multi__a2.md
scripts/impot_revenu/impot_revenu_prelevement_source__multi__a4.md
scripts/impot_revenu/impot_revenu_decote__multi__a4.md
