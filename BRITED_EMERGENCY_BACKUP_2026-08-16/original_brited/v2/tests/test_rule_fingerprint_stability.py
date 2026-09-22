from collections import defaultdict

from v2.knowledge.compiler.knowledge_compiler import (
    KnowledgeCompiler,
)
from v2.knowledge.compiler.rule_fingerprint import (
    RuleFingerprintBuilder,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


RUN_COUNT = 3


print("=" * 70)
print("RULE FINGERPRINT STABILITY TEST")
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

runs: list[dict[str, str]] = []

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

    compiled = compiler.compile(
        knowledge
    )

    run_fingerprints: dict[str, str] = {}

    for rule in compiled.rules:

        fingerprint = RuleFingerprintBuilder.build(
            family=compiled.family,
            chapter=compiled.chapter,
            rule=rule,
        )

        run_fingerprints[
            fingerprint
        ] = rule.id

    runs.append(
        run_fingerprints
    )

    print(
        "RULES      :",
        len(compiled.rules),
    )

    print(
        "FINGERPRINTS :",
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

fingerprint_rule_ids: dict[
    str,
    list[str],
] = defaultdict(list)

for run_index, run in enumerate(
    runs,
    start=1,
):

    for fingerprint, rule_id in run.items():

        fingerprint_presence[
            fingerprint
        ].append(
            run_index
        )

        fingerprint_rule_ids[
            fingerprint
        ].append(
            rule_id
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
print("FINGERPRINTS TOTAUX :", len(fingerprint_presence))

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

    print("Aucun fingerprint stable.")

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

        print("RULE IDS")

        for rule_id in fingerprint_rule_ids[
            fingerprint
        ]:

            print(
                "-",
                rule_id,
            )


print()
print("=" * 70)
print("FINGERPRINTS INSTABLES")
print("=" * 70)

if not unstable_fingerprints:

    print("Aucun fingerprint instable.")

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

        print("RULE IDS")

        for rule_id in fingerprint_rule_ids[
            fingerprint
        ]:

            print(
                "-",
                rule_id,
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
