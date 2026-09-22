import streamlit as st


def render_knowledge_inspector(
    knowledge,
) -> None:
    """
    Affiche le contenu d'un chapitre compilé.

    Le composant est volontairement indépendant
    du loader et du catalogue.
    Il ne fait qu'afficher le modèle reçu.
    """

    st.success(
        f"{len(knowledge.rules)} règles chargées."
    )

    st.divider()

    st.header(
        f"{knowledge.family} / {knowledge.chapter}"
    )

    for index, rule in enumerate(
        knowledge.rules,
        start=1,
    ):

        rule_type = getattr(
            rule.rule_type,
            "value",
            str(rule.rule_type),
        )

        severity = getattr(
            rule.severity,
            "value",
            str(rule.severity),
        )

        with st.expander(
            f"{index}. {rule_type}",
            expanded=False,
        ):

            st.markdown("### Statement")
            st.write(rule.statement)

            st.markdown(
                f"**Severity :** {severity}"
            )

            st.markdown("### Conditions")

            if rule.conditions:
                for condition in rule.conditions:
                    st.markdown(
                        f"- {condition}"
                    )
            else:
                st.caption("Aucune")

            st.markdown(
                "### Required Elements"
            )

            if rule.required_elements:
                for element in rule.required_elements:
                    st.markdown(
                        f"- {element}"
                    )
            else:
                st.caption("Aucun")

            st.markdown(
                "### Forbidden Interpretations"
            )

            if rule.forbidden_interpretations:
                for interpretation in (
                    rule.forbidden_interpretations
                ):
                    st.markdown(
                        f"- {interpretation}"
                    )
            else:
                st.caption("Aucune")

            st.markdown(
                "### Legal References"
            )

            if rule.legal_references:
                for reference in (
                    rule.legal_references
                ):
                    st.markdown(
                        f"- {reference}"
                    )
            else:
                st.caption("Aucune")

            st.markdown(
                "### Source Anchors"
            )

            if rule.source_anchors:
                for anchor in (
                    rule.source_anchors
                ):
                    st.code(anchor)
            else:
                st.caption("Aucune")
                