from v2.knowledge.registry import KnowledgeRegistry

from v2.studio.editorial.editorial_composer import EditorialComposer
from v2.studio.editorial.editorial_context import EditorialContext

from v2.studio.editorial.editorial_types import EditorialAngle

from v2.studio.models.brand_strategy import (
    AudienceLevel,
    Platform,
)

from v2.studio.models.publication import (
    ContentFormat,
    PublicationObjective,
)


def main():

    topic = KnowledgeRegistry().get_topics_by_family(
        "assurance_vie"
    )[0]

    context = EditorialContext(

        platform=Platform.INSTAGRAM,

        format=ContentFormat.CAROUSEL,

        objective=PublicationObjective.ENGAGEMENT,

        audience=AudienceLevel.BEGINNER,

        angle=EditorialAngle.MYTH,

    )

    blueprint = EditorialComposer().compose(

        topic,

        context,

    )

    print()

    print("=" * 60)

    print("EDITORIAL BLUEPRINT")

    print("=" * 60)

    print()

    print(blueprint)


if __name__ == "__main__":
    main()
    