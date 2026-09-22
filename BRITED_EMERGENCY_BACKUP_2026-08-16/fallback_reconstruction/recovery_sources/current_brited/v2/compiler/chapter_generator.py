from pathlib import Path


ASSURANCE_VIE_CHAPTERS = [
    "fondamentaux",
    "contrats",
    "fonctionnement",
    "supports_investissement",
    "gestion",
    "versements",
    "arbitrages",
    "rachats",
    "avances",
    "nantissement",
    "fiscalite_generale",
    "fiscalite_avant_8_ans",
    "fiscalite_apres_8_ans",
    "prelevements_sociaux",
    "ifi",
    "clause_beneficiaire",
    "transmission",
    "demembrement",
    "succession",
    "assurance_vie_luxembourgeoise",
    "conformite",
    "cas_pratiques",
]


def generate_family(
    family: str,
    chapters: list[str],
):

    root = (
        Path("v2")
        / "knowledge"
        / "plans"
        / "v2"
        / "knowledge"
        / family
    )

    root.mkdir(parents=True, exist_ok=True)

    for chapter in chapters:

        path = root / f"{chapter}.md"

        if path.exists():
            print(f"⏭ {chapter}")
            continue

        path.write_text(
f"""---
pillar: epargne
family: {family}
chapter: {chapter}
---

# {chapter.replace("_", " ").title()}

""",
            encoding="utf-8",
        )

        print(f"✅ {chapter}")


if __name__ == "__main__":

    generate_family(
        "assurance_vie",
        ASSURANCE_VIE_CHAPTERS,
    )
    