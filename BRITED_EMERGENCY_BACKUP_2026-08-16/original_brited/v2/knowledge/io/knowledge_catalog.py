from pathlib import Path


class KnowledgeCatalog:
    """
    Catalogue des connaissances compilées.

    Arborescence attendue :

    data/
        knowledge/
            compiled/
                assurance_vie/
                    rachats.json
                    beneficiaire.json
                pea/
                    fiscalite.json
    """

    def __init__(
        self,
        root: str | Path = "data/knowledge/compiled",
    ) -> None:
        self.root = Path(root)

    def families(self) -> list[str]:
        """
        Retourne la liste des familles disponibles.
        """

        if not self.root.exists():
            return []

        return sorted(
            directory.name
            for directory in self.root.iterdir()
            if directory.is_dir()
        )

    def chapters(
        self,
        family: str,
    ) -> list[str]:
        """
        Retourne les chapitres disponibles
        pour une famille.
        """

        family_path = self.root / family

        if not family_path.exists():
            return []

        return sorted(
            file.stem
            for file in family_path.glob("*.json")
        )

    def exists(
        self,
        family: str,
        chapter: str,
    ) -> bool:
        """
        Vérifie qu'un chapitre compilé existe.
        """

        return (
            self.root
            / family
            / f"{chapter}.json"
        ).exists()
    