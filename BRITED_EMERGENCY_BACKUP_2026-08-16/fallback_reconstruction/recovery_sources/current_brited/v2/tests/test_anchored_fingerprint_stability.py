from collections import defaultdict

from v2.knowledge.compiler.anchored_fingerprint import (
    AnchoredRuleFingerprint,
)
from v2.knowledge.compiler.knowledge_compiler import (
    KnowledgeCompiler,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print(
    "=" * 70
)

print(
    "ANCHORED RULE FINGERPRINT STABILITY TEST"
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


compiler = KnowledgeCompiler()

runs: list[
    dict[str, list[str]]
] = []


for run_index in range(
    1,
    4,
):

    print()
    print(
        "=" * 70
    )

    print(
        f"COMPILATION {run_index}/3"
    )

    print(
        "=" * 70
    )

    compiled = compiler.compile(
        knowledge
    )

    fingerprints: dict[
        str,
        list[str],
    ] = defaultdict(list)

    for rule in compiled.rules:

        fingerprint = (
            AnchoredRuleFingerprint.build(
                source_id=compiled.source_id,
                rule=rule,
            )
        )

        fingerprints[
            fingerprint
        ].append(
            rule.id
        )

    runs.append(
        dict(fingerprints)
    )

    print(
        f"RULES        : {len(compiled.rules)}"
    )

    print(
        "FINGERPRINTS : "
        f"{len(fingerprints)}"
    )

    print()

    for rule in compiled.rules:

        fingerprint = (
            AnchoredRuleFingerprint.build(
                source_id=compiled.source_id,
                rule=rule,
            )
        )

        print(
            "-" * 70
        )

        print(
            f"ID          : {rule.id}"
        )

        print(
            "ANCHORS"
        )

        for anchor in rule.source_anchors:

            print(
                f"- {anchor}"
            )

        print(
            f"FINGERPRINT : {fingerprint}"
        )


fingerprint_runs: dict[
    str,
    set[int],
] = defaultdict(set)

fingerprint_rule_ids: dict[
    str,
    set[str],
] = defaultdict(set)


for run_index, fingerprints in enumerate(
    runs,
    start=1,
):

    for fingerprint, rule_ids in (
        fingerprints.items()
    ):

        fingerprint_runs[
            fingerprint
        ].add(
            run_index
        )

        fingerprint_rule_ids[
            fingerprint
        ].update(
            rule_ids
        )


stable_fingerprints = {
    fingerprint
    for fingerprint, run_indexes
    in fingerprint_runs.items()
    if len(run_indexes) == len(runs)
}


unstable_fingerprints = (
    set(fingerprint_runs)
    - stable_fingerprints
)


print()
print(
    "=" * 70
)

print(
    "ANALYSE INTER-RUNS"
)

print(
    "=" * 70
)

print()

print(
    "FINGERPRINTS TOTAUX : "
    f"{len(fingerprint_runs)}"
)

print(
    "STABLES             : "
    f"{len(stable_fingerprints)}"
)

print(
    "INSTABLES           : "
    f"{len(unstable_fingerprints)}"
)


print()
print(
    "=" * 70
)

print(
    "FINGERPRINTS STABLES"
)

print(
    "=" * 70
)


if not stable_fingerprints:

    print(
        "Aucun fingerprint ancré stable."
    )


for fingerprint in sorted(
    stable_fingerprints
):

    print()

    print(
        f"FINGERPRINT : {fingerprint}"
    )

    print(
        "RUNS        : "
        f"{sorted(fingerprint_runs[fingerprint])}"
    )

    print(
        "RULE IDS"
    )

    for rule_id in sorted(
        fingerprint_rule_ids[
            fingerprint
        ]
    ):

        print(
            f"- {rule_id}"
        )


print()
print(
    "=" * 70
)

print(
    "FINGERPRINTS INSTABLES"
)

print(
    "=" * 70
)


if not unstable_fingerprints:

    print(
        "Aucun fingerprint ancré instable."
    )


for fingerprint in sorted(
    unstable_fingerprints
):

    print()

    print(
        f"FINGERPRINT : {fingerprint}"
    )

    print(
        "RUNS        : "
        f"{sorted(fingerprint_runs[fingerprint])}"
    )

    print(
        "RULE IDS"
    )

    for rule_id in sorted(
        fingerprint_rule_ids[
            fingerprint
        ]
    ):

        print(
            f"- {rule_id}"
        )


stability_rate = 0.0

if fingerprint_runs:

    stability_rate = (
        len(stable_fingerprints)
        / len(fingerprint_runs)
        * 100
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
    f"RUNS                : {len(runs)}"
)

print(
    "FINGERPRINTS TOTAUX : "
    f"{len(fingerprint_runs)}"
)

print(
    "STABLES             : "
    f"{len(stable_fingerprints)}"
)

print(
    "INSTABLES           : "
    f"{len(unstable_fingerprints)}"
)

print(
    "TAUX DE STABILITÉ   : "
    f"{stability_rate:.2f} %"
)


print()
print(
    "=" * 70
)

print(
    "VERDICT"
)

print(
    "=" * 70
)


if stability_rate >= 80:

    print(
        "ANCRAGE SOURCE SUFFISAMMENT STABLE"
    )

elif stability_rate >= 50:

    print(
        "ANCRAGE SOURCE PARTIELLEMENT STABLE"
    )

else:

    print(
        "ANCRAGE SOURCE INSUFFISAMMENT STABLE"
    )
    