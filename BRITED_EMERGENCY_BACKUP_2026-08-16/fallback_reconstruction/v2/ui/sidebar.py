import streamlit as st


def render_sidebar():

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

    return platform, subject, generate