---
id: retraite_decote_surcote
titre: Partir un trimestre trop tôt coûte à vie, pas une seule année
domaine: retraite
type: notion
statut: valide
difficulte: intermediaire
potentiel_viral: 9
cree_le: 2026-07-27
revise_le: 2026-07-27
alias: [décote, surcote, taux plein, âge de départ]
resume: >-
  Liquider avant l'âge du taux plein automatique sans la durée d'assurance
  requise applique une décote définitive sur le taux de la pension. À l'âge du
  taux plein automatique, généralement 67 ans, cette décote ne s'applique plus,
  mais la pension peut rester proratisée si des trimestres manquent.
sources:
  - type: texte_legal
    ref: Code de la sécurité sociale, article L351-1 (taux plein)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047308748
    consulte_le: 2026-07-27
  - type: texte_legal
    ref: Code de la sécurité sociale, article D351-1-4 (surcote)
    url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047621158
    consulte_le: 2026-07-27
  - type: administration
    ref: Assurance retraite — décote et surcote
    url: https://www.lassuranceretraite.fr
    consulte_le: 2026-07-27
chiffres:
  - cle: Décote par trimestre manquant
    valeur: "0,625"
    unite: "%"
    source: 2
    a_verifier: true
  - cle: Nombre maximal de trimestres de décote
    valeur: "20"
    source: 2
    a_verifier: true
  - cle: Surcote par trimestre supplémentaire
    valeur: "1,25"
    unite: "%"
    source: 1
    a_verifier: true
  - cle: Âge d'annulation automatique de la décote
    valeur: "67"
    unite: "ans"
    source: 0
relations:
  prerequis_de:
    - retraite_trimestres_validation
  complete_par:
    - per_deduction_versements
    - protection_sociale_invalidite
erreurs_frequentes:
  - Croire que la décote se rattrape en travaillant plus tard. Elle est appliquée définitivement au moment de la liquidation.
  - Croire qu'atteindre l'âge légal suffit. Avant l'âge du taux plein automatique, il faut aussi la durée d'assurance requise pour éviter la décote.
  - Croire qu'une retraite au taux plein automatique à 67 ans garantit une pension complète : le taux est plein, mais le montant peut rester proratisé si des trimestres manquent.
  - Ignorer que la décote frappe aussi la retraite complémentaire, ce qui double son effet réel.
  - Liquider sans avoir demandé son relevé de carrière, alors que les erreurs y sont fréquentes et corrigibles.
questions_clients:
  - Que se passe-t-il si je pars avant d'avoir tous mes trimestres ?
  - Vaut-il mieux travailler un an de plus ?
  - Puis-je corriger ma carrière après la liquidation ?
a_ne_pas_dire:
  - Ne pas citer de taux ni de durée sans préciser la génération concernée : la réforme de 2023 les fait varier.
  - Ne pas conseiller un âge de départ : la décision dépend de l'état de santé, du métier et de la situation familiale.
---

## Le mécanisme

La pension du régime général dépend du salaire annuel moyen, du taux de calcul
et du rapport entre les trimestres acquis au régime général et les trimestres
requis. Avant l'âge du taux plein automatique, le taux maximal suppose une
durée d'assurance déterminée par la génération.

Liquider avant l'âge du taux plein automatique sans cette durée applique une
**décote** : le taux est minoré définitivement. À l'âge du taux plein
automatique, généralement 67 ans pour les personnes nées à partir de 1955, la
décote ne s'applique plus. Cependant, si des trimestres manquent, le montant de
la pension de base peut rester réduit par le coefficient de proratisation.

## Ce qui se joue vraiment

Une décote appliquée au moment de la liquidation n'est pas temporaire. Elle
réduit le taux de calcul pour toute la durée de la pension. Il faut donc
distinguer la décote, le taux plein automatique et la proratisation.

L'effet est en pratique plus lourd encore, car la décote frappe aussi la
retraite complémentaire, calculée selon ses propres règles. Le manque à gagner
réel dépasse donc le pourcentage annoncé pour le seul régime de base.

## Le point de vigilance

Tout se joue sur le relevé de carrière, où les erreurs sont fréquentes :
trimestres d'apprentissage oubliés, périodes de chômage mal reportées, employeur
disparu. Ces corrections se demandent avant la liquidation. Après, elles
deviennent nettement plus difficiles à obtenir.
**Concept** : `retraite_decote_surcote`

---

| # | Beat | Narration | Visuel | Texte écran |
|--:|------|-----------|--------|-------------|
| 1 | Hook | Perdre 100 euros par mois à la retraite n’est jamais temporaire. | Plan serré sur un relevé de pension avec une ligne en rouge indiquant une retenue mensuelle. | 100 € en moins, à vie |
| 2 | Enjeu | Rater un trimestre, c’est perdre sur chaque mois, pendant toutes vos années de retraite. Ce n’est pas juste une erreur qui dure un an. | Visage d’une personne qui s’interroge devant ses comptes, caméra sur ses mains calculant le total sur une calculatrice. | Un choix à vie |
| 3 | Mécanisme | Dans le régime général, partir sans tous ses trimestres impose une décote. Cette diminution de la pension s’applique si vous n’avez pas validé la durée requise selon votre année de naissance. Elle est calculée par trimestre manquant, et s’applique à chaque paiement, pendant toute la retraite, sauf si vous atteignez 67 ans, âge de suppression automatique de la décote. | Infographie animée montrant deux chemins : une ligne bleue continue après le taux plein, une ligne rouge baisse si la durée n'est pas atteinte. | Décote : règle définitive |
| 4 | Exemple chiffré | Imaginons Julie. Sa retraite de base aurait dû être de 1 600 euros par mois. Il lui manque un trimestre, elle prend sa retraite quand même. Sa pension passe à 1 500 euros par mois. Sur vingt ans, Julie perd 1 200 euros par an, donc 24 000 euros au total. Cette différence ne disparaît jamais. | Montage : Portrait de Julie côté texte, carton animé “1 600 €” barré et remplacé par “1 500 €”, puis pile de billets et calculateur en incrustation. | Julie : 24 000 € perdus |
| 5 | Erreur fréquente | Beaucoup pensent qu’en continuant à travailler après, la décote s’efface. Ce n’est pas le cas : c’est le choix au moment du départ qui compte. Vérifier vos relevés avant de liquider est donc essentiel. | Plan sur écran d’ordinateur affichant un relevé de carrière, avec doigt qui montre une ligne oubliée. | Pas de rattrapage possible |
| 6 | Clôture | Vous pensiez que la décote était temporaire ? Enregistrez si ça peut éviter une mauvaise surprise à quelqu’un autour de vous. | Main qui coche une case « à vérifier » sur une liste « retraite » ; mouvement de caméra vers l’écran de recherches. | Décote : pensez-y |

---

## Narration continue

Perdre 100 euros par mois à la retraite n’est jamais temporaire. Rater un trimestre, c’est perdre sur chaque mois, pendant toutes vos années de retraite. Ce n’est pas juste une erreur qui dure un an. Dans le régime général, partir sans tous ses trimestres impose une décote. Cette diminution de la pension s’applique si vous n’avez pas validé la durée requise selon votre année de naissance. Elle est calculée par trimestre manquant, et s’applique à chaque paiement, pendant toute la retraite, sauf si vous atteignez 67 ans, âge de suppression automatique de la décote. Imaginons Julie. Sa retraite de base aurait dû être de 1 600 euros par mois. Il lui manque un trimestre, elle prend sa retraite quand même. Sa pension passe à 1 500 euros par mois. Sur vingt ans, Julie perd 1 200 euros par an, donc 24 000 euros au total. Cette différence ne disparaît jamais. Beaucoup pensent qu’en continuant à travailler après, la décote s’efface. Ce n’est pas le cas : c’est le choix au moment du départ qui compte. Vérifier vos relevés avant de liquider est donc essentiel. Vous pensiez que la décote était temporaire ? Enregistrez si ça peut éviter une mauvaise surprise à quelqu’un autour de vous.

## Légende

Une décote appliquée à votre départ en retraite dure toute la vie, pas seulement quelques années. Vérifiez bien vos trimestres avant de liquider. Contenu à vocation pédagogique. Ne constitue ni un conseil en investissement, ni une recommandation personnalisée.

## Hashtags

#patrimoinefrançais #retraite2024 #comprendreladecote #prépareraretraite #levéria

## Sources

- Code de la sécurité sociale, article L351-1 (taux plein) — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047308748
- Assurance retraite — décote et surcote — https://www.lassuranceretraite.fr
---

| # | Beat | Narration | Visuel | Texte écran |
|--:|------|-----------|--------|-------------|
| 1 | Hook | Quatre trimestres manquants à la retraite, c’est moins chaque mois… à vie. | Gros plan sur un calendrier de bureau, mise en évidence de 4 cases vides à la fin d'une année. | 4 trimestres, impact à vie |
| 2 | Enjeu | Un départ trop tôt n’impacte pas seulement une année mais réduit chaque versement de pension, pour toute la retraite, y compris la complémentaire. | Zoom sur un portefeuille ouvert, billets qui disparaissent progressivement à chaque passage de main. | Pension réduite chaque mois |
| 3 | Mécanisme | Pour obtenir une retraite au taux plein, il ne suffit pas d’atteindre l’âge légal. Il faut avoir le nombre de trimestres exigé selon son année de naissance. Si ce total n’est pas atteint le jour où l’on liquide sa retraite, une réduction s’applique définitivement sur la pension de base. Cette réduction s’ajoute aussi, souvent, à la complémentaire. | Graphique simple d’un puzzle représentant une carrière professionnelle, avec une pièce manquante correspondant à un trimestre manquant. | Taux plein = âge ET trimestres |
| 4 | Exemple chiffré | Prenons Clara, qui part en retraite avec quatre trimestres en moins. Au lieu de toucher 1 600 euros par mois, sa pension tombe à 1 500. Sur vingt ans, cela représente 24 000 euros de moins, même si elle a eu l’âge requis. Ce montant manqué s’étend sur toute la durée de sa retraite. | Plan sur un relevé de pension avec la somme 1 600 euros barrée, remplacée par 1 500 euros, puis calcul à la main sur une feuille. | 1 600 € devient 1 500 € |
| 5 | Erreur fréquente | En réalité, cette réduction n’est jamais retirée, sauf à partir de 67 ans (âge d’annulation de la décote). L’erreur se joue souvent sur un relevé de carrière incomplet. | Ordinateur affichant un relevé de carrière, loupe sur des trimestres oubliés ou absents. | Erreur : décote à vie |
| 6 | Clôture | Votre relevé de carrière est-il complet ? Enregistrez ce rappel avant de prendre toute décision et parlez-en autour de vous. | Plan dynamique sur un smartphone affichant une checklist de trimestres, geste de sauvegarde ou partage à l’écran. | Pensez à vérifier ! |

---

## Narration continue

Quatre trimestres manquants à la retraite, c’est moins chaque mois… à vie. Un départ trop tôt n’impacte pas seulement une année mais réduit chaque versement de pension, pour toute la retraite, y compris la complémentaire. Pour obtenir une retraite au taux plein, il ne suffit pas d’atteindre l’âge légal. Il faut avoir le nombre de trimestres exigé selon son année de naissance. Si ce total n’est pas atteint le jour où l’on liquide sa retraite, une réduction s’applique définitivement sur la pension de base. Cette réduction s’ajoute aussi, souvent, à la complémentaire. Prenons Clara, qui part en retraite avec quatre trimestres en moins. Au lieu de toucher 1 600 euros par mois, sa pension tombe à 1 500. Sur vingt ans, cela représente 24 000 euros de moins, même si elle a eu l’âge requis. Ce montant manqué s’étend sur toute la durée de sa retraite. En réalité, cette réduction n’est jamais retirée, sauf à partir de 67 ans (âge d’annulation de la décote). L’erreur se joue souvent sur un relevé de carrière incomplet. Votre relevé de carrière est-il complet ? Enregistrez ce rappel avant de prendre toute décision et parlez-en autour de vous.

## Légende

L’âge seul ne suffit pas : chaque trimestre manquant peut réduire vos revenus à vie. Pensez à vérifier votre carrière avant tout départ en retraite. Contenu à vocation pédagogique. Ne constitue ni un conseil en investissement, ni une recommandation personnalisée.

## Hashtags

#retraite #pension #trimestres #droitssociaux #gestionpatrimoine

## Sources

- Code de la sécurité sociale, article L351-1
- Code de la sécurité sociale, article D351-1-4
- Assurance retraite — décote et surcote — www.lassuranceretraite.fr

---

| # | Beat | Narration | Visuel | Texte écran |
|--:|------|-----------|--------|-------------|
| 1 | Hook | Saviez-vous que le family office n'a aucune reconnaissance officielle ? N'importe qui peut se prévaloir du titre de family office, car ce n'est pas une appellation réglementée. | Gros plan sur une plaque élégante de bureau affichant « Family Office » ; fondu vers des mains anonymes qui installent la plaque. | Family office : un nom, pas un diplôme |
| 2 | Enjeu | Si vous confiez tout à une structure non vérifiée, vous risquez de payer cher pour un service qui n’offre ni cohérence ni sécurité renforcée pour votre patrimoine. | Plan serré sur des papiers officiels signés à la hâte, puis transition vers un visage dubitatif, dossier en main. | Vérifiez avant de confier |
| 3 | Mécanisme | Le family office coordonne plusieurs experts : notaire, avocat, banquier. Son rôle est de donner une vue d'ensemble et d’arbitrer quand les conseils se contredisent. Mais la loi ne protège pas ce métier. Ce qui compte vraiment, c’est l’agrément de chacun et la façon dont ils sont rémunérés, honoraires ou rétrocessions. | Mouvement latéral sur une table de réunion avec des professions différentes représentées (code couleur ou accessoires distinctifs), puis arrêt caméra sur une main qui relie visuellement les dossiers. | La cohérence, pas le placement |
| 4 | Exemple chiffré | Imaginez Laura, 38 ans. Elle possède une entreprise estimée à un million d’euros, un appartement à 500 000 euros et un compte-titres. Elle sollicite un family office. Si celui-ci touche des rétrocessions des produits recommandés, il peut privilégier ses propres intérêts, et non la cohérence entre la transmission familiale et la gestion d’entreprise. | Split-screen : côté gauche, Laura discute avec un interlocuteur ; côté droit, piles de documents étiquetés ‘Entreprise’, ‘Immobilier’, ‘Placements’. Zoom sur le virement ou la commission. | Rémunération : la vraie question |
| 5 | Erreur fréquente | Beaucoup pensent qu’un family office garantit un conseil neutre. En réalité, sans contrôle sur les agréments ni sur leur rémunération, le risque de conflits d’intérêts reste élevé, surtout si la structure est payée par rétrocessions. | Animation simple : fenêtres pop-up ‘Neutre ?’, qui se ferment sur la mention ‘Vérifiez les agréments’ ; case à cocher sur mode de rémunération. | Pas automatic. de garanties |
| 6 | Clôture | Vous aviez déjà vérifié les agréments d’un family office avant de confier votre patrimoine ? Pensez à enregistrer ce point d’alerte pour vos proches. | Plan final d’un écran d’ordinateur sur lequel une page ‘Vérifier un professionnel’ est ouverte. | Pensez à vérifier |

---

## Narration continue

Saviez-vous que le family office n'a aucune reconnaissance officielle ? N'importe qui peut se prévaloir du titre de family office, car ce n'est pas une appellation réglementée. Si vous confiez tout à une structure non vérifiée, vous risquez de payer cher pour un service qui n’offre ni cohérence ni sécurité renforcée pour votre patrimoine. Le family office coordonne plusieurs experts : notaire, avocat, banquier. Son rôle est de donner une vue d'ensemble et d’arbitrer quand les conseils se contredisent. Mais la loi ne protège pas ce métier. Ce qui compte vraiment, c’est l’agrément de chacun et la façon dont ils sont rémunérés, honoraires ou rétrocessions. Imaginez Laura, 38 ans. Elle possède une entreprise estimée à un million d’euros, un appartement à 500 000 euros et un compte-titres. Elle sollicite un family office. Si celui-ci touche des rétrocessions des produits recommandés, il peut privilégier ses propres intérêts, et non la cohérence entre la transmission familiale et la gestion d’entreprise. Beaucoup pensent qu’un family office garantit un conseil neutre. En réalité, sans contrôle sur les agréments ni sur leur rémunération, le risque de conflits d’intérêts reste élevé, surtout si la structure est payée par rétrocessions. Vous aviez déjà vérifié les agréments d’un family office avant de confier votre patrimoine ? Pensez à enregistrer ce point d’alerte pour vos proches.

## Légende

Le family office n’offre pas de garanties automatiques. Vérifiez les agréments et la rémunération avant de confier votre patrimoine. Contenu à vocation pédagogique. Ne constitue ni un conseil en investissement, ni une recommandation personnalisée.

## Hashtags

#patrimoinecomplexe #familyoffice #conseilindependant #coherencedupatrimoine #conflitsdinterets
