from v2.models.knowledge_models import Topic
from v2.knowledge.reports.topic_quality import TopicQualityReport
from v2.knowledge.validators.topic_validator import TopicValidator


class KnowledgeValidator(TopicValidator):

    def validate(
        self,
        topic: Topic,
    ) -> TopicQualityReport:

        report = TopicQualityReport()

        # Description

        if topic.description.strip():
            report.add_success("description")
        else:
            report.add_failure(
                "description",
                "Ajouter une description."
            )

        # Objectif

        if topic.objective.strip():
            report.add_success("objective")
        else:
            report.add_failure(
                "objective",
                "Ajouter un objectif."
            )

        # Key points

        if len(topic.key_points) >= 3:
            report.add_success("key_points")
        else:
            report.add_failure(
                "key_points",
                "Ajouter au moins 3 key_points."
            )

        # Vocabulary

        if len(topic.vocabulary) >= 3:
            report.add_success("vocabulary")
        else:
            report.add_failure(
                "vocabulary",
                "Ajouter davantage de vocabulaire."
            )

        # Keywords

        if len(topic.keywords) >= 5:
            report.add_success("keywords")
        else:
            report.add_failure(
                "keywords",
                "Ajouter davantage de mots-clés."
            )

        return report
    