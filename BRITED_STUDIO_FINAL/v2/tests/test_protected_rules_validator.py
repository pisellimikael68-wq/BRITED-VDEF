from v2.agents.models import PlannedTopic, WrittenTopic
from v2.knowledge.builders.knowledge_context_builder import (
    KnowledgeContextBuilder,
)
from v2.knowledge.validators.protected_rules_validator import (
    ProtectedRulesValidator,
)


def build_written_topic(
    description: str,
) -> WrittenTopic:

    return WrittenTopic(
        id="assurance_vie_fiscalite_rachat_test",
        title="Fiscalité du rachat en assurance-vie",
        summary=(
            "La fiscalité du rachat en assurance-vie porte "
            "sur les produits compris dans les sommes retirées. "
            "Elle dépend notamment de la durée du contrat, "
            "de la date de versement des primes et du seuil "
            "de 150 000 euros."
        ),
        description=description,
        keywords=[
            "assurance-vie",
            "rachat",
            "fiscalité",
        ],
        vocabulary=[
            "rachat total",
            "rachat partiel",
            "produits imposables",
        ],
        examples=[
            (
                "Pour 200 000 euros de primes et une valeur "
                "de rachat de 250 000 euros, un rachat partiel "
                "de 50 000 euros comprend 40 000 euros de primes, "
                "soit 200 000 × 50 000 / 250 000, et "
                "10 000 euros de produits."
            )
        ],
        legal_sources=[
            (
                "Instruction fiscale du 1er septembre 1994 "
                "n° 5 I-5-94"
            )
        ],
        prompt_hash="test",
    )


planned_topic = PlannedTopic(
    id="assurance_vie_fiscalite_rachat_test",
    title="Fiscalité du rachat en assurance-vie",
    editorial_order=1,
)

context = KnowledgeContextBuilder().build(
    family="assurance_vie",
    chapter="rachats",
    topic=planned_topic,
)

validator = ProtectedRulesValidator()


# ==========================================================
# TOPIC CORRECT
# ==========================================================

valid_topic = build_written_topic(
    """
    En cas de rachat total, les produits imposables
    correspondent à la différence entre la valeur de rachat
    et le total des primes versées.

    En cas de rachat partiel, les produits imposables
    correspondent au montant du rachat diminué de la
    quote-part de primes. Cette quote-part de primes est
    calculée proportionnellement à partir des primes versées
    multipliées par le rapport entre le montant du rachat
    et la valeur de rachat totale à la date du rachat.

    Pour les rachats successifs, les primes déjà réputées
    remboursées lors des rachats antérieurs sont retranchées
    des primes prises en compte pour un rachat ultérieur.

    Pour les primes versées à compter du 27 septembre 2017,
    lorsque le contrat a plus de huit ans, la fraction des
    produits correspondant aux primes relevant du seuil de
    150 000 euros est associée au taux forfaitaire de 7,5 %.

    La fraction des produits correspondant à la part de primes
    dépassant 150 000 euros est associée au taux de 12,8 %.

    Le dépassement du seuil de 150 000 euros ne conduit pas
    à appliquer automatiquement le taux de 12,8 % à
    l'intégralité des produits. Le taux de 12,8 % concerne
    uniquement la fraction des produits correspondant à la
    part de primes dépassant le seuil.

    Un montant de primes inférieur au seuil de 150 000 euros
    ne constitue pas une exonération générale d'impôt sur
    le revenu.
    """
)


# ==========================================================
# ERREUR 1 — 12,8 % GLOBAL
# ==========================================================

invalid_global_128 = build_written_topic(
    """
    En cas de rachat total, les produits imposables
    correspondent à la différence entre la valeur de rachat
    et le total des primes versées.

    En cas de rachat partiel, la quote-part de primes est
    calculée proportionnellement à partir des primes versées
    multipliées par le rapport entre le montant du rachat
    et la valeur de rachat totale à la date du rachat.

    Pour les rachats successifs, les primes déjà réputées
    remboursées sont retranchées des primes prises en compte
    lors d'un rachat ultérieur.

    Pour les primes versées à compter du 27 septembre 2017
    et un contrat de plus de huit ans, le taux de 7,5 %
    s'articule avec le seuil de 150 000 euros.

    La fraction des produits correspondant aux primes
    excédant 150 000 euros relève du taux de 12,8 %.

    Lorsque le montant des primes dépasse 150 000 euros,
    l'intégralité des produits est imposée au taux de 12,8 %.

    Un montant inférieur à 150 000 euros ne constitue pas
    une exonération générale d'impôt sur le revenu.
    """
)


# ==========================================================
# ERREUR 2 — FAUSSE EXONÉRATION
# ==========================================================

invalid_exemption = build_written_topic(
    """
    En cas de rachat total, les produits imposables
    correspondent à la différence entre la valeur de rachat
    et le total des primes versées.

    En cas de rachat partiel, la quote-part de primes est
    calculée proportionnellement à partir des primes versées
    multipliées par le rapport entre le montant du rachat
    et la valeur de rachat totale à la date du rachat.

    Pour les rachats successifs, les primes déjà réputées
    remboursées sont retranchées des primes prises en compte
    lors d'un rachat ultérieur.

    Pour les primes versées à compter du 27 septembre 2017
    et un contrat de plus de huit ans, la fraction des produits
    correspondant aux primes relevant du seuil de 150 000 euros
    est associée au taux de 7,5 %.

    La fraction des produits correspondant à la part de primes
    dépassant 150 000 euros est associée au taux de 12,8 %.

    Le taux de 12,8 % concerne uniquement la fraction des
    produits correspondant à la part de primes dépassant
    le seuil de 150 000 euros.

    Lorsque les primes sont inférieures à 150 000 euros,
    les produits sont exonérés d'impôt sur le revenu.
    """
)


def print_report(
    label: str,
    topic: WrittenTopic,
) -> bool:

    report = validator.validate(
        topic=topic,
        protected_rules=context.protected_rules,
    )

    print()
    print("=" * 70)
    print(label)
    print("=" * 70)

    print("VALID :", report.valid)
    print("ISSUES :", report.issue_count)

    for issue in report.issues:

        print()
        print("RULE ID       :", issue.rule_id)
        print("VALIDATOR KEY :", issue.validator_key)
        print("MESSAGE       :", issue.message)

    return report.valid


valid_result = print_report(
    "TOPIC CORRECT",
    valid_topic,
)

global_128_result = print_report(
    "ERREUR 12,8 % GLOBAL",
    invalid_global_128,
)

exemption_result = print_report(
    "ERREUR EXONÉRATION",
    invalid_exemption,
)


print()
print("=" * 70)
print("RÉSULTAT GLOBAL")
print("=" * 70)

test_valid = (
    valid_result is True
    and global_128_result is False
    and exemption_result is False
)

print("TOPIC CORRECT ACCEPTÉ      :", valid_result)
print(
    "ERREUR 12,8 % REJETÉE     :",
    not global_128_result,
)
print(
    "ERREUR EXONÉRATION REJETÉE:",
    not exemption_result,
)

print()
print("PROTECTED RULES GATE VALIDE :", test_valid)

if not test_valid:
    raise SystemExit(1)
