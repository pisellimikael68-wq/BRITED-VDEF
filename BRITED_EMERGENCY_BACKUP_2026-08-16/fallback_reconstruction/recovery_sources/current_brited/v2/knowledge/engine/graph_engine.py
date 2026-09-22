from v2.knowledge.registry import KnowledgeRegistry
from v2.models.knowledge_models import Topic

from .recommendation_engine import RecommendationEngine
from .traversal import GraphTraversal


class GraphEngine:
    """
    Point d'entrée unique du Knowledge Graph.
    """

    def __init__(
        self,
        registry: KnowledgeRegistry,
    ):

        self.registry = registry
        self.traversal = GraphTraversal(self)
        self.recommendation = RecommendationEngine(self)

    # ==========================================================
    # Topic
    # ==========================================================

    def topic(
        self,
        topic_id: str,
    ) -> Topic | None:

        return self.registry.get_topic(topic_id)

    # ==========================================================
    # Exists
    # ==========================================================

    def exists(
        self,
        topic_id: str,
    ) -> bool:

        return self.topic(topic_id) is not None

    # ==========================================================
    # Neighbors
    # ==========================================================

    def neighbors(
        self,
        topic_id: str,
    ) -> list[Topic]:

        topic = self.topic(topic_id)

        if topic is None:
            return []

        neighbors = []

        for relation in topic.relations:

            other = self.topic(relation.target)

            if other is not None:
                neighbors.append(other)

        return neighbors

    # ==========================================================
    # Reachable
    # ==========================================================

    def reachable(
        self,
        topic_id: str,
        max_depth: int = 2,
    ) -> list[Topic]:

        ids = self.traversal.reachable(
            topic_id,
            max_depth=max_depth,
        )

        return [

            self.topic(topic_id)

            for topic_id in ids

            if self.topic(topic_id) is not None

        ]

    # ==========================================================
    # Shortest Path
    # ==========================================================

    def shortest_path(
        self,
        source: str,
        target: str,
    ) -> list[Topic]:

        ids = self.traversal.shortest_path(
            source,
            target,
        )

        return [

            self.topic(topic_id)

            for topic_id in ids

            if self.topic(topic_id) is not None

        ]

    # ==========================================================
    # Recommendation
    # ==========================================================

    def recommend(
        self,
        topic_id: str,
        limit: int = 5,
    ) -> list[Topic]:

        return self.recommendation.recommend(
            topic_id,
            limit=limit,
        )

    # ==========================================================
    # Degree
    # ==========================================================

    def degree(
        self,
        topic_id: str,
    ) -> int:

        topic = self.topic(topic_id)

        if topic is None:
            return 0

        return len(topic.relations)
    