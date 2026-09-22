from v2.agents.models import PlannedTopic
from v2.knowledge.builders.topic_builder import TopicBuilder
from v2.knowledge.sources.academic_models import (
    AcademicKnowledge,
    ProtectedRule,
)
from v2.knowledge.sources.context_models import (
    KnowledgeContext,
)


class KnowledgeContextBuilder:
    """
    Construit le contexte Knowledge transmis au Writer.

    Le contenu académique général et les règles protégées
    sont volontairement transportés séparément.

    Les règles protégées restent structurées afin de permettre
    leur injection dans les prompts et leur validation
    déterministe après génération.
    """

    def __init__(self):

        self.topic_builder = TopicBuilder()

    def build(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
    ) -> KnowledgeContext:

        blocks = self.topic_builder.build(
            family=family,
            chapter=chapter,
            topic=topic,
        )

        academic_content = "\n\n".join(
            self._render_block(block)
            for block in blocks
        )

        protected_rules = self._collect_protected_rules(
            blocks
        )

        return KnowledgeContext(
            topic_id=topic.id,
            academic_content=academic_content,
            protected_rules=protected_rules,
            source_ids=[
                block.id
                for block in blocks
            ],
            source_types=sorted(
                {
                    block.source_type
                    for block in blocks
                }
            ),
        )

    @staticmethod
    def _collect_protected_rules(
        blocks: list[AcademicKnowledge],
    ) -> list[ProtectedRule]:
        """
        Agrège les règles protégées structurées.

        Les doublons sont supprimés par identifiant
        tout en conservant l'ordre d'apparition.
        """

        protected_rules: list[ProtectedRule] = []

        seen_ids: set[str] = set()

        for block in blocks:

            for rule in block.protected_rules:

                if rule.id in seen_ids:
                    continue

                seen_ids.add(rule.id)

                protected_rules.append(rule)

        return protected_rules

    @staticmethod
    def _render_block(
        block: AcademicKnowledge,
    ) -> str:

        sections = [
            f"TITRE DU BLOC : {block.title}",
        ]

        if block.summary:

            sections.append(
                "RÉSUMÉ :\n"
                + block.summary
            )

        if block.key_points:

            sections.append(
                "POINTS CLÉS :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.key_points
                )
            )

        if block.rules:

            sections.append(
                "RÈGLES :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.rules
                )
            )

        if block.thresholds:

            sections.append(
                "SEUILS :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.thresholds
                )
            )

        if block.sensitive_dates:

            sections.append(
                "DATES SENSIBLES :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.sensitive_dates
                )
            )

        if block.examples:

            sections.append(
                "EXEMPLES :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.examples
                )
            )

        if block.vocabulary:

            sections.append(
                "VOCABULAIRE :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.vocabulary
                )
            )

        if block.legal_references:

            sections.append(
                "RÉFÉRENCES PRÉSENTES DANS LES NOTES :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.legal_references
                )
            )

        if block.attention_points:

            sections.append(
                "POINTS D'ATTENTION :\n"
                + "\n".join(
                    f"- {value}"
                    for value in block.attention_points
                )
            )

        sections.append(
            "PROVENANCE : "
            f"{block.origin} / "
            f"{block.academic_year}"
        )

        return "\n\n".join(sections)
    