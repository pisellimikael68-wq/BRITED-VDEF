from v2.studio.models.publication import Publication
from v2.studio.models.script import Script


class ScriptEngine:
    """
    Construit un Script structuré à partir d'une Publication.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def generate(
        self,
        publication: Publication,
    ) -> Script:

        topic = publication.topic

        script = Script(

            title=publication.title,

            format=publication.format,

            hook=publication.hook,

            call_to_action=publication.call_to_action,

            legal_sources=topic.legal_sources,

            vocabulary=topic.vocabulary,

        )

        for section in publication.structure:

            content = self._build_section(
                topic=topic,
                section=section,
            )

            if content:

                script.add_section(
                    section,
                    content,
                )

        script.conclusion = self._build_conclusion(topic)

        return script

    # ==========================================================
    # BUILD SECTION
    # ==========================================================

    def _build_section(
        self,
        topic,
        section: str,
    ) -> str:

        section = section.lower()

        if section == "définition":
            return topic.description

        if section == "explication":
            return "\n".join(
                f"• {point}"
                for point in topic.key_points
            )

        if section == "points clés":
            return "\n".join(
                f"• {point}"
                for point in topic.key_points
            )

        if section == "exemple":

            if topic.examples:
                return topic.examples[0]

            return ""

        if section == "cas pratique":

            if topic.examples:
                return topic.examples[0]

            return ""

        if section == "idée reçue":

            if topic.misconceptions:
                return topic.misconceptions[0]

            return ""

        if section == "pourquoi c'est faux":

            if topic.misconceptions:
                return (
                    "Cette affirmation est inexacte. "
                    "Voici pourquoi."
                )

            return ""

        if section == "la bonne explication":
            return topic.description

        if section == "erreur":

            if topic.common_mistakes:
                return topic.common_mistakes[0]

            return ""

        if section == "conséquences":

            if topic.attention_points:
                return "\n".join(
                    f"• {point}"
                    for point in topic.attention_points
                )

            return ""

        if section == "bonne pratique":

            if topic.expert_tips:
                return "\n".join(
                    f"• {tip}"
                    for tip in topic.expert_tips
                )

            return ""

        if section == "question":

            if topic.client_questions:
                return topic.client_questions[0]

            return topic.title

        if section == "réponse":
            return topic.description

        if section == "présentation":
            return topic.description

        if section == "avantages":

            return "\n".join(
                f"• {point}"
                for point in topic.key_points
            )

        if section == "inconvénients":

            if topic.attention_points:
                return "\n".join(
                    f"• {point}"
                    for point in topic.attention_points
                )

            return ""

        if section == "comment choisir":

            if topic.expert_tips:
                return "\n".join(
                    f"• {tip}"
                    for tip in topic.expert_tips
                )

            return ""

        if section == "à retenir":

            return "\n".join(
                f"• {point}"
                for point in topic.key_points[:3]
            )

        return ""

    # ==========================================================
    # CONCLUSION
    # ==========================================================

    def _build_conclusion(
        self,
        topic,
    ) -> str:

        if topic.objective:

            return topic.objective

        return ""
    
    