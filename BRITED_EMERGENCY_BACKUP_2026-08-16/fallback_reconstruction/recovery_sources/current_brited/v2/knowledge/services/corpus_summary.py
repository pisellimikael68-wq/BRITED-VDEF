from dataclasses import dataclass


@dataclass(frozen=True)
class CorpusSummary:
    """
    Résumé global du corpus compilé.

    Cet objet ne contient aucune logique métier.
    Il transporte uniquement les indicateurs calculés
    par le CorpusService.
    """

    families: int
    chapters: int
    rules: int
    legal_references: int
    source_anchors: int
    