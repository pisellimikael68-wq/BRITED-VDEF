from v2.knowledge.compiler.seed_knowledge_compiler import (
    SeedKnowledgeCompiler,
)
from v2.knowledge.compiler.compiled_knowledge_writer import (
    CompiledKnowledgeWriter,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print("=" * 70)
print("SEED KNOWLEDGE COMPILER TEST")
print("=" * 70)


loader = AcademicKnowledgeLoader()

knowledge = next(
    block
    for block in loader.load_family(
        "assurance_vie"
    )
    if block.id
    == "assurance_vie_rachats_academic_2025"
)


compiler = SeedKnowledgeCompiler()

compiled = compiler.compile(
    knowledge
)

# ------------------------------------------------------------------
# Sauvegarde du corpus compilé
# ------------------------------------------------------------------

writer = CompiledKnowledgeWriter()

output_path = writer.write(
    compiled
)


print()
print("SOURCE :", compiled.source_id)
print("RULES  :", len(compiled.rules))
print("OUTPUT :", output_path)


for rule in compiled.rules:

    print()
    print("-" * 70)

    print("ID       :", rule.id)
    print("TYPE     :", rule.rule_type.value)
    print("SEVERITY :", rule.severity.value)

    print()
    print("PRIMARY ANCHOR")
    print("-", rule.source_anchors[0])

    print()
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
print("CONTRÔLES")
print("=" * 70)


rule_ids = [
    rule.id
    for rule in compiled.rules
]

primary_anchors = [
    rule.source_anchors[0]
    for rule in compiled.rules
]


print(
    "11 RÈGLES :",
    len(compiled.rules) == 11,
)

print(
    "IDS UNIQUES :",
    len(rule_ids) == len(set(rule_ids)),
)

print(
    "PRIMARY ANCHORS UNIQUES :",
    len(primary_anchors)
    == len(set(primary_anchors)),
)

print(
    "IDENTITÉ SEED CONSERVÉE :",
    all(
        rule.id
        == (
            f"{compiled.source_id}"
            f"::{rule.source_anchors[0]}"
        )
        for rule in compiled.rules
    ),
)


structure_valid = (
    len(compiled.rules) == 11
    and len(rule_ids) == len(set(rule_ids))
    and len(primary_anchors)
    == len(set(primary_anchors))
    and all(
        rule.id
        == (
            f"{compiled.source_id}"
            f"::{rule.source_anchors[0]}"
        )
        for rule in compiled.rules
    )
)


print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "SEED KNOWLEDGE COMPILER VALIDE :",
    structure_valid,
)
