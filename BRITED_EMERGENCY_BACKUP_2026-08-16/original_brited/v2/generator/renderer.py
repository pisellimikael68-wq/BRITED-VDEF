from pathlib import Path

from .models import ChapterDefinition


def render_python(chapter: ChapterDefinition, output_path: str | Path):
    output_path = Path(output_path)

    lines = []

    lines.append("from v2.knowledge.models import Topic")
    lines.append("")
    lines.append("")
    lines.append(
        f"{chapter.chapter.upper()}_TOPICS = ["
    )

    for topic in chapter.topics:

        lines.append("    Topic(")
        lines.append(f'        id="{topic.id}",')
        lines.append(f'        title="{topic.title}",')
        lines.append(f'        pillar="{chapter.pillar}",')
        lines.append(f'        family="{chapter.family}",')
        lines.append(f'        chapter="{chapter.chapter}",')
        lines.append('        description="",')
        lines.append('        objective="",')
        lines.append(f'        difficulty="{topic.difficulty}",')
        lines.append(f"        priority={topic.priority},")
        lines.append(
            f"        editorial_order={topic.editorial_order},"
        )
        lines.append("    ),")
        lines.append("")

    lines.append("]")

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
    