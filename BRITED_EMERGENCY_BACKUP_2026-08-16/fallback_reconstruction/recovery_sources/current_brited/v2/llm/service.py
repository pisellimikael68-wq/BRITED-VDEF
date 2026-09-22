from v2.agents.models import PlannedTopic, WrittenTopic
from v2.core.logger import get_logger
from v2.llm.factory import LLMFactory
from v2.llm.schemas.written_topic import WrittenTopicSchema
from v2.prompts.loader import PromptLoader
from v2.prompts.renderer import PromptRenderer


class LLMService:
    """
    Service de haut niveau utilisé par les agents.

    Il est responsable de :
    - charger le prompt,
    - injecter les variables,
    - appeler le LLM,
    - convertir la réponse en modèle métier.
    """

    def __init__(self):

        self.logger = get_logger(__name__)

        self.llm = LLMFactory.create()

    def write_topic(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
    ) -> WrittenTopic:

        self.logger.info(
            f"Rédaction du topic '{topic.id}'"
        )

        prompt = PromptLoader.load("writer/topic.md")

        prompt = PromptRenderer.render(
            prompt,
            family=family,
            chapter=chapter,
            title=topic.title,
        )

        result = self.llm.generate(
            prompt=prompt,
            response_model=WrittenTopicSchema,
        )

        self.logger.info(
            f"Topic '{topic.id}' rédigé"
        )

        return WrittenTopic(
            id=topic.id,
            title=result.title or topic.title,
            summary=result.summary,
            description=result.description,
            keywords=result.keywords,
            vocabulary=result.vocabulary,
            examples=result.examples,
            legal_sources=result.legal_sources,
        )
    