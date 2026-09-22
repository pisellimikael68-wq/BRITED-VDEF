from v2.studio.editorial.editorial_context import EditorialContext
from v2.studio.editorial.editorial_types import EditorialAngle

from v2.studio.editorial.playbook.engines.hook_engine import HookEngine

from v2.studio.models.brand_strategy import (
    AudienceLevel,
    Platform,
)

from v2.studio.models.publication import (
    ContentFormat,
    PublicationObjective,
)


def main():

    context = EditorialContext(

        platform=Platform.INSTAGRAM,

        format=ContentFormat.CAROUSEL,

        objective=PublicationObjective.ENGAGEMENT,

        audience=AudienceLevel.BEGINNER,

        angle=EditorialAngle.MYTH,

    )

    hook = HookEngine().select(context)

    print()

    print("=" * 60)

    print("HOOK")

    print("=" * 60)

    print()

    print(hook)


if __name__ == "__main__":
    main()
    