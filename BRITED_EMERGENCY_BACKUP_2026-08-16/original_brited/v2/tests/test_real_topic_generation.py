from pathlib import Path

from v2.agents.models import PlannedTopic
from v2.pipelines.topic_generation_pipeline import (
    TopicGenerationPipeline,
)


FAMILY = "assurance_vie"
CHAPTER = "fiscalite"

TOPIC_ID = "assurance_vie_fiscalite_rachat_reel_test"


def main():

    print("=" * 60)
    print("REAL TOPIC GENERATION TEST")
    print("=" * 60)

    topic = PlannedTopic(
        id=TOPIC_ID,
        title="Fiscalité du rachat en assurance-vie",
        editorial_order=1,
    )

    pipeline = TopicGenerationPipeline()

    output = (
        pipeline.exporter.output_dir
        / FAMILY
        / CHAPTER
        / f"{TOPIC_ID}.md"
    )

    # Suppression du fichier de test précédent
    # afin de forcer un premier cycle réel complet.
    if output.exists():

        print(
            f"Suppression du Markdown existant : {output}"
        )

        output.unlink()

    print()
    print("Lancement de la génération réelle...")
    print()

    report = pipeline.generate(
        family=FAMILY,
        chapter=CHAPTER,
        topic=topic,
        force=True,
    )

    print()
    print("=" * 60)
    print("RÉSULTAT")
    print("=" * 60)

    print(
        f"Générés : {len(report.generated_files)}"
    )

    print(
        f"Ignorés : {report.skipped}"
    )

    print(
        f"Erreurs : {len(report.errors)}"
    )

    print(
        f"Markdown présent : {output.exists()}"
    )

    if report.generated_files:

        print()
        print("Fichiers générés :")

        for generated_file in report.generated_files:

            print(
                f"- {generated_file}"
            )

    if report.errors:

        print()
        print("Erreurs :")

        for error in report.errors:

            print(
                f"- {error.topic_id}: "
                f"{error.message}"
            )

    if output.exists():

        print()
        print("=" * 60)
        print("CONTENU MARKDOWN")
        print("=" * 60)
        print()

        content = output.read_text(
            encoding="utf-8"
        )

        print(content)


if __name__ == "__main__":

    main()
    