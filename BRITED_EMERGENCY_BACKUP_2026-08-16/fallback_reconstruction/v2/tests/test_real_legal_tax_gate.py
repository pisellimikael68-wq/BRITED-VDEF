from pathlib import Path

from v2.agents.models import PlannedTopic
from v2.pipelines.topic_generation_pipeline import (
    TopicGenerationPipeline,
)


def main():

    print("=" * 60)
    print("REAL LEGAL & TAX GATE TEST")
    print("=" * 60)

    topic = PlannedTopic(
        id="assurance_vie_fiscalite_rachat_legal_tax_test",
        title="Fiscalité du rachat en assurance-vie",
        editorial_order=1,
    )

    pipeline = TopicGenerationPipeline()

    output = Path(
        "generated/assurance_vie/fiscalite/"
        "assurance_vie_fiscalite_rachat_legal_tax_test.md"
    )

    if output.exists():
        output.unlink()

    print("\nLancement de la génération réelle...\n")

    report = pipeline.generate(
        family="assurance_vie",
        chapter="fiscalite",
        topic=topic,
        force=True,
    )

    print("\n" + "=" * 60)
    print("RÉSULTAT")
    print("=" * 60)

    print(f"Générés : {len(report.generated_files)}")
    print(f"Ignorés : {report.skipped}")
    print(f"Erreurs : {len(report.errors)}")
    print(f"Markdown présent : {output.exists()}")

    if report.errors:

        print("\nErreurs :")

        for error in report.errors:
            print(
                f"- {error.topic_id}: "
                f"{error.message}"
            )

    if output.exists():

        print("\n" + "=" * 60)
        print("CONTENU MARKDOWN")
        print("=" * 60)

        print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
    