from v2.models.knowledge_models import Family


FAMILIES = [

    # ==========================================================
    # ÉPARGNER
    # ==========================================================

    Family(
        id="assurance_vie",
        title="Assurance-vie",
        pillar="epargner",
        description="Utiliser l'assurance-vie comme outil d'épargne, d'investissement et de transmission.",
    ),

    Family(
        id="livrets",
        title="Livrets d'épargne",
        pillar="epargner",
        description="Comprendre les différents livrets réglementés et bancaires.",
    ),

    Family(
        id="pea",
        title="PEA",
        pillar="epargner",
        description="Plan d'Épargne en Actions.",
    ),

    Family(
        id="compte_titres",
        title="Compte-titres",
        pillar="epargner",
        description="Investir librement sur les marchés financiers.",
    ),

    # ==========================================================
    # INVESTIR
    # ==========================================================

    Family(
        id="actions",
        title="Actions",
        pillar="investir",
        description="Investir en actions.",
    ),

    Family(
        id="obligations",
        title="Obligations",
        pillar="investir",
        description="Investir en obligations.",
    ),

    Family(
        id="private_equity",
        title="Private Equity",
        pillar="investir",
        description="Investir dans des entreprises non cotées.",
    ),

    Family(
        id="produits_structures",
        title="Produits structurés",
        pillar="investir",
        description="Comprendre les produits structurés.",
    ),

    # ==========================================================
    # IMMOBILIER
    # ==========================================================

    Family(
        id="sci",
        title="SCI",
        pillar="immobilier",
        description="Sociétés Civiles Immobilières.",
    ),

    Family(
        id="lmnp",
        title="LMNP",
        pillar="immobilier",
        description="Location Meublée Non Professionnelle.",
    ),

    Family(
        id="scpi",
        title="SCPI",
        pillar="immobilier",
        description="Sociétés Civiles de Placement Immobilier.",
    ),

    Family(
        id="investissement_locatif",
        title="Investissement locatif",
        pillar="immobilier",
        description="Construire un patrimoine immobilier locatif.",
    ),

    # ==========================================================
    # TRANSMISSION
    # ==========================================================

    Family(
        id="donations",
        title="Donations",
        pillar="transmettre",
        description="Préparer la transmission de son vivant.",
    ),

    Family(
        id="successions",
        title="Successions",
        pillar="transmettre",
        description="Comprendre les règles successorales.",
    ),

    Family(
        id="demembrement",
        title="Démembrement",
        pillar="transmettre",
        description="Usufruit et nue-propriété.",
    ),

    Family(
        id="pacte_dutreil",
        title="Pacte Dutreil",
        pillar="transmettre",
        description="Transmission d'entreprise.",
    ),

    # ==========================================================
    # FISCALITÉ
    # ==========================================================

    Family(
        id="impot_revenu",
        title="Impôt sur le revenu",
        pillar="optimiser_fiscalite",
        description="Comprendre l'impôt sur le revenu.",
    ),

    Family(
        id="ifi",
        title="IFI",
        pillar="optimiser_fiscalite",
        description="Impôt sur la Fortune Immobilière.",
    ),

    Family(
        id="plus_values",
        title="Plus-values",
        pillar="optimiser_fiscalite",
        description="Fiscalité des plus-values.",
    ),

    Family(
        id="fiscalite_epargne",
        title="Fiscalité de l'épargne",
        pillar="optimiser_fiscalite",
        description="Fiscalité des placements financiers.",
    ),

]
