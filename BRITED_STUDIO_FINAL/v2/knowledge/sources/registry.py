from pathlib import Path

from v2.knowledge.sources.models import SourceDocument


class SourceRegistry:
    """
    Registre des documents sources utilisés
    pour construire la Knowledge Base BRITED.
    """

    def __init__(
        self,
        source_dir: str = "data/sources/dauphine",
    ):

        self.source_dir = Path(source_dir)

        self.documents = self._build_documents()

        self.documents_by_id = {
            document.id: document
            for document in self.documents
        }

    def _build_documents(
        self,
    ) -> list[SourceDocument]:
        """
        Déclare explicitement les documents académiques
        actuellement raccordés au moteur Knowledge.
        """

        return [
            SourceDocument(
                id="assurance_vie_notes_2025",
                title=(
                    "Notes personnelles - Assurance-vie"
                ),
                path=(
                    self.source_dir
                    / "M1_S1_ASSURANCE_VIE.pdf"
                ),
                source_type="academic_notes",
                origin="pierre_louis_gomet_notes",
                academic_year="2025",
                metadata={
                    "family": "assurance_vie",
                    "pillar": "epargne",
                },
            ),
        ]

    def get(
        self,
        document_id: str,
    ) -> SourceDocument | None:
        """
        Retourne un document par son identifiant.
        """

        return self.documents_by_id.get(
            document_id
        )

    def by_family(
        self,
        family: str,
    ) -> list[SourceDocument]:
        """
        Retourne les documents associés à une famille.
        """

        return [
            document
            for document in self.documents
            if document.metadata.get("family") == family
        ]

    def existing_documents(
        self,
    ) -> list[SourceDocument]:
        """
        Retourne uniquement les fichiers réellement présents.
        """

        return [
            document
            for document in self.documents
            if document.exists()
        ]

    def missing_documents(
        self,
    ) -> list[SourceDocument]:
        """
        Retourne les documents déclarés mais absents du disque.
        """

        return [
            document
            for document in self.documents
            if not document.exists()
        ]
    