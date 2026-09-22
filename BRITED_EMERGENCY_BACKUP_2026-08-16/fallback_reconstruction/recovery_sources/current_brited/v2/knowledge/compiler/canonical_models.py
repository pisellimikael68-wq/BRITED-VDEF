from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CanonicalRule:
    """
    Représentation canonique d'une CompiledRule.

    Une CanonicalRule normalise la représentation d'une
    règle afin de permettre :

    - le fingerprint ;
    - la déduplication ;
    - les comparaisons entre corpus ;
    - les futurs moteurs de recherche.

    Une CanonicalRule ne fusionne jamais plusieurs règles.
    """

    id: str

    family: str

    chapter: str

    rule_type: str

    statement: str

    keywords: tuple[str, ...] = ()

    conditions: tuple[str, ...] = ()

    required_elements: tuple[str, ...] = ()

    forbidden_interpretations: tuple[str, ...] = ()

    legal_references: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class CanonicalKnowledge:
    """
    Ensemble canonique d'un bloc Knowledge compilé.
    """

    source_id: str

    family: str

    chapter: str

    rules: tuple[CanonicalRule, ...] = ()
    