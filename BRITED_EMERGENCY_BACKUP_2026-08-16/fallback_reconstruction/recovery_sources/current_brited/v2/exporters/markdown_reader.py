from pathlib import Path


class MarkdownReader:
    """
    Lit les métadonnées d'un fichier Markdown BRITED.
    """

    def read_frontmatter(
        self,
        path: Path,
    ) -> dict[str, str]:
        """
        Lit le frontmatter YAML simple d'un fichier Markdown.

        Cette méthode ne dépend volontairement pas
        d'une bibliothèque YAML externe.
        """

        if not path.exists():
            return {}

        lines = path.read_text(
            encoding="utf-8",
        ).splitlines()

        if not lines or lines[0].strip() != "---":
            return {}

        metadata: dict[str, str] = {}

        for line in lines[1:]:

            line = line.strip()

            if line == "---":
                break

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            metadata[key.strip()] = value.strip()

        return metadata

    def read_prompt_hash(
        self,
        path: Path,
    ) -> str | None:
        """
        Retourne le prompt_hash enregistré dans le Markdown.
        """

        metadata = self.read_frontmatter(path)

        prompt_hash = metadata.get("prompt_hash")

        if not prompt_hash:
            return None

        return prompt_hash
    