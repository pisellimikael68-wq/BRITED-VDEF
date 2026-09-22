from v2.models.knowledge_models import Topic

COMPARAISONS_TOPICS: list[Topic] = []

Topic(
    id="assurance_vie_comparaison_livret_a",
    title="Assurance-vie ou Livret A : lequel choisir ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre les principales différences entre une assurance-vie et un Livret A afin de choisir l'enveloppe la plus adaptée à ses objectifs patrimoniaux.",
    objective="Expliquer que le Livret A et l'assurance-vie répondent à des besoins différents et qu'ils sont souvent complémentaires plutôt que concurrents.",
    difficulty="Débutant",
    priority=10,
    version=1,
    keywords=[
        "assurance-vie",
        "livret A",
        "comparaison",
        "épargne",
        "placement",
        "liquidité",
        "fiscalité",
        "patrimoine",
    ],
    key_points=[
        "Le Livret A privilégie la disponibilité immédiate des fonds.",
        "L'assurance-vie est une enveloppe patrimoniale destinée à des projets de moyen et long terme.",
        "Les deux solutions peuvent être complémentaires dans une stratégie patrimoniale.",
        "Le choix dépend principalement de l'horizon de placement, du niveau de risque accepté et des objectifs poursuivis.",
        "Comparer uniquement le rendement ne permet pas de choisir le placement le plus adapté.",
    ],
    examples=[
        "Julie, 27 ans, souhaite constituer une épargne de précaution. Elle conserve plusieurs mois de dépenses sur son Livret A et investit progressivement le surplus sur une assurance-vie afin de préparer des projets à plus long terme.",

        "Marc, 49 ans, dispose déjà d'une épargne de sécurité suffisante. Il ouvre une assurance-vie afin de préparer sa retraite et transmettre une partie de son patrimoine à ses enfants.",

        "Claire hésite entre ouvrir un Livret A ou une assurance-vie. Après avoir identifié ses objectifs, elle comprend que les deux produits répondent à des besoins différents et décide de les utiliser de manière complémentaire.",
    ],
    vocabulary=[
        "Livret A",
        "assurance-vie",
        "liquidité",
        "épargne de précaution",
        "placement",
        "transmission",
        "allocation",
        "horizon de placement",
    ],
    legal_sources=[
        "Code monétaire et financier",
        "Code des assurances",
        "Code général des impôts",
    ],
    analogies=[
        "Le Livret A est comparable à une réserve d'eau facilement accessible en cas d'urgence. L'assurance-vie ressemble davantage à un verger que l'on plante aujourd'hui pour récolter ses fruits dans plusieurs années.",
    ],
    misconceptions=[
        "L'assurance-vie remplace le Livret A.",
        "Le Livret A est toujours le meilleur placement.",
        "Il faut choisir entre l'un ou l'autre.",
        "Le rendement est le seul critère de comparaison.",
    ],
    common_mistakes=[
        "Investir toute son épargne sur un seul support.",
        "Utiliser une assurance-vie comme épargne de précaution.",
        "Comparer uniquement les performances.",
        "Oublier les objectifs de transmission et de fiscalité.",
    ],
    expert_tips=[
        "Dans de nombreuses stratégies patrimoniales, le Livret A et l'assurance-vie ne s'opposent pas : ils remplissent des fonctions différentes. Le Livret A répond aux besoins de court terme, tandis que l'assurance-vie permet généralement de construire une stratégie à moyen et long terme.",
    ],
    attention_points=[
        "L'épargne de précaution doit généralement rester immédiatement disponible.",
        "L'assurance-vie prend davantage de sens sur une durée longue.",
        "Le choix dépend toujours de la situation patrimoniale globale.",
    ],
    client_questions=[
        "Quel placement choisir ?",
        "Le Livret A est-il plus intéressant ?",
        "Puis-je avoir les deux ?",
        "Quel produit privilégier pour commencer à épargner ?",
    ],
    client_objections=[
        "Je préfère garder mon argent disponible.",
        "Je ne veux pas prendre de risque.",
        "Je pensais que l'assurance-vie remplaçait le Livret A.",
    ],
    client_fears=[
        "Choisir le mauvais placement.",
        "Bloquer inutilement son épargne.",
        "Prendre un risque inadapté.",
    ],
    client_goals=[
        "Constituer une épargne de précaution.",
        "Préparer des projets de long terme.",
        "Diversifier son patrimoine.",
        "Optimiser son organisation patrimoniale.",
    ],
    client_intents=[
        "assurance-vie ou livret A",
        "meilleur placement",
        "où placer son argent",
        "comparer assurance-vie et livret A",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_questions_pourquoi_assurance_vie",
        "assurance_vie_questions_retirer_argent",
        "assurance_vie_supports_principe_general",
        "assurance_vie_fiscalite_principe_general",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[
        "assurance_vie_comparaison_pea",
    ],
),

Topic(
    id="assurance_vie_comparaison_pea",
    title="Assurance-vie ou PEA : lequel choisir ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre les principales différences entre une assurance-vie et un Plan d'Épargne en Actions (PEA) afin de choisir l'enveloppe la plus adaptée à ses objectifs patrimoniaux.",
    objective="Expliquer que l'assurance-vie et le PEA poursuivent des objectifs différents et qu'ils peuvent être utilisés de manière complémentaire dans une stratégie patrimoniale.",
    difficulty="Intermédiaire",
    priority=10,
    version=1,
    keywords=[
        "PEA",
        "assurance-vie",
        "comparaison",
        "actions",
        "fiscalité",
        "investissement",
        "transmission",
        "patrimoine",
    ],
    key_points=[
        "Le PEA est principalement destiné à l'investissement en actions européennes.",
        "L'assurance-vie permet d'investir sur une gamme beaucoup plus large de supports.",
        "Les deux enveloppes disposent de régimes fiscaux spécifiques.",
        "L'assurance-vie présente des atouts particuliers en matière de transmission patrimoniale.",
        "Le choix dépend des objectifs d'investissement, de l'horizon de placement et de la stratégie patrimoniale globale.",
    ],
    examples=[
        "Julie, 31 ans, souhaite investir régulièrement sur les marchés actions afin de faire croître son patrimoine à long terme. Elle s'intéresse au PEA pour son exposition aux actions tout en conservant une assurance-vie pour préparer d'autres projets.",

        "Marc, 56 ans, possède déjà un PEA investi en actions. Il ouvre une assurance-vie afin de diversifier ses investissements et préparer la transmission d'une partie de son patrimoine.",

        "Claire, 43 ans, hésite entre ouvrir un PEA ou une assurance-vie. Après avoir identifié ses objectifs, elle comprend que les deux enveloppes répondent à des besoins complémentaires plutôt qu'à une logique de concurrence.",
    ],
    vocabulary=[
        "PEA",
        "actions",
        "unités de compte",
        "fonds euros",
        "allocation",
        "diversification",
        "transmission",
        "enveloppe fiscale",
    ],
    legal_sources=[
        "Code monétaire et financier",
        "Code général des impôts",
        "Code des assurances",
    ],
    analogies=[
        "Le PEA est comparable à une boîte à outils spécialisée pour investir en actions. L'assurance-vie ressemble davantage à une boîte à outils multifonction permettant d'accéder à de nombreuses classes d'actifs et d'organiser la transmission du patrimoine.",
    ],
    misconceptions=[
        "Le PEA est toujours meilleur que l'assurance-vie.",
        "L'assurance-vie est réservée aux personnes prudentes.",
        "Il faut choisir entre un PEA et une assurance-vie.",
        "Les deux produits remplissent exactement la même fonction.",
    ],
    common_mistakes=[
        "Comparer uniquement la fiscalité.",
        "Oublier les objectifs de transmission.",
        "Choisir une enveloppe sans tenir compte de l'horizon de placement.",
        "Croire que le PEA permet tous les types d'investissement.",
    ],
    expert_tips=[
        "Dans de nombreux patrimoines, le PEA et l'assurance-vie sont complémentaires. Le premier peut constituer une excellente enveloppe pour investir en actions, tandis que la seconde offre une grande souplesse d'investissement et des avantages spécifiques en matière de transmission.",
    ],
    attention_points=[
        "Chaque enveloppe possède ses propres règles de fonctionnement et de fiscalité.",
        "Le choix doit être guidé par les objectifs patrimoniaux avant les considérations fiscales.",
        "Une stratégie diversifiée peut intégrer simultanément un PEA et une assurance-vie.",
    ],
    client_questions=[
        "Dois-je ouvrir un PEA ou une assurance-vie ?",
        "Quel produit est le plus rentable ?",
        "Puis-je avoir les deux ?",
        "Lequel choisir pour préparer ma retraite ?",
    ],
    client_objections=[
        "Je pensais que le PEA rendait l'assurance-vie inutile.",
        "Je ne veux pas multiplier les placements.",
        "Je cherche le produit qui rapporte le plus.",
    ],
    client_fears=[
        "Choisir la mauvaise enveloppe.",
        "Passer à côté d'un avantage fiscal.",
        "Construire une stratégie patrimoniale inadaptée.",
    ],
    client_goals=[
        "Investir à long terme.",
        "Diversifier son patrimoine.",
        "Optimiser sa fiscalité.",
        "Préparer la transmission de son patrimoine.",
    ],
    client_intents=[
        "PEA ou assurance-vie",
        "comparaison PEA assurance-vie",
        "quel placement choisir",
        "investir en actions",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_comparaison_livret_a",
        "assurance_vie_comparaison_per",
        "assurance_vie_supports_unites_compte",
        "assurance_vie_transmission_principe_general",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
        "assurance_vie_supports_principe_general",
    ],
    next_topics=[
        "assurance_vie_comparaison_per",
    ],
),

Topic(
    id="assurance_vie_comparaison_pea",
    title="Assurance-vie ou PEA : lequel choisir ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre les principales différences entre une assurance-vie et un Plan d'Épargne en Actions (PEA) afin de choisir l'enveloppe la plus adaptée à ses objectifs patrimoniaux.",
    objective="Expliquer que l'assurance-vie et le PEA poursuivent des objectifs différents et qu'ils peuvent être utilisés de manière complémentaire dans une stratégie patrimoniale.",
    difficulty="Intermédiaire",
    priority=10,
    version=1,
    keywords=[
        "PEA",
        "assurance-vie",
        "comparaison",
        "actions",
        "fiscalité",
        "investissement",
        "transmission",
        "patrimoine",
    ],
    key_points=[
        "Le PEA est principalement destiné à l'investissement en actions européennes.",
        "L'assurance-vie permet d'investir sur une gamme beaucoup plus large de supports.",
        "Les deux enveloppes disposent de régimes fiscaux spécifiques.",
        "L'assurance-vie présente des atouts particuliers en matière de transmission patrimoniale.",
        "Le choix dépend des objectifs d'investissement, de l'horizon de placement et de la stratégie patrimoniale globale.",
    ],
    examples=[
        "Julie, 31 ans, souhaite investir régulièrement sur les marchés actions afin de faire croître son patrimoine à long terme. Elle s'intéresse au PEA pour son exposition aux actions tout en conservant une assurance-vie pour préparer d'autres projets.",

        "Marc, 56 ans, possède déjà un PEA investi en actions. Il ouvre une assurance-vie afin de diversifier ses investissements et préparer la transmission d'une partie de son patrimoine.",

        "Claire, 43 ans, hésite entre ouvrir un PEA ou une assurance-vie. Après avoir identifié ses objectifs, elle comprend que les deux enveloppes répondent à des besoins complémentaires plutôt qu'à une logique de concurrence.",
    ],
    vocabulary=[
        "PEA",
        "actions",
        "unités de compte",
        "fonds euros",
        "allocation",
        "diversification",
        "transmission",
        "enveloppe fiscale",
    ],
    legal_sources=[
        "Code monétaire et financier",
        "Code général des impôts",
        "Code des assurances",
    ],
    analogies=[
        "Le PEA est comparable à une boîte à outils spécialisée pour investir en actions. L'assurance-vie ressemble davantage à une boîte à outils multifonction permettant d'accéder à de nombreuses classes d'actifs et d'organiser la transmission du patrimoine.",
    ],
    misconceptions=[
        "Le PEA est toujours meilleur que l'assurance-vie.",
        "L'assurance-vie est réservée aux personnes prudentes.",
        "Il faut choisir entre un PEA et une assurance-vie.",
        "Les deux produits remplissent exactement la même fonction.",
    ],
    common_mistakes=[
        "Comparer uniquement la fiscalité.",
        "Oublier les objectifs de transmission.",
        "Choisir une enveloppe sans tenir compte de l'horizon de placement.",
        "Croire que le PEA permet tous les types d'investissement.",
    ],
    expert_tips=[
        "Dans de nombreux patrimoines, le PEA et l'assurance-vie sont complémentaires. Le premier peut constituer une excellente enveloppe pour investir en actions, tandis que la seconde offre une grande souplesse d'investissement et des avantages spécifiques en matière de transmission.",
    ],
    attention_points=[
        "Chaque enveloppe possède ses propres règles de fonctionnement et de fiscalité.",
        "Le choix doit être guidé par les objectifs patrimoniaux avant les considérations fiscales.",
        "Une stratégie diversifiée peut intégrer simultanément un PEA et une assurance-vie.",
    ],
    client_questions=[
        "Dois-je ouvrir un PEA ou une assurance-vie ?",
        "Quel produit est le plus rentable ?",
        "Puis-je avoir les deux ?",
        "Lequel choisir pour préparer ma retraite ?",
    ],
    client_objections=[
        "Je pensais que le PEA rendait l'assurance-vie inutile.",
        "Je ne veux pas multiplier les placements.",
        "Je cherche le produit qui rapporte le plus.",
    ],
    client_fears=[
        "Choisir la mauvaise enveloppe.",
        "Passer à côté d'un avantage fiscal.",
        "Construire une stratégie patrimoniale inadaptée.",
    ],
    client_goals=[
        "Investir à long terme.",
        "Diversifier son patrimoine.",
        "Optimiser sa fiscalité.",
        "Préparer la transmission de son patrimoine.",
    ],
    client_intents=[
        "PEA ou assurance-vie",
        "comparaison PEA assurance-vie",
        "quel placement choisir",
        "investir en actions",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_comparaison_livret_a",
        "assurance_vie_comparaison_per",
        "assurance_vie_supports_unites_compte",
        "assurance_vie_transmission_principe_general",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
        "assurance_vie_supports_principe_general",
    ],
    next_topics=[
        "assurance_vie_comparaison_per",
    ],
),

Topic(
    id="assurance_vie_comparaison_compte_titres",
    title="Compte-titres ou assurance-vie : lequel choisir ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre les principales différences entre un compte-titres ordinaire et une assurance-vie afin de choisir l'enveloppe la plus adaptée à ses objectifs patrimoniaux.",
    objective="Expliquer que le compte-titres et l'assurance-vie répondent à des logiques d'investissement différentes et peuvent être utilisés de manière complémentaire.",
    difficulty="Intermédiaire",
    priority=9,
    version=1,
    keywords=[
        "compte-titres",
        "CTO",
        "assurance-vie",
        "comparaison",
        "investissement",
        "actions",
        "ETF",
        "fiscalité",
    ],
    key_points=[
        "Le compte-titres offre une très grande liberté d'investissement.",
        "L'assurance-vie constitue une enveloppe patrimoniale bénéficiant d'un cadre fiscal et successoral spécifique.",
        "Les règles fiscales applicables diffèrent selon l'enveloppe utilisée.",
        "L'assurance-vie présente des atouts particuliers en matière de transmission.",
        "Le choix dépend avant tout des objectifs patrimoniaux, de l'horizon d'investissement et du besoin de flexibilité.",
    ],
    examples=[
        "Julie, 29 ans, souhaite investir librement sur des actions internationales et des ETF. Elle choisit un compte-titres pour accéder à un univers d'investissement très large, tout en conservant une assurance-vie pour préparer sa transmission.",

        "Marc, 58 ans, possède déjà un portefeuille d'actions sur un compte-titres. Il ouvre une assurance-vie afin de diversifier son patrimoine et bénéficier d'une enveloppe adaptée à ses projets successoraux.",

        "Claire, 46 ans, hésite entre les deux solutions. Après avoir identifié ses objectifs, elle comprend que le compte-titres répond davantage à sa stratégie d'investissement, tandis que l'assurance-vie apporte une dimension patrimoniale complémentaire.",
    ],
    vocabulary=[
        "compte-titres",
        "CTO",
        "ETF",
        "actions",
        "obligations",
        "unités de compte",
        "enveloppe fiscale",
        "transmission",
    ],
    legal_sources=[
        "Code monétaire et financier",
        "Code général des impôts",
        "Code des assurances",
    ],
    analogies=[
        "Le compte-titres est comparable à un terrain totalement libre sur lequel vous choisissez presque tout ce que vous souhaitez construire. L'assurance-vie ressemble davantage à une maison déjà équipée, offrant un cadre patrimonial particulier avec ses propres avantages.",
    ],
    misconceptions=[
        "Le compte-titres est réservé aux professionnels.",
        "L'assurance-vie permet exactement les mêmes investissements qu'un compte-titres.",
        "Le compte-titres est toujours moins intéressant fiscalement.",
        "Il faut choisir définitivement entre les deux.",
    ],
    common_mistakes=[
        "Comparer uniquement la fiscalité.",
        "Ignorer les enjeux de transmission.",
        "Choisir une enveloppe sans définir son objectif patrimonial.",
        "Croire que toutes les classes d'actifs sont accessibles dans une assurance-vie.",
    ],
    expert_tips=[
        "Le compte-titres et l'assurance-vie répondent souvent à des usages différents. Le premier privilégie la liberté d'investissement, tandis que la seconde apporte un cadre patrimonial particulièrement intéressant pour diversifier son patrimoine et préparer sa transmission.",
    ],
    attention_points=[
        "Toutes les classes d'actifs ne sont pas nécessairement disponibles dans une assurance-vie.",
        "Les conséquences fiscales diffèrent selon l'enveloppe utilisée.",
        "La stratégie d'investissement doit toujours être cohérente avec les objectifs patrimoniaux.",
    ],
    client_questions=[
        "Quelle est la différence entre un compte-titres et une assurance-vie ?",
        "Puis-je investir en ETF dans une assurance-vie ?",
        "Lequel choisir pour investir en actions ?",
        "Puis-je détenir les deux ?",
    ],
    client_objections=[
        "Le compte-titres me semble trop risqué.",
        "Je préfère une enveloppe plus simple.",
        "Je cherche uniquement le meilleur rendement.",
    ],
    client_fears=[
        "Choisir une enveloppe inadaptée.",
        "Payer trop d'impôts.",
        "Limiter inutilement mes possibilités d'investissement.",
    ],
    client_goals=[
        "Investir efficacement.",
        "Diversifier son patrimoine.",
        "Optimiser la transmission.",
        "Choisir une enveloppe adaptée à ses projets.",
    ],
    client_intents=[
        "compte-titres ou assurance-vie",
        "comparaison CTO assurance-vie",
        "investir en actions",
        "ETF assurance-vie",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_comparaison_pea",
        "assurance_vie_comparaison_per",
        "assurance_vie_supports_unites_compte",
        "assurance_vie_questions_pourquoi_assurance_vie",
    ],
    prerequisites=[
        "assurance_vie_supports_principe_general",
        "assurance_vie_fiscalite_principe_general",
    ],
    next_topics=[
        "assurance_vie_comparaison_scpi",
    ],
),

Topic(
    id="assurance_vie_comparaison_scpi",
    title="SCPI ou assurance-vie : lequel choisir ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre les différences entre un investissement en SCPI et une assurance-vie, ainsi que les situations dans lesquelles ces deux solutions peuvent être complémentaires.",
    objective="Expliquer qu'une SCPI est un support d'investissement immobilier tandis que l'assurance-vie est une enveloppe patrimoniale pouvant notamment accueillir des SCPI selon les contrats.",
    difficulty="Intermédiaire",
    priority=9,
    version=1,
    keywords=[
        "SCPI",
        "assurance-vie",
        "immobilier",
        "comparaison",
        "revenus",
        "investissement",
        "patrimoine",
        "diversification",
    ],
    key_points=[
        "Une SCPI est un support d'investissement immobilier, alors que l'assurance-vie est une enveloppe patrimoniale.",
        "Certaines assurances-vie permettent d'investir dans des SCPI au sein du contrat.",
        "Les règles de fiscalité, de liquidité et de transmission diffèrent selon le mode de détention.",
        "Les SCPI répondent souvent à un objectif de diversification immobilière et de revenus potentiels.",
        "L'assurance-vie et les SCPI peuvent être complémentaires dans une stratégie patrimoniale.",
    ],
    examples=[
        "Julie, 43 ans, souhaite investir dans l'immobilier sans gérer directement un bien. Elle découvre les SCPI et compare un achat en direct avec une détention via son assurance-vie.",

        "Marc, 61 ans, recherche un complément de revenus pour la retraite. Avec son conseiller, il étudie l'intérêt d'intégrer des SCPI dans son assurance-vie afin de bénéficier du cadre patrimonial du contrat.",

        "Claire, 52 ans, possède déjà plusieurs biens immobiliers. Elle utilise une assurance-vie investie en partie en SCPI afin de diversifier son patrimoine sans acquérir un nouvel appartement.",
    ],
    vocabulary=[
        "SCPI",
        "immobilier",
        "parts",
        "revenus",
        "assurance-vie",
        "unités de compte",
        "diversification",
        "liquidité",
    ],
    legal_sources=[
        "Code monétaire et financier",
        "Code des assurances",
        "Code général des impôts",
    ],
    analogies=[
        "Comparer une SCPI à une assurance-vie revient un peu à comparer un livre à une bibliothèque : la SCPI est un investissement, tandis que l'assurance-vie est une enveloppe qui peut contenir différents investissements, dont parfois des SCPI.",
    ],
    misconceptions=[
        "Il faut choisir entre une SCPI et une assurance-vie.",
        "Une SCPI est une assurance-vie immobilière.",
        "Les SCPI ne peuvent pas être logées dans une assurance-vie.",
        "Les deux produits répondent exactement au même besoin.",
    ],
    common_mistakes=[
        "Comparer uniquement les rendements.",
        "Oublier les différences de liquidité.",
        "Ignorer les conséquences fiscales selon le mode de détention.",
        "Confondre support d'investissement et enveloppe patrimoniale.",
    ],
    expert_tips=[
        "La véritable question n'est généralement pas 'SCPI ou assurance-vie ?', mais 'Comment intégrer l'immobilier dans une stratégie patrimoniale globale ?'. Dans certains cas, détenir des SCPI au sein d'une assurance-vie peut permettre de combiner diversification immobilière et avantages propres à l'enveloppe.",
    ],
    attention_points=[
        "Toutes les assurances-vie ne proposent pas des SCPI.",
        "Les modalités de souscription, de valorisation et de retrait peuvent différer selon le contrat.",
        "Le niveau de risque et la liquidité des SCPI doivent être analysés avant tout investissement.",
    ],
    client_questions=[
        "Dois-je acheter des SCPI ou ouvrir une assurance-vie ?",
        "Puis-je détenir des SCPI dans mon assurance-vie ?",
        "Quelle est la différence entre les deux ?",
        "Quelle solution est la plus adaptée pour préparer ma retraite ?",
    ],
    client_objections=[
        "Je pensais qu'il fallait choisir entre immobilier et assurance-vie.",
        "Les SCPI me semblent compliquées.",
        "Je préfère investir uniquement dans la pierre.",
    ],
    client_fears=[
        "Faire un mauvais choix patrimonial.",
        "Manquer de liquidité.",
        "Choisir un investissement inadapté à mes objectifs.",
    ],
    client_goals=[
        "Diversifier son patrimoine.",
        "Investir dans l'immobilier.",
        "Préparer des revenus futurs.",
        "Optimiser son allocation patrimoniale.",
    ],
    client_intents=[
        "SCPI ou assurance-vie",
        "SCPI assurance-vie",
        "investissement immobilier",
        "comparaison SCPI",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_supports_unites_compte",
        "assurance_vie_questions_pourquoi_assurance_vie",
        "assurance_vie_comparaison_compte_titres",
        "assurance_vie_comparaison_capitalisation",
    ],
    prerequisites=[
        "assurance_vie_supports_principe_general",
    ],
    next_topics=[
        "assurance_vie_comparaison_capitalisation",
    ],
),

Topic(
    id="assurance_vie_comparaison_capitalisation",
    title="Contrat de capitalisation ou assurance-vie : quelles différences ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre les principales différences entre un contrat de capitalisation et une assurance-vie afin d'identifier les situations dans lesquelles chaque enveloppe peut présenter un intérêt.",
    objective="Expliquer que le contrat de capitalisation et l'assurance-vie fonctionnent de manière proche pendant la phase d'épargne mais répondent à des logiques patrimoniales différentes, notamment en matière de transmission.",
    difficulty="Avancé",
    priority=8,
    version=1,
    keywords=[
        "contrat de capitalisation",
        "assurance-vie",
        "comparaison",
        "capitalisation",
        "transmission",
        "succession",
        "donation",
        "personne morale",
    ],
    key_points=[
        "Le contrat de capitalisation et l'assurance-vie permettent d'investir sur des supports similaires.",
        "Le contrat de capitalisation ne se dénoue pas automatiquement au décès de son titulaire.",
        "L'assurance-vie bénéficie d'un régime spécifique en matière de transmission grâce à la clause bénéficiaire.",
        "Le contrat de capitalisation peut être transmis par donation ou succession dans des conditions propres à cette enveloppe.",
        "Le choix dépend principalement des objectifs patrimoniaux, de la stratégie de transmission et de la situation du souscripteur.",
    ],
    examples=[
        "Julie, 48 ans, souhaite transmettre progressivement une partie de son patrimoine à ses enfants. Son conseiller compare l'intérêt d'un contrat de capitalisation et d'une assurance-vie selon ses objectifs de transmission.",

        "Marc dirige une société disposant d'une trésorerie importante. Il étudie le contrat de capitalisation comme solution d'investissement adaptée aux personnes morales, en complément d'autres placements.",

        "Claire, 67 ans, souhaite protéger son conjoint tout en préparant la transmission à ses enfants. Après comparaison, elle comprend que l'assurance-vie répond davantage à cet objectif grâce à la clause bénéficiaire.",
    ],
    vocabulary=[
        "contrat de capitalisation",
        "assurance-vie",
        "clause bénéficiaire",
        "succession",
        "donation",
        "personne morale",
        "transmission",
        "capitalisation",
    ],
    legal_sources=[
        "Code des assurances",
        "Code général des impôts",
        "Code civil",
    ],
    analogies=[
        "Le contrat de capitalisation et l'assurance-vie ressemblent à deux véhicules construits sur la même plateforme : leur fonctionnement quotidien est proche, mais leur destination patrimoniale diffère, notamment lors de la transmission.",
    ],
    misconceptions=[
        "Le contrat de capitalisation est une assurance-vie.",
        "Les deux produits sont totalement identiques.",
        "Le contrat de capitalisation bénéficie automatiquement d'une clause bénéficiaire.",
        "Le contrat de capitalisation est réservé aux très grandes fortunes.",
    ],
    common_mistakes=[
        "Choisir l'une des deux enveloppes sans réfléchir aux objectifs de transmission.",
        "Confondre succession et clause bénéficiaire.",
        "Ignorer que le contrat de capitalisation peut être détenu dans certaines situations par une personne morale.",
        "Comparer uniquement la fiscalité des rachats.",
    ],
    expert_tips=[
        "Le contrat de capitalisation est souvent méconnu alors qu'il constitue un outil patrimonial particulièrement intéressant dans certaines stratégies de transmission, de donation ou de gestion de trésorerie. L'assurance-vie reste toutefois la référence lorsque l'objectif principal est de transmettre un capital à des bénéficiaires désignés.",
    ],
    attention_points=[
        "Le décès du titulaire n'entraîne pas les mêmes conséquences selon l'enveloppe choisie.",
        "Les règles civiles et fiscales diffèrent en matière de transmission.",
        "Le choix doit être cohérent avec la stratégie patrimoniale globale.",
    ],
    client_questions=[
        "Quelle est la différence entre un contrat de capitalisation et une assurance-vie ?",
        "Pourquoi choisir un contrat de capitalisation ?",
        "Peut-on transmettre un contrat de capitalisation ?",
        "Lequel est le plus adapté à mon patrimoine ?",
    ],
    client_objections=[
        "Je ne connais pas le contrat de capitalisation.",
        "L'assurance-vie me semble plus simple.",
        "Je pensais que c'était exactement le même produit.",
    ],
    client_fears=[
        "Choisir la mauvaise enveloppe.",
        "Ne pas optimiser la transmission.",
        "Passer à côté d'une solution patrimoniale adaptée.",
    ],
    client_goals=[
        "Structurer son patrimoine.",
        "Préparer une transmission.",
        "Diversifier ses enveloppes patrimoniales.",
        "Choisir la solution la plus adaptée à ses objectifs.",
    ],
    client_intents=[
        "contrat de capitalisation ou assurance-vie",
        "comparaison contrat de capitalisation",
        "transmission patrimoine",
        "placement patrimonial",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_comparaison_scpi",
        "assurance_vie_comparaison_luxembourg",
        "assurance_vie_transmission_principe_general",
        "assurance_vie_clause_beneficiaire_definition",
    ],
    prerequisites=[
        "assurance_vie_transmission_principe_general",
    ],
    next_topics=[
        "assurance_vie_comparaison_luxembourg",
    ],
),

Topic(
    id="assurance_vie_comparaison_luxembourg",
    title="Assurance-vie française ou luxembourgeoise : quelles différences ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre les principales différences entre une assurance-vie française et une assurance-vie luxembourgeoise afin d'identifier les situations dans lesquelles chacune peut être pertinente.",
    objective="Expliquer que l'assurance-vie luxembourgeoise répond principalement à des besoins patrimoniaux spécifiques et ne constitue pas systématiquement une alternative supérieure à une assurance-vie française.",
    difficulty="Avancé",
    priority=8,
    version=1,
    keywords=[
        "assurance-vie luxembourgeoise",
        "Luxembourg",
        "triangle de sécurité",
        "banque privée",
        "patrimoine",
        "comparaison",
        "expatriation",
        "gestion internationale",
    ],
    key_points=[
        "L'assurance-vie française et luxembourgeoise reposent sur le même principe d'enveloppe patrimoniale.",
        "L'assurance-vie luxembourgeoise est souvent utilisée dans des stratégies patrimoniales internationales ou pour des patrimoines importants.",
        "Le cadre réglementaire luxembourgeois prévoit des mécanismes spécifiques de protection des actifs des souscripteurs.",
        "L'univers d'investissement peut être plus large selon les contrats et les profils d'investisseurs.",
        "Le choix dépend du patrimoine, des objectifs, de la mobilité internationale et de la stratégie patrimoniale globale."
    ],
    examples=[
        "Julie, dirigeante d'entreprise, envisage de s'expatrier dans quelques années. Avec son conseiller, elle compare les avantages d'une assurance-vie française et luxembourgeoise afin d'anticiper la mobilité de son patrimoine.",

        "Marc possède un patrimoine financier conséquent réparti dans plusieurs pays. Il étudie une assurance-vie luxembourgeoise afin de centraliser une partie de ses investissements dans une enveloppe adaptée à sa situation internationale.",

        "Claire, résidente française, recherche simplement une solution pour préparer sa retraite et transmettre son patrimoine. Après comparaison, elle constate qu'une assurance-vie française répond pleinement à ses besoins."
    ],
    vocabulary=[
        "triangle de sécurité",
        "Luxembourg",
        "compagnie d'assurance",
        "dépositaire",
        "banque dépositaire",
        "expatriation",
        "gestion internationale",
        "banque privée",
    ],
    legal_sources=[
        "Code des assurances",
        "Réglementation luxembourgeoise applicable aux assurances",
        "Directive Solvabilité II",
    ],
    analogies=[
        "L'assurance-vie luxembourgeoise n'est pas une version 'premium' de l'assurance-vie française. C'est plutôt un véhicule conçu pour répondre à des situations patrimoniales plus spécifiques, notamment lorsque le patrimoine devient international ou particulièrement important."
    ],
    misconceptions=[
        "L'assurance-vie luxembourgeoise est toujours meilleure.",
        "Elle est réservée aux milliardaires.",
        "Elle permet d'échapper à la fiscalité française.",
        "Tout le monde devrait ouvrir une assurance-vie au Luxembourg."
    ],
    common_mistakes=[
        "Choisir une assurance-vie luxembourgeoise uniquement pour son image.",
        "Penser que le Luxembourg supprime les obligations fiscales françaises.",
        "Comparer uniquement les mécanismes de protection.",
        "Ignorer les coûts et les conditions d'accès selon les contrats."
    ],
    expert_tips=[
        "L'assurance-vie luxembourgeoise prend tout son sens lorsqu'elle répond à un véritable besoin patrimonial : mobilité internationale, patrimoine financier important, diversification des dépositaires ou accès à une architecture financière plus ouverte. En dehors de ces situations, une assurance-vie française peut parfaitement répondre aux objectifs recherchés."
    ],
    attention_points=[
        "Toutes les situations patrimoniales ne justifient pas une assurance-vie luxembourgeoise.",
        "Les conditions d'accès diffèrent selon les assureurs.",
        "Les aspects fiscaux doivent toujours être analysés en fonction de la résidence fiscale du souscripteur."
    ],
    client_questions=[
        "Pourquoi choisir une assurance-vie luxembourgeoise ?",
        "Qu'est-ce que le triangle de sécurité ?",
        "Est-elle plus sûre qu'une assurance-vie française ?",
        "À partir de quel patrimoine est-elle pertinente ?"
    ],
    client_objections=[
        "Je pensais que c'était réservé aux très grandes fortunes.",
        "On m'a dit qu'il fallait absolument investir au Luxembourg.",
        "Cela me semble beaucoup trop complexe."
    ],
    client_fears=[
        "Choisir une solution inadaptée.",
        "Passer à côté d'une meilleure protection.",
        "Complexifier inutilement son patrimoine."
    ],
    client_goals=[
        "Structurer un patrimoine important.",
        "Préparer une mobilité internationale.",
        "Diversifier les solutions patrimoniales.",
        "Comprendre les différences entre les deux enveloppes."
    ],
    client_intents=[
        "assurance-vie luxembourgeoise",
        "Luxembourg ou France",
        "triangle de sécurité",
        "comparaison assurance-vie"
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_comparaison_capitalisation",
        "assurance_vie_questions_faillite_assureur",
        "assurance_vie_cas_particuliers_expatriation",
        "assurance_vie_questions_pourquoi_assurance_vie",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[
        "assurance_vie_comparaison_quel_placement",
    ],
),

Topic(
    id="assurance_vie_comparaison_quel_placement",
    title="Quel placement choisir selon son objectif patrimonial ?",
    pillar="comparer",
    family="assurance_vie",
    chapter="comparaisons",
    description="Comprendre qu'il n'existe pas de placement universellement meilleur qu'un autre et que chaque solution patrimoniale répond à un objectif spécifique.",
    objective="Expliquer que le choix d'un placement dépend avant tout des objectifs, de l'horizon d'investissement, du niveau de risque accepté, des besoins de liquidité et de la situation patrimoniale du souscripteur.",
    difficulty="Intermédiaire",
    priority=10,
    version=1,
    keywords=[
        "placement",
        "comparaison",
        "objectif patrimonial",
        "assurance-vie",
        "PEA",
        "PER",
        "Livret A",
        "SCPI",
        "investissement",
        "patrimoine",
    ],
    key_points=[
        "Il n'existe pas de meilleur placement dans l'absolu.",
        "Chaque enveloppe répond à un objectif patrimonial particulier.",
        "Le choix dépend notamment de l'horizon d'investissement, de la fiscalité, de la liquidité et du niveau de risque accepté.",
        "Plusieurs placements peuvent être complémentaires au sein d'une même stratégie patrimoniale.",
        "Une stratégie efficace consiste souvent à combiner plusieurs enveloppes plutôt qu'à rechercher un produit unique."
    ],
    examples=[
        "Julie, 28 ans, souhaite constituer une épargne de précaution, préparer un achat immobilier dans quelques années et commencer à investir pour sa retraite. Plutôt que de rechercher un produit unique, elle répartit progressivement son épargne entre plusieurs solutions adaptées à chacun de ses objectifs.",

        "Marc, 55 ans, prépare sa retraite tout en souhaitant transmettre une partie de son patrimoine à ses enfants. Avec son conseiller, il combine différentes enveloppes afin de répondre simultanément à plusieurs besoins patrimoniaux.",

        "Claire, cheffe d'entreprise, vient de céder sa société. Son patrimoine ayant profondément évolué, elle construit une stratégie diversifiée intégrant plusieurs solutions d'investissement plutôt que de concentrer son capital sur un seul placement."
    ],
    vocabulary=[
        "objectif patrimonial",
        "allocation",
        "diversification",
        "horizon de placement",
        "liquidité",
        "risque",
        "enveloppe patrimoniale",
        "stratégie patrimoniale",
    ],
    legal_sources=[
        "Code monétaire et financier",
        "Code des assurances",
        "Code général des impôts",
    ],
    analogies=[
        "Choisir un placement revient à choisir un outil dans une boîte à outils : un marteau n'est pas meilleur qu'un tournevis. Tout dépend du travail que l'on souhaite réaliser."
    ],
    misconceptions=[
        "Il existe un placement meilleur que tous les autres.",
        "Il suffit de choisir le produit qui rapporte le plus.",
        "Un seul placement peut répondre à tous les besoins.",
        "Le meilleur placement est le même pour tout le monde.",
    ],
    common_mistakes=[
        "Choisir un placement uniquement pour son rendement.",
        "Construire son patrimoine autour d'un seul produit.",
        "Oublier les objectifs de transmission.",
        "Négliger son horizon d'investissement.",
        "Comparer uniquement la fiscalité.",
    ],
    expert_tips=[
        "La première question qu'un conseiller patrimonial se pose n'est jamais 'Quel produit choisir ?' mais 'Quel est votre objectif ?'. Une fois cet objectif clairement identifié, il devient beaucoup plus simple de sélectionner les enveloppes patrimoniales les plus pertinentes et de les combiner si nécessaire."
    ],
    attention_points=[
        "Les objectifs patrimoniaux évoluent au fil de la vie.",
        "Une stratégie patrimoniale doit être régulièrement réévaluée.",
        "La diversification reste un principe essentiel de gestion des risques.",
    ],
    client_questions=[
        "Quel est le meilleur placement aujourd'hui ?",
        "Comment choisir entre plusieurs solutions ?",
        "Puis-je cumuler plusieurs placements ?",
        "Par où commencer lorsque je souhaite investir ?",
    ],
    client_objections=[
        "Je voudrais simplement savoir quel est le meilleur produit.",
        "Je ne veux pas multiplier les placements.",
        "Toutes ces solutions me semblent trop complexes.",
    ],
    client_fears=[
        "Faire le mauvais choix.",
        "Passer à côté d'une meilleure opportunité.",
        "Construire une stratégie inadaptée.",
    ],
    client_goals=[
        "Construire une stratégie patrimoniale cohérente.",
        "Diversifier son patrimoine.",
        "Préparer plusieurs projets de vie.",
        "Faire des choix adaptés à ses objectifs.",
    ],
    client_intents=[
        "meilleur placement",
        "quel placement choisir",
        "comparer les placements",
        "où investir son argent",
    ],
    recommended_formats=[
        "instagram_reel",
        "carrousel",
        "faq",
        "article",
    ],
    related_topics=[
        "assurance_vie_comparaison_livret_a",
        "assurance_vie_comparaison_pea",
        "assurance_vie_comparaison_per",
        "assurance_vie_comparaison_compte_titres",
        "assurance_vie_comparaison_scpi",
        "assurance_vie_comparaison_capitalisation",
        "assurance_vie_comparaison_luxembourg",
    ],
    prerequisites=[
        "assurance_vie_fondamentaux_definition",
    ],
    next_topics=[],
),

