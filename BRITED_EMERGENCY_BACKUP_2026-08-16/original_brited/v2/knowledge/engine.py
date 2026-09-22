from v2.models.editorial_brief import EditorialBrief
from v2.services.knowledge_service import KnowledgeService


class KnowledgeEngine:

    def __init__(self):

        self.service = KnowledgeService()

    def build(
        self,
        subject: str,
    ) -> EditorialBrief:

        topics = self.service.search(subject)

        brief = EditorialBrief(
            subject=subject,
            topics=topics,
        )

        for topic in topics:

            brief.misconceptions.extend(
                topic.misconceptions
            )

            brief.client_questions.extend(
                topic.client_questions
            )

            brief.analogies.extend(
                topic.analogies
            )

            brief.recommended_formats.extend(
                topic.recommended_formats
            )

            brief.legal_sources.extend(
                topic.legal_sources
            )

            brief.keywords.extend(
                topic.keywords
            )

        # ----------------------------------------
        # Suppression des doublons
        # ----------------------------------------

        brief.misconceptions = sorted(
            set(brief.misconceptions)
        )

        brief.client_questions = sorted(
            set(brief.client_questions)
        )

        brief.analogies = sorted(
            set(brief.analogies)
        )

        brief.recommended_formats = sorted(
            set(brief.recommended_formats)
        )

        brief.legal_sources = sorted(
            set(brief.legal_sources)
        )

        brief.keywords = sorted(
            set(brief.keywords)
        )

        return brief
    