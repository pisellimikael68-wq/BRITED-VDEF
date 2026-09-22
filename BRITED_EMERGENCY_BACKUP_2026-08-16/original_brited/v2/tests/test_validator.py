from v2.knowledge.io.compiled_knowledge_loader import (
    CompiledKnowledgeLoader,
)
from v2.knowledge.io.knowledge_catalog import (
    KnowledgeCatalog,
)
from v2.knowledge.validation import (
    Validator,
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

print("=== Validation Report ===")
print(f"Famille             : {family}")
print(f"Chapitre            : {chapter}")
print(f"Valide              : {report.is_valid}")
print(f"Nombre d'issues     : {report.issue_count}")
print(f"Erreurs             : {report.error_count}")
print(f"Avertissements      : {report.warning_count}")
print(f"Informations        : {report.info_count}")
print(f"Règles exécutées    : {report.executed_rules}")
print(f"Temps d'exécution   : {report.execution_time:.6f} s")
