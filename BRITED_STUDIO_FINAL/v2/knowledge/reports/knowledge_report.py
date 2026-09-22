from collections import Counter

from v2.knowledge.registry import KnowledgeRegistry
from v2.knowledge.validators.graph_validator import GraphValidationReport
from v2.knowledge.reports.models import KnowledgeReport


class KnowledgeReportGenerator:

    def __init__(
        self,
        registry: KnowledgeRegistry,
        graph_report: GraphValidationReport,
    ):
        self.registry = registry
        self.graph_report = graph_report

    def generate(self) -> KnowledgeReport:

        topics = self.registry.topics

        report = KnowledgeReport()

        report.topic_count = len(topics)

        degrees = [
            len(topic.relations)
            for topic in topics
        ]

        report.relation_count = sum(degrees)

        if degrees:
            report.average_degree = round(
                sum(degrees) / len(degrees),
                2,
            )
            report.min_degree = min(degrees)
            report.max_degree = max(degrees)

        relation_counter = Counter()

        for topic in topics:

            for relation in topic.relations:
                relation_counter[relation.relation_type] += 1

            if topic.description:
                report.topics_with_description += 1

            if topic.keywords:
                report.topics_with_keywords += 1

            if topic.vocabulary:
                report.topics_with_vocabulary += 1

            if topic.examples:
                report.topics_with_examples += 1

            if topic.legal_sources:
                report.topics_with_sources += 1

        report.relation_types = dict(relation_counter)

        report.duplicate_ids = len(self.graph_report.duplicate_ids)
        report.missing_links = (
            len(self.graph_report.missing_related_topics)
            + len(self.graph_report.missing_prerequisites)
            + len(self.graph_report.missing_next_topics)
            + len(self.graph_report.missing_relations)
        )
        report.orphan_topics = len(self.graph_report.orphan_topics)
        report.cycles = len(self.graph_report.cycles)

        report.knowledge_score = self._score(report)

        return report

    def _score(
        self,
        report: KnowledgeReport,
    ) -> int:

        score = 100

        if report.topic_count == 0:
            return 0

        if report.orphan_topics:
            score -= 20

        if report.missing_links:
            score -= 25

        if report.duplicate_ids:
            score -= 25

        if report.average_degree < 1:
            score -= 10

        return max(0, min(100, score))
    