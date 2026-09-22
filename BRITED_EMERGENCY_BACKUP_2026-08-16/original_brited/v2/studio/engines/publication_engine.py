from v2.models.knowledge_models import Topic

from v2.studio.engines.angle_engine import AngleEngine

from v2.studio.editorial.editorial_patterns import (
    EDITORIAL_PATTERNS,
)

from v2.studio.models.publication import Publication


class PublicationEngine:
    """
    Transforme un Topic en véritable brief éditorial.
    """

    def __init__(self):

        self.angle_engine = AngleEngine()

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        topic: Topic,
    ) -> Publication:

        angle = self.angle_engine.select(topic)

        pattern = EDITORIAL_PATTERNS[angle]

        return Publication(

            topic=topic,

            angle=angle,

            pattern=pattern,

            format=self._select_format(topic),

            title=topic.title,

            hook=self._generate_hook(topic, angle),

            objective=topic.objective,

            structure=pattern.structure,

            call_to_action=pattern.cta,

        )

    # ==========================================================
    # FORMAT
    # ==========================================================

    def _select_format(
        self,
        topic: Topic,
    ) -> str:

        if topic.recommended_formats:
            return topic.recommended_formats[0]

        return "carousel"

    # ==========================================================
    # HOOK
    # ==========================================================

    def _generate_hook(
        self,
        topic: Topic,
        angle,
    ) -> str:

        match angle.value:

            case "faq":
                return topic.client_questions[0]

            case "myth":
                return topic.misconceptions[0]

            case "mistake":
                return topic.common_mistakes[0]

            case "comparison":
                return topic.title

            case "story":
                return (
                    f"Imaginez la situation suivante : "
                    f"{topic.examples[0]}"
                )

            case _:
                return topic.title
            
            