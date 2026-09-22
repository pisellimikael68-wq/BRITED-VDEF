from pathlib import Path
import csv

from .models import RawChapter, RawTopic
from .families import FAMILY_TO_PILLAR


def parse_chapter(path: Path) -> RawChapter:
    """
    Parse un chapitre Markdown et retourne un RawChapter.
    """

    family = path.parent.name
    chapter = path.stem

    pillar = FAMILY_TO_PILLAR.get(family, "inconnu")

    table_lines = []

    with open(path, encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line.startswith("|"):
                continue

            # Ignore la ligne de séparation Markdown
            if set(
                line.replace("|", "")
                    .replace("-", "")
                    .replace(":", "")
                    .strip()
            ) == set():
                continue

            table_lines.append(line)

    reader = csv.reader(
        table_lines,
        delimiter="|",
    )

    rows = []

    for row in reader:

        row = [cell.strip() for cell in row if cell.strip()]

        if row:
            rows.append(row)

    # --------------------------------------------------
    # Aucun tableau détecté
    # --------------------------------------------------

    if not rows:
        return RawChapter(
            pillar=pillar,
            family=family,
            chapter=chapter,
            topics=[],
        )

    header = rows[0]

    topics = []

    for values in rows[1:]:

        data = dict(zip(header, values))

        topics.append(

            RawTopic(

                id=data["id"],

                title=data["title"],

                editorial_order=int(data["editorial_order"]),

                difficulty=data["difficulty"],

                priority=int(data["priority"]),

            )

        )

    return RawChapter(

        pillar=pillar,

        family=family,

        chapter=chapter,

        topics=topics,

    )
