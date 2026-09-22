---
id: fiscalite_plafonnement_niches
titre: Le plafonnement global des niches fiscales
domaine: fiscalite
type: regime_fiscal
statut: valide
difficulte: intermediaire
potentiel_viral: 8
cree_le: 2026-07-29
revise_le: 2026-07-29
alias:
- plafonnement des niches
- 10000 euros niches fiscales
- cumul réductions d'impôt
resume: Les avantages fiscaux cumulés d'un foyer sont plafonnés à 10 000 € par an, porté à 18 000 € pour
  certains dispositifs outre-mer et cinéma. Plusieurs dispositifs majeurs — dont les dons et l'emploi
  à domicile pour partie — en sont exclus.
sources:
- type: texte_legal
  ref: CGI, article 200-0 A (plafonnement global des avantages fiscaux)
- type: texte_legal
  ref: CGI, article 199 undecies A (investissements outre-mer)
- type: texte_legal
  ref: CGI, article 200 (réduction pour dons aux œuvres)
- type: bofip
  ref: BOI-IR-LIQ-20-20-10 (plafonnement global)
  url: https://bofip.impots.gouv.fr/doctrine/BOI-IR-LIQ-20-20-10
  consulte_le: 2026-07-29
chiffres:
- cle: Plafond global de droit commun
  valeur: 10 000
  unite: €
  source: 0
  commentaire: par an et par foyer fiscal
- cle: Plafond majoré pour certains dispositifs outre-mer et Sofica
  valeur: 18 000
  unite: €
  source: 0
relations:
  regi_par:
  - fiscalite_quotient_familial
  complete_par:
  - immobilier_revenus_fonciers_micro
  s_applique_a:
  - immobilier_deficit_foncier
  - per_deduction_versements
  alternative_a:
  - fiscalite_quotient_familial
erreurs_frequentes:
- Croire que toutes les réductions entrent dans le plafond. Les dons aux œuvres et plusieurs dispositifs
  sociaux en sont exclus.
- Confondre déduction du revenu et réduction d'impôt. Le plafonnement ne vise que les secondes ; le déficit
  foncier et les versements PER sont des déductions.
- Empiler des dispositifs sans vérifier le cumul, et perdre l'avantage de celui souscrit en dernier.
- Croire que la fraction perdue est reportable. Elle ne l'est généralement pas, sauf disposition spécifique
  propre à certains dispositifs.
questions_clients:
- Puis-je cumuler plusieurs dispositifs de défiscalisation ?
- Mes dons comptent-ils dans le plafond ?
- Que se passe-t-il si je dépasse ?
a_ne_pas_dire:
- Ne jamais dire au spectateur quel dispositif de défiscalisation souscrire. Montrer l'effet du plafond
  sur un cas fictif reste permis.
- Ne pas présenter une réduction d'impôt comme un rendement — l'avantage fiscal ne compense pas un mauvais
  investissement.
---

## Le mécanisme

L'article 200-0 A limite la somme des avantages fiscaux dont un foyer peut
bénéficier au titre d'une année : **10 000 €**, tous dispositifs plafonnés
confondus.

Un plafond majoré de 18 000 € s'applique à certains investissements outre-mer et
aux souscriptions au capital de Sofica.

Ce qui dépasse est perdu. Il n'y a pas de report sur l'année suivante, sauf pour
les rares dispositifs qui prévoient expressément un étalement.

## Ce qui se joue vraiment

La distinction décisive est celle entre **déduction du revenu** et **réduction
d'impôt**.

Une déduction diminue le revenu imposable avant application du barème : versements
sur un PER, déficit foncier, pension alimentaire. Elle n'est pas concernée par le
plafonnement.

Une réduction ou un crédit s'impute sur l'impôt calculé : investissement
locatif, FCPI, garde d'enfants. C'est cette catégorie que le plafond vise.

Un contribuable qui pense avoir « atteint le plafond » alors qu'il n'a que des
déductions se prive donc de dispositifs qu'il pourrait encore utiliser — et
l'inverse est tout aussi fréquent.

## Le point de vigilance

L'ordre d'imputation compte. Quand plusieurs dispositifs plafonnés coexistent,
c'est celui souscrit en dernier qui saute — alors même que c'est souvent celui
pour lequel un engagement pluriannuel a été pris.

Enfin, un dispositif qui procure un avantage fiscal reste un investissement. Un
bien mal situé, un fonds illiquide ou une opération surévaluée à l'entrée ne
deviennent pas rentables parce que l'État en rembourse une fraction.
scripts/fiscalite/fiscalite_quotient_familial__multi__a3.md:12:| 1 | Hook | Rattacher son enfant étudiant peut coûter plus cher que lui verser une pension. Même avec un plafond d’avantage à 1 807 euros en 2026. | Plan serré sur une main tenant deux lettres d’avis d’imposition, puis glisse vers un étudiant devant son ordinateur. | Plafond demi-part : 1 807 € |
scripts/fiscalite/fiscalite_quotient_familial__multi__a3.md:14:| 3 | Mécanisme | Le quotient familial attribue une demi-part pour chacun des deux premiers enfants rattachés, mais l'avantage fiscal est plafonné. Pour un enfant majeur, soit vous le rattachez, soit vous déduisez une pension alimentaire. Si vous atteignez déjà le plafond d’avantage par demi-part, le rattachement rapporte moins que la déduction de la pension. | Tableau montrant deux colonnes : « Rattachement » et « Pension alimentaire », avec des zones surlignées. | Rattachement ou pension ? |
scripts/fiscalite/fiscalite_quotient_familial__multi__a3.md:15:| 4 | Exemple chiffré | Prenons Léa, une fille majeure, étudiante. Ses parents sont un couple marié, déjà en tranche élevée. Le rattachement ouvre à 0,5 part de plus, mais l’économie d’impôt est plafonnée à 1 807 euros en 2026. S’ils déduisent une pension, la somme déduite peut dépasser ce plafond, avec une vraie économie si leur revenu est élevé. | Animation d’un calcul avec 1 807 € affiché, puis un second calcule une pension déduite plus élevée. | Le calcul change tout |
scripts/fiscalite/fiscalite_quotient_familial__multi__a3.md:23:Rattacher son enfant étudiant peut coûter plus cher que lui verser une pension. Même avec un plafond d’avantage à 1 807 euros en 2026. Le mauvais choix peut amputer vos économies d’impôts de plusieurs centaines d’euros. Et ça ne dépend pas uniquement du nombre d’enfants ou de votre tranche. Le quotient familial attribue une demi-part pour chacun des deux premiers enfants rattachés, mais l'avantage fiscal est plafonné. Pour un enfant majeur, soit vous le rattachez, soit vous déduisez une pension alimentaire. Si vous atteignez déjà le plafond d’avantage par demi-part, le rattachement rapporte moins que la déduction de la pension. Prenons Léa, une fille majeure, étudiante. Ses parents sont un couple marié, déjà en tranche élevée. Le rattachement ouvre à 0,5 part de plus, mais l’économie d’impôt est plafonnée à 1 807 euros en 2026. S’ils déduisent une pension, la somme déduite peut dépasser ce plafond, avec une vraie économie si leur revenu est élevé. Beaucoup croient que rattacher son enfant donne toujours l’avantage maximal. Mais si votre quotient est déjà plafonné, vous perdez la possibilité de déduire une pension potentiellement plus intéressante fiscalement. Envisagez-vous de comparer les deux méthodes avant de déclarer ? Enregistrez cette vidéo pour ne pas oublier de refaire le calcul à chaque rentrée.
scripts/fiscalite/fiscalite_quotient_familial__multi__a4.md:14:| 3 | Mécanisme | Le rattachement d’un enfant majeur étudiant donne une demi-part supplémentaire au foyer pour le calcul de l’impôt. Mais le gain fiscal lié au quotient familial est plafonné à 1 807 euros par demi-part pour l’imposition 2026. Si vos revenus sont élevés, cet avantage est vite atteint, et l’économie ne progresse plus, quel que soit le revenu. | Animation graphique montrant un barème fiscal, une division par parts puis arrêt net du gain dès le plafond. | Avantage bloqué à 1 807 € |
scripts/fiscalite/fiscalite_quotient_familial__multi__a4.md:15:| 4 | Exemple chiffré | Prenons Judith. Son foyer est imposé à un taux élevé. Rattacher son fils étudiant lui donne droit à une demi-part en plus, mais dès que l’économie atteint 1 807 euros, le plafond bloque le gain. Verser une pension alimentaire pourrait alors lui permettre de déduire un montant plus important, selon sa situation concrète. | Plan sur un parent remplissant deux scénarios : une case demi-part barrée à 1 807 €, une autre montrant une ligne « pension déduite » plus haute. | Rattacher ou déduire ? |
scripts/fiscalite/fiscalite_quotient_familial__multi__a4.md:23:Rattacher son enfant étudiant n’offre pas toujours 1 807 euros d’économie d’impôt. Si vous gagnez bien votre vie, mal choisir entre rattachement ou pension peut vous coûter plusieurs centaines d’euros chaque année, sans que vous le réalisiez. Le rattachement d’un enfant majeur étudiant donne une demi-part supplémentaire au foyer pour le calcul de l’impôt. Mais le gain fiscal lié au quotient familial est plafonné à 1 807 euros par demi-part pour l’imposition 2026. Si vos revenus sont élevés, cet avantage est vite atteint, et l’économie ne progresse plus, quel que soit le revenu. Prenons Judith. Son foyer est imposé à un taux élevé. Rattacher son fils étudiant lui donne droit à une demi-part en plus, mais dès que l’économie atteint 1 807 euros, le plafond bloque le gain. Verser une pension alimentaire pourrait alors lui permettre de déduire un montant plus important, selon sa situation concrète. Beaucoup pensent qu’il suffit de rattacher pour maximiser l’économie d’impôt. Mais au-delà du plafond, ils perdent le bénéfice d’une pension alimentaire déduite, parfois plus avantageuse pour les revenus élevés. C’est l’erreur qui coûte le plus cher. Qui, dans votre entourage, compare ces deux options avant de choisir ? Mieux vaut vérifier son calcul ou enregistrer cette vidéo pour y revenir au moment de déclarer.
scripts/fiscalite/fiscalite_quotient_familial__multi__a1.md:12:| 1 | Hook | 1 807 euros : c'est le maximum que chaque demi-part peut faire économiser. Pas centime de plus, même pour votre voisin. | Gros plan sur un avis d’imposition, surlignage du montant "1 807 €", puis zoom sur deux boîtes aux lettres voisines. | 1 807 € par demi-part |
scripts/fiscalite/fiscalite_quotient_familial__multi__a1.md:14:| 3 | Mécanisme | Le quotient familial divise d’abord le revenu imposable par un nombre de parts, selon le nombre d’enfants. Plus il y a de parts, plus l’impôt diminue. Mais ce gain est plafonné : chaque demi-part d’enfant ne peut pas réduire l’impôt de plus de 1 807 euros. Si votre impôt baisse davantage, le fisc bloque la réduction à ce plafond. | Schéma animé : fraction du revenu par les parts, apparaissant "+0,5 part par enfant", puis apparition d’un cadenas symbolisant le plafond. | Réduction plafonnée |
scripts/fiscalite/fiscalite_quotient_familial__multi__a1.md:15:| 4 | Exemple chiffré | Imaginez Alice et Ben, deux voisins mariés, chacun avec deux enfants. Leurs revenus diffèrent : Alice gagne 40 000 euros, Ben en gagne 90 000. Ils ont tous deux trois parts. Alice ne bénéficie pas pleinement du plafond et son économie d’impôt reste assez faible. Ben atteint le maximum, soit 3 614 euros grâce à ses deux demi-parts enfants, mais pas un euro de plus. | Split screen : Alice et Ben, fiche de paie à l’appui, calculatrice à la main. Le chiffre 40 000 € s’affiche, puis 90 000 €. En bas d’écran, la limite 3 614 € apparaît pour Ben. | Jusqu’à 3 614 € |
scripts/fiscalite/fiscalite_quotient_familial__multi__a1.md:…5408 tokens truncated…pilent. Une main tente d’en jeter un, puis hésite. | Trois ans ? Parfois plus |
scripts/fiscalite/fiscalite_controle_fiscal__multi__a4.md:14:| 3 | Mécanisme | Pour les comptes bancaires et certains avoirs financiers non déclarés détenus à l'étranger, l’administration a dix ans pour contrôler. Ce délai s’applique uniquement en cas d’absence totale de déclaration de ces avoirs. Dès qu’un compte bancaire détenu à l’étranger est oublié, la période de reprise peut s’étendre bien au-delà du délai classique. | Split-screen : à gauche, dossier « France » avec post-it « 3 ans » ; à droite, dossier « Étranger » avec post-it « 10 ans ». | Avoirs étrangers : délai spécial |
scripts/fiscalite/fiscalite_controle_fiscal__multi__a4.md:15:| 4 | Exemple chiffré | Antoine ouvre en 2012 un compte à l’étranger avec 15 000 euros. Il oublie de le déclarer en France. En 2022, dix ans plus tard, l’administration découvre le compte. Elle a encore le droit de demander des explications et d’appliquer une régularisation, car le délai de dix ans n’est pas dépassé. | Plan chronologique sur calendrier : 2012, ouverture du compte, puis survol rapide d’années jusqu’à 2022, où un tampon « contrôle fiscal » apparaît en rouge. | Exemple : 10 ans contrôlables |
scripts/fiscalite/fiscalite_controle_fiscal__multi__a4.md:16:| 5 | Erreur fréquente | L’erreur la plus courante ? Penser que tous les documents se jettent après trois ans. Mais pour un compte à l’étranger non déclaré, même un dossier vieux de neuf ans peut rester contrôlable. Jeter trop tôt, c’est s’exposer à ne plus pouvoir justifier la situation. | Plan sur une poubelle : une main y glisse un relevé bancaire étranger de 2015, puis sursaut, main qui le récupère. | Erreur : délai trop court |
scripts/fiscalite/fiscalite_controle_fiscal__multi__a4.md:17:| 6 | Clôture / CTA | Vous pensiez que tout était prescrit après trois ans ? Enregistrez ce rappel, ça peut éviter de mauvaises surprises sur vos anciens placements à l’étranger. | Plan sur quelqu’un qui sauvegarde un document sur son téléphone, air soulagé. | Gardez ce rappel utile |
scripts/fiscalite/fiscalite_controle_fiscal__multi__a4.md:23:Un compte oublié à l’étranger ? L’administration fiscale peut s’y intéresser dix ans plus tard. Vous pensiez que tout était prescrit après trois ans ? Ce délai de prescription s’applique principalement à l’impôt sur le revenu ; pour les avoirs à l’étranger non déclarés, le délai atteint dix ans. Pour les comptes bancaires et certains avoirs financiers non déclarés détenus à l'étranger, l’administration a dix ans pour contrôler. Ce délai s’applique uniquement en cas d’absence totale de déclaration de ces avoirs. Dès qu’un compte bancaire détenu à l’étranger est oublié, la période de reprise peut s’étendre bien au-delà du délai classique. Antoine ouvre en 2012 un compte à l’étranger avec 15 000 euros. Il oublie de le déclarer en France. En 2022, dix ans plus tard, l’administration découvre le compte. Elle a encore le droit de demander des explications et d’appliquer une régularisation, car le délai de dix ans n’est pas dépassé. L’erreur la plus courante ? Penser que tous les documents se jettent après trois ans. Mais pour un compte à l’étranger non déclaré, même un dossier vieux de neuf ans peut rester contrôlable. Jeter trop tôt, c’est s’exposer à ne plus pouvoir justifier la situation. Vous pensiez que tout était prescrit après trois ans ? Enregistrez ce rappel, ça peut éviter de mauvaises surprises sur vos anciens placements à l’étranger.
scripts/fiscalite/fiscalite_controle_fiscal__multi__a4.md:27:Avoirs à l’étranger jamais déclarés : le contrôle peut remonter dix ans, même si tout semblait oublié. Connaissez-vous la règle ? Contenu à vocation pédagogique. Ne constitue ni un conseil en investissement, ni une recommandation personnalisée.
scripts/fiscalite/fiscalite_controle_fiscal__multi__a4.md:39:Rythme soutenu, musique légère mais tendue, transitions vives entre chaque beat. Les plans concrets sur les documents renforcent l’ancrage dans la vie réelle. Faire ressortir la notion de temps qui passe, insister visuellement sur la différence de délai France/Étranger.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a1.md:6:**Concept** : `fiscalite_plafonnement_niches`
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a1.md:12:| 1 | Hook | Vous pensez avoir rempli votre quota avec 10 000 € de réductions d’impôt ? Ce n’est pas le bon plafond. | Main qui coche une case « Plafond atteint » sur avis d’imposition, gros plan sur le chiffre 10 000 €. | 10 000 € : pas le seul plafond |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a1.md:14:| 3 | Mécanisme | Le plafond global de 10 000 euros vise uniquement les réductions et crédits d’impôt, comme le dispositif Pinel ou l’investissement dans certaines sociétés. Les déductions du revenu imposable — comme un versement sur un Plan Épargne Retraite ou des travaux créant du déficit foncier — n’entrent pas dans ce calcul, car elles diminuent votre revenu avant impôt. | Tableau simple : d’un côté, « Réduction d’impôt = plafond » ; de l’autre, « Déduction du revenu = hors plafond ». | Plafond : réduc. ≠ déduction |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a1.md:15:| 4 | Exemple chiffré | Imaginons Alice : elle obtient 8 000 euros de réduction d’impôt grâce à un investissement locatif, et déduit en plus 4 000 euros de versements sur un Plan Épargne Retraite. Malgré le plafond des 10 000 euros, ses déductions du revenu — les 4 000 euros — restent possibles, car seules ses réductions sont concernées. | Fiche avec le détail du calcul : ligne réduction d’impôt 8 000 €, ligne déduction 4 000 €, et case plafond cochée uniquement sur la ligne réduction. | Réduction plafonnée, déduction non |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a1.md:16:| 5 | Erreur fréquente | La confusion entre déduction et réduction d’impôt fait perdre des avantages à beaucoup de contribuables. Certains arrêtent tout en atteignant 10 000 euros, alors qu’ils pouvaient continuer avec des déductions sans dépasser aucun plafond. | Plan de geste : dossier marqué « Arrêté » posé sur un bureau, puis révélation d’un dossier « Déduction encore possible » resté fermé. | Ne stoppez pas trop tôt |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a1.md:23:Vous pensez avoir rempli votre quota avec 10 000 € de réductions d’impôt ? Ce n’est pas le bon plafond. Beaucoup renoncent à des avantages fiscaux en pensant à tort que le plafond global bloque tout. Mais mélanger plafonds, c’est parfois laisser de l’argent sur la table. Le plafond global de 10 000 euros vise uniquement les réductions et crédits d’impôt, comme le dispositif Pinel ou l’investissement dans certaines sociétés. Les déductions du revenu imposable — comme un versement sur un Plan Épargne Retraite ou des travaux créant du déficit foncier — n’entrent pas dans ce calcul, car elles diminuent votre revenu avant impôt. Imaginons Alice : elle obtient 8 000 euros de réduction d’impôt grâce à un investissement locatif, et déduit en plus 4 000 euros de versements sur un Plan Épargne Retraite. Malgré le plafond des 10 000 euros, ses déductions du revenu — les 4 000 euros — restent possibles, car seules ses réductions sont concernées. La confusion entre déduction et réduction d’impôt fait perdre des avantages à beaucoup de contribuables. Certains arrêtent tout en atteignant 10 000 euros, alors qu’ils pouvaient continuer avec des déductions sans dépasser aucun plafond. Qui, autour de vous, confond plafond et déduction ? Enregistrez ce rappel ou partagez-le à l’ami qui aime surveiller son impôt.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a1.md:31:#impot #avantagefiscal #gestionpatrimoniale #declarationrevenus #nichefiscale
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:1:# Dons, emploi à domicile : sauf erreur, pas plafonnés à 10 000 €
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:5:**Angle** : Certains avantages fiscaux, comme les dons ou l'emploi à domicile, ne sont pas plafonnés et échappent donc au plafond global de 10 000 euros.  
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:6:**Concept** : `fiscalite_plafonnement_niches`
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:12:| 1 | Hook | Le plafond fiscal de 10 000 euros ne bloque pas tous vos avantages. Beaucoup de contribuables l’ignorent. | Gros plan dynamique sur une calculatrice affichant « 10 000 », main qui hésite à entrer un montant supplémentaire. | 10 000 € : mais pas toujours ! |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:14:| 3 | Mécanisme | Le plafond global des niches fiscales, actuellement fixé à 10 000 euros par an et par foyer, s’applique uniquement aux réductions et crédits d'impôt visés par la loi. Mais certains dispositifs majeurs, comme les dons aux œuvres et une partie des dépenses pour l'emploi à domicile, en sont exclus. Pour ces dépenses, la réduction n’entre pas dans le calcul du plafond. | Main qui coche une case « Dons », tandis qu’une autre coche « Investissement locatif » ; l’écran affiche un graphique : certains rectangles dépassent le « plafond », d’autres non. | Tous les avantages ne sont pas plafonnés |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:15:| 4 | Exemple chiffré | Prenons Samira : en 2023, elle donne 2 000 euros à une association d’intérêt général et emploie une aide à domicile pour 5 000 euros de dépenses ouvrant droit à crédit d’impôt. Même si elle bénéficie déjà de 10 000 euros de réductions d’impôt sur d’autres placements, ces 7 000 euros supplémentaires seront pris en compte, car don et emploi à domicile échappent au plafond global. | Tableau simple avec trois colonnes : « Dons : 2 000 € », « Emploi domicile : 5 000 € », « Autres réductions : 10 000 € ». Flèche verte qui passe ces montants sans être arrêtée par un trait « plafond ». | Calcul concret : 17 000 € d’avantage |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:23:Le plafond fiscal de 10 000 euros ne bloque pas tous vos avantages. Beaucoup de contribuables l’ignorent. Vous risquez de passer à côté d’économies d'impôt importantes si vous croyez, à tort, que tous vos dons ou frais d’emploi à domicile sont limités par ce plafond. Le plafond global des niches fiscales, actuellement fixé à 10 000 euros par an et par foyer, s’applique uniquement aux réductions et crédits d'impôt visés par la loi. Mais certains dispositifs majeurs, comme les dons aux œuvres et une partie des dépenses pour l'emploi à domicile, en sont exclus. Pour ces dépenses, la réduction n’entre pas dans le calcul du plafond. Prenons Samira : en 2023, elle donne 2 000 euros à une association d’intérêt général et emploie une aide à domicile pour 5 000 euros de dépenses ouvrant droit à crédit d’impôt. Même si elle bénéficie déjà de 10 000 euros de réductions d’impôt sur d’autres placements, ces 7 000 euros supplémentaires seront pris en compte, car don et emploi à domicile échappent au plafond global. Erreur très courante : penser que tout avantage fiscal est plafonné. Si vous arrêtez vos dons ou votre aide à domicile croyant être bloqué par le plafond, vous perdez un bénéfice légal qui ne devait pas être limité. Vous étiez au courant ? Dites-nous si le plafond global a déjà limité vos économies, ou partagez cette astuce avec vos proches pour éviter la confusion.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a4.md:27:Dons, garde à domicile : tous vos réductions d’impôt ne sont pas plafonnées à 10 000 €. Beaucoup de contribuables l’ignorent ! Contenu à vocation pédagogique. Ne constitue ni un conseil en investissement, ni une recommandation personnalisée.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:5:**Angle** : Vous pouvez perdre tout l’avantage fiscal de votre dernier investissement si vous dépassez le plafond global des niches fiscales.  
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:6:**Concept** : `fiscalite_plafonnement_niches`
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:12:| 1 | Hook | Le plafonnement global, c’est dix mille euros d’avantage fiscal, pas un de plus. | Gros plan sur un relevé d'impôts, surlignage du chiffre 10 000 €, puis plan serré sur un visage surpris. | 10 000 € par an |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:13:| 2 | Enjeu | Si vous placez sans compter, votre dernier dispositif fiscal peut perdre tout son intérêt. Plusieurs années d’engagement… pour aucun avantage fiscal à l’arrivée. | Suites rapides d’images : main qui signe un contrat, puis zoom sur une case « réduction d’impôt » barrée d’une croix rouge. | Dernier gagné, dernier perdu |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:14:| 3 | Mécanisme | Le plafond global limite la somme des réductions et crédits d’impôt à dix mille euros par an, pour chaque foyer fiscal. Si vous dépassez, l’avantage fiscal en trop n’est pas reporté sur les années suivantes. Seules certaines opérations outre-mer ou cinéma voient ce plafond porter à dix-huit mille euros. Les déductions du revenu n’entrent pas dans ce calcul. | Tableau comparant colonne « Réduction d’impôt » et colonne « Déduction du revenu ». Animation visuelle montrant un curseur qui monte à 10 000 €, puis blocage. | Plafond : 10 000 €/an |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:15:| 4 | Exemple chiffré | Imaginons Camille : elle cumule deux dispositifs de réduction d’impôt, un à 6 000 €, l’autre à 6 000 €. Total : 12 000 € attendus. Mais le plafond est de 10 000 €. Résultat : Camille perd deux mille euros d’économie d’impôt, généralement sur le dernier dispositif souscrit, même s’il dure plusieurs années. | Visuel animé d’un calcul : 6 000 + 6 000 = 12 000, puis moins 2 000 avec une flèche rouge. Photo de Camille, sourire qui retombe. | Perte : 2 000 € |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:23:Le plafonnement global, c’est dix mille euros d’avantage fiscal, pas un de plus. Si vous placez sans compter, votre dernier dispositif fiscal peut perdre tout son intérêt. Plusieurs années d’engagement… pour aucun avantage fiscal à l’arrivée. Le plafond global limite la somme des réductions et crédits d’impôt à dix mille euros par an, pour chaque foyer fiscal. Si vous dépassez, l’avantage fiscal en trop n’est pas reporté sur les années suivantes. Seules certaines opérations outre-mer ou cinéma voient ce plafond porter à dix-huit mille euros. Les déductions du revenu n’entrent pas dans ce calcul. Imaginons Camille : elle cumule deux dispositifs de réduction d’impôt, un à 6 000 €, l’autre à 6 000 €. Total : 12 000 € attendus. Mais le plafond est de 10 000 €. Résultat : Camille perd deux mille euros d’économie d’impôt, généralement sur le dernier dispositif souscrit, même s’il dure plusieurs années. Beaucoup pensent que multiplier les placements maximise leurs avantages fiscaux. Mais sans vérifier le cumul, on risque de perdre l’intégralité de l’avantage fiscal du nouvel investissement. C’est l’engagement récent qui saute, sans possibilité de report. Aviez-vous déjà fait le calcul sur vos propres dispositifs ? Sauvegardez la vidéo pour vérifier votre plafond avant de souscrire.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:27:Le plafonnement global des niches fiscales peut effacer l’avantage de votre dernier investissement. Faites le point avant de vous engager ! Contenu à vocation pédagogique. Ne constitue ni un conseil en investissement, ni une recommandation personnalisée.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a2.md:31:#défiscalisation #nichesfiscales #impotrevenu #plafondfiscal #gestionpatrimoine
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a3.md:6:**Concept** : `fiscalite_plafonnement_niches`
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a3.md:12:| 1 | Hook | Si vous dépassez 10 000 euros d’avantage fiscal, c’est toujours la dernière réduction signée qui saute en premier. | Zoom sur des liasses de billets superposées, puis main ajoutant une enveloppe datée du jour. | 10 000 € de plafond |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a3.md:14:| 3 | Mécanisme | Si vous cumulez plusieurs réductions d’impôt soumises au plafond de 10 000 euros par an, il se peut que leur total dépasse ce seuil. Dans ce cas, c’est la réduction liée au dernier dispositif souscrit dans l’année qui est supprimée en premier, sans report possible, sauf exception prévue par la loi. | Suivi d’une main ordonnant, puis superposant visuellement trois contrats datés, le dernier ajoutant un post-it 'supprimé'. | La dernière saute |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a3.md:15:| 4 | Exemple chiffré | Paul utilise 7 000 euros avec un investissement locatif début janvier. En octobre, il place 5 000 euros dans un fonds défiscalisant. Ses réductions atteignent donc 12 000 euros. Comme le plafond légal est de 10 000 euros, les 2 000 euros de trop sont retirés du second avantage, celui souscrit en octobre. Ils sont définitivement perdus. | Tableau avec deux lignes : "Janvier : 7 000 €" et "Octobre : 5 000 €", puis surlignage rouge de "2 000 € perdus" sur la seconde ligne. | Exemple concret |
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a3.md:23:Si vous dépassez 10 000 euros d’avantage fiscal, c’est toujours la dernière réduction signée qui saute en premier. Un ordre mal choisi peut vous coûter l’avantage fiscal d’une année entière, même si vous aviez envisagé de répartir le dépassement autrement. Si vous cumulez plusieurs réductions d’impôt soumises au plafond de 10 000 euros par an, il se peut que leur total dépasse ce seuil. Dans ce cas, c’est la réduction liée au dernier dispositif souscrit dans l’année qui est supprimée en premier, sans report possible, sauf exception prévue par la loi. Paul utilise 7 000 euros avec un investissement locatif début janvier. En octobre, il place 5 000 euros dans un fonds défiscalisant. Ses réductions atteignent donc 12 000 euros. Comme le plafond légal est de 10 000 euros, les 2 000 euros de trop sont retirés du second avantage, celui souscrit en octobre. Ils sont définitivement perdus. Beaucoup pensent qu’ils peuvent choisir quel avantage fiscal conserver en cas de dépassement, ou que l’excédent sera automatiquement reporté sur l'an prochain. Ce n’est pas le cas : seul le dernier dispositif souscrit saute, sauf dispositif prévoyant explicitement un étalement. Aviez-vous déjà fait attention à l’ordre de vos souscriptions ? Enregistrez ce post pour y penser la prochaine fois que vous investirez.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a3.md:27:Le plafond des niches fiscales ne pardonne pas l’ordre des signatures. Exemple simplifié sous conditions légales. Contenu à vocation pédagogique. Ne constitue ni un conseil en investissement, ni une recommandation personnalisée.
scripts/fiscalite/fiscalite_plafonnement_niches__multi__a3.md:31:#reductionsimpot #nichesfiscales #patrimoine #plafonnementfiscal #investissements
