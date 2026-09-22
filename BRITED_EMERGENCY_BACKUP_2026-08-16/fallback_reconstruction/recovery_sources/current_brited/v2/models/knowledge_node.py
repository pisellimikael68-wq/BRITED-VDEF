from dataclasses import dataclass, field


@dataclass
class KnowledgeNode:

    title: str = ""

    definition: str = ""

    rules: list[str] = field(default_factory=list)

    taxation: list[str] = field(default_factory=list)

    misconceptions: list[str] = field(default_factory=list)

    faq: list[str] = field(default_factory=list)

    examples: list[str] = field(default_factory=list)

    references: list[str] = field(default_factory=list)
    