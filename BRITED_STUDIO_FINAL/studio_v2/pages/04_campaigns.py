import streamlit as st

from studio_v2.services.campaign_service import CampaignService

from v2.studio.models.campaign import (
    Campaign,
    CampaignGoal,
    CampaignIntent,
    CampaignScope,
    CampaignStatus,
    CampaignType,
)

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
    Identity,
    Platform,
    PublishingProfile,
    ToneProfile,
)


def build_default_strategy() -> BrandStrategy:
    return BrandStrategy(
        id="brited_default",
        name="BRITED",
        description="Stratégie éditoriale neutre pour contenus patrimoniaux.",
        identity=Identity(
            creator_type=CreatorType.OTHER,
            business_name=None,
            activity="Création de contenu patrimonial",
        ),
        editorial_identity=EditorialIdentity(
            archetype=EditorialArchetype.PEDAGOGUE,
            positioning="Pédagogie patrimoniale claire, neutre et accessible.",
            promise="Expliquer les sujets patrimoniaux sans conseil personnalisé.",
            values=["pédagogie", "rigueur", "neutralité"],
        ),
        business_goals=BusinessGoals(
            notoriety=25,
            authority=50,
            acquisition=0,
            loyalty=25,
        ),
        audience=AudienceProfile(
            segments=[AudienceSegment.GENERAL_PUBLIC],
            level=AudienceLevel.BEGINNER,
        ),
        tone=ToneProfile(),
        publishing=PublishingProfile(
            platforms=[Platform.INSTAGRAM],
            posts_per_week=3,
            duration_weeks=8,
        ),
        ai_profile=AIProfile(),
    )


st.title("🎯 Campagnes")

st.caption("Créer une campagne complète avec calendrier et scripts")

st.divider()

campaign_name = st.text_input(
    "Nom de la campagne",
    value="Assurance-vie Evergreen",
)

family = st.text_input(
    "Famille",
    value="assurance_vie",
)

duration_weeks = st.slider(
    "Durée",
    min_value=1,
    max_value=12,
    value=8,
)

st.info("Pour l’instant, BRITED génère 3 publications par semaine.")

if st.button("🚀 Créer la campagne"):

    campaign = Campaign(
        id=campaign_name.lower().replace(" ", "_"),
        name=campaign_name,
        description=f"Campagne éditoriale sur {family}",
        strategy=build_default_strategy(),
        campaign_type=CampaignType.EVERGREEN,
        intent=CampaignIntent.EDUCATE,
        goal=CampaignGoal(
            title="Créer une campagne de contenus",
            description="Générer un calendrier éditorial et les scripts associés.",
        ),
        scope=CampaignScope(
            families=[family],
        ),
        duration_weeks=duration_weeks,
        status=CampaignStatus.DRAFT,
    )

    with st.spinner("Génération de la campagne en cours..."):

        bundle = CampaignService().create(campaign)

        st.session_state["current_bundle"] = bundle

    st.success(
        f"Campagne créée : {len(bundle.scripts)} scripts générés."
    )

if "current_bundle" in st.session_state:

    bundle = st.session_state["current_bundle"]

    st.divider()

    st.header("📅 Calendrier généré")

    script_index = 0

    for week in bundle.planning.weeks:

        st.subheader(f"Semaine {week.week}")

        for topic in week.topics:

            script = bundle.scripts[script_index]

            with st.expander(f"{topic.title}"):

                st.write(f"**Chapitre :** {topic.chapter}")
                st.write(f"**Difficulté :** {topic.difficulty}")

                st.markdown("### Script")

                st.markdown(f"**Hook :** {script.hook}")

                for section in script.sections:
                    st.markdown(f"#### {section.title}")
                    st.write(section.content)

                st.markdown("#### Conclusion")
                st.write(script.conclusion)

                st.markdown("#### CTA")
                st.write(script.call_to_action)

            script_index += 1

            