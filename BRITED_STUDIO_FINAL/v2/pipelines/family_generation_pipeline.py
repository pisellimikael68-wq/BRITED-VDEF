from datetime import datetime

from v2.agents.planner.planner import PlannerAgent
from v2.core.logger import get_logger
from v2.pipelines.chapter_generation_pipeline import (
    ChapterGenerationPipeline,
)
from v2.pipelines.models import GenerationReport
from v2.pipelines.options import GenerationOptions


class FamilyGenerationPipeline:
    """
    Génère une famille complète de connaissances.
    """

    def __init__(self):

        self.logger = get_logger(__name__)

        self.planner = PlannerAgent()
        self.chapter_pipeline = ChapterGenerationPipeline()

    def generate(
        self,
        *,
        family: str,
        options: GenerationOptions | None = None,
    ) -> GenerationReport:

        options = options or GenerationOptions()

        self.logger.info(
            f"Début de génération de la famille '{family}'"
        )

        planned_family = self.planner.plan(
            family=family,
        )

        report = GenerationReport()
        report.started_at = datetime.now()

        for chapter in planned_family.chapters:

            if (
                options.chapters is not None
                and chapter.name not in options.chapters
            ):
                continue

            self.logger.info(
                f"Génération du chapitre '{chapter.name}'"
            )

            chapter_report = self.chapter_pipeline.generate(
                family=planned_family.name,
                chapter=chapter,
                force=options.force,
            )

            report.generated_files.extend(
                chapter_report.generated_files
            )

            report.errors.extend(
                chapter_report.errors
            )

            report.skipped += chapter_report.skipped

            self.logger.info(
                f"Chapitre '{chapter.name}' terminé "
                f"({chapter_report.generated} générés, "
                f"{chapter_report.skipped} ignorés, "
                f"{chapter_report.failed} erreurs)"
            )

        report.finished_at = datetime.now()

        self.logger.info(
            f"Famille '{family}' terminée "
            f"({report.generated} générés, "
            f"{report.skipped} ignorés, "
            f"{report.failed} erreurs, "
            f"{report.duration_seconds:.1f} s)"
        )

        return report
    