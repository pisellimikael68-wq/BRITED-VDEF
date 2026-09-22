from v2.studio.engines.planning_engine import PlanningEngine


def main():

    engine = PlanningEngine()

    planning = engine.generate(
        family="assurance_vie",
        weeks=8,
        posts_per_week=3,
    )

    planning.display()


if __name__ == "__main__":
    main()

from v2.knowledge.registry import KnowledgeRegistry

registry = KnowledgeRegistry()

topics = registry.get_topics_by_family("assurance_vie")

chapters = sorted({topic.chapter for topic in topics})

print("\nChapitres disponibles :")

for chapter in chapters:
    print("-", chapter)