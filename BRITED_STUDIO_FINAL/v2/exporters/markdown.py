from pathlib import Path


class MarkdownExporter:

    def export(self, context):

        output_dir = Path("outputs/instagram")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{context.subject}.md"
        path = output_dir / filename

        with open(path, "w", encoding="utf-8") as f:

            f.write(f"# {context.script.title}\n\n")

            f.write("## Hook\n\n")
            f.write(context.script.hook)
            f.write("\n\n")

            f.write("## Script\n\n")
            f.write(context.script.body)
            f.write("\n\n")

            f.write("## CTA\n\n")
            f.write(context.script.cta)
            f.write("\n")

        return path