from v2.models.knowledge_models import Topic

from v2.knowledge.reports.topic_quality import TopicQualityReport

from v2.knowledge.validators.identity_validator import IdentityValidator

from v2.knowledge.validators.knowledge_validator import KnowledgeValidator


class GoldValidator:

    def __init__(self):

        self.validators = [

            IdentityValidator(),

             KnowledgeValidator(),

        ]

    def validate(
        self,
        topic: Topic,
    ) -> TopicQualityReport:

        report = TopicQualityReport()

        for validator in self.validators:

            partial = validator.validate(topic)

            report.passed_rules.extend(partial.passed_rules)

            report.failed_rules.extend(partial.failed_rules)

            report.warnings.extend(partial.warnings)

            report.suggestions.extend(partial.suggestions)

        return report
    