import streamlit as st

from v2.knowledge.services.corpus_summary import CorpusSummary


def render_dashboard(summary: CorpusSummary) -> None:
    """
    Affiche les indicateurs globaux du corpus compilé.

    Le composant ne calcule aucune donnée.
    Il reçoit un CorpusSummary déjà construit
    par le CorpusService.
    """

    st.header("Corpus")

    columns = st.columns(5)

    columns[0].metric(
        label="Familles",
        value=summary.families,
    )

    columns[1].metric(
        label="Chapitres",
        value=summary.chapters,
    )

    columns[2].metric(
        label="Règles",
        value=summary.rules,
    )

    columns[3].metric(
        label="Références légales",
        value=summary.legal_references,
    )

    columns[4].metric(
        label="Ancres sources",
        value=summary.source_anchors,
    )

    if summary.legal_references == 0 and summary.rules > 0:
        st.warning(
            "Le corpus contient des règles, mais aucune référence légale "
            "n'a été détectée."
        )

    st.divider()
    