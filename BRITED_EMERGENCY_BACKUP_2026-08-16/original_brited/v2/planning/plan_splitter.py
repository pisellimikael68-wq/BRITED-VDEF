from pathlib import Path
from v2.core.slug import slugify
import re


class PlanSplitter:
    """
    Découpe un plan éditorial maître en un fichier Markdown
    par chapitre.

    Source :
        v2/knowledge/plans/assurance_vie_plan.md

    Cible :
        v2/knowledge/plans/assurance_vie/
            fondamentaux.md
            ouverture.md
            fonctionnement.md
            ...
    """

    def split(
        self,
        *,
        family: str,
    ) -> None:

        source = (
            Path("v2")
            / "knowledge"
            / "plans"
            / f"{family}_plan.md"
        )

        if not source.exists():
            raise FileNotFoundError(source)

        destination = (
            Path("v2")
            / "knowledge"
            / "plans"
            / family
        )

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        text = source.read_text(
            encoding="utf-8",
        )

        sections = re.split(
            r"(?m)^# CHAPITRE \d+\s*$",
            text,
        )

        # La première section contient uniquement l'en-tête du document.
        for section in sections[1:]:

            lines = section.strip().splitlines()

            if not lines:
                continue

            chapter_name = None
            topics = []

            for line in lines:

                line = line.strip()

                if line.startswith("## "):
                    chapter_name = slugify(
                        line.removeprefix("## ").strip()
                    )
                    chapter_name = {
                        "supports_d_investissement": "supports_investissement",
                    }.get(chapter_name, chapter_name)
                    continue

                if line.startswith("| assurance_"):
                    columns = [
                        c.strip()
                        for c in line.strip("|").split("|")
                    ]

                    if columns:
                        topics.append(columns[0])

            if not chapter_name:
                continue

            output = destination / f"{chapter_name}.md"

            content = [
                f"# {chapter_name.replace('_', ' ').title()}",
                "",
            ]

            for topic in topics:
                content.append(f"## {topic}")

            output.write_text(
                "\n".join(content),
                encoding="utf-8",
            )

        print(
            f"✅ Plan '{family}' découpé dans {destination}"
        )


if __name__ == "__main__":

    PlanSplitter().split(
        family="assurance_vie",
    )
