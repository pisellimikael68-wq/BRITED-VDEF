from tests.subjects import SUBJECTS
from v2.pipelines.instagram_pipeline import InstagramPipeline


def main():

    pipeline = InstagramPipeline()

    print("\n==============================")
    print("      BRITED BENCHMARK")
    print("==============================\n")

    scores = []

    for subject in SUBJECTS:

        print(f"\nSujet : {subject}")

        context = pipeline.run(subject)

        score = context.review.score

        scores.append(score)

        print(f"Score : {score}/100")

    average = sum(scores) / len(scores)

    print("\n==============================")
    print(f"Score moyen : {average:.1f}/100")
    print("==============================\n")


if __name__ == "__main__":
    main()
    