import streamlit as st

from v2.studio.engines.planning_engine import PlanningEngine

# ==========================================================
# HEADER
# ==========================================================

st.title("📅 Calendrier éditorial")

st.caption("Planification automatique des contenus")

st.divider()

# ==========================================================
# PARAMÈTRES
# ==========================================================

family = st.text_input(
    "Famille",
    value="assurance_vie",
)

weeks = st.slider(
    "Nombre de semaines",
    min_value=1,
    max_value=12,
    value=8,
)

posts = st.slider(
    "Publications par semaine",
    min_value=1,
    max_value=7,
    value=3,
)

# ==========================================================
# GENERATION
# ==========================================================

if st.button("🚀 Générer le calendrier"):

    planning = PlanningEngine().generate(
        family=family,
        weeks=weeks,
        posts_per_week=posts,
    )

    st.divider()

    for week in planning.weeks:

        st.subheader(f"📅 Semaine {week.week}")

        for topic in week.topics:

            col1, col2 = st.columns([5,1])

            with col1:

                st.write(f"**{topic.title}**")

                st.caption(topic.chapter)

            with col2:

                st.button(
                    "✍️",
                    key=topic.id,
                )

        st.divider()
        