from v2.knowledge.registry import KnowledgeRegistry
from v2.models.knowledge_models import Topic


class KnowledgeService:

    def __init__(self):
        self.registry = KnowledgeRegistry()

    def search(self, query: str) -> list[Topic]:
        return self.registry.search(query)

    def by_family(self, family: str) -> list[Topic]:
        return self.registry.get_topics_by_family(family)

    def by_pillar(self, pillar: str) -> list[Topic]:
        return self.registry.get_topics_by_pillar(pillar)

    def priority(self, minimum: int = 8) -> list[Topic]:
        return self.registry.get_priority_topics(minimum)