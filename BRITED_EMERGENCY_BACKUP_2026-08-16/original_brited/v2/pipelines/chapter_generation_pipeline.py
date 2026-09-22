from v2.agents.models import PlannedChapter
from v2.pipelines.models import GenerationError, GenerationReport
from v2.pipelines.topic_generation_pipeline import TopicGenerationPipeline


class ChapterGenerationPipeline:
    """
    Génère tous les topics d'un chapitre.

    Une erreur sur un topic n'interrompt pas la génération
    des autres topics.
    """

    def __init__(self):

        self.topic_pipeline = TopicGenerationPipeline()

    def generate(
        self,
        *,
        family: str,
        chapter: PlannedChapter,
        force: bool = False,
    ) -> GenerationReport:

        report = GenerationReport()

        topics = sorted(
            chapter.topics,
            key=lambda topic: topic.editorial_order,
        )

        for topic in topics:

            try:

                output = self.topic_pipeline.generate(
                    family=family,
                    chapter=chapter.name,
                    topic=topic,
                    force=force,
                )

                if output is None:

                    report.skipped += 1

                else:

                    report.generated_files.append(output)

            except Exception as e:

                report.errors.append(

                    GenerationError(
                        topic_id=topic.id,
                        message=str(e),
                    )

                )

        return report
    