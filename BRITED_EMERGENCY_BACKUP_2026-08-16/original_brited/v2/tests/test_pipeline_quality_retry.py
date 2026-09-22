from pathlib import Path

from v2.agents.models import PlannedTopic, WrittenTopic
from v2.pipelines.topic_generation_pipeline import (
    TopicGenerationPipeline,
)


def build_weak_topic(topic_id: str) -> WrittenTopic:

    return WrittenTopic(
        id=topic_id,
        title="Test faible",
        summary="Résumé trop court.",
        description="Description trop courte.",
        keywords=["test"],
        vocabulary=["test"],
        examples=[],
        legal_sources=[],
        prompt_hash="test",
    )


def build_valid_topic(topic_id: str) -> WrittenTopic:

    return WrittenTopic(
        id=topic_id,
        title="Test corrigé",
        summary=(
            "Ce résumé présente de manière suffisamment développée "
            "le mécanisme patrimonial étudié ainsi que ses principaux "
            "enjeux juridiques, fiscaux et opérationnels."
        ),
        description=(
            "Cette description développe précisément le mécanisme étudié. "
            "Elle expose son fonctionnement, son intérêt patrimonial, "
            "les conditions nécessaires à sa mise en œuvre ainsi que les "
            "principaux points de vigilance. Elle permet également de "
            "comprendre les conséquences juridiques et fiscales du dispositif "
            "dans une logique pédagogique et professionnelle suffisamment "
            "détaillée pour satisfaire les exigences du contrôle qualité."
        ),
        keywords=[
            "assurance-vie",
            "fiscalité",
            "patrimoine",
        ],
        vocabulary=[
            "souscripteur",
            "bénéficiaire",
        ],
        examples=[
            (
                "Un souscripteur verse 100 000 euros sur un contrat "
                "d'assurance-vie afin d'illustrer le mécanisme étudié."
            )
        ],
        legal_sources=[
            "Code des assurances, article L132-12"
        ],
        prompt_hash="test",
    )


def main():

    pipeline = TopicGenerationPipeline()

    topic = PlannedTopic(
        id="assurance_vie_quality_retry_test",
        title="Test Quality Retry",
        editorial_order=1,
    )

    output = Path(
        "generated/assurance_vie/tests/"
        "assurance_vie_quality_retry_test.md"
    )

    if output.exists():
        output.unlink()

    calls = {
        "write": 0,
        "correct": 0,
        "quality_issues": None,
    }

    def fake_write(
        *,
        family,
        chapter,
        topic,
    ):

        calls["write"] += 1

        return build_weak_topic(topic.id)

    def fake_correct(
        *,
        family,
        chapter,
        topic,
        written,
        quality_issues,
    ):

        calls["correct"] += 1
        calls["quality_issues"] = quality_issues

        return build_valid_topic(topic.id)

    pipeline.writer.write = fake_write
    pipeline.writer.correct = fake_correct

    report = pipeline.generate(
        family="assurance_vie",
        chapter="tests",
        topic=topic,
        force=True,
    )

    print("=" * 60)
    print("GUIDED QUALITY RETRY TEST")
    print("=" * 60)

    print(f"Appels write   : {calls['write']}")
    print(f"Appels correct : {calls['correct']}")
    print(
        "Anomalies transmises :",
        calls["quality_issues"],
    )

    print(f"Générés : {len(report.generated_files)}")
    print(f"Ignorés : {report.skipped}")
    print(f"Erreurs : {len(report.errors)}")
    print(f"Markdown présent : {output.exists()}")

    for error in report.errors:
        print(
            f"- {error.topic_id}: {error.message}"
        )


if __name__ == "__main__":
    main()
    