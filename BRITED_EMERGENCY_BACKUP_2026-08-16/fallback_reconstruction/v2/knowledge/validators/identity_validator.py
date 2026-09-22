from v2.knowledge.validators.topic_validator import TopicValidator
from v2.knowledge.reports.topic_quality import TopicQualityReport


class IdentityValidator(TopicValidator):

    def validate(self, topic):

        report = TopicQualityReport()

        if topic.id:
            report.add_success("id")
        else:
            report.add_failure(
                "id",
                "Le Topic doit posséder un identifiant."
            )

        return report
    