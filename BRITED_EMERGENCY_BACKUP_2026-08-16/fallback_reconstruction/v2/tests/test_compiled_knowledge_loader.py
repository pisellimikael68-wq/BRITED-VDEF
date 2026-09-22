from v2.knowledge.io.compiled_knowledge_loader import (
    CompiledKnowledgeLoader,
)


print("=" * 70)
print("COMPILED KNOWLEDGE LOADER TEST")
print("=" * 70)

loader = CompiledKnowledgeLoader()

knowledge = loader.load(
    family="assurance_vie",
    chapter="rachats",
)

print()
print(f"SOURCE   : {knowledge.source_id}")
print(f"FAMILY   : {knowledge.family}")
print(f"CHAPTER  : {knowledge.chapter}")
print(f"RULES    : {len(knowledge.rules)}")

assert knowledge.family == "assurance_vie"
assert knowledge.chapter == "rachats"
assert len(knowledge.rules) == 11

print()
print("=" * 70)
print("PREMIÈRES RÈGLES")
print("=" * 70)

for rule in knowledge.rules[:3]:

    print()
    print(rule.id)
    print(rule.rule_type.value)
    print(rule.severity.value)
    print(rule.statement)

print()
print("=" * 70)
print("LOADER VALIDE : True")
print("=" * 70)
