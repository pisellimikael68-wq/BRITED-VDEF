from v2.agents.models import PlannedTopic
from v2.llm import LLMService


def main():

    topic = PlannedTopic(
        id="assurance_vie_definition",
        title="Définition de l'assurance-vie",
        editorial_order=1,
    )

    service = LLMService()

    print()
    print("===== Génération =====")
    print()

    written = service.write_topic(
        family="assurance_vie",
        chapter="fondamentaux",
        topic=topic,
    )

    print("ID :", written.id)
    print()

    print("Titre :")
    print(written.title)
    print()

    print("Description :")
    print(written.description)
    print()

    print("Keywords :")
    print(written.keywords)
    print()

    print("Vocabulary :")
    print(written.vocabulary)
    print()

    print("Examples :")
    print(written.examples)
    print()

    print("Sources :")
    print(written.legal_sources)
    print()


if __name__ == "__main__":
    main()
    