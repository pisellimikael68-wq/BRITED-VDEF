from collections import defaultdict

from v2.knowledge.compiler.canonical_fingerprint import (
    CanonicalRuleFingerprintBuilder,
)
from v2.knowledge.compiler.knowledge_compiler import (
    KnowledgeCompiler,
)
from v2.knowledge.compiler.rule_canonicalizer import (
    SemanticRuleCanonicalizer,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


RUN_COUNT = 3


print("=" * 70)
print("CANONICAL RULE FINGERPRINT STABILITY TEST")
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


runs: list[dict[str, list[str]]] = []


for run_index in range(
    1,
    RUN_COUNT + 1,
):

    print()
    print("=" * 70)
    print(
        f"COMPILATION {run_index}/{RUN_COUNT}"
    )
    print("=" * 70)

    compiler = KnowledgeCompiler()

    canonicalizer = SemanticRuleCanonicalizer()

    compiled = compiler.compile(
        knowledge
    )

    print(
        "COMPILED RULES  :",
        len(compiled.rules),
    )

    canonical_rules = canonicalizer.canonicalize(
        compiled
    )

    print(
        "CANONICAL RULES :",
        len(canonical_rules),
    )

    run_fingerprints: dict[
        str,
        list[str],
    ] = {}

    for rule in canonical_rules:

        fingerprint = (
            CanonicalRuleFingerprintBuilder.build(
                rule
            )
        )

        if fingerprint in run_fingerprints:

            print()
            print(
                "WARNING DUPLICATE FINGERPRINT :",
                fingerprint,
            )

            print(
                "EXISTING SOURCE IDS :",
                run_fingerprints[
                    fingerprint
                ],
            )

            print(
                "NEW SOURCE IDS      :",
                rule.source_rule_ids,
            )

        run_fingerprints[
            fingerprint
        ] = rule.source_rule_ids

    runs.append(
        run_fingerprints
    )

    print(
        "CANONICAL FINGERPRINTS :",
        len(run_fingerprints),
    )


print()
print("=" * 70)
print("ANALYSE INTER-RUNS")
print("=" * 70)


fingerprint_presence: dict[
    str,
    list[int],
] = defaultdict(list)

fingerprint_source_ids: dict[
    str,
    list[list[str]],
] = defaultdict(list)


for run_index, run in enumerate(
    runs,
    start=1,
):

    for fingerprint, source_ids in run.items():

        fingerprint_presence[
            fingerprint
        ].append(
            run_index
        )

        fingerprint_source_ids[
            fingerprint
        ].append(
            source_ids
        )


stable_fingerprints = {
    fingerprint: run_indexes
    for fingerprint, run_indexes
    in fingerprint_presence.items()
    if len(run_indexes) == RUN_COUNT
}


unstable_fingerprints = {
    fingerprint: run_indexes
    for fingerprint, run_indexes
    in fingerprint_presence.items()
    if len(run_indexes) != RUN_COUNT
}


print()
print(
    "FINGERPRINTS TOTAUX :",
    len(fingerprint_presence),
)

print(
    "STABLES             :",
    len(stable_fingerprints),
)

print(
    "INSTABLES           :",
    len(unstable_fingerprints),
)


print()
print("=" * 70)
print("FINGERPRINTS STABLES")
print("=" * 70)


if not stable_fingerprints:

    print(
        "Aucun fingerprint canonique stable."
    )

else:

    for fingerprint in sorted(
        stable_fingerprints
    ):

        print()
        print(
            "FINGERPRINT :",
            fingerprint,
        )

        print(
            "RUNS        :",
            stable_fingerprints[
                fingerprint
            ],
        )

        print(
            "SOURCE RULE IDS"
        )

        for source_ids in fingerprint_source_ids[
            fingerprint
        ]:

            print(
                "-",
                ", ".join(source_ids),
            )


print()
print("=" * 70)
print("FINGERPRINTS INSTABLES")
print("=" * 70)


if not unstable_fingerprints:

    print(
        "Aucun fingerprint canonique instable."
    )

else:

    for fingerprint in sorted(
        unstable_fingerprints
    ):

        print()
        print(
            "FINGERPRINT :",
            fingerprint,
        )

        print(
            "RUNS        :",
            unstable_fingerprints[
                fingerprint
            ],
        )

        print(
            "SOURCE RULE IDS"
        )

        for source_ids in fingerprint_source_ids[
            fingerprint
        ]:

            print(
                "-",
                ", ".join(source_ids),
            )


total_fingerprints = len(
    fingerprint_presence
)

stable_count = len(
    stable_fingerprints
)


if total_fingerprints:

    stability_rate = (
        stable_count
        / total_fingerprints
        * 100
    )

else:

    stability_rate = 0.0


print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "RUNS                :",
    RUN_COUNT,
)

print(
    "FINGERPRINTS TOTAUX :",
    total_fingerprints,
)

print(
    "STABLES             :",
    stable_count,
)

print(
    "INSTABLES           :",
    len(unstable_fingerprints),
)

print(
    "TAUX DE STABILITÉ   :",
    f"{stability_rate:.2f} %",
)


print()
print("=" * 70)
print("VERDICT")
print("=" * 70)


if stability_rate >= 80:

    print(
        "CANONICALISATION TRÈS STABLE"
    )

elif stability_rate >= 70:

    print(
        "CANONICALISATION EXPLOITABLE"
    )

elif stability_rate >= 50:

    print(
        "CANONICALISATION PARTIELLEMENT STABLE"
    )

else:

    print(
        "CANONICALISATION INSUFFISAMMENT STABLE"
    )
    