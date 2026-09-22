from pathlib import Path


class PromptLoader:

    ROOT = Path(__file__).parent

    @classmethod
    def load(
        cls,
        relative_path: str,
    ) -> str:

        path = cls.ROOT / relative_path

        return path.read_text(
            encoding="utf-8",
        )
    