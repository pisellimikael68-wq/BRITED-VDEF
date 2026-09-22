from pathlib import Path

from v2.agents.models import PlannedTopic
from v2.pipelines.topic_generation_pipeline import (
    TopicGenerationPipeline,
)


def main():

    topic = PlannedTopic(
        id=(
            "assurance_vie_fiscalite_"
            "rachat_legal_tax_test"
        ),
        title="Fiscalité du rachat en assurance-vie",
        editorial_order=1,
    )

    family = "assurance_vie"
    chapter = "fiscalite"

    pipeline = TopicGenerationPipeline()

    output = (
        pipeline.exporter.output_dir
        / family
        / chapter
        / f"{topic.id}.md"
    )

    # Suppression du Markdown précédent afin de forcer
    # un véritable test de génération end-to-end.
    if output.exists():
        output.unlink()

    print("=" * 60)
    print("REAL LEGAL & TAX GATE TEST")
    print("=" * 60)

    print()
    print("Lancement de la génération réelle...")
    print()

    report = pipeline.generate(
        family=family,
        chapter=chapter,
        topic=topic,
        force=True,
    )

    print()
    print("=" * 60)
    print("RÉSULTAT")
    print("=" * 60)

    print(
        f"Générés : "
        f"{len(report.generated_files)}"
    )

    print(
        f"Ignorés : "
        f"{report.skipped}"
    )

    print(
        f"Erreurs : "
        f"{len(report.errors)}"
    )

    print(
        f"Markdown présent : "
        f"{output.exists()}"
    )

    if report.generated_files:

        print()
        print("Fichiers générés :")

        for generated_file in report.generated_files:
            print(f"- {generated_file}")

    if report.errors:

        print()
        print("Erreurs :")

        for error in report.errors:

            print(
                f"- {error.topic_id}: "
                f"{error.message}"
            )

    if output.exists():

        content = output.read_text(
            encoding="utf-8"
        )

        print()
        print("=" * 60)
        print("CONTRÔLES KNOWLEDGE BRIDGE")
        print("=" * 60)

        checks = {
            "27 septembre 2017": (
                "27 septembre 2017"
                in content
            ),
            "150 000": (
                "150 000"
                in content
            ),
            "Rachat partiel": (
                "rachat partiel"
                in content.lower()
            ),
            "Produits": (
                "produits"
                in content.lower()
            ),
            "Primes versées": (
                "primes versées"
                in content.lower()
            ),
            "Provenance interne absente": (
                "pierre_louis_gomet_notes"
                not in content
            ),
            "Knowledge Base absente": (
                "knowledge base"
                not in content.lower()
            ),
            "Socle académique absent": (
                "socle académique"
                not in content.lower()
            ),
        }

        for label, result in checks.items():

            print(
                f"{label:<32} : "
                f"{result}"
            )

        print()
        print("=" * 60)
        print("CONTENU MARKDOWN")
        print("=" * 60)

        print(content)


if __name__ == "__main__":
    main()
    