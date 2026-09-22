from v2.knowledge.compiler.rule_seed_builder import (
    RuleSeedBuilder,
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
    "RULE SEED BUILDER TEST"
)

print(
    "=" * 70
)


loader = AcademicKnowledgeLoader()

knowledge_blocks = loader.load_family(
    "assurance_vie"
)

knowledge = next(
    block
    for block in knowledge_blocks
    if block.id
    == "assurance_vie_rachats_academic_2025"
)


fragment_builder = (
    SourceFragmentBuilder()
)

fragments = fragment_builder.build(
    knowledge
)


seed_builder = RuleSeedBuilder()

seeds = seed_builder.build(
    fragments
)


print()

print(
    f"SOURCE : {knowledge.id}"
)

print(
    f"RULE FRAGMENTS : "
    f"{len([f for f in fragments if f.section == 'rules'])}"
)

print(
    f"SEEDS : {len(seeds)}"
)


print()

for seed in seeds:

    print(
        "-" * 70
    )

    print(
        f"STABLE ID      : {seed.stable_id}"
    )

    print(
        f"PRIMARY ANCHOR : {seed.primary_anchor}"
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
        "SUPPORTING ANCHORS"
    )

    if seed.supporting_anchors:

        for anchor in (
            seed.supporting_anchors
        ):

            print(
                f"- {anchor}"
            )

    else:

        print(
            "- AUCUN"
        )


stable_ids = [
    seed.stable_id
    for seed in seeds
]


primary_anchors = [
    seed.primary_anchor
    for seed in seeds
]


rule_fragment_count = len(
    [
        fragment
        for fragment in fragments
        if fragment.section == "rules"
    ]
)


print()
print(
    "=" * 70
)

print(
    "CONTRÔLES"
)

print(
    "=" * 70
)


print(
    "1 SEED PAR RULE : "
    f"{len(seeds) == rule_fragment_count}"
)

print(
    "STABLE IDS UNIQUES : "
    f"{len(stable_ids) == len(set(stable_ids))}"
)

print(
    "PRIMARY ANCHORS UNIQUES : "
    f"{len(primary_anchors) == len(set(primary_anchors))}"
)

print(
    "TOUS LES PRIMARY SONT RULES : "
    f"{all(anchor.startswith('rules:') for anchor in primary_anchors)}"
)


structure_valid = (
    len(seeds) == rule_fragment_count
    and len(stable_ids)
    == len(set(stable_ids))
    and len(primary_anchors)
    == len(set(primary_anchors))
    and all(
        anchor.startswith(
            "rules:"
        )
        for anchor in primary_anchors
    )
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

print(
    "RULE SEED STRUCTURE VALIDE : "
    f"{structure_valid}"
)
