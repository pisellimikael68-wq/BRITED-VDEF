from dataclasses import replace

from v2.knowledge.compiler.canonical_fingerprint import (
    CanonicalRuleFingerprintBuilder,
)
from v2.knowledge.compiler.canonical_models import (
    CanonicalRule,
)


print("=" * 70)
print("CANONICAL FINGERPRINT TEST")
print("=" * 70)


rule = CanonicalRule(
    id="rule_1",
    family="assurance_vie",
    chapter="rachats",
    rule_type="formula",
    statement="assiette taxable = valeur de rachat - primes",
    keywords=(
        "assiette taxable",
        "rachat",
    ),
    conditions=(
        "contrat racheté",
        "rachat total",
    ),
    required_elements=(
        "valeur de rachat",
        "primes versées",
    ),
    forbidden_interpretations=(
        "confondre avec un rachat partiel",
    ),
    legal_references=(
        "CGI art. 125-0 A",
    ),
)


builder = CanonicalRuleFingerprintBuilder()


fp1 = builder.build(rule)
fp2 = builder.build(rule)


same_twice = fp1 == fp2


rule_other_id = replace(
    rule,
    id="autre_id",
)

same_id = (
    builder.build(rule_other_id)
    == fp1
)


rule_order = replace(
    rule,
    conditions=tuple(
        reversed(rule.conditions)
    ),
    required_elements=tuple(
        reversed(rule.required_elements)
    ),
    legal_references=tuple(
        reversed(rule.legal_references)
    ),
)

same_order = (
    builder.build(rule_order)
    == fp1
)


rule_statement = replace(
    rule,
    statement="autre mécanisme",
)

statement_changed = (
    builder.build(rule_statement)
    != fp1
)


rule_type = replace(
    rule,
    rule_type="tax_rate",
)

type_changed = (
    builder.build(rule_type)
    != fp1
)


rule_condition = replace(
    rule,
    conditions=(
        "autre condition",
    ),
)

condition_changed = (
    builder.build(rule_condition)
    != fp1
)


rule_required = replace(
    rule,
    required_elements=(
        "autre élément",
    ),
)

required_changed = (
    builder.build(rule_required)
    != fp1
)


print()
print("FINGERPRINT")
print(fp1)

print()
print("=" * 70)
print("CONTRÔLES")
print("=" * 70)

print(
    "DÉTERMINISME                 :",
    same_twice,
)

print(
    "ID IGNORÉ                    :",
    same_id,
)

print(
    "ORDRE DES LISTES IGNORÉ      :",
    same_order,
)

print(
    "STATEMENT MODIFIÉ DÉTECTÉ    :",
    statement_changed,
)

print(
    "RULE TYPE MODIFIÉ DÉTECTÉ    :",
    type_changed,
)

print(
    "CONDITION MODIFIÉE DÉTECTÉE  :",
    condition_changed,
)

print(
    "REQUIRED MODIFIÉ DÉTECTÉ     :",
    required_changed,
)


valid = all(
    (
        same_twice,
        same_id,
        same_order,
        statement_changed,
        type_changed,
        condition_changed,
        required_changed,
    )
)

print()
print("=" * 70)
print("RÉSULTAT")
print("=" * 70)

print(
    "CANONICAL FINGERPRINT VALIDE :",
    valid,
)
