from dataclasses import dataclass, field

from v2.knowledge.validation.validation_issue import (
    ValidationIssue,
)

from v2.knowledge.validation.validation_severity import (
    ValidationSeverity,
)

catalog = KnowledgeCatalog()

families = catalog.families()

assert len(families) > 0, "Aucune famille disponible."

family = families[0]

chapters = catalog.chapters(family)

assert len(chapters) > 0, (
    f"Aucun chapitre disponible pour la famille '{family}'."
)

chapter = chapters[0]

loader = CompiledKnowledgeLoader()

knowledge = loader.load(
    family=family,
    chapter=chapter,
)

validator = Validator()

report = validator.validate(
    knowledge,
)

print(
    report.summary(
        family=family,
        chapter=chapter,
    )
)
