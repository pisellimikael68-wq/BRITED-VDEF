from v2.agents.models import PlannedTopic
from v2.agents.writer.writer import WriterAgent
from v2.core.logger import get_logger
from v2.exporters.markdown_reader import MarkdownReader
from v2.exporters.markdown_writer import MarkdownWriter
from v2.knowledge.builders.knowledge_context_builder import (
    KnowledgeContextBuilder,
)
from v2.knowledge.validators.protected_rules_validator import (
    ProtectedRulesValidator,
)
from v2.knowledge.validators.topic_legal_tax_validator import (
    TopicLegalTaxValidator,
)
from v2.knowledge.validators.topic_quality_validator import (
    TopicQualityValidator,
)
from v2.pipelines.models import (
    GenerationError,
    GenerationReport,
)
from v2.services.llm_service import LLMService


logger = get_logger(__name__)


class TopicGenerationPipeline:
    """
    Génère, contrôle puis exporte un topic en Markdown.

    La génération est incrémentale :
    - fichier absent -> génération,
    - hash identique -> topic ignoré,
    - hash différent -> régénération,
    - force=True -> régénération systématique.

    La génération passe par trois contrôles :
    - Quality Gate éditorial,
    - Legal & Tax Gate juridique et fiscal,
    - Protected Rules Gate déterministe.

    Un topic rejeté peut faire l'objet d'une correction
    guidée avant un rejet définitif.
    """

    MAX_GENERATION_ATTEMPTS = 4

    def __init__(self):

        self.writer = WriterAgent()

        self.exporter = MarkdownWriter()
        self.reader = MarkdownReader()

        self.llm_service = LLMService()

        self.knowledge_context_builder = (
            KnowledgeContextBuilder()
        )

        self.quality_validator = (
            TopicQualityValidator()
        )

        self.legal_tax_validator = (
            TopicLegalTaxValidator()
        )

        self.protected_rules_validator = (
            ProtectedRulesValidator()
        )

    def generate(
        self,
        *,
        family: str,
        chapter: str,
        topic: PlannedTopic,
        force: bool = False,
    ) -> GenerationReport:

        report = GenerationReport()

        output = (
            self.exporter.output_dir
            / family
            / chapter
            / f"{topic.id}.md"
        )

        try:

            # ==================================================
            # KNOWLEDGE CONTEXT
            # ==================================================

            knowledge_context = (
                self.knowledge_context_builder.build(
                    family=family,
                    chapter=chapter,
                    topic=topic,
                )
            )

            # ==================================================
            # PROMPT HASH
            # ==================================================

            current_prompt_hash = (
                self.llm_service.compute_topic_prompt_hash(
                    family=family,
                    chapter=chapter,
                    topic=topic,
                )
            )

            # ==================================================
            # INCREMENTAL GENERATION
            # ==================================================

            if output.exists() and not force:

                stored_prompt_hash = (
                    self.reader.read_prompt_hash(
                        output
                    )
                )

                if (
                    stored_prompt_hash
                    == current_prompt_hash
                ):

                    logger.info(
                        "Topic '%s' inchangé, ignoré.",
                        topic.id,
                    )

                    report.skipped += 1

                    return report

                logger.info(
                    "Topic '%s' obsolète, régénération.",
                    topic.id,
                )

            written = None
            last_validation_report = None
            quality_issues = None

            # ==================================================
            # GENERATION / CORRECTION LOOP
            # ==================================================

            for attempt in range(
                1,
                self.MAX_GENERATION_ATTEMPTS + 1,
            ):

                # ----------------------------------------------
                # WRITER
                # ----------------------------------------------

                if attempt == 1:

                    logger.info(
                        "Rédaction du topic '%s' "
                        "(tentative qualité %s/%s)",
                        topic.id,
                        attempt,
                        self.MAX_GENERATION_ATTEMPTS,
                    )

                    written = self.writer.write(
                        family=family,
                        chapter=chapter,
                        topic=topic,
                    )

                else:

                    logger.info(
                        "Correction guidée du topic '%s' "
                        "(tentative qualité %s/%s)",
                        topic.id,
                        attempt,
                        self.MAX_GENERATION_ATTEMPTS,
                    )

                    written = self.writer.correct(
                        family=family,
                        chapter=chapter,
                        topic=topic,
                        written=written,
                        quality_issues=quality_issues,
                    )

                # ==================================================
                # QUALITY GATE
                # ==================================================

                logger.info(
                    "Contrôle qualité du topic '%s'",
                    topic.id,
                )

                quality_report = (
                    self.quality_validator.validate(
                        written
                    )
                )

                last_validation_report = (
                    quality_report
                )

                if not quality_report.valid:

                    quality_issues = (
                        self._format_quality_issues(
                            quality_report
                        )
                    )

                    logger.warning(
                        "Topic '%s' rejeté par le "
                        "Quality Gate à la tentative "
                        "%s/%s : %s",
                        topic.id,
                        attempt,
                        self.MAX_GENERATION_ATTEMPTS,
                        quality_issues,
                    )

                    continue

                logger.info(
                    "Topic '%s' validé par le "
                    "Quality Gate à la tentative %s",
                    topic.id,
                    attempt,
                )

                # ==================================================
                # LEGAL & TAX GATE
                # ==================================================

                logger.info(
                    "Contrôle juridique et fiscal "
                    "du topic '%s'",
                    topic.id,
                )

                legal_tax_report = (
                    self.legal_tax_validator.validate(
                        written
                    )
                )

                last_validation_report = (
                    legal_tax_report
                )

                if not legal_tax_report.valid:

                    quality_issues = (
                        self._format_quality_issues(
                            legal_tax_report
                        )
                    )

                    logger.warning(
                        "Topic '%s' rejeté par le "
                        "Legal & Tax Gate à la tentative "
                        "%s/%s : %s",
                        topic.id,
                        attempt,
                        self.MAX_GENERATION_ATTEMPTS,
                        quality_issues,
                    )

                    continue

                logger.info(
                    "Topic '%s' validé par le "
                    "Legal & Tax Gate à la tentative %s",
                    topic.id,
                    attempt,
                )

                # ==================================================
                # PROTECTED RULES GATE
                # ==================================================

                logger.info(
                    "Contrôle des règles protégées "
                    "du topic '%s'",
                    topic.id,
                )

                protected_rules_report = (
                    self.protected_rules_validator.validate(
                        topic=written,
                        protected_rules=(
                            knowledge_context.protected_rules
                        ),
                    )
                )

                last_validation_report = (
                    protected_rules_report
                )

                if not protected_rules_report.valid:

                    quality_issues = (
                        self._format_quality_issues(
                            protected_rules_report
                        )
                    )

                    logger.warning(
                        "Topic '%s' rejeté par le "
                        "Protected Rules Gate à la tentative "
                        "%s/%s : %s",
                        topic.id,
                        attempt,
                        self.MAX_GENERATION_ATTEMPTS,
                        quality_issues,
                    )

                    continue

                logger.info(
                    "Topic '%s' validé par le "
                    "Protected Rules Gate à la tentative %s",
                    topic.id,
                    attempt,
                )

                break

            # ==================================================
            # FINAL VALIDATION
            # ==================================================

            if (
                written is None
                or last_validation_report is None
                or not last_validation_report.valid
            ):

                issues = self._format_quality_issues(
                    last_validation_report
                )

                report.errors.append(
                    GenerationError(
                        topic_id=topic.id,
                        message=(
                            "Validation rejetée après "
                            f"{self.MAX_GENERATION_ATTEMPTS} "
                            "tentatives : "
                            f"{issues}"
                        ),
                    )
                )

                return report

            # ==================================================
            # MARKDOWN EXPORT
            # ==================================================

            output = self.exporter.write(
                family=family,
                chapter=chapter,
                topic=written,
                prompt_hash=current_prompt_hash,
            )

            report.generated_files.append(
                output
            )

            logger.info(
                "Topic '%s' rédigé",
                topic.id,
            )

        except Exception as exc:

            logger.exception(
                "Erreur pendant la génération "
                "du topic '%s'",
                topic.id,
            )

            report.errors.append(
                GenerationError(
                    topic_id=topic.id,
                    message=str(exc),
                )
            )

        return report

    @staticmethod
    def _format_quality_issues(
        validation_report,
    ) -> str:

        if validation_report is None:

            return (
                "Aucun rapport de validation disponible."
            )

        return "; ".join(
            (
                f"{issue.field}: "
                f"{issue.message}"
            )
            for issue in validation_report.issues
        )
    