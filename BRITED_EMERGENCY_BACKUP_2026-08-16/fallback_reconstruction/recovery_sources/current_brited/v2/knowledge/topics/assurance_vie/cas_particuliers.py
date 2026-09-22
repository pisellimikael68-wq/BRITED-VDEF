from v2.models.knowledge_models import Topic

CAS_PARTICULIERS_TOPICS: list[Topic] = []

Topic(
    id="assurance_vie_cas_particuliers_enfant_mineur",
    title="Assurance-vie pour un enfant mineur : quelles règles ?",
    pillar="transmettre",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre dans quelles conditions un enfant mineur peut détenir une assurance-vie et quelles sont les conséquences juridiques et patrimoniales de cette détention.",
    objective="Expliquer le fonctionnement d'une assurance-vie ouverte au nom d'un enfant mineur, les règles d'administration du contrat et les précautions à prendre avant d'effectuer des versements.",
    difficulty="Intermédiaire",
    priority=9,
    version=1,
    keywords=[
        "enfant mineur",
        "assurance-vie",
        "administration légale",
        "parents",
        "donation",
        "patrimoine",
        "majorité",
        "épargne",
    ],
    key_points=[
        "Un enfant mineur peut être titulaire d'une assurance-vie.",
        "Le contrat est administré par ses représentants légaux jusqu'à sa majorité ou son émancipation.",
        "Les sommes versées appartiennent juridiquement à l'enfant.",
        "Les versements doivent être cohérents avec l'intérêt de l'enfant et la stratégie patrimoniale familiale.",
        "L'assurance-vie peut constituer un outil de préparation des études, d'un premier logement ou d'une transmission anticipée."
    ],
    examples=[
        "Julie et Thomas ouvrent une assurance-vie au nom de leur fille dès sa naissance afin de constituer progressivement un capital destiné à financer ses études supérieures.",

        "Les grands-parents de Lucas souhaitent lui transmettre progressivement une partie de leur patrimoine. Ils réalisent des versements sur son assurance-vie dans le cadre de leur stratégie de transmission.",

        "À sa majorité, Emma devient pleinement titulaire des droits attachés à son contrat et peut décider de poursuivre sa stratégie d'investissement ou d'effectuer un rachat, selon les règles applicables."
    ],
    vocabulary=[
        "mineur",
        "administration légale",
        "représentant légal",
        "souscripteur",
        "titulaire",
        "majorité",
        "donation",
        "patrimoine",
    ],
    legal_sources=[
        "Code civil",
        "Code des assurances",
        "Code général des impôts",
    ],
    analogies=[
        "Ouvrir une assurance-vie pour un enfant revient à planter un arbre dont il deviendra propriétaire. Les parents en prennent soin pendant son enfance, mais l'arbre lui appartient."
    ],
    misconceptions=[
        "Les parents restent propriétaires de l'argent versé sur le contrat.",
        "Un mineur ne peut pas détenir une assurance-vie.",
        "Les fonds reviennent automatiquement aux parents.",
        "L'enfant ne pourra jamais disposer librement de son contrat."
    ],
    common_mistakes=[
        "Confondre le patrimoine des parents avec celui de l'enfant.",
        "Ouvrir un contrat sans définir un objectif patrimonial.",
        "Négliger les conséquences juridiques des versements.",
        "Oublier de revoir la stratégie lorsque l'enfant grandit."
    ],
    expert_tips=[
        "Avant d'ouvrir une assurance-vie au nom d'un enfant, il est utile de définir précisément l'objectif poursuivi : études, premier logement, transmission ou constitution d'un capital de long terme. Le choix des supports d'investissement et le rythme des versements pourront ensuite être adaptés à cet objectif."
    ],
    attention_points=[
        "Les sommes investies appartiennent juridiquement à l'enfant.",
        "Les représentants légaux administrent le contrat dans l'intérêt du mineur.",
        "Certaines opérations importantes peuvent être soumises à des règles particulières de protection du mineur."
    ],
    client_questions=[
        "Puis-je ouvrir une assurance-vie pour mon enfant ?",
        "À qui appartient l'argent ?",
        "Qui gère le contrat jusqu'à sa majorité ?",
        "Mon enfant pourra-t-il récupérer librement les fonds ?",
    ],
    client_objections=[
        "Je préfère garder le contrôle de cette épargne.",
        "Je pensais que le contrat restait au nom des parents.",
        "Mon enfant est encore trop jeune."
    ],
    client_fears=[
        "Perdre le contrôle de l'épargne.",
        "Faire une erreur juridique.",
        "Choisir une stratégie inadaptée."
    ],
    client_goals=[
        "Constituer un capital pour son enfant.",
        "Préparer les études ou un premier achat immobilier.",
        "Organiser une transmission progressive.",
        "Investir sur un horizon de long terme."
    ],
    client_intents=[
        "assurance-vie enfant",
        "assurance-vie mineur",
        "ouvrir une assurance-vie pour son enfant",
        "épargner pour ses enfants",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_questions_enfant",
        "assurance_vie_transmission_principe_general",
        "assurance_vie_versements_libres_programmes",
        "assurance_vie_clause_beneficiaire_definition",
    ],
    prerequisites=[
        "assurance_vie_questions_enfant",
    ],
    next_topics=[
        "assurance_vie_cas_particuliers_demembrement",
    ],
),

Topic(
    id="assurance_vie_cas_particuliers_demembrement",
    title="Le démembrement de la clause bénéficiaire : dans quels cas est-il utilisé ?",
    pillar="transmettre",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre le principe du démembrement de la clause bénéficiaire d'une assurance-vie et les situations patrimoniales dans lesquelles cette technique peut être utilisée.",
    objective="Expliquer que le démembrement de la clause bénéficiaire permet de répartir les droits entre usufruitier et nu-propriétaire afin de répondre à certains objectifs de protection et de transmission.",
    difficulty="Avancé",
    priority=8,
    version=1,
    keywords=[
        "démembrement",
        "clause bénéficiaire",
        "usufruit",
        "nue-propriété",
        "assurance-vie",
        "transmission",
        "succession",
        "patrimoine",
    ],
    key_points=[
        "La clause bénéficiaire peut prévoir un démembrement entre usufruitier et nu-propriétaire.",
        "Cette technique est fréquemment utilisée pour protéger un conjoint tout en préparant la transmission aux enfants.",
        "Le démembrement produit des effets civils et fiscaux spécifiques.",
        "La rédaction de la clause bénéficiaire est essentielle pour sécuriser le dispositif.",
        "Cette stratégie nécessite une réflexion patrimoniale approfondie."
    ],
    examples=[
        "À la naissance de leur deuxième enfant, Julie et Thomas souhaitent protéger le conjoint survivant tout en préparant la transmission familiale. Ils étudient avec leur conseiller l'intérêt d'une clause bénéficiaire démembrée.",

        "Marc, veuf avec des enfants d'un premier mariage, souhaite concilier protection de son nouveau conjoint et préservation des droits de ses enfants. Le démembrement de la clause bénéficiaire fait partie des solutions analysées.",

        "Claire possède un patrimoine financier important. Avant de modifier sa clause bénéficiaire, elle réalise une étude patrimoniale afin de mesurer les conséquences civiles et fiscales d'un éventuel démembrement."
    ],
    vocabulary=[
        "usufruit",
        "nu-propriétaire",
        "quasi-usufruit",
        "créance de restitution",
        "clause bénéficiaire",
        "démembrement",
        "transmission",
        "succession",
    ],
    legal_sources=[
        "Code civil",
        "Code des assurances",
        "Code général des impôts",
        "BOFiP - Assurance-vie",
    ],
    analogies=[
        "Le démembrement revient à partager les prérogatives attachées à un même capital : une personne bénéficie de son usage selon les modalités prévues, tandis qu'une autre est appelée à en recueillir la pleine propriété ultérieurement."
    ],
    misconceptions=[
        "Le démembrement est réservé aux très grandes fortunes.",
        "Il s'agit uniquement d'un mécanisme fiscal.",
        "Une clause standard suffit dans toutes les situations.",
        "Le démembrement est automatiquement adapté à toutes les familles."
    ],
    common_mistakes=[
        "Utiliser une clause bénéficiaire standard alors que la situation familiale est complexe.",
        "Sous-estimer les conséquences civiles du démembrement.",
        "Négliger la rédaction précise de la clause bénéficiaire.",
        "Mettre en place un démembrement sans en comprendre les effets."
    ],
    expert_tips=[
        "Le démembrement de la clause bénéficiaire constitue un outil d'ingénierie patrimoniale particulièrement utile dans certaines situations familiales. Sa mise en œuvre suppose toutefois une rédaction rigoureuse et une analyse globale des objectifs civils, fiscaux et successoraux."
    ],
    attention_points=[
        "Chaque démembrement doit être adapté à la situation familiale.",
        "La rédaction de la clause bénéficiaire est déterminante.",
        "Les conséquences civiles et fiscales doivent être analysées conjointement."
    ],
    client_questions=[
        "Qu'est-ce qu'une clause bénéficiaire démembrée ?",
        "Pourquoi prévoir un usufruit et une nue-propriété ?",
        "Dans quels cas cette technique est-elle utilisée ?",
        "Est-ce adapté à ma situation familiale ?",
    ],
    client_objections=[
        "Cela me paraît beaucoup trop complexe.",
        "Je préfère une clause bénéficiaire classique.",
        "Je pensais que cette technique était réservée aux grandes fortunes."
    ],
    client_fears=[
        "Faire une erreur de rédaction.",
        "Créer un conflit entre les bénéficiaires.",
        "Mettre en place une stratégie inadaptée."
    ],
    client_goals=[
        "Protéger son conjoint.",
        "Préparer la transmission aux enfants.",
        "Structurer efficacement son patrimoine.",
        "Comprendre les outils d'ingénierie patrimoniale."
    ],
    client_intents=[
        "clause bénéficiaire démembrée",
        "usufruit assurance-vie",
        "nue-propriété assurance-vie",
        "démembrement assurance-vie",
    ],
    recommended_formats=[
        "article",
        "faq",
        "carrousel",
        "linkedin_post",
    ],
    related_topics=[
        "assurance_vie_clause_beneficiaire_definition",
        "assurance_vie_clause_beneficiaire_redaction",
        "assurance_vie_transmission_principe_general",
        "assurance_vie_erreurs_clause_beneficiaire",
    ],
    prerequisites=[
        "assurance_vie_clause_beneficiaire_definition",
        "assurance_vie_transmission_principe_general",
    ],
    next_topics=[
        "assurance_vie_cas_particuliers_expatriation",
    ],
),

Topic(
    id="assurance_vie_cas_particuliers_expatriation",
    title="Que devient une assurance-vie en cas d'expatriation ?",
    pillar="proteger",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre les principales conséquences d'une expatriation sur une assurance-vie et les points d'attention à analyser avant un départ à l'étranger.",
    objective="Expliquer que l'expatriation ne met pas automatiquement fin à une assurance-vie mais peut modifier son traitement fiscal, les modalités de gestion du contrat et la stratégie patrimoniale du souscripteur.",
    difficulty="Avancé",
    priority=9,
    version=1,
    keywords=[
        "expatriation",
        "non-résident",
        "assurance-vie",
        "résidence fiscale",
        "fiscalité",
        "convention fiscale",
        "patrimoine",
        "international",
    ],
    key_points=[
        "Une assurance-vie peut généralement être conservée après une expatriation.",
        "Le changement de résidence fiscale peut modifier la fiscalité applicable aux rachats.",
        "Les conventions fiscales internationales peuvent avoir une incidence sur le traitement du contrat.",
        "Tous les assureurs n'acceptent pas les mêmes pays de résidence.",
        "Une expatriation constitue souvent l'occasion de réexaminer l'organisation patrimoniale globale."
    ],
    examples=[
        "Julie accepte une opportunité professionnelle à Singapour. Avant son départ, elle vérifie avec son assureur les conséquences de son changement de résidence fiscale sur son assurance-vie.",

        "Marc part vivre au Portugal après son départ à la retraite. Il analyse les conséquences de cette expatriation sur la fiscalité de ses futurs rachats et sur son organisation patrimoniale.",

        "Claire s'installe aux Émirats arabes unis après la cession de son entreprise. Son patrimoine devenant international, elle réévalue la place de son assurance-vie dans sa stratégie globale."
    ],
    vocabulary=[
        "résidence fiscale",
        "non-résident",
        "expatriation",
        "convention fiscale",
        "rachat",
        "assureur",
        "patrimoine international",
        "mobilité internationale",
    ],
    legal_sources=[
        "Code général des impôts",
        "Code des assurances",
        "Conventions fiscales internationales",
    ],
    analogies=[
        "Une assurance-vie voyage avec son titulaire, mais ses règles fiscales peuvent changer selon le pays dans lequel celui-ci s'installe, comme un permis de conduire dont les règles d'utilisation varient selon le pays."
    ],
    misconceptions=[
        "Je dois obligatoirement fermer mon assurance-vie avant de quitter la France.",
        "Une assurance-vie française devient automatiquement inutile à l'étranger.",
        "L'expatriation supprime toute fiscalité sur l'assurance-vie.",
        "Les règles sont identiques dans tous les pays."
    ],
    common_mistakes=[
        "S'expatrier sans informer son assureur.",
        "Ne pas analyser les conséquences du changement de résidence fiscale.",
        "Croire que les conventions fiscales produisent les mêmes effets dans tous les pays.",
        "Conserver une stratégie patrimoniale conçue uniquement pour une résidence française."
    ],
    expert_tips=[
        "Une expatriation est souvent un événement patrimonial majeur. Avant le départ, il est utile de vérifier les conséquences civiles, fiscales et pratiques sur l'ensemble de son patrimoine, y compris l'assurance-vie. Cette analyse permet d'éviter des décisions prises dans l'urgence une fois installé à l'étranger."
    ],
    attention_points=[
        "Les conséquences varient selon le pays de résidence.",
        "Les conventions fiscales jouent souvent un rôle déterminant.",
        "Les conditions d'acceptation des non-résidents diffèrent selon les assureurs."
    ],
    client_questions=[
        "Puis-je conserver mon assurance-vie si je pars vivre à l'étranger ?",
        "Dois-je fermer mon contrat ?",
        "Comment seront imposés mes futurs rachats ?",
        "Tous les assureurs acceptent-ils les non-résidents ?",
    ],
    client_objections=[
        "Je pensais que mon contrat devenait inutile.",
        "On m'a dit qu'il fallait clôturer mon assurance-vie.",
        "La fiscalité internationale me semble trop complexe."
    ],
    client_fears=[
        "Perdre les avantages de mon contrat.",
        "Subir une double imposition.",
        "Faire une erreur avant mon départ."
    ],
    client_goals=[
        "Préparer sereinement son expatriation.",
        "Conserver une stratégie patrimoniale cohérente.",
        "Comprendre les conséquences de sa mobilité internationale.",
        "Sécuriser son patrimoine."
    ],
    client_intents=[
        "assurance-vie expatriation",
        "assurance-vie non-résident",
        "garder une assurance-vie à l'étranger",
        "expatriation assurance-vie",
    ],
    recommended_formats=[
        "article",
        "faq",
        "carrousel",
        "linkedin_post",
    ],
    related_topics=[
        "assurance_vie_comparaison_luxembourg",
        "assurance_vie_cas_particuliers_non_resident",
        "assurance_vie_questions_faillite_assureur",
        "assurance_vie_questions_pourquoi_assurance_vie",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[
        "assurance_vie_cas_particuliers_divorce",
    ],
),

Topic(
    id="assurance_vie_cas_particuliers_divorce",
    title="Que devient une assurance-vie en cas de divorce ?",
    pillar="proteger",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre les principales conséquences d'un divorce sur une assurance-vie et les éléments juridiques qui influencent le devenir du contrat.",
    objective="Expliquer que les conséquences d'un divorce sur une assurance-vie dépendent notamment du régime matrimonial, de l'origine des fonds investis et de la qualité du souscripteur.",
    difficulty="Avancé",
    priority=9,
    version=1,
    keywords=[
        "divorce",
        "assurance-vie",
        "régime matrimonial",
        "communauté",
        "séparation de biens",
        "clause bénéficiaire",
        "liquidation",
        "patrimoine",
    ],
    key_points=[
        "Le divorce n'entraîne pas automatiquement la clôture d'une assurance-vie.",
        "Le régime matrimonial influence le traitement du contrat lors de la liquidation du patrimoine.",
        "L'origine des fonds investis constitue un élément déterminant.",
        "La clause bénéficiaire mérite d'être relue après un divorce.",
        "Le divorce est souvent l'occasion de revoir l'ensemble de son organisation patrimoniale."
    ],
    examples=[
        "Après quinze années de mariage, Julie et Marc divorcent. Ils analysent le traitement de leurs contrats d'assurance-vie dans le cadre de la liquidation de leur régime matrimonial.",

        "Claire avait ouvert une assurance-vie avant son mariage avec des fonds personnels. Lors de son divorce, elle vérifie les conséquences de cette situation sur son contrat.",

        "À la suite de son divorce, Thomas conserve son assurance-vie mais met immédiatement à jour sa clause bénéficiaire afin qu'elle corresponde à sa nouvelle situation familiale."
    ],
    vocabulary=[
        "régime matrimonial",
        "communauté",
        "séparation de biens",
        "liquidation",
        "récompense",
        "clause bénéficiaire",
        "souscripteur",
        "fonds propres",
    ],
    legal_sources=[
        "Code civil",
        "Code des assurances",
        "Code général des impôts",
    ],
    analogies=[
        "Une assurance-vie lors d'un divorce ressemble à un bien immobilier : il ne suffit pas de savoir qu'il existe, il faut comprendre à qui il appartient juridiquement, avec quels fonds il a été financé et quelles sont les règles du régime matrimonial."
    ],
    misconceptions=[
        "Le divorce ferme automatiquement l'assurance-vie.",
        "L'ex-conjoint perd automatiquement tous ses droits.",
        "La clause bénéficiaire est modifiée automatiquement après le divorce.",
        "Toutes les assurances-vie sont traitées de la même manière lors d'un divorce."
    ],
    common_mistakes=[
        "Oublier de relire la clause bénéficiaire après un divorce.",
        "Penser que le régime matrimonial est sans incidence.",
        "Ignorer l'origine des fonds ayant financé le contrat.",
        "Prendre des décisions avant d'avoir analysé les conséquences patrimoniales."
    ],
    expert_tips=[
        "Le divorce constitue un événement patrimonial majeur. Au-delà de l'assurance-vie, il est généralement pertinent de réexaminer l'ensemble de son organisation patrimoniale : clause bénéficiaire, stratégie de transmission, allocation des actifs et objectifs de long terme."
    ],
    attention_points=[
        "Les conséquences dépendent du régime matrimonial.",
        "L'origine des fonds investis peut être déterminante.",
        "La clause bénéficiaire mérite une attention particulière après une séparation."
    ],
    client_questions=[
        "Mon assurance-vie sera-t-elle partagée ?",
        "Dois-je fermer mon contrat ?",
        "Que devient mon ex-conjoint dans la clause bénéficiaire ?",
        "Le régime matrimonial change-t-il les règles ?",
    ],
    client_objections=[
        "Je pensais que tout était automatiquement partagé.",
        "Je croyais que le divorce supprimait la clause bénéficiaire.",
        "La situation me paraît très complexe."
    ],
    client_fears=[
        "Perdre une partie de mon patrimoine.",
        "Oublier une démarche importante.",
        "Laisser mon ex-conjoint bénéficiaire sans le vouloir."
    ],
    client_goals=[
        "Comprendre les conséquences du divorce.",
        "Protéger son patrimoine.",
        "Mettre à jour sa stratégie patrimoniale.",
        "Sécuriser la transmission future."
    ],
    client_intents=[
        "divorce assurance-vie",
        "partage assurance-vie divorce",
        "clause bénéficiaire divorce",
        "assurance-vie régime matrimonial",
    ],
    recommended_formats=[
        "article",
        "faq",
        "carrousel",
        "linkedin_post",
    ],
    related_topics=[
        "assurance_vie_erreurs_clause_beneficiaire",
        "assurance_vie_clause_beneficiaire_modification",
        "assurance_vie_cas_particuliers_demembrement",
        "assurance_vie_transmission_principe_general",
    ],
    prerequisites=[
        "assurance_vie_clause_beneficiaire_definition",
    ],
    next_topics=[
        "assurance_vie_cas_particuliers_chef_entreprise",
    ],
),

Topic(
    id="assurance_vie_cas_particuliers_chef_entreprise",
    title="Pourquoi un chef d'entreprise utilise-t-il une assurance-vie ?",
    pillar="entreprendre",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre les principaux usages de l'assurance-vie dans la gestion du patrimoine privé d'un chef d'entreprise.",
    objective="Expliquer que l'assurance-vie peut constituer un outil patrimonial pertinent pour un dirigeant afin de diversifier son patrimoine privé, préparer une cession, organiser la transmission ou investir des liquidités personnelles.",
    difficulty="Avancé",
    priority=9,
    version=1,
    keywords=[
        "chef d'entreprise",
        "dirigeant",
        "assurance-vie",
        "cession",
        "patrimoine privé",
        "holding",
        "diversification",
        "transmission",
    ],
    key_points=[
        "Le patrimoine professionnel d'un dirigeant est souvent fortement concentré sur son entreprise.",
        "L'assurance-vie peut contribuer à diversifier le patrimoine privé.",
        "Après une cession d'entreprise, elle peut constituer une des enveloppes étudiées pour réorganiser une partie des liquidités personnelles.",
        "Elle peut également s'intégrer dans une stratégie de préparation de la retraite ou de transmission.",
        "Le choix de cette enveloppe dépend toujours des objectifs patrimoniaux du dirigeant et de sa situation personnelle."
    ],
    examples=[
        "Après la vente de son entreprise, Marc dispose d'un capital important. Avant de l'investir, il réalise un bilan patrimonial afin de répartir ses liquidités entre plusieurs solutions, dont une assurance-vie.",

        "Claire dirige une PME depuis quinze ans. Son patrimoine étant principalement constitué de la valeur de son entreprise, elle souhaite progressivement développer un patrimoine financier personnel grâce à une assurance-vie.",

        "Thomas prépare la transmission de son patrimoine familial plusieurs années avant son départ à la retraite. L'assurance-vie fait partie des outils étudiés avec son conseiller afin d'organiser cette transmission."
    ],
    vocabulary=[
        "chef d'entreprise",
        "patrimoine professionnel",
        "patrimoine privé",
        "cession",
        "liquidités",
        "diversification",
        "allocation",
        "transmission",
    ],
    legal_sources=[
        "Code des assurances",
        "Code général des impôts",
        "Code de commerce",
    ],
    analogies=[
        "Le patrimoine d'un chef d'entreprise ressemble souvent à une équipe qui ne compterait qu'un seul joueur. Diversifier progressivement son patrimoine privé permet d'équilibrer davantage l'ensemble."
    ],
    misconceptions=[
        "L'assurance-vie est réservée aux particuliers salariés.",
        "Après une cession d'entreprise, il faut investir immédiatement tout le capital.",
        "Le patrimoine professionnel suffit à préparer la retraite.",
        "L'assurance-vie est uniquement un outil de transmission."
    ],
    common_mistakes=[
        "Conserver l'essentiel de son patrimoine sur un seul actif professionnel.",
        "Investir rapidement après une cession sans réflexion patrimoniale globale.",
        "Confondre patrimoine professionnel et patrimoine privé.",
        "Reporter la diversification jusqu'à la fin de la carrière."
    ],
    expert_tips=[
        "Chez un chef d'entreprise, l'assurance-vie est rarement envisagée isolément. Elle s'inscrit généralement dans une stratégie patrimoniale plus large intégrant la diversification des actifs, la préparation de la retraite, la protection de la famille et l'organisation de la transmission."
    ],
    attention_points=[
        "Les objectifs d'un dirigeant évoluent souvent au fil du développement de son entreprise.",
        "Une cession d'entreprise constitue un événement patrimonial majeur qui mérite une réflexion globale.",
        "L'assurance-vie n'est qu'un des outils pouvant être mobilisés selon la situation."
    ],
    client_questions=[
        "Pourquoi un chef d'entreprise ouvre-t-il une assurance-vie ?",
        "Que faire après la vente de son entreprise ?",
        "Comment diversifier un patrimoine très concentré ?",
        "L'assurance-vie est-elle adaptée aux dirigeants ?",
    ],
    client_objections=[
        "Mon entreprise constitue déjà mon patrimoine.",
        "Je verrai après la cession.",
        "Je préfère réinvestir immédiatement dans un nouveau projet."
    ],
    client_fears=[
        "Conserver un patrimoine insuffisamment diversifié.",
        "Mal gérer les liquidités issues d'une cession.",
        "Ne pas préparer correctement la retraite ou la transmission."
    ],
    client_goals=[
        "Diversifier son patrimoine privé.",
        "Préparer une cession d'entreprise.",
        "Organiser la transmission familiale.",
        "Construire un patrimoine financier indépendant de l'entreprise."
    ],
    client_intents=[
        "assurance-vie chef d'entreprise",
        "cession entreprise patrimoine",
        "diversification dirigeant",
        "placement après vente entreprise",
    ],
    recommended_formats=[
        "linkedin_post",
        "article",
        "carrousel",
        "faq",
    ],
    related_topics=[
        "assurance_vie_comparaison_luxembourg",
        "assurance_vie_comparaison_capitalisation",
        "assurance_vie_questions_pourquoi_assurance_vie",
        "assurance_vie_cas_particuliers_gros_patrimoine",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[
        "assurance_vie_cas_particuliers_personne_vulnerable",
    ],
),

Topic(
    id="assurance_vie_cas_particuliers_personne_vulnerable",
    title="Assurance-vie et personne protégée : quelles règles en cas de tutelle ou de curatelle ?",
    pillar="proteger",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre les conséquences d'une mesure de protection juridique sur la souscription, la gestion et les opérations réalisées sur une assurance-vie.",
    objective="Expliquer que l'assurance-vie demeure accessible aux personnes protégées, mais que certaines décisions sont encadrées afin de préserver leurs intérêts.",
    difficulty="Avancé",
    priority=8,
    version=1,
    keywords=[
        "tutelle",
        "curatelle",
        "habilitation familiale",
        "personne protégée",
        "assurance-vie",
        "protection juridique",
        "majeur protégé",
        "patrimoine",
    ],
    key_points=[
        "Une personne protégée peut détenir une assurance-vie.",
        "Les règles applicables varient selon la mesure de protection mise en place.",
        "Certaines opérations peuvent nécessiter l'assistance ou la représentation du protecteur, voire une autorisation lorsqu'elle est prévue par les textes.",
        "Les intérêts patrimoniaux de la personne protégée doivent toujours être préservés.",
        "Les conséquences doivent être analysées au regard de chaque situation juridique."
    ],
    examples=[
        "À la suite d'un accident, Jean est placé sous curatelle. Avant de modifier son assurance-vie, son entourage vérifie les règles applicables à cette mesure de protection.",

        "Marie entre sous tutelle après une perte d'autonomie. Son tuteur souhaite effectuer un rachat sur son assurance-vie afin de financer certaines dépenses. Les conséquences juridiques de cette opération sont étudiées avant toute décision.",

        "À la suite d'une mesure d'habilitation familiale, les proches de Claire réexaminent l'organisation de son patrimoine afin de s'assurer que son assurance-vie reste adaptée à sa situation."
    ],
    vocabulary=[
        "tutelle",
        "curatelle",
        "habilitation familiale",
        "majeur protégé",
        "protecteur",
        "représentation",
        "assistance",
        "patrimoine",
    ],
    legal_sources=[
        "Code civil",
        "Code des assurances",
    ],
    analogies=[
        "La mesure de protection agit comme un garde-fou : elle ne retire pas automatiquement l'assurance-vie, mais encadre certaines décisions afin de protéger les intérêts de la personne vulnérable."
    ],
    misconceptions=[
        "Une personne sous tutelle ne peut plus avoir d'assurance-vie.",
        "Tous les actes sont interdits dès l'ouverture d'une mesure de protection.",
        "Les règles sont identiques en tutelle, en curatelle et en habilitation familiale.",
        "Le protecteur peut librement prendre toutes les décisions concernant le contrat."
    ],
    common_mistakes=[
        "Croire qu'une mesure de protection entraîne automatiquement la clôture du contrat.",
        "Ne pas vérifier les règles applicables avant d'effectuer une opération importante.",
        "Confondre les différents régimes de protection.",
        "Négliger les conséquences patrimoniales d'une mesure de protection."
    ],
    expert_tips=[
        "Lorsqu'une mesure de protection est mise en place, il est souvent pertinent de réaliser un audit patrimonial complet. L'assurance-vie n'est qu'un élément parmi d'autres : l'ensemble des actifs, des pouvoirs de gestion et des objectifs patrimoniaux mérite d'être réexaminé."
    ],
    attention_points=[
        "Les règles diffèrent selon la mesure de protection.",
        "Certaines opérations peuvent être soumises à un formalisme particulier.",
        "La protection de la personne demeure la priorité de toute décision patrimoniale."
    ],
    client_questions=[
        "Une personne sous tutelle peut-elle conserver son assurance-vie ?",
        "Qui peut gérer le contrat ?",
        "Peut-on effectuer un rachat ?",
        "Les règles sont-elles les mêmes en curatelle ?",
    ],
    client_objections=[
        "Je pensais que le contrat devait être fermé.",
        "La réglementation me paraît très complexe.",
        "Je crains de commettre une erreur juridique."
    ],
    client_fears=[
        "Prendre une décision contraire aux intérêts de la personne protégée.",
        "Ne pas respecter les règles applicables.",
        "Mettre en difficulté la gestion du patrimoine."
    ],
    client_goals=[
        "Protéger le patrimoine d'un proche.",
        "Comprendre les conséquences d'une mesure de protection.",
        "Gérer le contrat dans un cadre sécurisé.",
        "Préserver les intérêts de la personne vulnérable."
    ],
    client_intents=[
        "assurance-vie tutelle",
        "assurance-vie curatelle",
        "majeur protégé assurance-vie",
        "gestion assurance-vie personne protégée",
    ],
    recommended_formats=[
        "article",
        "faq",
        "linkedin_post",
        "carrousel",
    ],
    related_topics=[
        "assurance_vie_cas_particuliers_enfant_mineur",
        "assurance_vie_clause_beneficiaire_definition",
        "assurance_vie_transmission_principe_general",
        "assurance_vie_erreurs_clause_beneficiaire",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[
        "assurance_vie_cas_particuliers_non_resident",
    ],
),

Topic(
    id="assurance_vie_cas_particuliers_non_resident",
    title="Peut-on conserver une assurance-vie lorsqu'on devient non-résident ?",
    pillar="proteger",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre les principales conséquences du statut de non-résident sur une assurance-vie française et les points à vérifier avant ou après un changement de résidence fiscale.",
    objective="Expliquer qu'un changement de résidence fiscale n'impose pas, en principe, la clôture d'une assurance-vie, mais qu'il peut avoir des conséquences patrimoniales, fiscales et pratiques selon la situation.",
    difficulty="Avancé",
    priority=8,
    version=1,
    keywords=[
        "non-résident",
        "résidence fiscale",
        "assurance-vie",
        "international",
        "fiscalité",
        "convention fiscale",
        "rachat",
        "patrimoine",
    ],
    key_points=[
        "Une assurance-vie peut généralement être conservée après un changement de résidence fiscale.",
        "Le statut de non-résident peut modifier la fiscalité applicable aux rachats.",
        "Les conventions fiscales internationales peuvent influencer le traitement du contrat.",
        "Les conditions de gestion peuvent varier selon le pays de résidence et selon les assureurs.",
        "Le passage au statut de non-résident constitue une bonne occasion de réexaminer sa stratégie patrimoniale."
    ],
    examples=[
        "Après plusieurs années en France, Julie s'installe au Canada pour des raisons professionnelles. Elle conserve son assurance-vie mais analyse les conséquences de son nouveau statut de non-résidente sur son patrimoine.",

        "Marc prend sa retraite en Espagne. Avant d'effectuer un rachat sur son assurance-vie, il vérifie les règles applicables compte tenu de sa résidence fiscale.",

        "Claire vit désormais à Singapour. Son assureur lui demande de mettre à jour certaines informations administratives afin de maintenir son contrat dans de bonnes conditions."
    ],
    vocabulary=[
        "non-résident",
        "résidence fiscale",
        "convention fiscale",
        "rachat",
        "assureur",
        "mobilité internationale",
        "patrimoine international",
        "fiscalité",
    ],
    legal_sources=[
        "Code général des impôts",
        "Code des assurances",
        "Conventions fiscales internationales",
    ],
    analogies=[
        "Conserver une assurance-vie en devenant non-résident ressemble à conserver un compte bancaire dans un autre pays : le contrat continue d'exister, mais certaines règles peuvent évoluer en fonction de votre nouvelle résidence."
    ],
    misconceptions=[
        "Je dois obligatoirement fermer mon assurance-vie si je quitte la France.",
        "La fiscalité française disparaît automatiquement lorsque je deviens non-résident.",
        "Tous les assureurs appliquent les mêmes règles aux non-résidents.",
        "Les conventions fiscales produisent toujours les mêmes effets."
    ],
    common_mistakes=[
        "Ne pas informer son assureur de son changement de résidence.",
        "Réaliser un rachat sans vérifier les conséquences fiscales.",
        "Supposer que les règles sont identiques dans tous les pays.",
        "Ne pas mettre à jour son organisation patrimoniale après un départ à l'étranger."
    ],
    expert_tips=[
        "Le passage au statut de non-résident mérite une analyse patrimoniale globale. Au-delà de l'assurance-vie, il est souvent utile de revoir l'ensemble des actifs financiers, immobiliers et successoraux afin de vérifier leur cohérence avec le nouveau contexte international."
    ],
    attention_points=[
        "Les conséquences dépendent principalement du pays de résidence.",
        "Les conventions fiscales doivent être prises en compte.",
        "Chaque assureur applique ses propres conditions d'acceptation et de gestion des non-résidents."
    ],
    client_questions=[
        "Puis-je garder mon assurance-vie en vivant à l'étranger ?",
        "Dois-je prévenir mon assureur ?",
        "Comment seront imposés mes rachats ?",
        "Mon contrat reste-t-il valable ?",
    ],
    client_objections=[
        "Je pensais devoir fermer mon contrat.",
        "La fiscalité internationale me paraît trop complexe.",
        "Je ne sais pas si mon assureur accepte les non-résidents."
    ],
    client_fears=[
        "Perdre les avantages de mon assurance-vie.",
        "Être soumis à une double imposition.",
        "Faire une erreur lors de mon changement de résidence."
    ],
    client_goals=[
        "Conserver son patrimoine dans un cadre sécurisé.",
        "Comprendre les conséquences du statut de non-résident.",
        "Adapter sa stratégie patrimoniale à l'international.",
        "Préparer sereinement sa mobilité."
    ],
    client_intents=[
        "assurance-vie non-résident",
        "garder une assurance-vie à l'étranger",
        "résidence fiscale assurance-vie",
        "contrat assurance-vie expatrié",
    ],
    recommended_formats=[
        "article",
        "linkedin_post",
        "faq",
        "carrousel",
    ],
    related_topics=[
        "assurance_vie_cas_particuliers_expatriation",
        "assurance_vie_comparaison_luxembourg",
        "assurance_vie_questions_retirer_argent",
        "assurance_vie_fiscalite_rachat",
    ],
    prerequisites=[
        "assurance_vie_cas_particuliers_expatriation",
    ],
    next_topics=[
        "assurance_vie_cas_particuliers_gros_patrimoine",
    ],
),

Topic(
    id="assurance_vie_cas_particuliers_gros_patrimoine",
    title="Quand un patrimoine important conduit-il à repenser son assurance-vie ?",
    pillar="structurer",
    family="assurance_vie",
    chapter="cas_particuliers",
    description="Comprendre pourquoi l'évolution d'un patrimoine peut conduire à réexaminer la place de l'assurance-vie dans une stratégie patrimoniale globale.",
    objective="Expliquer qu'à mesure qu'un patrimoine se développe, l'assurance-vie demeure un outil pertinent mais s'inscrit généralement dans une réflexion plus large de diversification, de gouvernance et de transmission.",
    difficulty="Avancé",
    priority=10,
    version=1,
    keywords=[
        "gros patrimoine",
        "assurance-vie",
        "diversification",
        "allocation",
        "transmission",
        "gouvernance patrimoniale",
        "banque privée",
        "ingénierie patrimoniale",
    ],
    key_points=[
        "L'évolution d'un patrimoine conduit souvent à réévaluer l'organisation des actifs.",
        "L'assurance-vie reste un outil patrimonial, mais elle s'intègre dans une stratégie plus globale.",
        "La diversification peut porter sur les actifs, les enveloppes patrimoniales, les établissements ou les juridictions, selon les objectifs poursuivis.",
        "Les enjeux de transmission, de gouvernance familiale et de protection du patrimoine prennent progressivement davantage d'importance.",
        "Il n'existe aucun seuil universel à partir duquel une stratégie doit être modifiée."
    ],
    examples=[
        "Après la cession de son entreprise, Marc voit son patrimoine financier fortement augmenter. Il réalise un audit patrimonial complet afin de revoir la répartition de ses actifs, la place de son assurance-vie et sa stratégie de transmission.",

        "Claire constitue progressivement un patrimoine immobilier, financier et professionnel. Avec son conseiller, elle réorganise ses différentes enveloppes afin qu'elles répondent à des objectifs complémentaires plutôt que redondants.",

        "Une famille prépare la transmission intergénérationnelle de son patrimoine. L'assurance-vie reste un outil important, mais elle est désormais articulée avec d'autres mécanismes patrimoniaux étudiés dans une approche globale."
    ],
    vocabulary=[
        "allocation stratégique",
        "diversification",
        "gouvernance patrimoniale",
        "transmission",
        "architecture patrimoniale",
        "banque privée",
        "ingénierie patrimoniale",
        "allocation d'actifs",
    ],
    legal_sources=[
        "Code des assurances",
        "Code général des impôts",
        "Code civil",
    ],
    analogies=[
        "Au début, un patrimoine ressemble à une maison que l'on aménage pièce par pièce. Lorsqu'il devient plus important, il se rapproche d'un quartier entier qu'il faut organiser de manière cohérente. L'assurance-vie reste un bâtiment essentiel, mais elle n'est plus le seul."
    ],
    misconceptions=[
        "L'assurance-vie ne sert plus lorsque le patrimoine devient important.",
        "Il existe un montant précis à partir duquel il faut changer totalement de stratégie.",
        "Les patrimoines importants utilisent uniquement des solutions complexes.",
        "Une seule assurance-vie suffit toujours, quelle que soit l'évolution du patrimoine."
    ],
    common_mistakes=[
        "Conserver une organisation patrimoniale devenue inadaptée à l'évolution du patrimoine.",
        "Multiplier les produits sans stratégie globale.",
        "Négliger les enjeux de gouvernance familiale.",
        "Reporter les réflexions sur la transmission malgré l'évolution du patrimoine."
    ],
    expert_tips=[
        "L'augmentation d'un patrimoine ne remet pas en cause l'intérêt de l'assurance-vie. Elle conduit surtout à s'interroger sur sa place dans une stratégie patrimoniale plus large intégrant la diversification, la transmission, la gouvernance familiale et, selon les situations, d'autres outils juridiques et fiscaux."
    ],
    attention_points=[
        "Chaque patrimoine évolue selon son histoire et ses objectifs.",
        "La diversification ne concerne pas uniquement les investissements, mais aussi l'organisation patrimoniale.",
        "Les stratégies patrimoniales doivent être régulièrement réévaluées."
    ],
    client_questions=[
        "Mon assurance-vie est-elle toujours adaptée à mon patrimoine ?",
        "Faut-il plusieurs assurances-vie ?",
        "Quand faut-il revoir son organisation patrimoniale ?",
        "Comment structurer un patrimoine important ?",
    ],
    client_objections=[
        "Mon assurance-vie me suffit largement.",
        "Je ne souhaite pas complexifier mon patrimoine.",
        "Je verrai plus tard lorsque mon patrimoine sera encore plus important."
    ],
    client_fears=[
        "Conserver une organisation patrimoniale inadaptée.",
        "Négliger la transmission familiale.",
        "Passer à côté d'une meilleure structuration patrimoniale."
    ],
    client_goals=[
        "Structurer durablement son patrimoine.",
        "Diversifier ses outils patrimoniaux.",
        "Préparer la transmission familiale.",
        "Mettre en place une gouvernance adaptée à l'évolution du patrimoine."
    ],
    client_intents=[
        "gros patrimoine assurance-vie",
        "structurer un patrimoine important",
        "plusieurs assurances-vie",
        "organisation patrimoniale",
    ],
    recommended_formats=[
        "linkedin_post",
        "article",
        "carrousel",
        "faq",
    ],
    related_topics=[
        "assurance_vie_cas_particuliers_chef_entreprise",
        "assurance_vie_comparaison_luxembourg",
        "assurance_vie_comparaison_capitalisation",
        "assurance_vie_comparaison_quel_placement",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
        "assurance_vie_transmission_principe_general",
    ],
    next_topics=[],
),

