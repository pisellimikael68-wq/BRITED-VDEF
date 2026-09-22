from dataclasses import dataclass, field


@dataclass
class TopicDefinition:
    id: str
    title: str
    editorial_order: int
    difficulty: str
    priority: int


@dataclass
class ChapterDefinition:
    family: str
    chapter: str
    pillar: str
    title: str

    topics: list[TopicDefinition] = field(default_factory=list)
    