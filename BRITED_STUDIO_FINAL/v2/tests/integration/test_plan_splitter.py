from pathlib import Path

from v2.planning.plan_splitter import PlanSplitter


def main():

    splitter = PlanSplitter()

    splitter.split(
        family="assurance_vie",
    )

    root = (
        Path("v2")
        / "knowledge"
        / "plans"
        / "assurance_vie"
    )

    print()

    print("=" * 60)
    print("CHAPITRES GÉNÉRÉS")
    print("=" * 60)

    for file in sorted(root.glob("*.md")):
        print(file.name)


if __name__ == "__main__":
    main()
    