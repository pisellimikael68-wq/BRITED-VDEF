import streamlit as st

from v2.knowledge.io.knowledge_catalog import KnowledgeCatalog


def render_corpus_selector(
    catalog: KnowledgeCatalog,
) -> tuple[str, str] | tuple[None, None]:
    """
    Affiche le sélecteur du corpus.

    Retourne :
        (family, chapter)

    ou

        (None, None)

    si aucun corpus n'est disponible.
    """

    st.header("Explorer le corpus")

    families = catalog.families()

    if not families:
        st.warning(
            "Aucune famille disponible."
        )
        return None, None

    family = st.selectbox(
        "Famille",
        families,
    )

    chapters = catalog.chapters(
        family,
    )

    if not chapters:
        st.warning(
            "Aucun chapitre disponible."
        )
        return None, None

    chapter = st.selectbox(
        "Chapitre",
        chapters,
    )

    return family, chapter
