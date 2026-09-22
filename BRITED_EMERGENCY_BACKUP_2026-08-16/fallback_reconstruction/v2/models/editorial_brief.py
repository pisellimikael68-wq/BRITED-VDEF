from dataclasses import dataclass, field

from v2.models.knowledge_models import Topic


@dataclass
class EditorialBrief:

    subject: str

    topics: list[Topic] = field(default_factory=list)

    misconceptions: list[str] = field(default_factory=list)

    client_questions: list[str] = field(default_factory=list)

    analogies: list[str] = field(default_factory=list)

    recommended_formats: list[str] = field(default_factory=list)

    legal_sources: list[str] = field(default_factory=list)

    keywords: list[str] = field(default_factory=list)
    