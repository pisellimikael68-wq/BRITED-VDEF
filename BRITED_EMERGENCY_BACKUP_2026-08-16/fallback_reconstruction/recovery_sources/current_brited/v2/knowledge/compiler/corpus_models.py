from dataclasses import dataclass, field

from v2.knowledge.compiler.canonical_models import (
    CanonicalRule,
)


@dataclass(slots=True, frozen=True)
class KnowledgeCorpus:
    """
    Corpus canonique complet de BRITED.

    Il contient l'ensemble des règles canoniques
    produites à partir des connaissances académiques.
    """

    rules: list[CanonicalRule] = field(
        default_factory=list,
    )
    