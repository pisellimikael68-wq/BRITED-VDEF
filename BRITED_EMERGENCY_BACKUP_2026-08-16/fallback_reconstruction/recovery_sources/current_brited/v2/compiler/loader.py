from v2.compiler.builder import build_topic
from v2.compiler.discovery import discover_chapters, discover_families
from v2.compiler.models import RawChapter
from v2.compiler.parser import parse_chapter

from v2.knowledge.enrichers.navigation_enricher import NavigationEnricher
from v2.knowledge.enrichers.relationship_enricher import RelationshipEnricher
from v2.knowledge.enrichers.semantic_enricher import SemanticEnricher


class Chapter:

    def __init__(
        self,
        name: str,
        topics,
    ):
        self.name = name
        self.topics = topics


class Family:

    def __init__(
        self,
        name: str,
        chapters,
    ):
        self.name = name
        self.chapters = chapters


def load_families() -> list[Family]:

    families: list[Family] = []

    # ==========================================================
    # Chargement des familles
    # ==========================================================

    for family_path in discover_families():

        chapters: list[Chapter] = []

        for chapter_path in discover_chapters(family_path):

            raw_chapter: RawChapter = parse_chapter(chapter_path)

            topics = [

                build_topic(
                    raw_topic,
                    raw_chapter,
                )

                for raw_topic in raw_chapter.topics

            ]

            chapters.append(

                Chapter(
                    name=raw_chapter.chapter,
                    topics=topics,
                )

            )

        families.append(

            Family(
                name=family_path.name,
                chapters=chapters,
            )

        )

    # ==========================================================
    # Enrichissement automatique
    # ==========================================================

    print("🧠 NavigationEnricher...")
    NavigationEnricher().enrich(families)

    print("🧠 RelationshipEnricher...")
    RelationshipEnricher().enrich(families)

    print("🧠 SemanticEnricher...")
    SemanticEnricher().enrich(families)

    return families
