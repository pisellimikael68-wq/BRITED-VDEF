import argparse
import subprocess
import sys

from v2.agents.models import PlannedFamily
from v2.agents.writer.writer import WriterAgent
from v2.exporters.markdown_writer import MarkdownWriter
from v2.planning.markdown_plan_loader import MarkdownPlanLoader


class KnowledgeGenerationPipeline:
    """
    Pipeline autonome :
    Markdown plan -> WriterAgent -> MarkdownWriter -> Compiler
    """

    def __init__(self):
        self.loader = MarkdownPlanLoader()
        self.writer = WriterAgent()
        self.markdown_writer = MarkdownWriter()

    def run(
        self,
        family: str,
        chapter: str,
        limit: int | None = None,
        compile_after: bool = True,
    ):
        print()
        print("========== BRITED V2 Knowledge Generation ==========")
        print()

        print("📚 Chargement du plan...")
        planned_family = self.loader.load(family)

        selected_chapters = [
            planned_chapter
            for planned_chapter in planned_family.chapters
            if planned_chapter.name == chapter
        ]

        if not selected_chapters:
            raise ValueError(f"Chapitre introuvable : {chapter}")

        selected_chapter = selected_chapters[0]

        if limit is not None:
            selected_chapter.topics = selected_chapter.topics[:limit]

        scoped_family = PlannedFamily(
            pillar=planned_family.pillar,
            name=planned_family.name,
            chapters=[selected_chapter],
        )

        print(f"Famille  : {family}")
        print(f"Chapitre : {chapter}")
        print(f"Topics   : {len(selected_chapter.topics)}")
        print()

        print("✍️ Rédaction IA...")
        written_by_chapter = self.writer.write(scoped_family)

        print()
        print("💾 Écriture Markdown...")

        output_path = self.markdown_writer.write_chapter(
            family=scoped_family,
            chapter=selected_chapter,
            topics=written_by_chapter[selected_chapter.name],
        )

        print(f"✅ {output_path}")

        if compile_after:
            print()
            print("⚙️ Compilation BRITED...")
            subprocess.run(
                [sys.executable, "-m", "v2.compiler.compile"],
                check=True,
            )

        print()
        print("✅ Génération terminée")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--family", required=True)
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no-compile", action="store_true")

    args = parser.parse_args()

    KnowledgeGenerationPipeline().run(
        family=args.family,
        chapter=args.chapter,
        limit=args.limit,
        compile_after=not args.no_compile,
    )


if __name__ == "__main__":
    main()
    