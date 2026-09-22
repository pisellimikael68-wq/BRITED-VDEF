from collections import Counter

from v2.knowledge.compiler.models import (
    RuleSeverity,
)
from v2.knowledge.compiler.rule_seed_builder import (
    RuleSeedBuilder,
)
from v2.knowledge.compiler.seed_semantic_policy import (
    SeedSemanticPolicy,
)
from v2.knowledge.compiler.seed_severity_policy import (
    SeedSeverityPolicy,
)
from v2.knowledge.compiler.source_fragment_builder import (
    SourceFragmentBuilder,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print(
    "=" * 70
)

print(
    "SEED SEVERITY POLICY TEST"
)

print(
    "=" * 70
)


loader = AcademicKnowledgeLoader()

knowledge = next(
    block
    for block in loader.load_family(
        "assurance_vie"
    )
    if (
        block.id
        == "assurance_vie_rachats_academic_2025"
    )
)


fragment_builder = SourceFragmentBuilder()

seed_builder = RuleSeedBuilder()

semantic_policy = SeedSemanticPolicy()

severity_policy = SeedSeverityPolicy()


fragments = fragment_builder.build(
    knowledge
)

seeds = seed_builder.build(
    fragments
)


results = []

for seed in seeds:

    rule_type = semantic_policy.classify(
        seed
    )

    severity = severity_policy.classify(
        seed=seed,
        rule_type=rule_type,
    )

    results.append(
        (
            seed,
            rule_type,
            severity,
        )
    )


print()

print(
    "SOURCE :",
    knowledge.id,
)

print(
    "SEEDS  :",
    len(seeds),
)


for (
    seed,
    rule_type,
    severity,
) in results:

    print()

    print(
        "-" * 70
    )

    print(
        "STABLE ID :",
        seed.stable_id,
    )

    print(
        "ANCHOR    :",
        seed.primary_anchor,
    )

    print(
        "TYPE      :",
        rule_type.value,
    )

    print(
        "SEVERITY  :",
        severity.value,
    )

    print()

    print(
        "PRIMARY CONTENT"
    )

    print(
        seed.primary_content
    )


print()

print(
    "=" * 70
)

print(
    "DISTRIBUTION"
)

print(
    "=" * 70
)


distribution = Counter(
    severity.value
    for _, _, severity in results
)


for severity, count in sorted(
    distribution.items()
):

    print(
        f"{severity:<10}: {count}"
    )


print()

print(
    "=" * 70
)

print(
    "DÉTERMINISME"
)

print(
    "=" * 70
)


second_run = [
    severity_policy.classify(
        seed=seed,
        rule_type=semantic_policy.classify(
            seed
        ),
    )
    for seed in seeds
]


first_run = [
    severity
    for _, _, severity in results
]


deterministic = (
    first_run == second_run
)


print(
    "MÊME SÉVÉRITÉ SUR 2 RUNS :",
    deterministic,
)


print()

print(
    "=" * 70
)

print(
    "RÉSULTAT"
)

print(
    "=" * 70
)


valid = (
    len(results) == len(seeds)
    and all(
        isinstance(
            severity,
            RuleSeverity,
        )
        for _, _, severity in results
    )
    and deterministic
)


print(
    "SEED SEVERITY POLICY VALIDE :",
    valid,
)
