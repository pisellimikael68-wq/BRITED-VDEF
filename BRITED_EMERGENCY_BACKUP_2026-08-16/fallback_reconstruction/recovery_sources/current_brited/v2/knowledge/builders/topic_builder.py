import re
import unicodedata

from v2.agents.models import PlannedTopic
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)
from v2.knowledge.sources.academic_models import (
    AcademicKnowledge,
)


class TopicBuilder:
    """
    Sélectionne les blocs de connaissance académique
    pertinents pour un topic planifié.
    """

    def __init__(self):

        self.loader = AcademicKnowledgeLoader()

    def build(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
    ) -> list[AcademicKnowledge]:
        """
        Retourne les blocs Knowledge pertinents
        pour le topic demandé.
        """

        blocks = self.loader.load_family(
            family
        )

        if not blocks:
            return []

        ranked_blocks = []

        for block in blocks:

            score = self._compute_score(
                chapter=chapter,
                topic=topic,
                block=block,
            )

            if score > 0:

                ranked_blocks.append(
                    (
                        score,
                        block,
                    )
                )

        ranked_blocks.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            block
            for _, block in ranked_blocks
        ]

    def _compute_score(
        self,
        *,
        chapter: str,
        topic: PlannedTopic,
        block: AcademicKnowledge,
    ) -> int:
        """
        Calcule un score simple de pertinence.
        """

        score = 0

        normalized_chapter = self._normalize(
            chapter
        )

        normalized_block_chapter = self._normalize(
            block.chapter
        )

        if (
            normalized_chapter
            == normalized_block_chapter
        ):

            score += 10

        topic_tokens = self._tokens(
            topic.title
        )

        block_tokens = self._tokens(
            block.searchable_content()
        )

        common_tokens = (
            topic_tokens
            & block_tokens
        )

        score += len(common_tokens)

        return score

    @classmethod
    def _tokens(
        cls,
        value: str,
    ) -> set[str]:

        normalized = cls._normalize(
            value
        )

        return {
            token
            for token in re.findall(
                r"[a-z0-9]+",
                normalized,
            )
            if len(token) >= 4
        }

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:

        value = unicodedata.normalize(
            "NFKD",
            value,
        )

        value = "".join(
            character
            for character in value
            if not unicodedata.combining(
                character
            )
        )

        return value.lower()
    