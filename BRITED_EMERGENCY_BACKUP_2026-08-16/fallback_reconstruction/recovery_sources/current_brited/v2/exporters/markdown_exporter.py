from pathlib import Path
from datetime import datetime


class MarkdownExporter:

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

        output_file = output_dir / "script.md"

        review = context.review
        script = context.script
        angle = context.selected_angle

        with open(output_file, "w", encoding="utf-8") as f:

            f.write("# BRITED\n\n")

            f.write("## Informations\n\n")

            f.write(f"- Date : {date}\n")
            f.write(f"- Sujet : {context.subject}\n")

            if angle:
                f.write(f"- Angle : {angle.title}\n")

            if review:
                f.write(f"- Score : {review.score}/100\n")

            f.write("\n---\n\n")

            f.write(f"# {script.title}\n\n")

            f.write("## Hook\n\n")
            f.write(script.hook.strip())
            f.write("\n\n")

            f.write("## Script\n\n")
            f.write(script.body.strip())
            f.write("\n\n")

            f.write("## CTA\n\n")
            f.write(script.cta.strip())
            f.write("\n\n")

            if review:

                f.write("---\n\n")

                f.write("# Review\n\n")

                f.write(f"## Score global\n\n{review.score}/100\n\n")

                if review.strengths:

                    f.write("## Points forts\n\n")

                    for point in review.strengths:
                        f.write(f"- {point}\n")

                    f.write("\n")

                if review.weaknesses:

                    f.write("## Faiblesses\n\n")

                    for point in review.weaknesses:
                        f.write(f"- {point}\n")

                    f.write("\n")

                if review.rewrite_needed:

                    f.write("## Réécriture demandée\n\n")

                    for instruction in review.rewrite_instructions:
                        f.write(f"- {instruction}\n")

                    f.write("\n")

        return output_file
    