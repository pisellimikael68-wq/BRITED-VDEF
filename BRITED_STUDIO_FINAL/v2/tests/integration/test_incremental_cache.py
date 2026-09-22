from v2.agents.models import PlannedTopic
from v2.pipelines.topic_generation_pipeline import (
    TopicGenerationPipeline,
)


def main():

    pipeline = TopicGenerationPipeline()

    topic = PlannedTopic(
        id="assurance_vie_cache_test",
        title="Définition de l'assurance-vie",
        editorial_order=1,
    )

    print()
    print("=" * 60)
    print("PREMIER LANCEMENT")
    print("=" * 60)

    first_report = pipeline.generate(
        family="assurance_vie",
        chapter="cache_test",
        topic=topic,
    )

    print(
        f"Générés : {first_report.generated} | "
        f"Ignorés : {first_report.skipped} | "
        f"Erreurs : {first_report.failed}"
    )

    print()
    print("=" * 60)
    print("SECOND LANCEMENT")
    print("=" * 60)

    second_report = pipeline.generate(
        family="assurance_vie",
        chapter="cache_test",
        topic=topic,
    )

    print(
        f"Générés : {second_report.generated} | "
        f"Ignorés : {second_report.skipped} | "
        f"Erreurs : {second_report.failed}"
    )


if __name__ == "__main__":
    main()
    