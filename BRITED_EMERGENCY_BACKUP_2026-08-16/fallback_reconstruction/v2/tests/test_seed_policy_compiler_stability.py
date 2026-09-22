from v2.knowledge.compiler.rule_seed_builder import (
    RuleSeedBuilder,
)
from v2.knowledge.compiler.seed_knowledge_compiler import (
    SeedKnowledgeCompiler,
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
print("SEED POLICY COMPILER STABILITY TEST")
print("=" * 70)


SOURCE_ID = (
    "assurance_vie_rachats_academic_2025"
)


loader = AcademicKnowledgeLoader()

knowledge = next(
    block
    for block in loader.load_family(
        "assurance_vie"
    )
    if block.id == SOURCE_ID
)


fragment_builder = SourceFragmentBuilder()
seed_builder = RuleSeedBuilder()
semantic_policy = SeedSemanticPolicy()
compiler = SeedKnowledgeCompiler()


fragments = fragment_builder.build(
    knowledge
)

seeds = seed_builder.build(
    fragments
)


seed_by_id = {
    seed.stable_id: seed
    for seed in seeds
}


compiled = compiler.compile(
    knowledge
)


print()
print("SOURCE :", knowledge.id)
print("SEEDS  :", len(seeds))
print("RULES  :", len(compiled.rules))


print()
print("=" * 70)
print("COMPARAISON POLICY / COMPILER")
print("=" * 70)


matches: list[bool] = []


for rule in compiled.rules:

    seed = seed_by_id[
        rule.id
    ]

    expected_type = (
        semantic_policy.classify(
            seed
        )
    )

    match = (
        rule.rule_type
        == expected_type
    )

    matches.append(match)

    print()
    print("-" * 70)

    print(
        "RULE ID       :",
        rule.id,
    )

    print(
        "PRIMARY ANCHOR:",
        seed.primary_anchor,
    )

    print(
        "POLICY TYPE   :",
        expected_type.value,
    )

    print(
        "COMPILED TYPE :",
        rule.rule_type.value,
    )

    print(
        "MATCH         :",
        match,
    )


same_count = (
    len(seeds)
    == len(compiled.rules)
)

all_types_match = all(
    matches
)


print()
print("=" * 70)
print("CONTRÔLES")
print("=" * 70)

print(
    "MÊME NOMBRE SEEDS / RULES :",
    same_count,
)

print(
    "TOUS LES TYPES CONFORMES  :",
    all_types_match,
)


print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "POLICY COMPILER STABLE :",
    (
        same_count
        and all_types_match
    ),
)