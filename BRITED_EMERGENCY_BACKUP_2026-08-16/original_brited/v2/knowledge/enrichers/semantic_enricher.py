from collections import defaultdict

from v2.models.knowledge_models import Topic


class SemanticEnricher:
    """
    Construit un index sémantique et crée
    automatiquement les relations entre topics
    proches.
    """

    MIN_SIMILARITY = 0.35

    def enrich(self, families):

        keyword_index = defaultdict(set)

        all_topics: list[Topic] = []

        for family in families:

            for chapter in family.chapters:

                all_topics.extend(chapter.topics)

                for topic in chapter.topics:

                    self._index_text(
                        keyword_index,
                        topic.id,
                        topic.title,
                    )

                    self._index_iterable(
                        keyword_index,
                        topic.id,
                        topic.keywords,
                    )

                    self._index_iterable(
                        keyword_index,
                        topic.id,
                        topic.vocabulary,
                    )

        self.keyword_index = keyword_index

        self.topics = {
            topic.id: topic
            for topic in all_topics
        }

        self._create_semantic_relations()

        return families

    # ==========================================================
    # Construction des relations
    # ==========================================================

    def _create_semantic_relations(self):

        for topic in self.topics.values():

            candidates = self._candidate_topics(topic)

            for candidate in candidates:

                if candidate.id == topic.id:
                    continue

                score = self.similarity(topic, candidate)

                if score < self.MIN_SIMILARITY:
                    continue

                if any(
                    relation.target == candidate.id
                    and relation.relation_type == "semantic"
                    for relation in topic.relations
                ):
                    continue

                topic.add_relation(
                    target=candidate.id,
                    relation_type="semantic",
                    score=round(score, 3),
                    source="SemanticEnricher",
                )

    # ==========================================================
    # Recherche des candidats
    # ==========================================================

    def _candidate_topics(
        self,
        topic: Topic,
    ) -> list[Topic]:

        candidates = set()

        for word in self._topic_words(topic):

            for topic_id in self.keyword_index.get(word, ()):

                if topic_id != topic.id:

                    candidates.add(topic_id)

        return [
            self.topics[topic_id]
            for topic_id in sorted(candidates)
        ]

    # ==========================================================
    # Similarité
    # ==========================================================

    def similarity(
        self,
        topic_a: Topic,
        topic_b: Topic,
    ) -> float:

        words_a = self._topic_words(topic_a)
        words_b = self._topic_words(topic_b)

        if not words_a or not words_b:
            return 0.0

        intersection = words_a & words_b
        union = words_a | words_b

        return len(intersection) / len(union)

    # ==========================================================
    # Extraction des mots
    # ==========================================================

    def _topic_words(
        self,
        topic: Topic,
    ) -> set[str]:

        words = set()

        self._collect_text(words, topic.title)

        for value in topic.keywords:
            self._collect_text(words, value)

        for value in topic.vocabulary:
            self._collect_text(words, value)

        return words

    def _collect_text(
        self,
        words: set[str],
        text: str,
    ):

        if not text:
            return

        for word in text.lower().split():

            word = word.strip(" ,.;:!?()[]{}\"'")

            if len(word) >= 3:

                words.add(word)

    # ==========================================================
    # Index
    # ==========================================================

    def _index_text(
        self,
        index,
        topic_id,
        text,
    ):

        if not text:
            return

        for word in text.lower().split():

            word = word.strip(" ,.;:!?()[]{}\"'")

            if len(word) >= 3:

                index[word].add(topic_id)

    def _index_iterable(
        self,
        index,
        topic_id,
        values,
    ):

        for value in values:

            self._index_text(
                index,
                topic_id,
                value,
            )
            