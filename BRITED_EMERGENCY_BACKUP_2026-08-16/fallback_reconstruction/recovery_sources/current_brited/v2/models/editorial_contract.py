from dataclasses import dataclass


@dataclass
class EditorialContract:

    audience: str = ""

    objective: str = ""

    key_message: str = ""

    tone: str = ""

    format: str = ""

    cta: str = ""

    mandatory_points: list[str] = None

    forbidden_points: list[str] = None
    