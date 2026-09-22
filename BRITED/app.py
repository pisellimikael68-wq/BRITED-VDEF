import streamlit as st

from v2.core.factory import PipelineFactory
from v2.ui.sidebar import render_sidebar
from v2.ui.result import render_result


# ==========================================
# Configuration
# ==========================================

st.set_page_config(
    page_title="BRITED Studio",
    page_icon="🏛️",
    layout="wide",
)


# ==========================================
# Interface
# ==========================================

platform, subject, generate = render_sidebar()

st.title("🏛️ BRITED Studio")
st.caption("Le moteur IA de génération de contenu patrimonial")

st.divider()


# ==========================================
# Génération
# ==========================================

if generate:

    if not subject:

        st.warning("Veuillez saisir un sujet.")

    else:

        with st.spinner("Génération en cours..."):

            pipeline = PipelineFactory.create(platform)

            context = pipeline.run(subject)

        render_result(context)

else:

    st.info(
        "👈 Choisissez une plateforme, saisissez un sujet puis cliquez sur **Générer**."
    )