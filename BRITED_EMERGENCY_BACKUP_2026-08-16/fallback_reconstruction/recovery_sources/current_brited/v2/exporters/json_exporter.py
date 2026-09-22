import json

from pathlib import Path
from datetime import datetime


class JsonExporter:

    def export(self, context):

        date = datetime.now().strftime("%Y-%m-%d")

        safe_subject = (
            context.subject.replace("/", "-")
            .replace("\\", "-")
            .replace(":", "")
            .replace("?", "")
            .replace("*", "")
            .replace('"', "")
            .strip()
        )

        output_dir = (
            Path("exports")
            / date
            / safe_subject
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = output_dir / "script.json"

        review = context.review
        script = context.script
        angle = context.selected_angle
        editorial = context.editorial

        data = {

            "metadata": {

                "generated_at": date,
                "subject": context.subject,
                "pipeline": "instagram",
                "version": "1.0",

            },

            "editorial": {

                "audience": editorial.audience if editorial else "",
                "objective": editorial.objective if editorial else "",
                "key_message": editorial.key_message if editorial else "",
                "tone": editorial.tone if editorial else "",
                "emotion": editorial.emotion if editorial else "",
                "complexity": editorial.complexity if editorial else "",
                "format": editorial.format if editorial else "",
                "cta_strategy": editorial.cta_strategy if editorial else "",

            },

            "angle": {

                "title": angle.title if angle else "",
                "description": angle.description if angle else "",
                "score": angle.score if angle else 0,

            },

            "script": {

                "title": script.title,
                "hook": script.hook,
                "body": script.body,
                "cta": script.cta,

            },

            "review": {

                "global_score": review.score,

                "patrimonial_score": review.patrimonial_score,
                "pedagogy_score": review.pedagogy_score,
                "instagram_score": review.instagram_score,
                "hook_score": review.hook_score,
                "cta_score": review.cta_score,
                "compliance_score": review.compliance_score,

                "strengths": review.strengths,
                "weaknesses": review.weaknesses,

                "rewrite_needed": review.rewrite_needed,
                "rewrite_instructions": review.rewrite_instructions,

            },

        }

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return output_file
    