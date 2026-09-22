from pathlib import Path

from v2.agents.models import (
    PlannedChapter,
    PlannedFamily,
    PlannedTopic,
)


class MarkdownPlanLoader:
    """
    Charge une famille de connaissances à partir des plans
    éditoriaux Markdown.
    """

    def load(
        self,
        family: str,
    ) -> PlannedFamily:

        root = (
            Path("v2")
            / "knowledge"
            / "plans"
            / family
        )

        if not root.exists():
            raise FileNotFoundError(
                f"Plan introuvable : {root}"
            )

        planned_family = PlannedFamily(
            pillar="",
            name=family,
        )

        for md_file in sorted(root.glob("*.md")):

            chapter = PlannedChapter(
                name=md_file.stem,
            )

            lines = md_file.read_text(
                encoding="utf-8",
            ).splitlines()

            editorial_order = 1

            for line in lines:

                line = line.strip()

                if not line.startswith("## "):
                    continue

                topic_id = line.removeprefix("## ").strip()

                title = (
                    topic_id
                    .replace("_", " ")
                    .replace("-", " ")
                    .title()
                )

                chapter.topics.append(
                    PlannedTopic(
                        id=topic_id,
                        title=title,
                        editorial_order=editorial_order,
                    )
                )

                editorial_order += 1

            planned_family.chapters.append(chapter)

        return planned_family
    