from v2.knowledge.registry import KnowledgeRegistry
from v2.studio.engines.angle_engine import AngleEngine


def main():

    registry = KnowledgeRegistry()
    engine = AngleEngine()

    topics = registry.get_topics_by_family("assurance_vie")

    for topic in topics[:20]:
        angle = engine.select(topic)
        print(f"{topic.title} → {angle.value}")


if __name__ == "__main__":
    main()

    