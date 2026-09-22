from collections import Counter

from v2.knowledge.compiler.rule_seed_builder import (
    RuleSeedBuilder,
)
from v2.knowledge.compiler.seed_semantic_policy import (
    SeedSemanticPolicy,
)
from v2.knowledge.compiler.source_fragment_builder import (
    SourceFragmentBuilder,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print("=" * 70)
print("SEED SEMANTIC POLICY TEST")
print("=" * 70)


loader = AcademicKnowledgeLoader()

knowledge_items = loader.load_all()

knowledge = next(
    item
    for item in knowledge_items
    if item.id
    == "assurance_vie_rachats_academic_2025"
)


fragment_builder = SourceFragmentBuilder()

fragments = fragment_builder.build(
    knowledge
)


seed_builder = RuleSeedBuilder()

seeds = seed_builder.build(
    fragments
)


policy = SeedSemanticPolicy()


results = []

for seed in seeds:

    rule_type = policy.classify(
        seed
    )

    scores = policy.score(
        seed
    )

    results.append(
        (
            seed,
            rule_type,
            scores,
        )
    )


print()
print(f"SOURCE : {knowledge.id}")
print(f"SEEDS  : {len(seeds)}")
print()


for seed, rule_type, scores in results:

    print("-" * 70)

    print(
    f"STABLE ID : {seed.stable_id}"
    )

    print(
        f"ANCHOR    : "
        f"{seed.primary_anchor}"
    )

    print(
        f"TYPE      : {rule_type.value}"
    )

    print()

    print("PRIMARY CONTENT")

    print(
        seed.primary_content
    )

    print()

    print("SCORES")

    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    for candidate_type, score in sorted_scores:

        print(
            f"- "
            f"{candidate_type.value:<15}"
            f": {score}"
        )


print()
print("=" * 70)
print("DISTRIBUTION")
print("=" * 70)


distribution = Counter(
    rule_type.value
    for _, rule_type, _ in results
)

for rule_type, count in sorted(
    distribution.items()
):

    print(
        f"{rule_type:<15}: {count}"
    )


print()
print("=" * 70)
print("DÉTERMINISME")
print("=" * 70)


second_run = [
    policy.classify(seed)
    for seed in seeds
]

first_run = [
    rule_type
    for _, rule_type, _ in results
]


deterministic = (
    first_run
    == second_run
)


print(
    f"MÊME CLASSIFICATION SUR 2 RUNS : "
    f"{deterministic}"
)


print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)


valid = (
    len(results) == len(seeds)
    and deterministic
)


print(
    f"SEED SEMANTIC POLICY VALIDE : "
    f"{valid}"
)
