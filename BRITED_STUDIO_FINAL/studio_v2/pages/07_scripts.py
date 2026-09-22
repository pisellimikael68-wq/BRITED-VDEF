import streamlit as st

from v2.knowledge.registry import KnowledgeRegistry

from v2.studio.engines.angle_engine import AngleEngine
from v2.studio.engines.publication_engine import PublicationEngine
from v2.studio.engines.script_engine import ScriptEngine


# ==========================================================
# HEADER
# ==========================================================

st.title("✍️ Générateur de scripts")

st.caption("Production de contenus BRITED")

st.divider()


# ==========================================================
# CHOIX DU TOPIC
# ==========================================================

registry = KnowledgeRegistry()

families = sorted({t.family for t in registry.topics})

family = st.selectbox(
    "Famille",
    families,
)

topics = registry.get_topics_by_family(family)

topic = st.selectbox(
    "Sujet",
    topics,
    format_func=lambda t: t.title,
)

st.divider()


# ==========================================================
# GENERATION
# ==========================================================

if st.button("🚀 Générer le script"):

    publication = PublicationEngine().generate(topic)

    script = ScriptEngine().generate(publication)

    angle = AngleEngine().select(topic)

    st.success("Script généré")

    st.subheader("🎯 Angle éditorial")

    st.code(angle.value)

    st.subheader("📰 Titre")

    st.write(script.title)

    st.subheader("🎣 Hook")

    st.info(script.hook)

    st.subheader("📝 Contenu")

    for section in script.sections:

        st.markdown(f"### {section.title}")

        if isinstance(section.content, list):

            for item in section.content:

                st.write(f"• {item}")

        else:

            st.write(section.content)

    st.subheader("🎬 Conclusion")

    st.write(script.conclusion)

    st.subheader("📣 CTA")

    st.success(script.call_to_action)

    st.subheader("⚖️ Sources")

    for source in script.sources:

        st.write(f"• {source}")

    st.divider()

    st.download_button(

        label="📥 Télécharger en Markdown",

        data=str(script),

        file_name="script.md",

        mime="text/markdown",

    )
    