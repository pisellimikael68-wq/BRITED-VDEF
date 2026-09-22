import csv
import time
from datetime import datetime
from pathlib import Path

from v2.tests.subjects import SUBJECTS
from v2.pipelines.instagram import InstagramPipeline


def main():

    pipeline = InstagramPipeline()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    output_dir = Path("outputs/benchmarks")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"benchmark_{timestamp}.csv"

    print("\n==========================================")
    print("           BRITED BENCHMARK")
    print("==========================================")

    rows = []

    scores = []
    execution_times = []

    for subject in SUBJECTS:

        print(f"\nSujet : {subject}")
        print("-" * 50)

        start = time.perf_counter()

        context = pipeline.run(subject)

        elapsed = time.perf_counter() - start

        score = context.review.score

        rows.append({
            "subject": subject,
            "score": score,
            "execution_time": round(elapsed, 2),
        })

        scores.append(score)
        execution_times.append(elapsed)

        print(
            f"Score : {score}/100 | Temps : {elapsed:.2f} s"
        )

    with open(output_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "subject",
                "score",
                "execution_time",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    average_score = sum(scores) / len(scores)
    average_time = sum(execution_times) / len(execution_times)

    best = max(rows, key=lambda r: r["score"])
    worst = min(rows, key=lambda r: r["score"])

    fastest = min(rows, key=lambda r: r["execution_time"])
    slowest = max(rows, key=lambda r: r["execution_time"])

    excellent = len([r for r in rows if r["score"] >= 95])
    good = len([r for r in rows if 90 <= r["score"] < 95])
    weak = len([r for r in rows if r["score"] < 90])

    print("\n==========================================")
    print("         BRITED DASHBOARD")
    print("==========================================")

    print("\n📊 Général")
    print(f"Nombre de sujets : {len(rows)}")
    print(f"Score moyen      : {average_score:.1f}/100")
    print(f"Temps moyen      : {average_time:.2f} s")

    print("\n🏆 Meilleur sujet")
    print(f"{best['subject']} ({best['score']}/100)")

    print("\n⚠️ Sujet le plus faible")
    print(f"{worst['subject']} ({worst['score']}/100)")

    print("\n📈 Répartition")
    print(f"95-100 : {excellent}")
    print(f"90-94  : {good}")
    print(f"<90    : {weak}")

    print("\n⚡ Performances")
    print(
        f"Plus rapide : {fastest['subject']} ({fastest['execution_time']:.2f} s)"
    )
    print(
        f"Plus lent   : {slowest['subject']} ({slowest['execution_time']:.2f} s)"
    )

    print(f"\n📄 CSV exporté : {output_path}")

    print("\n==========================================")
    print(f"Benchmark exécuté le {timestamp}")
    print("==========================================")


if __name__ == "__main__":
    main()
    