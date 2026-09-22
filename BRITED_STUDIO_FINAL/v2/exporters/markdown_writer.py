from pathlib import Path

from v2.agents.models import WrittenTopic


class MarkdownWriter:
    """
    Exporte un WrittenTopic au format Markdown.

    Le hash du prompt peut être stocké dans le front matter
    afin de permettre la génération incrémentale.
    """

    def __init__(self, output_dir: str = "generated"):

        self.output_dir = Path(output_dir)

    def write(
        self,
        *,
        family: str,
        chapter: str,
        topic: WrittenTopic,
        prompt_hash: str | None = None,
    ) -> Path:

        directory = self.output_dir / family / chapter
        directory.mkdir(parents=True, exist_ok=True)

        output = directory / f"{topic.id}.md"

        output.write_text(
            self._render(
                family=family,
                chapter=chapter,
                topic=topic,
                prompt_hash=prompt_hash,
            ),
            encoding="utf-8",
        )

        return output

    def _render(
        self,
        *,
        family: str,
        chapter: str,
        topic: WrittenTopic,
        prompt_hash: str | None = None,
    ) -> str:

        keywords = "\n".join(
            f"- {keyword}"
            for keyword in topic.keywords
        )

        vocabulary = "\n".join(
            f"- {word}"
            for word in topic.vocabulary
        )

        examples = "\n\n".join(
            f"### Exemple {i + 1}\n\n{example}"
            for i, example in enumerate(topic.examples)
        )

        sources = "\n".join(
            f"- {source}"
            for source in topic.legal_sources
        )

        prompt_hash_line = ""

        if prompt_hash is not None:
            prompt_hash_line = (
                f"prompt_hash: {prompt_hash}\n"
            )

        return f"""---
id: {topic.id}
title: {topic.title}
family: {family}
chapter: {chapter}
generated: true
{prompt_hash_line}---

# {topic.title}

## Résumé

{topic.summary}

---

## Description

{topic.description}

---

## Mots-clés

{keywords}

---

## Vocabulaire

{vocabulary}

---

## Exemples

{examples}

---

## Sources

{sources}
"""
    