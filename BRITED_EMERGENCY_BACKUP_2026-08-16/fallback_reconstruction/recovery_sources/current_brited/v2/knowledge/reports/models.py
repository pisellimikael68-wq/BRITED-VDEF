from dataclasses import dataclass, field


@dataclass(slots=True)
class KnowledgeReport:

    topic_count: int = 0
    relation_count: int = 0

    average_degree: float = 0.0
    min_degree: int = 0
    max_degree: int = 0

    relation_types: dict[str, int] = field(default_factory=dict)

    topics_with_description: int = 0
    topics_with_keywords: int = 0
    topics_with_vocabulary: int = 0
    topics_with_examples: int = 0
    topics_with_sources: int = 0

    duplicate_ids: int = 0
    missing_links: int = 0
    orphan_topics: int = 0
    cycles: int = 0

    knowledge_score: int = 0
    