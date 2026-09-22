from v2.models.knowledge_models import Topic


ASSURANCE_VIE_TOPICS = [

    # ==========================================================
    # ASSURANCE-VIE — FONDAMENTAUX
    # ==========================================================

    Topic(
        id="assurance_vie_definition",
        title="Qu'est-ce qu'une assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        description="Comprendre la nature juridique et patrimoniale de l'assurance-vie.",
        objective="Expliquer que l'assurance-vie est un contrat d'épargne, d'investissement et de transmission.",
        difficulty="Débutant",
        priority=10,
        keywords=[
            "assurance-vie",
            "contrat",
            "épargne",
            "transmission",
        ],
        misconceptions=[
            "L'assurance-vie est une assurance décès.",
            "L'assurance-vie sert uniquement à transmettre.",
        ],
        client_questions=[
            "À quoi sert vraiment une assurance-vie ?",
            "Est-ce un placement ou une assurance ?",
        ],
        common_mistakes=[
            "Confondre assurance-vie et assurance décès.",
            "Réduire l'assurance-vie à un simple produit bancaire.",
        ],
        analogies=[
            "Un cadre souple qui peut accueillir plusieurs types de placements.",
        ],
        recommended_formats=[
            "Idée reçue",
            "Question client",
            "Définition simple",
        ],
    ),

    Topic(
        id="assurance_vie_vs_assurance_deces",
        title="Assurance-vie ou assurance décès : quelle différence ?",
        pillar="epargner",
        family="assurance_vie",
        description="Distinguer deux contrats souvent confondus.",
        objective="Montrer que l'assurance-vie peut servir de son vivant, contrairement à l'assurance décès.",
        difficulty="Débutant",
        priority=10,
        keywords=[
            "assurance décès",
            "assurance-vie",
            "capital décès",
            "épargne",
        ],
        misconceptions=[
            "L'assurance-vie ne sert qu'en cas de décès.",
            "Assurance-vie et assurance décès sont la même chose.",
        ],
        client_questions=[
            "Mes proches touchent-ils forcément quelque chose ?",
            "Puis-je utiliser mon assurance-vie de mon vivant ?",
        ],
        common_mistakes=[
            "Croire que le capital est versé uniquement au décès.",
        ],
        analogies=[
            "L'assurance décès protège surtout les proches ; l'assurance-vie peut aussi accompagner les projets de l'épargnant.",
        ],
        recommended_formats=[
            "Comparaison",
            "Mythe/Réalité",
            "Question client",
        ],
    ),

    Topic(
        id="assurance_vie_utilites",
        title="À quoi sert une assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        description="Présenter les grands usages de l'assurance-vie.",
        objective="Montrer que l'assurance-vie peut servir à épargner, investir, transmettre ou préparer un projet.",
        difficulty="Débutant",
        priority=10,
        keywords=[
            "épargne",
            "projet",
            "retraite",
            "transmission",
            "fiscalité",
        ],
        misconceptions=[
            "L'assurance-vie sert uniquement à transmettre.",
            "L'assurance-vie est réservée aux personnes âgées.",
        ],
        client_questions=[
            "Pourquoi ouvrir une assurance-vie ?",
            "Est-ce utile si je suis jeune ?",
        ],
        common_mistakes=[
            "N'utiliser l'assurance-vie que comme outil successoral.",
        ],
        analogies=[
            "Un couteau suisse patrimonial, à condition de comprendre ses règles.",
        ],
        recommended_formats=[
            "Liste pédagogique",
            "Cas pratique",
            "Carrousel",
        ],
    ),

    Topic(
        id="assurance_vie_accessibilite",
        title="L'assurance-vie est-elle réservée aux gros patrimoines ?",
        pillar="epargner",
        family="assurance_vie",
        description="Expliquer que l'assurance-vie est accessible à des profils très variés.",
        objective="Déconstruire l'idée selon laquelle l'assurance-vie serait réservée aux patrimoines importants.",
        difficulty="Débutant",
        priority=9,
        keywords=[
            "accessibilité",
            "petite épargne",
            "patrimoine",
            "versements",
        ],
        misconceptions=[
            "Il faut être riche pour ouvrir une assurance-vie.",
            "L'assurance-vie n'a d'intérêt qu'à partir d'un gros capital.",
        ],
        client_questions=[
            "Puis-je ouvrir une assurance-vie avec un petit montant ?",
            "Est-ce utile si j'épargne progressivement ?",
        ],
        common_mistakes=[
            "Attendre d'avoir un capital important avant d'ouvrir un contrat.",
        ],
        analogies=[
            "Un contenant patrimonial que l'on peut alimenter progressivement.",
        ],
        recommended_formats=[
            "Idée reçue",
            "Question client",
            "Cas pratique",
        ],
    ),

    Topic(
        id="assurance_vie_nombre_contrats",
        title="Peut-on avoir plusieurs contrats d'assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        description="Comprendre la possibilité de détenir plusieurs contrats d'assurance-vie.",
        objective="Expliquer qu'il est possible d'avoir plusieurs contrats, avec des objectifs différents.",
        difficulty="Débutant",
        priority=9,
        keywords=[
            "plusieurs contrats",
            "diversification",
            "assureur",
            "allocation",
        ],
        misconceptions=[
            "On ne peut avoir qu'une seule assurance-vie.",
            "Avoir plusieurs contrats est inutile.",
        ],
        client_questions=[
            "Puis-je ouvrir une deuxième assurance-vie ?",
            "Pourquoi certains épargnants ont plusieurs contrats ?",
        ],
        common_mistakes=[
            "Concentrer toute son épargne sur un seul contrat sans réflexion.",
        ],
        analogies=[
            "Comme avoir plusieurs enveloppes pour différents projets.",
        ],
        recommended_formats=[
            "Question client",
            "Erreur fréquente",
            "Comparaison",
        ],
    ),

    Topic(
        id="assurance_vie_age_ouverture",
        title="À quel âge ouvrir une assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        description="Comprendre l'intérêt de l'ancienneté fiscale du contrat.",
        objective="Expliquer pourquoi l'âge du contrat peut compter, sans inciter systématiquement à l'ouverture.",
        difficulty="Débutant",
        priority=9,
        keywords=[
            "âge",
            "ancienneté fiscale",
            "8 ans",
            "ouverture",
        ],
        misconceptions=[
            "Il faut attendre d'avoir beaucoup d'argent pour ouvrir une assurance-vie.",
            "L'assurance-vie ne sert qu'à la retraite.",
        ],
        client_questions=[
            "Est-ce trop tôt pour ouvrir une assurance-vie ?",
            "L'ancienneté du contrat est-elle importante ?",
        ],
        common_mistakes=[
            "Confondre ancienneté fiscale et obligation de versement important.",
        ],
        analogies=[
            "Ouvrir un contrat, c'est démarrer un compteur fiscal.",
        ],
        recommended_formats=[
            "Question client",
            "Idée reçue",
            "Cas pratique",
        ],
    ),

    Topic(
        id="assurance_vie_argent_bloque",
        title="L'argent est-il bloqué en assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        description="Déconstruire l'idée selon laquelle l'épargne serait bloquée pendant 8 ans.",
        objective="Expliquer la différence entre disponibilité des fonds et fiscalité du contrat.",
        difficulty="Débutant",
        priority=10,
        keywords=[
            "argent bloqué",
            "8 ans",
            "rachat",
            "disponibilité",
        ],
        misconceptions=[
            "L'argent est bloqué pendant 8 ans.",
            "Retirer avant 8 ans est interdit.",
        ],
        client_questions=[
            "Puis-je retirer mon argent avant 8 ans ?",
            "Que se passe-t-il si j'ai besoin de liquidités ?",
        ],
        common_mistakes=[
            "Confondre avantage fiscal après 8 ans et blocage des fonds.",
        ],
        analogies=[
            "La porte reste ouverte, mais la fiscalité change selon le moment où l'on sort.",
        ],
        recommended_formats=[
            "Idée reçue",
            "Mythe/Réalité",
            "Cas pratique",
        ],
    ),

    Topic(
        id="assurance_vie_fiscalite_8_ans",
        title="Pourquoi parle-t-on des 8 ans en assurance-vie ?",
        pillar="epargner",
        family="assurance_vie",
        description="Comprendre la portée fiscale du seuil des 8 ans.",
        objective="Clarifier que les 8 ans concernent la fiscalité des gains, pas la disponibilité de l'épargne.",
        difficulty="Débutant",
        priority=10,
        keywords=[
            "8 ans",
            "fiscalité",
            "abattement",
            "rachat",
        ],
        misconceptions=[
            "Il ne faut jamais retirer avant 8 ans.",
            "Le contrat devient utile uniquement après 8 ans.",
        ],
        client_questions=[
            "Que change vraiment le cap des 8 ans ?",
            "Est-ce grave de retirer avant 8 ans ?",
        ],
        common_mistakes=[
            "Présenter les 8 ans comme une durée de blocage.",
        ],
        analogies=[
            "Les 8 ans ne ferment pas la porte avant : ils changent seulement les conditions fiscales après.",
        ],
        recommended_formats=[
            "Question client",
            "Explication simple",
            "Erreur fréquente",
        ],
    ),

    Topic(
        id="assurance_vie_pour_enfant",
        title="Peut-on ouvrir une assurance-vie pour un enfant ?",
        pillar="epargner",
        family="assurance_vie",
        description="Comprendre les principes d'une assurance-vie ouverte au nom d'un mineur.",
        objective="Expliquer l'intérêt patrimonial et les précautions liées à l'ouverture pour un enfant.",
        difficulty="Intermédiaire",
        priority=8,
        keywords=[
            "mineur",
            "enfant",
            "parents",
            "épargne familiale",
        ],
        misconceptions=[
            "Un enfant ne peut pas avoir d'assurance-vie.",
            "Les parents peuvent toujours utiliser librement l'argent placé au nom de l'enfant.",
        ],
        client_questions=[
            "Puis-je ouvrir un contrat pour mon enfant ?",
            "Qui gère le contrat jusqu'à sa majorité ?",
        ],
        common_mistakes=[
            "Oublier que l'argent appartient juridiquement à l'enfant.",
        ],
        analogies=[
            "Une épargne construite pour l'enfant, mais gérée par ses représentants légaux jusqu'à sa majorité.",
        ],
        recommended_formats=[
            "Question client",
            "Cas pratique",
            "Point de vigilance",
        ],
    ),

    Topic(
        id="assurance_vie_solution_universelle",
        title="L'assurance-vie est-elle toujours la meilleure solution ?",
        pillar="epargner",
        family="assurance_vie",
        description="Nuancer l'idée selon laquelle l'assurance-vie conviendrait à toutes les situations.",
        objective="Montrer que l'assurance-vie est un outil puissant mais pas une solution universelle.",
        difficulty="Débutant",
        priority=9,
        keywords=[
            "solution universelle",
            "objectif patrimonial",
            "profil",
            "horizon",
        ],
        misconceptions=[
            "L'assurance-vie est toujours le meilleur placement.",
            "Tout le monde devrait avoir la même stratégie.",
        ],
        client_questions=[
            "L'assurance-vie est-elle adaptée à mon projet ?",
            "Quels sont ses avantages et ses limites ?",
        ],
        common_mistakes=[
            "Choisir l'assurance-vie sans définir son objectif patrimonial.",
        ],
        analogies=[
            "Un bon outil n'est utile que s'il correspond au bon besoin.",
        ],
        recommended_formats=[
            "Nuance pédagogique",
            "Erreur fréquente",
            "Question client",
        ],
    ),

]