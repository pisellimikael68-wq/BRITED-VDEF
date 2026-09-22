from v2.knowledge.compiler.seed_condition_policy import (
    SeedConditionPolicy,
)
from v2.knowledge.compiler.rule_seed_builder import (
    RuleSeedBuilder,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)

print("=" * 70)
print("SEED CONDITION POLICY TEST")
print("=" * 70)

loader = AcademicKnowledgeLoader()
knowledge = loader.load_all()[0]

from v2.knowledge.compiler.source_fragment_builder import (
    SourceFragmentBuilder,
)

fragment_builder = SourceFragmentBuilder()

fragments = fragment_builder.build(
    knowledge
)

seed_builder = RuleSeedBuilder()

seeds = seed_builder.build(
    fragments
)

policy = SeedConditionPolicy()

conditions_run1 = []
conditions_run2 = []

for seed in seeds:

    conditions = policy.build(seed)

    conditions_run1.append(conditions)

    print()

    print("-" * 70)

    print(seed.stable_id)

    if conditions:

        for condition in conditions:
            print(condition)

    else:
        print("(aucune condition déterministe)")

print()

print("=" * 70)
print("DÉTERMINISME")
print("=" * 70)

for seed in seeds:
    conditions_run2.append(
        policy.build(seed)
    )

print(
    "MÊMES CONDITIONS :",
    conditions_run1 == conditions_run2,
)

print()

print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "SEED CONDITION POLICY VALIDE :",
    conditions_run1 == conditions_run2,
)
