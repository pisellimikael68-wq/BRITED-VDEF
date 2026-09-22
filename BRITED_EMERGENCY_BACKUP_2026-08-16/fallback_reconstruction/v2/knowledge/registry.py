from collections import defaultdict

from v2.knowledge.taxonomy import PILLARS
from v2.knowledge.topics import ALL_TOPICS
from v2.models.knowledge_models import Topic


class KnowledgeRegistry:

    def __init__(self):

        self.pillars = PILLARS
        self.topics: list[Topic] = ALL_TOPICS

        # ==========================================================
        # INDEX
        # ==========================================================

        self.topics_by_id: dict[str, Topic] = {}

        self.topics_by_family: dict[str, list[Topic]] = defaultdict(list)

        self.topics_by_pillar: dict[str, list[Topic]] = defaultdict(list)

        self.topics_by_chapter: dict[tuple[str, str], list[Topic]] = defaultdict(list)

        for topic in self.topics:

            self.topics_by_id[topic.id] = topic

            self.topics_by_family[topic.family].append(topic)

            self.topics_by_pillar[topic.pillar].append(topic)

            self.topics_by_chapter[
                (topic.family, topic.chapter)
            ].append(topic)

    # ==========================================================
    # TOPIC
    # ==========================================================

    def get_topic(
        self,
        topic_id: str,
    ) -> Topic | None:

        return self.topics_by_id.get(topic_id)

    def exists(
        self,
        topic_id: str,
    ) -> bool:

        return topic_id in self.topics_by_id

    # ==========================================================
    # FAMILY
    # ==========================================================

    def get_topics_by_family(
        self,
        family: str,
    ) -> list[Topic]:

        return self.topics_by_family.get(family, [])

    # ==========================================================
    # CHAPTER
    # ==========================================================

    def get_topics_by_chapter(
        self,
        family: str,
        chapter: str,
    ) -> list[Topic]:

        return self.topics_by_chapter.get(
            (family, chapter),
            [],
        )

    # ==========================================================
    # PILLAR
    # ==========================================================

    def get_topics_by_pillar(
        self,
        pillar: str,
    ) -> list[Topic]:

        return self.topics_by_pillar.get(pillar, [])

    # ==========================================================
    # DIFFICULTY
    # ==========================================================

    def get_topics_by_difficulty(
        self,
        difficulty: str,
    ) -> list[Topic]:

        difficulty = difficulty.lower()

        return [

            topic

            for topic in self.topics

            if topic.difficulty.lower() == difficulty

        ]

    # ==========================================================
    # PRIORITY
    # ==========================================================

    def get_priority_topics(
        self,
        minimum: int = 8,
    ) -> list[Topic]:

        return [

            topic

            for topic in self.topics

            if topic.priority >= minimum

        ]

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(
        self,
        keyword: str,
    ) -> list[Topic]:

        keyword = keyword.lower()

        results: list[Topic] = []

        for topic in self.topics:

            searchable = [

                topic.title,

                topic.description,

                *topic.keywords,

                *topic.client_questions,

                *topic.misconceptions,

                *topic.common_mistakes,

                *topic.analogies,

                *topic.key_points,

                *topic.examples,

                *topic.vocabulary,

            ]

            if any(

                keyword in value.lower()

                for value in searchable

            ):

                results.append(topic)

        return results

    # ==========================================================
    # PILLARS
    # ==========================================================

    def get_pillar(
        self,
        pillar_id: str,
    ) -> dict | None:

        for pillar in self.pillars:

            if pillar["id"] == pillar_id:

                return pillar

        return None

    def get_all_pillars(
        self,
    ) -> list[dict]:

        return self.pillars
    