from v2.knowledge.compiler.corpus_compiler import (
    CorpusCompiler,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print("=" * 70)
print("CORPUS COMPILER TEST")
print("=" * 70)

loader = AcademicKnowledgeLoader()

knowledges = loader.load_all()

compiler = CorpusCompiler()

corpus = compiler.compile(
    knowledges
)

print()

print("KNOWLEDGES :", len(knowledges))
print("RULES      :", len(corpus.rules))

print()

print("=" * 70)
print("APERÇU")
print("=" * 70)

for rule in corpus.rules[:10]:

    print()

    print("-" * 70)

    print(
        "ID        :",
        rule.id,
    )

    print(
        "FAMILY    :",
        rule.family,
    )

    print(
        "CHAPTER   :",
        rule.chapter,
    )

    print(
        "TYPE      :",
        rule.rule_type,
    )

    print(
        "STATEMENT :",
        rule.statement,
    )

print()

print("=" * 70)
print("CONTRÔLES")
print("=" * 70)

print(
    "CORPUS NON VIDE      :",
    len(corpus.rules) > 0,
)

print(
    "AUCUNE RÈGLE VIDE    :",
    all(
        rule.statement.strip()
        for rule in corpus.rules
    ),
)

ids_are_unique = (
    len(
        {
            rule.id
            for rule in corpus.rules
        }
    )
    == len(corpus.rules)
)

print(
    "IDS UNIQUES          :",
    ids_are_unique,
)

corpus2 = compiler.compile(
    knowledges
)

same = corpus.rules == corpus2.rules

print(
    "DÉTERMINISME         :",
    same,
)

if not same:

    print()

    print("=" * 70)
    print("DIFFÉRENCES")
    print("=" * 70)

    for first, second in zip(
        corpus.rules,
        corpus2.rules,
        strict=True,
    ):

        if first == second:
            continue

        print()

        print("-" * 70)
        print(
            "RULE :",
            first.id,
        )

        if first.statement != second.statement:

            print()

            print("STATEMENT")

            print("RUN 1")
            print(first.statement)

            print()

            print("RUN 2")
            print(second.statement)

        if first.conditions != second.conditions:

            print()

            print("CONDITIONS")

            print("RUN 1")
            print(first.conditions)

            print()

            print("RUN 2")
            print(second.conditions)

        if (
            first.required_elements
            != second.required_elements
        ):

            print()

            print("REQUIRED ELEMENTS")

            print("RUN 1")
            print(first.required_elements)

            print()

            print("RUN 2")
            print(second.required_elements)

        if (
            first.forbidden_interpretations
            != second.forbidden_interpretations
        ):

            print()

            print("FORBIDDEN INTERPRETATIONS")

            print("RUN 1")
            print(first.forbidden_interpretations)

            print()

            print("RUN 2")
            print(second.forbidden_interpretations)

        if (
            first.legal_references
            != second.legal_references
        ):

            print()

            print("LEGAL REFERENCES")

            print("RUN 1")
            print(first.legal_references)

            print()

            print("RUN 2")
            print(second.legal_references)

print()

print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "CORPUS COMPILER VALIDE :",
    (
        same
        and ids_are_unique
        and len(corpus.rules) > 0
    ),
)
