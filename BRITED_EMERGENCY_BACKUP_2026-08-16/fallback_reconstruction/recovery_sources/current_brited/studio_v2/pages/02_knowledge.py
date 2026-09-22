import streamlit as st

from v2.knowledge.registry import KnowledgeRegistry

# ==========================================================
# DATA
# ==========================================================

registry = KnowledgeRegistry()

topics = registry.topics

families = sorted({t.family for t in topics})

# ==========================================================
# HEADER
# ==========================================================

st.title("📚 Knowledge Explorer")

st.caption("Explorez toute la base de connaissances BRITED")

st.divider()

# ==========================================================
# FAMILY
# ==========================================================

family = st.selectbox(

    "Famille",

    families,

)

family_topics = registry.get_topics_by_family(family)

titles = [topic.title for topic in family_topics]

title = st.selectbox(

    "Topic",

    titles,

)

topic = next(

    t

    for t in family_topics

    if t.title == title

)

# ==========================================================
# INFORMATIONS
# ==========================================================

st.divider()

st.header(topic.title)

col1, col2, col3 = st.columns(3)

col1.metric("Priorité", topic.priority)

col2.metric("Ordre", topic.editorial_order)

col3.metric("Version", topic.version)

st.write("### Description")

st.write(topic.description)

st.write("### Objectif")

st.write(topic.objective)

st.write("### Difficulté")

st.write(topic.difficulty)

# ==========================================================
# KEYWORDS
# ==========================================================

with st.expander("Mots-clés"):

    st.write(topic.keywords)

with st.expander("Points clés"):

    st.write(topic.key_points)

with st.expander("Exemples"):

    st.write(topic.examples)

with st.expander("Vocabulaire"):

    st.write(topic.vocabulary)

with st.expander("Erreurs fréquentes"):

    st.write(topic.common_mistakes)

with st.expander("Idées reçues"):

    st.write(topic.misconceptions)

with st.expander("Questions clients"):

    st.write(topic.client_questions)

with st.expander("Sources juridiques"):

    st.write(topic.legal_sources)

# ==========================================================
# NAVIGATION
# ==========================================================

st.divider()

st.write("### Navigation")

st.write("Prérequis")

st.write(topic.prerequisites)

st.write("Topics liés")

st.write(topic.related_topics)

st.write("Topics suivants")

st.write(topic.next_topics)
