from v2.models.knowledge_models import Topic


class NavigationEnricher:
    """
    Génère automatiquement :

    - prerequisites
    - next_topics

    ainsi que les relations de navigation du Knowledge Graph.
    """

    def enrich(self, families):

        for family in families:

            for chapter in family.chapters:

                topics = sorted(
                    chapter.topics,
                    key=lambda topic: topic.editorial_order,
                )

                self._link_sequence(topics)

        return families

    # ==========================================================
    # Navigation pédagogique
    # ==========================================================

    def _link_sequence(
        self,
        topics: list[Topic],
    ):

        for index, topic in enumerate(topics):

            # --------------------------------------------------
            # Prerequisite
            # --------------------------------------------------

            if index > 0:

                previous = topics[index - 1]

                if previous.id not in topic.prerequisites:

                    topic.prerequisites.append(previous.id)

                topic.add_relation(
                    target=previous.id,
                    relation_type="prerequisite",
                    score=1.0,
                    source="NavigationEnricher",
                )

            # --------------------------------------------------
            # Next
            # --------------------------------------------------

            if index < len(topics) - 1:

                nxt = topics[index + 1]

                if nxt.id not in topic.next_topics:

                    topic.next_topics.append(nxt.id)

                topic.add_relation(
                    target=nxt.id,
                    relation_type="next",
                    score=1.0,
                    source="NavigationEnricher",
                )
                