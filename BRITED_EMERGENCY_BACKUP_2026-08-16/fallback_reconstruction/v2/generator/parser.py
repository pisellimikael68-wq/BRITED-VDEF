import re

from pathlib import Path

from .models import ChapterDefinition, TopicDefinition


def parse_markdown(path: str | Path) -> ChapterDefinition:
    path = Path(path)

    content = path.read_text(encoding="utf-8")

    metadata = {}

    metadata_match = re.search(
        r"## Metadata(.*?)## Topics",
        content,
        re.DOTALL,
    )

    if metadata_match:
        for line in metadata_match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

    chapter = ChapterDefinition(
        family=metadata["family"],
        chapter=metadata["chapter"],
        pillar=metadata["pillar"],
        title=path.stem.replace("_", " ").title(),
    )

    topic_pattern = re.compile(
        r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|"
    )

    for match in topic_pattern.finditer(content):

        topic_id = match.group(1)

        if topic_id == "id":
            continue

        chapter.topics.append(
            TopicDefinition(
                id=topic_id,
                title=match.group(2),
                editorial_order=int(match.group(3)),
                difficulty=match.group(4),
                priority=int(match.group(5)),
            )
        )

    return chapter
