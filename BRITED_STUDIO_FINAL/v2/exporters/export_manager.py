from v2.exporters.markdown_exporter import MarkdownExporter
from v2.exporters.json_exporter import JsonExporter


class ExportManager:

    def __init__(self):

        self.exporters = [
            MarkdownExporter(),
            JsonExporter(),
        ]

    def export(self, context):

        exported_files = []

        for exporter in self.exporters:

            try:

                path = exporter.export(context)

                exported_files.append(path)

            except Exception as e:

                print(
                    f"[ExportManager] Erreur avec "
                    f"{exporter.__class__.__name__} : {e}"
                )

        return exported_files
    