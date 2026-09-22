from typing import TYPE_CHECKING

from v2.models.knowledge_models import Topic

if TYPE_CHECKING:
    from .graph_engine import GraphEngine


class RecommendationEngine:
    """
    Recommande les meilleurs topics à partir
    du Knowledge Graph.
    """

    def __init__(
        self,
        engine: "GraphEngine",
    ):
        self.engine = engine

    def recommend(
        self,
        topic_id: str,
        limit: int = 5,
    ) -> list[Topic]:

        topic = self.engine.topic(topic_id)

        if topic is None:
            return []

        ranked = sorted(
            topic.relations,
            key=lambda relation: relation.score,
            reverse=True,
        )

        recommendations = []

        for relation in ranked:

            candidate = self.engine.topic(relation.target)

            if candidate is not None:
                recommendations.append(candidate)

            if len(recommendations) >= limit:
                break

        return recommendations
    