from v2.knowledge.registry import KnowledgeRegistry
from v2.models.knowledge_models import Topic
from v2.studio.models.planning import Planning, PlanningWeek
from v2.studio.strategy.editorial_order import EDITORIAL_ORDER


class PlanningEngine:
    """
    Génère un planning éditorial à partir de la Knowledge Base.
    """

    def __init__(self):
        self.registry = KnowledgeRegistry()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        family: str,
        weeks: int,
        posts_per_week: int,
    ) -> Planning:

        topics = self._load_topics(family)

        topics = self._rank_topics(topics)

        planning_weeks = self._build_weeks(
            topics=topics,
            weeks=weeks,
            posts_per_week=posts_per_week,
        )

        return Planning(
            family=family,
            weeks=planning_weeks,
        )

    # ==========================================================
    # LOAD TOPICS
    # ==========================================================

    def _load_topics(
        self,
        family: str,
    ) -> list[Topic]:

        return self.registry.get_topics_by_family(family)

    # ==========================================================
    # RANK TOPICS
    # ==========================================================

    def _rank_topics(
        self,
        topics: list[Topic],
    ) -> list[Topic]:
        """
        Trie les Topics selon la progression pédagogique BRITED.
        """

        chapter_order = {
            chapter: index
            for index, chapter in enumerate(EDITORIAL_ORDER)
        }

        difficulty_order = {
            "débutant": 0,
            "beginner": 0,
            "intermédiaire": 1,
            "intermediate": 1,
            "avancé": 2,
            "advanced": 2,
        }

        ranked_topics = sorted(
            topics,
            key=lambda topic: (
                chapter_order.get(topic.chapter, 999),
                topic.editorial_order,
                -topic.priority,
                difficulty_order.get(
                    topic.difficulty.lower(),
                    99,
                ),
            ),
        )

        return ranked_topics

    # ==========================================================
    # BUILD WEEKS
    # ==========================================================

    def _build_weeks(
        self,
        topics: list[Topic],
        weeks: int,
        posts_per_week: int,
    ) -> list[PlanningWeek]:

        planning: list[PlanningWeek] = []

        index = 0

        for week in range(1, weeks + 1):

            week_topics = topics[
                index:index + posts_per_week
            ]

            if not week_topics:
                break

            planning.append(
                PlanningWeek(
                    week=week,
                    topics=week_topics,
                )
            )

            index += posts_per_week

        return planning
    
