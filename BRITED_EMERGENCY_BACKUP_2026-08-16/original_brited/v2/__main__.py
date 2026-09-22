import argparse

from v2.pipelines.family_generation_pipeline import (
    FamilyGenerationPipeline,
)
from v2.pipelines.options import GenerationOptions


def main():

    parser = argparse.ArgumentParser(
        prog="BRITED Studio V2",
    )

    parser.add_argument(
        "family",
        help="Famille de connaissances à générer.",
    )

    parser.add_argument(
        "--chapter",
        action="append",
        help="Limiter la génération à un ou plusieurs chapitres.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Régénérer les fichiers existants.",
    )

    args = parser.parse_args()

    pipeline = FamilyGenerationPipeline()

    report = pipeline.generate(
        family=args.family,
        options=GenerationOptions(
            chapters=args.chapter,
            force=args.force,
        ),
    )

    print(report)

    if report.generated_files:

        print()
        print("FICHIERS GÉNÉRÉS")
        print("-" * 60)

        for file in report.generated_files:
            print(file)


if __name__ == "__main__":
    main()
    