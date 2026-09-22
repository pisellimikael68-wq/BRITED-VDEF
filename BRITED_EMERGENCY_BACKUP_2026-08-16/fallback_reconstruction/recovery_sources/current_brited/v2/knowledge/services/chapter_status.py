from enum import Enum


class ChapterStatus(Enum):
    DRAFT = "draft"
    COMPILED = "compiled"
    VALIDATED = "validated"
    PUBLISHED = "published"
    