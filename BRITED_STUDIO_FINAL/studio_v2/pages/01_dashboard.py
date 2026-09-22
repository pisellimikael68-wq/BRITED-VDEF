import streamlit as st

from v2.knowledge.registry import KnowledgeRegistry

# ==========================================================
# DATA
# ==========================================================

registry = KnowledgeRegistry()

topics = registry.topics

families = sorted({t.family for t in topics})
chapters = sorted({t.chapter for t in topics})
pillars = sorted({t.pillar for t in topics})

# ==========================================================
# HEADER
# ==========================================================

st.title("🏛 Dashboard")

st.caption("Vue d'ensemble du Framework BRITED")

st.divider()

# ==========================================================
# METRICS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Topics",
    len(topics),
)

col2.metric(
    "Families",
    len(families),
)

col3.metric(
    "Chapters",
    len(chapters),
)

col4.metric(
    "Pillars",
    len(pillars),
)

st.divider()

# ==========================================================
# KNOWLEDGE
# ==========================================================

st.subheader("📚 Knowledge Base")

st.write("Familles disponibles :")

for family in families:

    st.write(f"• {family}")

st.divider()

# ==========================================================
# ARCHITECTURE
# ==========================================================

st.subheader("🏗 Framework")

modules = {

    "Knowledge Registry": True,

    "Planning Engine": True,

    "Campaign Engine": True,

    "Publication Engine": True,

    "Editorial Composer": True,

    "Hook Engine": True,

    "Script Engine": True,

    "CTA Engine": False,

    "Transition Engine": False,

    "Analytics": False,

}

for module, status in modules.items():

    if status:

        st.success(module)

    else:

        st.warning(module)

st.divider()

# ==========================================================
# ROADMAP
# ==========================================================

st.subheader("🚀 Avancement")

progress = int(

    sum(modules.values())

    / len(modules)

    * 100

)

st.progress(progress / 100)

st.write(f"{progress}% du Framework terminé.")
