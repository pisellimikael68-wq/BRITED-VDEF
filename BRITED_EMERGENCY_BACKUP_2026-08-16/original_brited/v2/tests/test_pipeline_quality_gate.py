from pathlib import Path

from v2.agents.models import PlannedTopic, WrittenTopic
from v2.pipelines.topic_generation_pipeline import (
    TopicGenerationPipeline,
)


def main():

    pipeline = TopicGenerationPipeline()

    topic = PlannedTopic(
        id="assurance_vie_quality_gate_test",
        title="Test Quality Gate",
        editorial_order=1,
    )

    bad_topic = WrittenTopic(
        id=topic.id,
        title=topic.title,
        summary="Résumé trop court.",
        description="Description trop courte.",
        keywords=["test"],
        vocabulary=["mot"],
        examples=[],
        legal_sources=[],
    )

    def fake_write(**kwargs):
        return bad_topic

    pipeline.writer.write = fake_write

    output = Path(
        "generated/assurance_vie/tests/"
        "assurance_vie_quality_gate_test.md"
    )

    if output.exists():
        output.unlink()

    report = pipeline.generate(
        family="assurance_vie",
        chapter="tests",
        topic=topic,
        force=True,
    )

    print("=" * 60)
    print("QUALITY GATE PIPELINE TEST")
    print("=" * 60)

    print(f"Générés : {report.generated}")
    print(f"Ignorés : {report.skipped}")
    print(f"Erreurs : {report.failed}")
    print(f"Markdown présent : {output.exists()}")

    for error in report.errors:
        print(
            f"- {error.topic_id}: "
            f"{error.message}"
        )


if __name__ == "__main__":
    main()
    