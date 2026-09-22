from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ProtectedRule:
    """
    Règle métier protégée issue du corpus Knowledge.

    Une règle protégée représente un mécanisme qui ne doit
    pas être déformé lors de la génération éditoriale.
    """

    id: str

    statement: str

    validator_key: str = ""

    legal_references: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True, frozen=True)
class AcademicKnowledge:
    """
    Représente un bloc de connaissance académique
    structuré à partir des notes personnelles utilisées
    comme socle Knowledge de BRITED.

    Ce modèle ne représente pas une source officielle.
    """

    id: str

    pillar: str
    family: str
    chapter: str

    title: str

    summary: str = ""

    key_points: list[str] = field(
        default_factory=list
    )

    rules: list[str] = field(
        default_factory=list
    )

    protected_rules: list[ProtectedRule] = field(
        default_factory=list
    )

    thresholds: list[str] = field(
        default_factory=list
    )

    sensitive_dates: list[str] = field(
        default_factory=list
    )

    examples: list[str] = field(
        default_factory=list
    )

    vocabulary: list[str] = field(
        default_factory=list
    )

    legal_references: list[str] = field(
        default_factory=list
    )

    attention_points: list[str] = field(
        default_factory=list
    )

    source_type: str = "academic_notes"

    origin: str = "pierre_louis_gomet_notes"

    academic_year: str = "2025"

    def searchable_content(self) -> str:
        """
        Construit le contenu textuel utilisable
        par le moteur de recherche Knowledge.
        """

        values = [
            self.title,
            self.summary,
            *self.key_points,
            *self.rules,
            *[
                rule.statement
                for rule in self.protected_rules
            ],
            *[
                reference
                for rule in self.protected_rules
                for reference in rule.legal_references
            ],
            *self.thresholds,
            *self.sensitive_dates,
            *self.examples,
            *self.vocabulary,
            *self.legal_references,
            *self.attention_points,
        ]

        return "\n".join(
            value
            for value in values
            if value
        )
    