from v2.models.knowledge_models import Topic


FONCTIONNEMENT_TOPICS: list[Topic] = [
    Topic(
        id="assurance_vie_fonctionnement_ouverture_contrat",
        title="Comment ouvrir une assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        chapter="fonctionnement",
        description="Comprendre les étapes d'ouverture d'un contrat d'assurance-vie.",
        objective="Expliquer le parcours de souscription d'une assurance-vie, de la demande jusqu'à l'ouverture effective du contrat.",
        difficulty="Débutant",
        priority=10,
        editorial_order=1,
        keywords=[
            "ouverture",
            "souscription",
            "contrat",
            "assureur",
            "versement initial",
            "signature",
            "adhésion",
        ],
        misconceptions=[
            "Ouvrir une assurance-vie est compliqué.",
            "Il faut être riche pour ouvrir un contrat.",
            "L'ouverture prend plusieurs semaines.",
        ],
        client_questions=[
            "Comment ouvrir une assurance-vie ?",
            "Combien de temps faut-il ?",
            "Puis-je ouvrir mon contrat en ligne ?",
            "Faut-il obligatoirement rencontrer un conseiller ?",
        ],
        common_mistakes=[
            "Choisir un contrat uniquement en fonction de la banque.",
            "Ne pas comparer les frais.",
            "Ne pas définir son objectif avant la souscription.",
            "Signer sans lire les conditions du contrat.",
        ],
        analogies=[
            "Ouvrir une assurance-vie revient à ouvrir une enveloppe dans laquelle on placera ensuite différents investissements.",
        ],
        key_points=[
            "La souscription peut être réalisée en agence ou à distance.",
            "Un bulletin de souscription est signé.",
            "Le contrat est ouvert auprès d'un assureur.",
            "Un premier versement est généralement demandé.",
            "Le contrat entre en vigueur après acceptation par l'assureur.",
        ],
        examples=[
            "Julie ouvre un contrat en ligne avec un premier versement de 500 €.",
            "Marc souscrit une assurance-vie auprès de son conseiller patrimonial.",
        ],
        vocabulary=[
            "bulletin de souscription",
            "assureur",
            "souscripteur",
            "adhésion",
            "versement initial",
        ],
        recommended_formats=[
            "FAQ",
            "Carrousel",
            "Question client",
            "Guide pratique",
        ],
        legal_sources=[
            "Code des assurances",
        ],
        related_topics=[
            "assurance_vie_fonctionnement_documents",
            "assurance_vie_fonctionnement_devoir_conseil",
            "assurance_vie_fondamentaux_definition",
        ],
    ),

    Topic(
        id="assurance_vie_fonctionnement_documents",
        title="Quels documents sont nécessaires pour ouvrir une assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        chapter="fonctionnement",
        description="Identifier les justificatifs demandés lors de la souscription.",
        objective="Expliquer les obligations réglementaires liées à l'identification du souscripteur.",
        difficulty="Débutant",
        priority=9,
        editorial_order=2,
        keywords=[
            "documents",
            "pièce d'identité",
            "justificatif de domicile",
            "RIB",
            "LCB-FT",
            "conformité",
        ],
        misconceptions=[
            "Une simple carte bancaire suffit.",
            "Les justificatifs sont facultatifs.",
            "Tous les assureurs demandent les mêmes documents sans exception.",
        ],
        client_questions=[
            "Quels papiers dois-je fournir ?",
            "Pourquoi l'assureur demande-t-il autant de documents ?",
            "Puis-je ouvrir un contrat sans justificatif de domicile ?",
        ],
        common_mistakes=[
            "Fournir des documents expirés.",
            "Oublier le justificatif d'identité.",
            "Ne pas comprendre les contrôles liés à la lutte contre le blanchiment.",
        ],
        analogies=[
            "Comme pour ouvrir un compte bancaire, l'assureur doit vérifier l'identité du client.",
        ],
        key_points=[
            "Une pièce d'identité valide est exigée.",
            "Un justificatif de domicile est généralement demandé.",
            "Un RIB est nécessaire pour les versements et rachats.",
            "L'assureur peut demander des informations sur l'origine des fonds.",
            "Ces contrôles répondent aux obligations réglementaires de conformité.",
        ],
        examples=[
            "Claire transmet sa carte d'identité, un justificatif de domicile et un RIB lors de sa souscription.",
            "L'assureur demande des précisions sur l'origine d'un versement exceptionnel de 300 000 €.",
        ],
        vocabulary=[
            "KYC",
            "LCB-FT",
            "justificatif",
            "origine des fonds",
            "RIB",
        ],
        recommended_formats=[
            "FAQ",
            "Checklist",
            "Carrousel",
        ],
        legal_sources=[
            "Code des assurances",
            "Code monétaire et financier",
        ],
        related_topics=[
            "assurance_vie_fonctionnement_ouverture_contrat",
            "assurance_vie_fonctionnement_devoir_conseil",
        ],
    ),
]
