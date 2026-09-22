from dataclasses import dataclass, field


@dataclass
class ContentBrief:

    subject: str = ""

    audience: str = ""

    objective: str = ""

    key_message: str = ""

    angle_title: str = ""

    angle_description: str = ""

    tone: str = ""

    format: str = ""

    cta: str = ""

    mandatory_points: list[str] = field(default_factory=list)

    references: list[str] = field(default_factory=list)

    knowledge_summary: list[str] = field(default_factory=list)
    