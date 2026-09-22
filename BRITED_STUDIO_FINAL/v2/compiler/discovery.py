from pathlib import Path

CONTENT_ROOT = Path("content")


def discover_families() -> list[Path]:
    return sorted(
        p
        for p in CONTENT_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


def discover_chapters(family: Path) -> list[Path]:
    """
    Retourne uniquement les chapitres Markdown non vides.
    """

    chapters = []

    for chapter in family.glob("*.md"):

        if chapter.name == "master_plan.md":
            continue

        if chapter.stat().st_size == 0:
            continue

        chapters.append(chapter)

    return sorted(chapters)
    