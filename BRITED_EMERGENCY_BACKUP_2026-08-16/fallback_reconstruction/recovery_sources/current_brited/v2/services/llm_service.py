from v2.agents.models import PlannedTopic, WrittenTopic
from v2.cache.hash import compute_hash
from v2.knowledge.builders.knowledge_context_builder import (
    KnowledgeContextBuilder,
)
from v2.llm.factory import LLMFactory
from v2.llm.schemas.written_topic import WrittenTopicSchema
from v2.prompts.loader import PromptLoader
from v2.prompts.renderer import PromptRenderer


class LLMService:
    """
    Service de haut niveau utilisé par les agents.

    Il est responsable de :
    - construire le contexte Knowledge,
    - construire les prompts,
    - injecter le socle académique,
    - injecter les règles protégées,
    - calculer le hash du prompt,
    - appeler le LLM,
    - convertir la réponse en modèle métier.
    """

    def __init__(self):

        self.llm = LLMFactory.create()

        self.knowledge_context_builder = (
            KnowledgeContextBuilder()
        )

    def build_topic_prompt(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
    ) -> str:
        """
        Construit le prompt final d'un topic.

        Le contenu académique général et les règles
        protégées sont injectés séparément.
        """

        prompt = PromptLoader.load(
            "writer/topic.md"
        )

        knowledge_context = (
            self.knowledge_context_builder.build(
                family=family,
                chapter=chapter,
                topic=topic,
            )
        )

        return PromptRenderer.render(
            prompt,
            family=family,
            chapter=chapter,
            title=topic.title,
            knowledge_context=(
                knowledge_context.academic_content
            ),
            protected_rules=(
                knowledge_context.render_protected_rules()
            ),
        )

    def compute_topic_prompt_hash(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
    ) -> str:
        """
        Calcule le hash du prompt final.

        Toute modification :
        - du prompt,
        - du contexte Knowledge,
        - ou des règles protégées

        modifie automatiquement le hash.
        """

        prompt = self.build_topic_prompt(
            family=family,
            chapter=chapter,
            topic=topic,
        )

        return compute_hash(prompt)

    def write_topic(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
    ) -> WrittenTopic:
        """
        Rédige un nouveau topic.
        """

        prompt = self.build_topic_prompt(
            family=family,
            chapter=chapter,
            topic=topic,
        )

        prompt_hash = compute_hash(prompt)

        result = self.llm.generate(
            prompt=prompt,
            response_model=WrittenTopicSchema,
        )

        return self._to_written_topic(
            topic=topic,
            result=result,
            prompt_hash=prompt_hash,
        )

    def correct_topic(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
        written: WrittenTopic,
        quality_issues: str,
    ) -> WrittenTopic:
        """
        Corrige un topic rejeté par un Gate.

        La correction reçoit :
        - le contenu académique pertinent,
        - les règles protégées,
        - le topic précédent,
        - les anomalies détectées.

        Les règles protégées sont réinjectées lors de
        chaque correction afin d'éviter qu'une tentative
        de réparation ne déforme un mécanisme technique.
        """

        prompt = PromptLoader.load(
            "writer/topic_correction.md"
        )

        knowledge_context = (
            self.knowledge_context_builder.build(
                family=family,
                chapter=chapter,
                topic=topic,
            )
        )

        rendered_prompt = PromptRenderer.render(
            prompt,
            family=family,
            chapter=chapter,
            title=topic.title,
            knowledge_context=(
                knowledge_context.academic_content
            ),
            protected_rules=(
                knowledge_context.render_protected_rules()
            ),
            previous_topic=self._render_written_topic(
                written
            ),
            quality_issues=quality_issues,
        )

        prompt_hash = self.compute_topic_prompt_hash(
            family=family,
            chapter=chapter,
            topic=topic,
        )

        result = self.llm.generate(
            prompt=rendered_prompt,
            response_model=WrittenTopicSchema,
        )

        return self._to_written_topic(
            topic=topic,
            result=result,
            prompt_hash=prompt_hash,
        )

    @staticmethod
    def _to_written_topic(
        *,
        topic: PlannedTopic,
        result: WrittenTopicSchema,
        prompt_hash: str,
    ) -> WrittenTopic:
        """
        Convertit le schéma LLM validé
        en modèle métier WrittenTopic.
        """

        return WrittenTopic(
            id=topic.id,
            title=result.title or topic.title,
            summary=result.summary,
            description=result.description,
            keywords=result.keywords,
            vocabulary=result.vocabulary,
            examples=result.examples,
            legal_sources=result.legal_sources,
            prompt_hash=prompt_hash,
        )

    @staticmethod
    def _render_written_topic(
        written: WrittenTopic,
    ) -> str:
        """
        Rend un WrittenTopic sous une forme textuelle
        exploitable par le prompt de correction.
        """

        return (
            f"TITRE : {written.title}\n\n"
            f"RÉSUMÉ :\n{written.summary}\n\n"
            f"DESCRIPTION :\n{written.description}\n\n"
            "MOTS-CLÉS :\n"
            + "\n".join(
                f"- {value}"
                for value in written.keywords
            )
            + "\n\nVOCABULAIRE :\n"
            + "\n".join(
                f"- {value}"
                for value in written.vocabulary
            )
            + "\n\nEXEMPLES :\n"
            + "\n".join(
                f"- {value}"
                for value in written.examples
            )
            + "\n\nSOURCES :\n"
            + "\n".join(
                f"- {value}"
                for value in written.legal_sources
            )
        )
    