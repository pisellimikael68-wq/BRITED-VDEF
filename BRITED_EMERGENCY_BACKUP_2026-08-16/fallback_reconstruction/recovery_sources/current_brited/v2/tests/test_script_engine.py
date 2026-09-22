from v2.knowledge.registry import KnowledgeRegistry

from v2.studio.engines.publication_engine import PublicationEngine
from v2.studio.engines.script_engine import ScriptEngine


def main():

    registry = KnowledgeRegistry()

    topic = registry.get_topic(
        "assurance_vie_fondamentaux_definition"
    )

    publication = PublicationEngine().generate(topic)

    script = ScriptEngine().generate(publication)

    script.display()


if __name__ == "__main__":
    main()
    