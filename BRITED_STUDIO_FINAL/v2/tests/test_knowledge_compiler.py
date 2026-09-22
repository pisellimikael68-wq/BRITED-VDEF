from v2.knowledge.compiler.knowledge_compiler import (
    KnowledgeCompiler,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print("=" * 70)
print("GENERIC KNOWLEDGE COMPILER TEST")
print("=" * 70)

loader = AcademicKnowledgeLoader()

blocks = loader.load_family(
    "assurance_vie"
)

knowledge = next(
    block
    for block in blocks
    if block.chapter == "rachats"
)

compiler = KnowledgeCompiler()

compiled = compiler.compile(
    knowledge
)

print()
print("SOURCE  :", compiled.source_id)
print("FAMILY  :", compiled.family)
print("CHAPTER :", compiled.chapter)
print("RULES   :", len(compiled.rules))

for rule in compiled.rules:

    print()
    print("-" * 70)

    print("ID       :", rule.id)
    print("TYPE     :", rule.rule_type)
    print("SEVERITY :", rule.severity)

    print()
print("SOURCE ANCHORS")

if rule.source_anchors:

    for anchor in rule.source_anchors:

        print(
            f"- {anchor}"
        )

else:

    print("- AUCUN")
    print("STATEMENT")
    print(rule.statement)

    print()
    print("CONDITIONS")
    for value in rule.conditions:
        print("-", value)

    print()
    print("REQUIRED")
    for value in rule.required_elements:
        print("-", value)

    print()
    print("FORBIDDEN")
    for value in rule.forbidden_interpretations:
        print("-", value)

    print()
    print("LEGAL REFERENCES")
    for value in rule.legal_references:
        print("-", value)

print()
print("=" * 70)
print("COMPILATION TERMINÉE")
print("=" * 70)
