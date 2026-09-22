from v2.agents.models import WrittenTopic
from v2.exporters.markdown_writer import MarkdownWriter


def main():

    topic = WrittenTopic(
        id="definition",
        title="Définition de l'assurance-vie",
        summary="Résumé de test",
        description="Description de test",
        keywords=["épargne", "contrat"],
        vocabulary=["souscripteur"],
        examples=["Exemple de test"],
        legal_sources=["Code des assurances"],
    )

    writer = MarkdownWriter()

    path = writer.write(
        family="assurance_vie",
        chapter="fondamentaux",
        topic=topic,
    )

    print(path)


if __name__ == "__main__":
    main()
    