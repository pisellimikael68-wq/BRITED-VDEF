from v2.models.knowledge_models import Topic

ERREURS_TOPICS: list[Topic] = []

Topic(
    id="assurance_vie_erreurs_attendre_8_ans",
    title="Erreur : attendre 8 ans avant d'ouvrir une assurance-vie",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi attendre huit ans avant d'ouvrir une assurance-vie est une erreur fréquente et comment fonctionne réellement l'ancienneté fiscale du contrat.",
    objective="Expliquer que les huit ans correspondent à un jalon fiscal et qu'il est généralement plus pertinent d'ouvrir son contrat dès que possible afin de faire courir son ancienneté.",
    difficulty="Débutant",
    priority=10,
    version=1,
    keywords=[
        "8 ans",
        "ancienneté fiscale",
        "assurance-vie",
        "ouverture",
        "erreur",
        "placement",
        "épargne",
        "fiscalité",
    ],
    key_points=[
        "Les huit ans ne correspondent pas à une période de blocage du contrat.",
        "L'ancienneté fiscale commence à courir dès l'ouverture de l'assurance-vie.",
        "Il est généralement préférable d'ouvrir un contrat tôt, même avec un premier versement modeste.",
        "Attendre plusieurs années avant d'ouvrir une assurance-vie peut retarder l'acquisition de son ancienneté fiscale.",
        "Une assurance-vie peut ensuite être alimentée progressivement selon les projets et les capacités d'épargne."
    ],
    examples=[
        "Julie, 26 ans, pense qu'il faut attendre d'avoir un patrimoine important avant d'ouvrir une assurance-vie. Son conseiller lui explique qu'un premier versement modeste permet déjà de faire courir l'ancienneté du contrat.",

        "Marc reporte chaque année l'ouverture de son assurance-vie en pensant qu'il attendra le bon moment. Dix ans plus tard, il réalise qu'il aurait déjà bénéficié d'une importante ancienneté fiscale s'il avait ouvert son contrat plus tôt.",

        "Claire ouvre une assurance-vie avec un faible montant puis augmente progressivement ses versements au fil de sa carrière. Elle bénéficie ainsi d'une enveloppe déjà ancienne lorsque ses objectifs patrimoniaux évoluent."
    ],
    vocabulary=[
        "ancienneté fiscale",
        "ouverture",
        "versement",
        "rachat",
        "fiscalité",
        "épargne",
        "contrat",
        "horizon de placement",
    ],
    legal_sources=[
        "Code général des impôts",
        "Code des assurances",
        "BOFiP - Assurance-vie",
    ],
    analogies=[
        "Attendre pour ouvrir une assurance-vie revient à attendre pour planter un arbre : plus vous commencez tard, plus vous retardez le moment où il produira ses fruits."
    ],
    misconceptions=[
        "Il faut attendre huit ans avant d'ouvrir une assurance-vie.",
        "L'assurance-vie est bloquée pendant huit ans.",
        "Ouvrir un contrat tôt ne présente aucun intérêt.",
        "Il faut déjà disposer d'un patrimoine important pour ouvrir une assurance-vie."
    ],
    common_mistakes=[
        "Reporter l'ouverture du contrat pendant plusieurs années.",
        "Attendre d'avoir un capital important avant de commencer.",
        "Confondre ancienneté fiscale et indisponibilité des fonds.",
        "Croire que l'ouverture d'une assurance-vie oblige à investir immédiatement des sommes importantes."
    ],
    expert_tips=[
        "En pratique, de nombreux conseillers recommandent d'ouvrir une assurance-vie dès lors qu'elle s'inscrit dans une stratégie patrimoniale, même avec un premier versement limité. Cela permet de faire courir son ancienneté fiscale tout en conservant la liberté d'effectuer des versements ultérieurs."
    ],
    attention_points=[
        "L'ouverture d'un contrat doit toujours répondre à un objectif patrimonial identifié.",
        "Les règles fiscales peuvent évoluer au fil du temps.",
        "L'ancienneté fiscale n'est qu'un des critères à prendre en compte dans une stratégie patrimoniale."
    ],
    client_questions=[
        "Dois-je attendre huit ans ?",
        "Puis-je ouvrir une assurance-vie avec seulement quelques centaines d'euros ?",
        "Quand faut-il ouvrir une assurance-vie ?",
        "Pourquoi parle-t-on toujours des huit ans ?",
    ],
    client_objections=[
        "Je préfère attendre d'avoir davantage d'épargne.",
        "Je suis encore trop jeune.",
        "Je pensais qu'il fallait attendre huit ans."
    ],
    client_fears=[
        "Ouvrir une assurance-vie trop tôt.",
        "Faire une erreur fiscale.",
        "Immobiliser inutilement son épargne."
    ],
    client_goals=[
        "Prendre date fiscalement.",
        "Préparer des projets futurs.",
        "Commencer à construire son patrimoine.",
        "Éviter les erreurs les plus fréquentes."
    ],
    client_intents=[
        "ouvrir une assurance-vie",
        "ancienneté fiscale",
        "assurance-vie 8 ans",
        "quand ouvrir une assurance-vie",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_questions_bloquee_8_ans",
        "assurance_vie_ouverture_pourquoi_ouvrir",
        "assurance_vie_fiscalite_8_ans",
        "assurance_vie_questions_pourquoi_assurance_vie",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
        "assurance_vie_questions_bloquee_8_ans",
    ],
    next_topics=[
        "assurance_vie_erreurs_clause_beneficiaire",
    ],
),

Topic(
    id="assurance_vie_erreurs_clause_beneficiaire",
    title="Erreur : ne jamais mettre à jour sa clause bénéficiaire",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi une clause bénéficiaire doit être régulièrement relue et adaptée aux évolutions familiales et patrimoniales.",
    objective="Expliquer qu'une clause bénéficiaire figée pendant plusieurs années peut ne plus correspondre aux volontés du souscripteur et compromettre l'efficacité de sa stratégie de transmission.",
    difficulty="Intermédiaire",
    priority=10,
    version=1,
    keywords=[
        "clause bénéficiaire",
        "transmission",
        "assurance-vie",
        "succession",
        "bénéficiaire",
        "divorce",
        "famille recomposée",
        "mise à jour",
    ],
    key_points=[
        "La clause bénéficiaire constitue l'un des éléments les plus importants d'une assurance-vie.",
        "Les événements familiaux peuvent rendre une clause ancienne inadaptée.",
        "Une clause bénéficiaire mérite d'être relue régulièrement.",
        "Une rédaction imprécise peut générer des difficultés lors du dénouement du contrat.",
        "La stratégie de transmission doit évoluer avec la situation patrimoniale et familiale."
    ],
    examples=[
        "Jean divorce mais oublie de modifier la clause bénéficiaire rédigée vingt ans auparavant. Au moment de son décès, celle-ci ne reflète plus ses volontés.",

        "Claire se remarie et accueille un nouvel enfant. Elle profite de cette évolution familiale pour revoir entièrement la rédaction de sa clause bénéficiaire afin qu'elle corresponde à sa nouvelle situation.",

        "Marc ouvre une assurance-vie à 35 ans. Vingt-cinq ans plus tard, il possède un patrimoine beaucoup plus important et une famille recomposée. Une simple relecture de sa clause permet d'identifier plusieurs adaptations nécessaires."
    ],
    vocabulary=[
        "clause bénéficiaire",
        "bénéficiaire",
        "acceptation",
        "transmission",
        "succession",
        "rédaction",
        "souscripteur",
        "dénouement",
    ],
    legal_sources=[
        "Code des assurances",
        "Code civil",
    ],
    analogies=[
        "Une clause bénéficiaire ressemble à un testament vivant : si votre vie évolue mais que vous ne la mettez jamais à jour, elle risque de ne plus refléter vos véritables intentions."
    ],
    misconceptions=[
        "Une clause bénéficiaire se rédige une seule fois.",
        "Mon testament suffit à modifier automatiquement ma clause bénéficiaire.",
        "La clause standard proposée lors de la souscription est toujours adaptée.",
        "Ma situation familiale n'a aucune incidence sur mon assurance-vie."
    ],
    common_mistakes=[
        "Ne jamais relire sa clause bénéficiaire.",
        "Conserver une clause standard malgré une famille recomposée.",
        "Oublier de modifier la clause après un mariage, un divorce ou une naissance.",
        "Rédiger une clause trop imprécise."
    ],
    expert_tips=[
        "Une bonne pratique consiste à relire sa clause bénéficiaire à chaque événement familial majeur : mariage, PACS, divorce, naissance, décès ou évolution significative du patrimoine. Une vérification régulière permet souvent d'éviter des conséquences très éloignées des intentions initiales."
    ],
    attention_points=[
        "La rédaction d'une clause bénéficiaire mérite une attention particulière.",
        "Les situations familiales complexes nécessitent souvent une rédaction adaptée.",
        "Toute modification doit être cohérente avec la stratégie patrimoniale globale."
    ],
    client_questions=[
        "À quelle fréquence faut-il revoir sa clause bénéficiaire ?",
        "Dois-je modifier ma clause après un divorce ?",
        "Mon testament suffit-il ?",
        "Puis-je changer librement ma clause bénéficiaire ?",
    ],
    client_objections=[
        "Ma clause a toujours été comme ça.",
        "Je n'ai pas un patrimoine suffisamment important.",
        "Je pense que mes héritiers s'arrangeront entre eux."
    ],
    client_fears=[
        "Que mes volontés ne soient pas respectées.",
        "Créer un conflit familial.",
        "Transmettre mon patrimoine aux mauvaises personnes."
    ],
    client_goals=[
        "Sécuriser la transmission de son patrimoine.",
        "Protéger ses proches.",
        "Adapter son assurance-vie à sa situation familiale.",
        "Éviter les erreurs de rédaction."
    ],
    client_intents=[
        "modifier une clause bénéficiaire",
        "mettre à jour une assurance-vie",
        "changer de bénéficiaire",
        "préparer sa transmission",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_clause_beneficiaire_definition",
        "assurance_vie_clause_beneficiaire_modification",
        "assurance_vie_transmission_principe_general",
        "assurance_vie_transmission_erreurs",
    ],
    prerequisites=[
        "assurance_vie_clause_beneficiaire_definition",
    ],
    next_topics=[
        "assurance_vie_erreurs_choisir_rendement",
    ],
),

Topic(
    id="assurance_vie_erreurs_choisir_rendement",
    title="Erreur : choisir son assurance-vie uniquement selon le rendement",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi choisir une assurance-vie uniquement en fonction de son rendement affiché constitue une erreur fréquente et quels critères doivent également être pris en compte.",
    objective="Expliquer que le rendement n'est qu'un élément parmi d'autres et qu'une assurance-vie doit être choisie en fonction de ses objectifs patrimoniaux, de la qualité des supports, des frais, de la gestion et de la stratégie globale.",
    difficulty="Intermédiaire",
    priority=10,
    version=1,
    keywords=[
        "rendement",
        "performance",
        "assurance-vie",
        "fonds euros",
        "unités de compte",
        "frais",
        "gestion",
        "allocation",
    ],
    key_points=[
        "Le rendement passé ne garantit jamais les performances futures.",
        "Une assurance-vie se choisit selon plusieurs critères et pas uniquement son rendement.",
        "La qualité des supports d'investissement est souvent plus importante que le rendement affiché une année donnée.",
        "Les frais, les options de gestion et les services proposés influencent également la qualité d'un contrat.",
        "Le meilleur contrat est celui qui correspond aux objectifs patrimoniaux du souscripteur."
    ],
    examples=[
        "Julie choisit une assurance-vie uniquement parce qu'elle affiche le meilleur rendement du fonds euros de l'année précédente. Quelques mois plus tard, elle réalise que le contrat propose très peu de supports adaptés à ses objectifs d'investissement.",

        "Marc compare deux contrats présentant des performances proches. Son conseiller lui montre que l'un offre davantage d'ETF, de SCPI et de solutions de gestion pilotée, ce qui répond mieux à sa stratégie patrimoniale.",

        "Claire sélectionne une assurance-vie après avoir analysé les frais, la diversité des supports, les options de gestion et les possibilités de transmission, plutôt que de s'arrêter au rendement annuel."
    ],
    vocabulary=[
        "rendement",
        "performance",
        "fonds euros",
        "unités de compte",
        "ETF",
        "SCPI",
        "allocation",
        "gestion pilotée",
    ],
    legal_sources=[
        "Code des assurances",
        "Code monétaire et financier",
    ],
    analogies=[
        "Choisir une assurance-vie uniquement pour son rendement revient à choisir une voiture uniquement parce qu'elle est rapide, sans regarder sa consommation, sa fiabilité, son confort ou ses équipements."
    ],
    misconceptions=[
        "Le meilleur contrat est celui qui affiche le meilleur rendement.",
        "Le rendement du fonds euros suffit pour comparer deux assurances-vie.",
        "Les performances passées permettent de prévoir les performances futures.",
        "Tous les contrats proposent les mêmes supports d'investissement."
    ],
    common_mistakes=[
        "Comparer uniquement les performances de l'année précédente.",
        "Ignorer les frais du contrat.",
        "Ne pas analyser la qualité des supports proposés.",
        "Choisir un contrat sans tenir compte de ses objectifs patrimoniaux."
    ],
    expert_tips=[
        "Un bon contrat d'assurance-vie ne se résume pas à un rendement annuel. Les frais, la richesse des supports, la qualité de la gestion, la solidité de l'assureur et la cohérence avec vos objectifs patrimoniaux sont souvent des critères tout aussi déterminants."
    ],
    attention_points=[
        "Les performances passées ne préjugent pas des performances futures.",
        "Tous les contrats n'offrent pas les mêmes possibilités d'investissement.",
        "Le rendement doit toujours être analysé en tenant compte du niveau de risque."
    ],
    client_questions=[
        "Quel est le meilleur rendement ?",
        "Comment comparer deux assurances-vie ?",
        "Les frais sont-ils vraiment importants ?",
        "Pourquoi les performances diffèrent-elles d'un contrat à l'autre ?",
    ],
    client_objections=[
        "Je veux simplement le contrat qui rapporte le plus.",
        "Les autres critères me semblent secondaires.",
        "Je regarde uniquement le classement des performances."
    ],
    client_fears=[
        "Choisir un contrat peu performant.",
        "Passer à côté d'un meilleur rendement.",
        "Faire un mauvais choix patrimonial."
    ],
    client_goals=[
        "Choisir une assurance-vie adaptée.",
        "Construire une stratégie de long terme.",
        "Optimiser son patrimoine.",
        "Investir de manière cohérente avec ses objectifs."
    ],
    client_intents=[
        "meilleure assurance-vie",
        "meilleur rendement assurance-vie",
        "comment choisir une assurance-vie",
        "comparer les assurances-vie",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_questions_combien_rapporte",
        "assurance_vie_supports_principe_general",
        "assurance_vie_supports_gestion_pilotee",
        "assurance_vie_comparaison_quel_placement",
    ],
    prerequisites=[
        "assurance_vie_supports_principe_general",
    ],
    next_topics=[
        "assurance_vie_erreurs_un_seul_support",
    ],
),

Topic(
    id="assurance_vie_erreurs_un_seul_support",
    title="Erreur : investir uniquement sur un seul support",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi concentrer toute son épargne sur un seul support d'investissement peut limiter l'efficacité d'une stratégie patrimoniale.",
    objective="Expliquer que la diversification des supports permet généralement de mieux adapter une assurance-vie aux objectifs, à l'horizon de placement et au profil de risque de chaque épargnant.",
    difficulty="Intermédiaire",
    priority=9,
    version=1,
    keywords=[
        "diversification",
        "fonds euros",
        "unités de compte",
        "allocation",
        "assurance-vie",
        "risque",
        "gestion",
        "investissement",
    ],
    key_points=[
        "Chaque support présente des caractéristiques différentes en matière de risque, de rendement potentiel et de liquidité.",
        "Investir uniquement sur un seul support peut limiter les possibilités offertes par une assurance-vie.",
        "La diversification permet de répartir les risques entre plusieurs classes d'actifs.",
        "L'allocation doit évoluer avec les objectifs patrimoniaux et l'horizon de placement.",
        "Il n'existe pas de répartition idéale valable pour tous les investisseurs."
    ],
    examples=[
        "Julie, 30 ans, investit l'intégralité de son assurance-vie sur le fonds euros alors qu'elle dispose d'un horizon d'investissement de plus de vingt-cinq ans. Elle découvre qu'une diversification progressive pourrait être plus cohérente avec ses objectifs.",

        "Marc, 62 ans, investit exclusivement en unités de compte à la recherche de performance. À l'approche de la retraite, il décide de rééquilibrer progressivement son allocation afin de réduire son exposition au risque.",

        "Claire révise son allocation tous les quelques années afin qu'elle reste cohérente avec l'évolution de sa situation familiale, professionnelle et patrimoniale."
    ],
    vocabulary=[
        "allocation",
        "diversification",
        "fonds euros",
        "unités de compte",
        "profil de risque",
        "volatilité",
        "rééquilibrage",
        "horizon de placement",
    ],
    legal_sources=[
        "Code des assurances",
        "Code monétaire et financier",
    ],
    analogies=[
        "Construire une assurance-vie avec un seul support revient à préparer un repas composé d'un seul aliment : même excellent, il ne répondra pas à tous les besoins. La diversification permet de rechercher un meilleur équilibre."
    ],
    misconceptions=[
        "Le fonds euros est toujours la meilleure solution.",
        "Il faut investir uniquement en unités de compte pour obtenir de la performance.",
        "Plus un portefeuille contient de supports, plus il est risqué.",
        "Une fois l'allocation choisie, il n'est plus nécessaire de la revoir."
    ],
    common_mistakes=[
        "Investir 100 % de son contrat sur un seul support.",
        "Confondre diversification et multiplication inutile des supports.",
        "Ne jamais réévaluer son allocation.",
        "Choisir ses investissements uniquement selon les performances récentes."
    ],
    expert_tips=[
        "Une bonne allocation est avant tout une allocation adaptée. Elle doit tenir compte de votre horizon de placement, de votre tolérance au risque et de vos objectifs patrimoniaux. La diversification n'a pas pour but d'améliorer systématiquement la performance, mais de construire un patrimoine plus équilibré."
    ],
    attention_points=[
        "La diversification ne supprime jamais le risque de perte.",
        "L'allocation mérite d'être revue régulièrement.",
        "Chaque investissement doit être cohérent avec les objectifs patrimoniaux poursuivis."
    ],
    client_questions=[
        "Dois-je investir uniquement sur le fonds euros ?",
        "Combien d'unités de compte faut-il détenir ?",
        "Comment diversifier mon assurance-vie ?",
        "Quand faut-il modifier son allocation ?",
    ],
    client_objections=[
        "Je préfère tout placer sur le support le plus sûr.",
        "Je veux uniquement les supports les plus performants.",
        "La diversification me semble trop compliquée."
    ],
    client_fears=[
        "Prendre trop de risques.",
        "Perdre une partie de mon capital.",
        "Faire une mauvaise allocation."
    ],
    client_goals=[
        "Construire une allocation équilibrée.",
        "Diversifier son patrimoine.",
        "Adapter son investissement à ses objectifs.",
        "Mieux gérer le risque."
    ],
    client_intents=[
        "diversifier son assurance-vie",
        "fonds euros ou unités de compte",
        "allocation assurance-vie",
        "comment investir son assurance-vie",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_supports_principe_general",
        "assurance_vie_supports_fonds_euros",
        "assurance_vie_supports_unites_compte",
        "assurance_vie_gestion_allocation",
        "assurance_vie_erreurs_choisir_rendement",
    ],
    prerequisites=[
        "assurance_vie_supports_principe_general",
    ],
    next_topics=[
        "assurance_vie_erreurs_cloturer_contrat",
    ],
),

Topic(
    id="assurance_vie_erreurs_cloturer_contrat",
    title="Erreur : clôturer son assurance-vie alors qu'un rachat partiel aurait pu suffire",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi clôturer entièrement une assurance-vie n'est pas toujours la solution la plus adaptée lorsqu'un besoin de liquidités se présente.",
    objective="Expliquer que, dans certaines situations, un rachat partiel peut permettre de répondre à un besoin de financement tout en conservant le contrat et son ancienneté fiscale.",
    difficulty="Intermédiaire",
    priority=9,
    version=1,
    keywords=[
        "rachat partiel",
        "rachat total",
        "clôture",
        "assurance-vie",
        "ancienneté fiscale",
        "liquidité",
        "épargne",
        "fiscalité",
    ],
    key_points=[
        "Un besoin de liquidités n'implique pas nécessairement la clôture du contrat.",
        "Le rachat partiel permet de retirer une partie de l'épargne tout en maintenant le contrat ouvert.",
        "Conserver un contrat ancien peut présenter un intérêt patrimonial, notamment sur le plan fiscal.",
        "Le choix entre un rachat partiel et un rachat total dépend des objectifs et de la situation du souscripteur.",
        "Chaque retrait mérite une réflexion patrimoniale avant toute décision."
    ],
    examples=[
        "Julie souhaite financer les travaux de sa résidence principale. Plutôt que de clôturer son assurance-vie, elle effectue un rachat partiel et conserve le reste de son épargne investie.",

        "Marc pense devoir fermer son contrat pour acheter un véhicule. Après analyse, il découvre qu'un retrait limité répond à son besoin tout en préservant l'ancienneté de son assurance-vie.",

        "Claire souhaite réorganiser son patrimoine. Avec son conseiller, elle compare les conséquences d'un rachat partiel et d'un rachat total avant de prendre une décision."
    ],
    vocabulary=[
        "rachat partiel",
        "rachat total",
        "ancienneté fiscale",
        "liquidité",
        "plus-value",
        "capital",
        "contrat",
        "épargne",
    ],
    legal_sources=[
        "Code des assurances",
        "Code général des impôts",
        "BOFiP - Assurance-vie",
    ],
    analogies=[
        "Clôturer une assurance-vie pour retirer une partie de son épargne revient souvent à vendre toute sa maison alors qu'il suffisait d'utiliser une seule pièce."
    ],
    misconceptions=[
        "Je dois fermer mon contrat pour récupérer mon argent.",
        "Un retrait entraîne automatiquement la clôture de l'assurance-vie.",
        "Le rachat partiel est réservé aux gros patrimoines.",
        "Une fois un retrait effectué, le contrat perd tout son intérêt."
    ],
    common_mistakes=[
        "Demander un rachat total alors qu'un besoin ponctuel aurait pu être couvert par un rachat partiel.",
        "Ne pas mesurer les conséquences de la clôture du contrat.",
        "Confondre retrait et fermeture de l'assurance-vie.",
        "Prendre une décision dans l'urgence sans analyser les alternatives."
    ],
    expert_tips=[
        "Avant de clôturer une assurance-vie, il est souvent utile d'examiner si un rachat partiel, un rachat programmé ou une autre solution permettrait d'atteindre le même objectif tout en conservant les avantages liés au contrat. Cette analyse doit toujours être réalisée au regard de votre situation patrimoniale."
    ],
    attention_points=[
        "Le rachat total peut être pertinent dans certaines situations.",
        "Les conséquences fiscales diffèrent selon les caractéristiques du contrat.",
        "Chaque décision doit être cohérente avec la stratégie patrimoniale globale."
    ],
    client_questions=[
        "Dois-je fermer mon assurance-vie pour récupérer mon argent ?",
        "Quelle différence entre un rachat partiel et un rachat total ?",
        "Puis-je effectuer plusieurs rachats ?",
        "Que devient mon contrat après un retrait ?",
    ],
    client_objections=[
        "Je préfère récupérer tout mon argent.",
        "Je pensais qu'il fallait fermer le contrat.",
        "Je ne comprends pas la différence entre les deux."
    ],
    client_fears=[
        "Perdre les avantages de mon contrat.",
        "Faire une erreur fiscale.",
        "Ne plus pouvoir utiliser mon assurance-vie."
    ],
    client_goals=[
        "Financer un projet.",
        "Conserver son ancienneté fiscale.",
        "Préserver la souplesse de son épargne.",
        "Prendre une décision adaptée à ses besoins."
    ],
    client_intents=[
        "fermer une assurance-vie",
        "rachat partiel",
        "rachat total",
        "retirer son argent",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_questions_retirer_argent",
        "assurance_vie_fiscalite_rachat",
        "assurance_vie_questions_bloquee_8_ans",
        "assurance_vie_erreurs_attendre_8_ans",
    ],
    prerequisites=[
        "assurance_vie_questions_retirer_argent",
        "assurance_vie_fiscalite_rachat",
    ],
    next_topics=[
        "assurance_vie_erreurs_pas_objectif",
    ],
),

Topic(
    id="assurance_vie_erreurs_pas_objectif",
    title="Erreur : ouvrir une assurance-vie sans objectif patrimonial",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi ouvrir une assurance-vie sans avoir identifié ses objectifs patrimoniaux constitue une erreur fréquente.",
    objective="Expliquer qu'une assurance-vie est une enveloppe patrimoniale au service d'un projet et non une finalité en elle-même.",
    difficulty="Débutant",
    priority=10,
    version=1,
    keywords=[
        "objectif patrimonial",
        "assurance-vie",
        "épargne",
        "placement",
        "stratégie",
        "patrimoine",
        "investissement",
        "projet",
    ],
    key_points=[
        "Une assurance-vie est un moyen au service d'un objectif patrimonial.",
        "Avant d'investir, il est essentiel d'identifier les projets que l'on souhaite financer ou préparer.",
        "L'horizon de placement, le besoin de liquidité et le niveau de risque influencent la stratégie d'investissement.",
        "Une même assurance-vie peut répondre à plusieurs objectifs si elle est correctement organisée.",
        "La meilleure stratégie patrimoniale est celle qui reste cohérente avec la situation personnelle et familiale."
    ],
    examples=[
        "Julie ouvre une assurance-vie parce qu'elle entend régulièrement qu'il s'agit du meilleur placement. Quelques années plus tard, elle réalise qu'elle n'avait jamais défini l'objectif de cette épargne.",

        "Marc souhaite préparer sa retraite tout en aidant ses enfants à financer leurs études. Avant d'investir, il identifie chacun de ses objectifs afin d'adapter son organisation patrimoniale.",

        "Claire vient de vendre son entreprise. Plutôt que d'investir immédiatement l'intégralité de son capital, elle prend le temps de définir ses besoins en matière de revenus, de transmission et de diversification."
    ],
    vocabulary=[
        "objectif patrimonial",
        "horizon de placement",
        "liquidité",
        "allocation",
        "diversification",
        "transmission",
        "profil de risque",
        "stratégie patrimoniale",
    ],
    legal_sources=[
        "Code des assurances",
        "Code monétaire et financier",
    ],
    analogies=[
        "Ouvrir une assurance-vie sans objectif revient à monter dans un train sans connaître sa destination : le voyage peut être agréable, mais rien ne garantit que vous arriverez là où vous vouliez aller."
    ],
    misconceptions=[
        "Il faut ouvrir une assurance-vie parce que tout le monde en possède une.",
        "Le produit est plus important que l'objectif.",
        "Une assurance-vie répond automatiquement à tous les besoins patrimoniaux.",
        "Le meilleur placement est le même pour tout le monde."
    ],
    common_mistakes=[
        "Souscrire un contrat sans définir de projet.",
        "Choisir un contrat uniquement parce qu'il est populaire.",
        "Construire son patrimoine autour d'un produit plutôt que d'un objectif.",
        "Ne jamais réévaluer ses objectifs au fil du temps."
    ],
    expert_tips=[
        "La première question à se poser n'est généralement pas 'Quelle assurance-vie choisir ?', mais 'Pourquoi est-ce que je souhaite investir ?'. Une fois l'objectif identifié, il devient beaucoup plus simple de déterminer si l'assurance-vie est une enveloppe pertinente et comment l'utiliser."
    ],
    attention_points=[
        "Les objectifs patrimoniaux évoluent au cours de la vie.",
        "Une stratégie doit être revue régulièrement.",
        "Le choix d'une enveloppe ne constitue qu'une étape de la réflexion patrimoniale."
    ],
    client_questions=[
        "Pourquoi ouvrir une assurance-vie ?",
        "Quel est mon objectif d'investissement ?",
        "Comment construire une stratégie patrimoniale ?",
        "Par où commencer ?",
    ],
    client_objections=[
        "Je veux simplement placer mon argent.",
        "Je choisirai mes objectifs plus tard.",
        "Je pensais que le produit suffisait."
    ],
    client_fears=[
        "Faire un mauvais choix.",
        "Investir sans réelle stratégie.",
        "Ne pas atteindre mes objectifs."
    ],
    client_goals=[
        "Donner du sens à son patrimoine.",
        "Préparer des projets de vie.",
        "Construire une stratégie cohérente.",
        "Choisir les enveloppes adaptées à ses besoins."
    ],
    client_intents=[
        "pourquoi ouvrir une assurance-vie",
        "objectif patrimonial",
        "comment investir",
        "stratégie patrimoniale",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_questions_pourquoi_assurance_vie",
        "assurance_vie_comparaison_quel_placement",
        "assurance_vie_gestion_profil_investisseur",
        "assurance_vie_erreurs_choisir_rendement",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[
        "assurance_vie_erreurs_pas_alimenter",
    ],
),

Topic(
    id="assurance_vie_erreurs_pas_alimenter",
    title="Erreur : ouvrir une assurance-vie puis ne plus jamais l'alimenter",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi ouvrir une assurance-vie sans prévoir de suivi ou de nouveaux versements peut limiter l'intérêt de cette enveloppe patrimoniale.",
    objective="Expliquer qu'une assurance-vie est généralement plus efficace lorsqu'elle s'inscrit dans une stratégie d'épargne et d'investissement suivie dans le temps, tout en rappelant qu'aucune obligation de versement régulier n'existe.",
    difficulty="Débutant",
    priority=9,
    version=1,
    keywords=[
        "versements",
        "épargne programmée",
        "assurance-vie",
        "investissement",
        "capitalisation",
        "patrimoine",
        "gestion",
        "long terme",
    ],
    key_points=[
        "Ouvrir une assurance-vie n'est que la première étape d'une stratégie patrimoniale.",
        "Un contrat peut être alimenté par des versements libres ou programmés selon les besoins.",
        "La régularité des versements peut permettre de construire progressivement un patrimoine.",
        "Il n'existe aucune obligation d'effectuer des versements réguliers.",
        "La stratégie d'alimentation du contrat doit rester cohérente avec les capacités d'épargne et les objectifs patrimoniaux."
    ],
    examples=[
        "Julie ouvre une assurance-vie avec 500 € puis oublie complètement son contrat pendant quinze ans. Elle réalise qu'elle aurait pu constituer un capital beaucoup plus important en effectuant de petits versements réguliers adaptés à son budget.",

        "Marc met en place un versement mensuel de 150 € qu'il ajuste progressivement à mesure que ses revenus augmentent. Cette discipline lui permet de développer son patrimoine sans effort important à chaque versement.",

        "Claire reçoit ponctuellement des primes professionnelles. Plutôt que d'effectuer des versements programmés, elle choisit d'alimenter son assurance-vie uniquement lors de ces événements, selon sa capacité d'épargne."
    ],
    vocabulary=[
        "versement libre",
        "versement programmé",
        "capitalisation",
        "horizon de placement",
        "épargne",
        "allocation",
        "patrimoine",
        "investissement",
    ],
    legal_sources=[
        "Code des assurances",
    ],
    analogies=[
        "Une assurance-vie ressemble à un jardin : l'ouvrir revient à planter la première graine. Pour qu'il se développe au fil du temps, il est souvent utile de continuer à l'entretenir, même progressivement."
    ],
    misconceptions=[
        "Une fois le contrat ouvert, il n'est plus nécessaire d'y penser.",
        "Il faut obligatoirement verser tous les mois.",
        "Seuls les gros versements permettent de construire un patrimoine.",
        "Un contrat ouvert suffit à lui seul à atteindre ses objectifs patrimoniaux."
    ],
    common_mistakes=[
        "Ouvrir un contrat puis l'oublier complètement.",
        "Penser qu'il faut attendre de disposer d'une somme importante avant d'effectuer un nouveau versement.",
        "Ne jamais revoir sa stratégie d'épargne.",
        "Ne pas adapter les versements à l'évolution de sa situation financière."
    ],
    expert_tips=[
        "Une stratégie patrimoniale est souvent plus efficace lorsqu'elle s'inscrit dans la durée. Des versements réguliers, même modestes, ou des versements ponctuels adaptés aux événements de vie peuvent contribuer à construire progressivement un patrimoine cohérent avec ses objectifs."
    ],
    attention_points=[
        "Les versements programmés sont une possibilité, jamais une obligation.",
        "Les capacités d'épargne évoluent au cours de la vie.",
        "Il est utile de revoir régulièrement sa stratégie d'investissement."
    ],
    client_questions=[
        "Dois-je effectuer des versements tous les mois ?",
        "Puis-je arrêter mes versements ?",
        "Est-il préférable de verser régulièrement ou ponctuellement ?",
        "Puis-je reprendre mes versements plus tard ?",
    ],
    client_objections=[
        "Je n'ai pas suffisamment de capacité d'épargne chaque mois.",
        "Je préfère investir uniquement lorsque je dispose d'un surplus de trésorerie.",
        "Je pensais qu'un seul versement suffisait."
    ],
    client_fears=[
        "Ne pas pouvoir respecter des versements réguliers.",
        "Construire un capital insuffisant.",
        "Mal utiliser mon assurance-vie."
    ],
    client_goals=[
        "Développer progressivement son patrimoine.",
        "Mettre en place une stratégie d'épargne durable.",
        "Adapter ses versements à sa situation.",
        "Préparer des projets de long terme."
    ],
    client_intents=[
        "versements assurance-vie",
        "épargne programmée",
        "alimenter une assurance-vie",
        "combien verser chaque mois",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_versements_libres_programmes",
        "assurance_vie_gestion_versements_programmes",
        "assurance_vie_erreurs_pas_objectif",
        "assurance_vie_questions_combien_verser",
    ],
    prerequisites=[
        "assurance_vie_versements_libres_programmes",
    ],
    next_topics=[
        "assurance_vie_erreurs_personnes_agees",
    ],
),

Topic(
    id="assurance_vie_erreurs_personnes_agees",
    title="Erreur : croire que l'assurance-vie est réservée aux personnes âgées",
    pillar="eviter",
    family="assurance_vie",
    chapter="erreurs",
    description="Comprendre pourquoi l'assurance-vie n'est pas un produit réservé aux retraités et peut répondre à des objectifs patrimoniaux à différents âges de la vie.",
    objective="Expliquer que l'intérêt d'une assurance-vie dépend avant tout des projets patrimoniaux du souscripteur et non de son âge.",
    difficulty="Débutant",
    priority=10,
    version=1,
    keywords=[
        "jeune",
        "retraite",
        "assurance-vie",
        "épargne",
        "placement",
        "patrimoine",
        "transmission",
        "ancienneté fiscale",
    ],
    key_points=[
        "L'assurance-vie n'est pas réservée aux personnes âgées.",
        "Les objectifs patrimoniaux évoluent au cours de la vie.",
        "Commencer tôt peut permettre de bénéficier d'un horizon d'investissement plus long et de faire courir l'ancienneté fiscale.",
        "L'assurance-vie peut servir à préparer de nombreux projets avant la retraite.",
        "L'intérêt d'un contrat dépend des objectifs poursuivis et non de l'âge du souscripteur."
    ],
    examples=[
        "Julie, 25 ans, ouvre une assurance-vie afin de constituer progressivement un capital pour ses futurs projets. Elle profite du temps pour investir régulièrement selon ses capacités d'épargne.",

        "Marc, 44 ans, utilise son assurance-vie pour préparer les études de ses enfants et compléter son patrimoine financier.",

        "Claire, 67 ans, conserve son assurance-vie principalement dans une logique de transmission et d'organisation successorale. Le même produit répond ainsi à un objectif très différent de celui de Julie."
    ],
    vocabulary=[
        "ancienneté fiscale",
        "horizon de placement",
        "capitalisation",
        "transmission",
        "épargne",
        "allocation",
        "patrimoine",
        "projet",
    ],
    legal_sources=[
        "Code des assurances",
        "Code général des impôts",
    ],
    analogies=[
        "Penser que l'assurance-vie est réservée aux personnes âgées revient à croire qu'il faut attendre la retraite pour commencer à préparer l'avenir. Plus un projet est anticipé, plus le temps peut devenir un allié."
    ],
    misconceptions=[
        "L'assurance-vie est uniquement destinée à préparer la succession.",
        "Il faut attendre d'être proche de la retraite pour ouvrir un contrat.",
        "Les jeunes n'ont aucun intérêt à ouvrir une assurance-vie.",
        "L'assurance-vie est réservée aux patrimoines importants."
    ],
    common_mistakes=[
        "Reporter l'ouverture d'une assurance-vie en raison de son âge.",
        "Attendre la retraite pour commencer à construire son patrimoine.",
        "Réduire l'assurance-vie à un simple outil de transmission.",
        "Croire qu'il existe un âge idéal pour ouvrir un contrat."
    ],
    expert_tips=[
        "L'âge est rarement le critère déterminant. Les véritables questions sont : quels sont vos projets, quel est votre horizon de placement et comment souhaitez-vous organiser votre patrimoine ? Le temps constitue souvent un atout précieux lorsqu'il est mis au service d'une stratégie patrimoniale cohérente."
    ],
    attention_points=[
        "Les objectifs patrimoniaux évoluent tout au long de la vie.",
        "Une assurance-vie peut répondre à des besoins très différents selon les étapes de vie.",
        "Chaque stratégie doit être adaptée à la situation personnelle du souscripteur."
    ],
    client_questions=[
        "Suis-je trop jeune pour ouvrir une assurance-vie ?",
        "À quel âge faut-il ouvrir une assurance-vie ?",
        "Est-ce uniquement un produit pour préparer la succession ?",
        "L'assurance-vie est-elle utile avant la retraite ?",
    ],
    client_objections=[
        "Je suis encore trop jeune pour penser à tout ça.",
        "Je verrai plus tard lorsque j'aurai davantage d'argent.",
        "L'assurance-vie est un produit pour les retraités."
    ],
    client_fears=[
        "Ouvrir un produit qui ne correspond pas à mon âge.",
        "Immobiliser inutilement mon épargne.",
        "Faire un choix prématuré."
    ],
    client_goals=[
        "Construire progressivement son patrimoine.",
        "Préparer différents projets de vie.",
        "Profiter d'un horizon d'investissement long.",
        "Comprendre à quoi sert réellement une assurance-vie."
    ],
    client_intents=[
        "assurance-vie jeune",
        "à quel âge ouvrir une assurance-vie",
        "assurance-vie avant la retraite",
        "ouvrir une assurance-vie à 25 ans",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_ouverture_pourquoi_ouvrir",
        "assurance_vie_questions_pourquoi_assurance_vie",
        "assurance_vie_erreurs_attendre_8_ans",
        "assurance_vie_comparaison_quel_placement",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[],
),

