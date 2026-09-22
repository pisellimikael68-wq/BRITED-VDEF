from v2.knowledge.io.compiled_knowledge_loader import (
    CompiledKnowledgeLoader,
)
from v2.knowledge.io.knowledge_catalog import (
    KnowledgeCatalog,
)
from v2.knowledge.services.corpus_summary import (
    CorpusSummary,
)


class CorpusService:
    """
    Service d'accès au corpus compilé.

    Il constitue le point d'entrée unique du Studio pour
    interroger le corpus.
    """

    def __init__(self) -> None:
        self.catalog = KnowledgeCatalog()
        self.loader = CompiledKnowledgeLoader()

    def summary(self) -> CorpusSummary:
        """
        Calcule un résumé global du corpus compilé.
        """

        families = self.catalog.families()

        chapter_count = 0
        rule_count = 0
        legal_reference_count = 0
        source_anchor_count = 0

        for family in families:

            chapters = self.catalog.chapters(family)

            chapter_count += len(chapters)

            for chapter in chapters:

                knowledge = self.loader.load(
                    family=family,
                    chapter=chapter,
                )

                rule_count += len(knowledge.rules)

                for rule in knowledge.rules:

                    legal_reference_count += len(
                        rule.legal_references
                    )

                    source_anchor_count += len(
                        rule.source_anchors
                    )

        return CorpusSummary(
            families=len(families),
            chapters=chapter_count,
            rules=rule_count,
            legal_references=legal_reference_count,
            source_anchors=source_anchor_count,
        )
    