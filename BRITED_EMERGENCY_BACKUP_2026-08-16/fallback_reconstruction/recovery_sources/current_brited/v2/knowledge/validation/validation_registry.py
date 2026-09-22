from v2.knowledge.validation.rules import (
    ConditionRule,
    ForbiddenInterpretationRule,
    LegalReferenceRule,
    RequiredElementRule,
    SourceAnchorRule,
)

VALIDATION_RULES = [
    LegalReferenceRule,
    SourceAnchorRule,
    ConditionRule,
    RequiredElementRule,
    ForbiddenInterpretationRule,
]
