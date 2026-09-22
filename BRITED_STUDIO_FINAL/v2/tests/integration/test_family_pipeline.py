from v2.pipelines.family_generation_pipeline import (
    FamilyGenerationPipeline,
)
from v2.pipelines.options import GenerationOptions


def main():

    pipeline = FamilyGenerationPipeline()

    report = pipeline.generate(
        family="assurance_vie",
        options=GenerationOptions(
            chapters=[
                "fondamentaux",
            ],
            force=False,
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
    