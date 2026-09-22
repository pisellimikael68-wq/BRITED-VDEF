from v2.agents.models import PlannedTopic
from v2.pipelines.topic_generation_pipeline import TopicGenerationPipeline


def main():

    pipeline = TopicGenerationPipeline()

    topic = PlannedTopic(
        id="definition",
        title="Définition de l'assurance-vie",
        editorial_order=1,
    )

    path = pipeline.generate(
        family="assurance_vie",
        chapter="fondamentaux",
        topic=topic,
    )

    print(f"\n✅ Markdown généré : {path}")


if __name__ == "__main__":
    main()
    