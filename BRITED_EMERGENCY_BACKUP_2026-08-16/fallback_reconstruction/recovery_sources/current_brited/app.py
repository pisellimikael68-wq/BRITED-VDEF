import streamlit as st

from v2.core.factory import PipelineFactory


# ==========================================
# Configuration
# ==========================================

st.set_page_config(
    page_title="BRITED Studio",
    page_icon="🏛️",
    layout="wide",
)


# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.title("🏛️ BRITED")

    st.caption("Studio IA patrimonial")

    st.divider()

    st.subheader("Nouvelle génération")

    platform = st.selectbox(
        "Plateforme",
        [
            "instagram",
        ],
    )

    subject = st.text_input(
        "Sujet",
        placeholder="Ex : Assurance-vie",
    )

    generate = st.button(
        "🚀 Générer",
        use_container_width=True,
    )

    st.divider()

    st.subheader("🚧 Bientôt")

    st.write("• Historique")
    st.write("• Dashboard")
    st.write("• Statistiques")
    st.write("• LinkedIn")
    st.write("• Newsletter")


# ==========================================
# Header
# ==========================================

st.title("🏛️ BRITED Studio")

st.caption(
    "Le moteur IA de génération de contenu patrimonial"
)

st.divider()


# ==========================================
# Résultat
# ==========================================

if generate:

    if not subject:

        st.warning("Veuillez saisir un sujet.")

    else:

        with st.spinner("Génération en cours..."):

            pipeline = PipelineFactory.create(platform)

            context = pipeline.run(subject)

        st.success("Contenu généré avec succès")

        col1, col2 = st.columns([3, 1])

        with col1:

            st.subheader("🏷️ Titre")
            st.write(context.script.title)

        with col2:

            st.metric(
                "Score qualité",
                f"{context.review.score}/100",
            )

        st.divider()

        st.subheader("🎣 Hook")
        st.write(context.script.hook)

        st.divider()

        st.subheader("📝 Script")
        st.write(context.script.body)

        st.divider()

        st.subheader("📣 CTA")
        st.write(context.script.cta)

else:

    st.info(
        "👈 Choisissez une plateforme, saisissez un sujet puis cliquez sur **Générer**."
    )
    