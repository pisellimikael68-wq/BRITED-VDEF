from v2.knowledge.compiler.rule_seed_builder import (
    RuleSeedBuilder,
)
from v2.knowledge.compiler.seed_statement_policy import (
    SeedStatementPolicy,
)
from v2.knowledge.compiler.source_fragment_builder import (
    SourceFragmentBuilder,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)

print("=" * 70)
print("SEED STATEMENT POLICY TEST")
print("=" * 70)

knowledge = AcademicKnowledgeLoader().load_all()[0]

fragments = SourceFragmentBuilder().build(
    knowledge
)

seeds = RuleSeedBuilder().build(
    fragments
)

policy = SeedStatementPolicy()

results = []

for seed in seeds:

    statement = policy.build(seed)

    results.append(statement)

    print()
    print("-" * 70)
    print(seed.stable_id)
    print()
    print(statement)

print()
print("=" * 70)
print("DÉTERMINISME")
print("=" * 70)

results2 = [
    policy.build(seed)
    for seed in seeds
]

print(
    "MÊMES STATEMENTS :",
    results == results2,
)

print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "SEED STATEMENT POLICY VALIDE :",
    results == results2,
)
