from dataclasses import dataclass, field

from v2.knowledge.registry import KnowledgeRegistry


@dataclass(slots=True)
class GraphValidationReport:

    duplicate_ids: list[str] = field(default_factory=list)

    missing_related_topics: list[tuple[str, str]] = field(default_factory=list)
    missing_prerequisites: list[tuple[str, str]] = field(default_factory=list)
    missing_next_topics: list[tuple[str, str]] = field(default_factory=list)
    missing_relations: list[tuple[str, str, str]] = field(default_factory=list)

    orphan_topics: list[str] = field(default_factory=list)
    cycles: list[list[str]] = field(default_factory=list)

    @property
    def valid(self) -> bool:

        return not any(
            (
                self.duplicate_ids,
                self.missing_related_topics,
                self.missing_prerequisites,
                self.missing_next_topics,
                self.missing_relations,
                self.orphan_topics,
                self.cycles,
            )
        )


class GraphValidator:

    def __init__(
        self,
        registry: KnowledgeRegistry,
    ):
        self.registry = registry

    def validate(self) -> GraphValidationReport:

        report = GraphValidationReport()

        seen: set[str] = set()

        for topic in self.registry.topics:

            if topic.id in seen:
                report.duplicate_ids.append(topic.id)
            else:
                seen.add(topic.id)

        incoming: dict[str, int] = {
            topic.id: 0
            for topic in self.registry.topics
        }

        for topic in self.registry.topics:

            for related in topic.related_topics:

                if self.registry.exists(related):
                    incoming[related] += 1
                else:
                    report.missing_related_topics.append(
                        (topic.id, related)
                    )

            for prerequisite in topic.prerequisites:

                if self.registry.exists(prerequisite):
                    incoming[prerequisite] += 1
                else:
                    report.missing_prerequisites.append(
                        (topic.id, prerequisite)
                    )

            for next_topic in topic.next_topics:

                if self.registry.exists(next_topic):
                    incoming[next_topic] += 1
                else:
                    report.missing_next_topics.append(
                        (topic.id, next_topic)
                    )

            for relation in topic.relations:

                if self.registry.exists(relation.target):
                    incoming[relation.target] += 1
                else:
                    report.missing_relations.append(
                        (
                            topic.id,
                            relation.target,
                            relation.relation_type,
                        )
                    )

        for topic in self.registry.topics:

            has_outgoing = (
                bool(topic.related_topics)
                or bool(topic.prerequisites)
                or bool(topic.next_topics)
                or bool(topic.relations)
            )

            has_incoming = incoming[topic.id] > 0

            if not has_incoming and not has_outgoing:
                report.orphan_topics.append(topic.id)

        return report
    