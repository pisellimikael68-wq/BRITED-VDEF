from v2.knowledge.compiler.knowledge_compiler import (
    KnowledgeCompiler,
)
from v2.knowledge.compiler.rule_fingerprint import (
    RuleFingerprintBuilder,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print("=" * 70)
print("RULE FINGERPRINT TEST")
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

fingerprints: dict[str, list[str]] = {}

for rule in compiled.rules:

    fingerprint = RuleFingerprintBuilder.build(
        family=compiled.family,
        chapter=compiled.chapter,
        rule=rule,
    )

    fingerprints.setdefault(
        fingerprint,
        [],
    ).append(
        rule.id
    )

    print()
    print("ID          :", rule.id)
    print("TYPE        :", rule.rule_type.value)
    print("FINGERPRINT :", fingerprint)

print()
print("=" * 70)
print("COLLISIONS")
print("=" * 70)

collisions = {
    fingerprint: rule_ids
    for fingerprint, rule_ids in fingerprints.items()
    if len(rule_ids) > 1
}

if not collisions:

    print("Aucune collision.")

else:

    for fingerprint, rule_ids in collisions.items():

        print()
        print("FINGERPRINT :", fingerprint)

        for rule_id in rule_ids:
            print("-", rule_id)

print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print("RULES      :", len(compiled.rules))
print("UNIQUE FPS :", len(fingerprints))
print("COLLISIONS :", len(collisions))
