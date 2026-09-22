from v2.studio.models.brand_strategy import (
    AIProfile,
    AudienceLevel,
    AudienceProfile,
    AudienceSegment,
    BrandStrategy,
    BusinessGoals,
    CreatorType,
    EditorialArchetype,
    EditorialIdentity,
    EditorialPreferences,
    Identity,
    Platform,
    PublishingProfile,
    ToneProfile,
)


EXAMPLE_BRAND_STRATEGY = BrandStrategy(
    id="leveria_cgp_default",
    name="Leveria - Stratégie éditoriale CGP",
    description="Stratégie éditoriale pour un cabinet de gestion de patrimoine pédagogique et premium.",
    identity=Identity(
        creator_type=CreatorType.CGP,
        business_name="Leveria",
        activity="Conseil en gestion de patrimoine",
        location="France",
    ),
    editorial_identity=EditorialIdentity(
        archetype=EditorialArchetype.PEDAGOGUE,
        positioning="Conseil patrimonial pédagogique, rigoureux et accessible.",
        promise="Rendre les décisions patrimoniales plus compréhensibles.",
        values=[
            "pédagogie",
            "rigueur",
            "neutralité",
            "clarté",
        ],
    ),
    business_goals=BusinessGoals(
        notoriety=30,
        authority=30,
        acquisition=30,
        loyalty=10,
    ),
    audience=AudienceProfile(
        segments=[
            AudienceSegment.ENTREPRENEUR,
            AudienceSegment.FAMILY,
            AudienceSegment.HNWI,
        ],
        level=AudienceLevel.INTERMEDIATE,
        language="fr",
    ),
    tone=ToneProfile(
        pedagogy=95,
        expertise=85,
        storytelling=70,
        emotion=25,
        humour=5,
        provocation=5,
    ),
    publishing=PublishingProfile(
        platforms=[
            Platform.INSTAGRAM,
            Platform.LINKEDIN,
        ],
        posts_per_week=3,
        duration_weeks=12,
    ),
    preferences=EditorialPreferences(
        preferred_families=[
            "assurance_vie",
        ],
        preferred_chapters=[
            "questions_clients",
            "comparaisons",
            "erreurs",
            "cas_particuliers",
        ],
    ),
    ai_profile=AIProfile(
        avoid_clickbait=True,
        always_use_examples=True,
        never_give_personal_advice=True,
        explain_with_nuance=True,
        preferred_length="medium",
    ),
)
