from dataclasses import dataclass, field


@dataclass
class EditorialStrategy:
    audience: str = ""
    objective: str = ""
    key_message: str = ""

    tone: str = ""
    emotion: str = ""
    complexity: str = ""

    format: str = ""

    cta_strategy: str = ""

    forbidden_points: list[str] = field(default_factory=list)


@dataclass
class EditorialContract:
    audience: str = ""
    objective: str = ""
    key_message: str = ""

    tone: str = ""

    format: str = ""

    cta: str = ""

    forbidden_points: list[str] = field(default_factory=list)
    