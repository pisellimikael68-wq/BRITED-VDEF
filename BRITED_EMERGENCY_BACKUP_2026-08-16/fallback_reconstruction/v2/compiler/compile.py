from pathlib import Path

from v2.compiler.family_init_generator import generate_family_init
from v2.compiler.loader import load_families
from v2.compiler.topics_init_generator import generate_topics_init
from v2.compiler.writer_python import write_chapter

from v2.knowledge.registry import KnowledgeRegistry
from v2.knowledge.validators.graph_validator import GraphValidator
from v2.knowledge.reports.knowledge_report import KnowledgeReportGenerator


def compile_knowledge():

    print()
    print("========== BRITED Knowledge Compiler ==========")
    print()

    families = load_families()

    chapter_count = 0
    topic_count = 0

    output_root = Path("v2") / "knowledge" / "topics"

    for family in families:

        print(f"📁 {family.name}")

        output_dir = output_root / family.name
        output_dir.mkdir(parents=True, exist_ok=True)

        for chapter in family.chapters:

            print(f"   └── {chapter.name}")

            write_chapter(
                output_dir=output_dir,
                module_name=chapter.name,
                variable_name=f"{chapter.name.upper()}_TOPICS",
                topics=chapter.topics,
            )

            chapter_count += 1
            topic_count += len(chapter.topics)

        generate_family_init(output_dir)

    generate_topics_init(output_root)

    registry = KnowledgeRegistry()
    graph_report = GraphValidator(registry).validate()

    print()

    if graph_report.valid:
        print("✅ Graph validation OK")
    else:
        print("❌ Graph validation FAILED")
        print()
        print(f"Duplicate IDs         : {len(graph_report.duplicate_ids)}")
        print(f"Missing related       : {len(graph_report.missing_related_topics)}")
        print(f"Missing prerequisites : {len(graph_report.missing_prerequisites)}")
        print(f"Missing next topics   : {len(graph_report.missing_next_topics)}")
        print(f"Missing relations     : {len(graph_report.missing_relations)}")
        print(f"Orphan topics         : {len(graph_report.orphan_topics)}")
        print(f"Cycles                : {len(graph_report.cycles)}")

    knowledge_report = KnowledgeReportGenerator(
        registry=registry,
        graph_report=graph_report,
    ).generate()

    print()
    print("---------- Knowledge Report ----------")
    print(f"Topics           : {knowledge_report.topic_count}")
    print(f"Relations        : {knowledge_report.relation_count}")
    print(f"Average degree   : {knowledge_report.average_degree}")
    print(f"Min degree       : {knowledge_report.min_degree}")
    print(f"Max degree       : {knowledge_report.max_degree}")
    print(f"Relation types   : {knowledge_report.relation_types}")
    print(f"Knowledge score  : {knowledge_report.knowledge_score}/100")
    print("--------------------------------------")

    print()
    print("==============================================")
    print("✅ Compilation terminée")
    print("==============================================")
    print()
    print(f"Familles  : {len(families)}")
    print(f"Chapitres : {chapter_count}")
    print(f"Topics    : {topic_count}")
    print()


if __name__ == "__main__":
    compile_knowledge()
    