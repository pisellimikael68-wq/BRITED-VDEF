from v2.models.knowledge_models import Topic


class RelationshipEnricher:
    """
    Génère des relations structurelles de proximité.

    Un topic est relié uniquement aux sujets
    pédagogiquement proches (±2 positions).
    """

    WINDOW_SIZE = 2

    def enrich(self, families):

        for family in families:

            for chapter in family.chapters:

                topics = sorted(
                    chapter.topics,
                    key=lambda topic: topic.editorial_order,
                )

                self._link_window(topics)

        return families

    # ==========================================================
    # Fenêtre pédagogique
    # ==========================================================

    def _link_window(
        self,
        topics: list[Topic],
    ):

        for index, topic in enumerate(topics):

            start = max(0, index - self.WINDOW_SIZE)
            end = min(len(topics), index + self.WINDOW_SIZE + 1)

            for other in topics[start:end]:

                if other.id == topic.id:
                    continue

                # -----------------------------
                # Compatibilité V1
                # -----------------------------

                if other.id not in topic.related_topics:

                    topic.related_topics.append(other.id)

                # -----------------------------
                # Distance pédagogique
                # -----------------------------

                distance = abs(index - topics.index(other))

                score = {
                    1: 0.95,
                    2: 0.80,
                }.get(distance, 0.60)

                topic.add_relation(
                    target=other.id,
                    relation_type="chapter",
                    score=score,
                    source="RelationshipEnricher",
                )
                