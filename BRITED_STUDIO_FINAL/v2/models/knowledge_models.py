from dataclasses import dataclass, field


@dataclass(slots=True)
class TopicRelation:
    """
    Représente une relation pondérée entre deux Topics.
    """

    target: str
    relation_type: str
    score: float = 1.0
    source: str = ""


@dataclass(slots=True)
class Topic:

    # ==========================================================
    # IDENTITÉ
    # ==========================================================

    id: str
    title: str
    pillar: str
    family: str
    chapter: str

    # ==========================================================
    # DESCRIPTION
    # ==========================================================

    description: str = ""
    objective: str = ""

    difficulty: str = "Débutant"
    priority: int = 5

    editorial_order: int = 999
    version: int = 1

    # ==========================================================
    # CONNAISSANCE
    # ==========================================================

    keywords: list[str] = field(default_factory=list)
    key_points: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    vocabulary: list[str] = field(default_factory=list)
    legal_sources: list[str] = field(default_factory=list)

    # ==========================================================
    # PÉDAGOGIE
    # ==========================================================

    analogies: list[str] = field(default_factory=list)
    misconceptions: list[str] = field(default_factory=list)
    common_mistakes: list[str] = field(default_factory=list)
    expert_tips: list[str] = field(default_factory=list)
    attention_points: list[str] = field(default_factory=list)

    # ==========================================================
    # CLIENT
    # ==========================================================

    client_questions: list[str] = field(default_factory=list)
    client_objections: list[str] = field(default_factory=list)
    client_fears: list[str] = field(default_factory=list)
    client_goals: list[str] = field(default_factory=list)
    client_intents: list[str] = field(default_factory=list)

    # ==========================================================
    # ÉDITORIAL
    # ==========================================================

    recommended_formats: list[str] = field(default_factory=list)

    # ==========================================================
    # Navigation historique
    # ==========================================================

    related_topics: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    next_topics: list[str] = field(default_factory=list)

    # ==========================================================
    # Nouveau Knowledge Graph
    # ==========================================================

    relations: list[TopicRelation] = field(default_factory=list)

    # ==========================================================
    # API
    # ==========================================================

    def add_relation(
        self,
        target: str,
        relation_type: str,
        score: float = 1.0,
        source: str = "",
    ) -> None:
        """
        Ajoute une relation au Topic.

        Si une relation existe déjà vers la même cible
        avec le même type, seul le meilleur score est conservé.
        """

        for relation in self.relations:

            if (
                relation.target == target
                and relation.relation_type == relation_type
            ):

                if score > relation.score:

                    relation.score = score
                    relation.source = source

                return

        self.relations.append(

            TopicRelation(

                target=target,
                relation_type=relation_type,
                score=score,
                source=source,

            )

        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def has_relation(
        self,
        target: str,
        relation_type: str | None = None,
    ) -> bool:

        for relation in self.relations:

            if relation.target != target:
                continue

            if relation_type is None:
                return True

            if relation.relation_type == relation_type:
                return True

        return False

    def get_relations(
        self,
        relation_type: str | None = None,
    ) -> list[TopicRelation]:

        if relation_type is None:
            return self.relations

        return [

            relation

            for relation in self.relations

            if relation.relation_type == relation_type

        ]
    