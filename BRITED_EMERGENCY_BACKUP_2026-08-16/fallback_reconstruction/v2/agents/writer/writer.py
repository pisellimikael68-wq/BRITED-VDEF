from v2.agents.models import PlannedTopic, WrittenTopic
from v2.services.llm_service import LLMService


class WriterAgent:
    """
    Agent chargé de rédiger et de corriger un topic.
    """

    def __init__(self):

        self.llm = LLMService()

    def write(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
    ) -> WrittenTopic:

        return self.llm.write_topic(
            family=family,
            chapter=chapter,
            topic=topic,
        )

    def correct(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
        written: WrittenTopic,
        quality_issues: str,
    ) -> WrittenTopic:
        """
        Corrige un topic rejeté par le Quality Gate.
        """

        return self.llm.correct_topic(
            family=family,
            chapter=chapter,
            topic=topic,
            written=written,
            quality_issues=quality_issues,
        )
    