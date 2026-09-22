import streamlit as st


def render_result(context):

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
    