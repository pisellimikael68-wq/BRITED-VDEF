from v2.knowledge.compiler.rule_canonicalizer import (
    RuleCanonicalizer,
)
from v2.knowledge.compiler.seed_knowledge_compiler import (
    SeedKnowledgeCompiler,
)
from v2.knowledge.loaders.academic_knowledge_loader import (
    AcademicKnowledgeLoader,
)


print("=" * 70)
print("RULE CANONICALIZER TEST")
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


compiler = SeedKnowledgeCompiler()
canonicalizer = RuleCanonicalizer()


compiled = compiler.compile(
    knowledge
)

canonical_first = canonicalizer.canonicalize(
    compiled
)

canonical_second = canonicalizer.canonicalize(
    compiled
)


print()
print("SOURCE          :", canonical_first.source_id)
print("FAMILY          :", canonical_first.family)
print("CHAPTER         :", canonical_first.chapter)
print("COMPILED RULES  :", len(compiled.rules))
print("CANONICAL RULES :", len(canonical_first.rules))


ids_preserved = (
    [rule.id for rule in compiled.rules]
    == [rule.id for rule in canonical_first.rules]
)

same_rule_count = (
    len(compiled.rules)
    == len(canonical_first.rules)
)

deterministic = (
    canonical_first
    == canonical_second
)

collections_are_tuples = all(
    isinstance(rule.keywords, tuple)
    and isinstance(rule.conditions, tuple)
    and isinstance(rule.required_elements, tuple)
    and isinstance(
        rule.forbidden_interpretations,
        tuple,
    )
    and isinstance(
        rule.legal_references,
        tuple,
    )
    for rule in canonical_first.rules
)

collections_are_sorted = all(
    rule.keywords
    == tuple(sorted(rule.keywords))
    and rule.conditions
    == tuple(sorted(rule.conditions))
    and rule.required_elements
    == tuple(
        sorted(rule.required_elements)
    )
    and rule.forbidden_interpretations
    == tuple(
        sorted(
            rule.forbidden_interpretations
        )
    )
    and rule.legal_references
    == tuple(
        sorted(rule.legal_references)
    )
    for rule in canonical_first.rules
)

collections_are_unique = all(
    len(rule.keywords)
    == len(set(rule.keywords))
    and len(rule.conditions)
    == len(set(rule.conditions))
    and len(rule.required_elements)
    == len(set(rule.required_elements))
    and len(
        rule.forbidden_interpretations
    )
    == len(
        set(rule.forbidden_interpretations)
    )
    and len(rule.legal_references)
    == len(set(rule.legal_references))
    for rule in canonical_first.rules
)


for rule in canonical_first.rules:

    print()
    print("-" * 70)
    print("ID       :", rule.id)
    print("TYPE     :", rule.rule_type)
    print("FAMILY   :", rule.family)
    print("CHAPTER  :", rule.chapter)
    print()
    print("STATEMENT")
    print(rule.statement)
    print()
    print("CONDITIONS")
    for value in rule.conditions:
        print("-", value)


print()
print("=" * 70)
print("CONTRÔLES")
print("=" * 70)

print(
    "MÊME NOMBRE DE RÈGLES :",
    same_rule_count,
)

print(
    "IDS CONSERVÉS         :",
    ids_preserved,
)

print(
    "COLLECTIONS EN TUPLES :",
    collections_are_tuples,
)

print(
    "COLLECTIONS TRIÉES    :",
    collections_are_sorted,
)

print(
    "DOUBLONS SUPPRIMÉS    :",
    collections_are_unique,
)

print(
    "DÉTERMINISME          :",
    deterministic,
)


valid = all(
    (
        same_rule_count,
        ids_preserved,
        collections_are_tuples,
        collections_are_sorted,
        collections_are_unique,
        deterministic,
    )
)


print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "RULE CANONICALIZER VALIDE :",
    valid,
)
