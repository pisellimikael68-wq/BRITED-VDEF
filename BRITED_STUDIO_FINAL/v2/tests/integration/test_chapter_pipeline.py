from v2.agents.planner.planner import PlannerAgent
from v2.pipelines.chapter_generation_pipeline import ChapterGenerationPipeline


def main():

    planner = PlannerAgent()

    family = planner.plan(
        family="assurance_vie",
    )

    chapter = next(
        c
        for c in family.chapters
        if c.name == "fondamentaux"
    )

    pipeline = ChapterGenerationPipeline()

    files = pipeline.generate(
        family=family.name,
        chapter=chapter,
    )

    print()

    print("=" * 60)
    print("CHAPITRE GÉNÉRÉ")
    print("=" * 60)

    for file in files:
        print(file)


if __name__ == "__main__":
    main()
    