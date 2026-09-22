import streamlit as st

# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="BRITED Studio",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🏛️ BRITED Studio")

st.caption(
    "Editorial Intelligence Platform"
)

st.divider()

st.success(
    "Bienvenue dans BRITED Studio V2."
)

st.markdown(
    """
Cette nouvelle version est construite autour du Framework BRITED.

Utilisez le menu de gauche pour naviguer dans les différents modules.
"""
)