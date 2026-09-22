from dataclasses import dataclass, field

from v2.models.knowledge_models import Topic


@dataclass(slots=True)
class KnowledgeRegistry:
    """
    Registre central des Topics compilés.
    """

    topics: dict[str, Topic] = field(default_factory=dict)

    def add(self, topic: Topic):
        self.topics[topic.id] = topic

    def get(self, topic_id: str) -> Topic:
        return self.topics[topic_id]

    def exists(self, topic_id: str) -> bool:
        return topic_id in self.topics

    def all(self) -> list[Topic]:
        return list(self.topics.values())

    def by_family(self, family: str) -> list[Topic]:
        return [
            topic
            for topic in self.topics.values()
            if topic.family == family
        ]

    def by_chapter(
        self,
        family: str,
        chapter: str,
    ) -> list[Topic]:
        return [
            topic
            for topic in self.topics.values()
            if topic.family == family
            and topic.chapter == chapter
        ]
    