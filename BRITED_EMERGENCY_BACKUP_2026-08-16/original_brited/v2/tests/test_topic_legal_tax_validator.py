from v2.agents.models import WrittenTopic
from v2.knowledge.validators.topic_legal_tax_validator import (
    TopicLegalTaxValidator,
)


def build_weak_tax_topic() -> WrittenTopic:

    return WrittenTopic(
        id="assurance_vie_legal_tax_test",
        title="Fiscalité du rachat en assurance-vie",
        summary=(
            "La fiscalité du rachat dépend de la durée du contrat "
            "et du montant des gains imposables."
        ),
        description=(
            "Après 8 ans, les gains peuvent être imposés à 7,5 %. "
            "Les prélèvements sociaux sont dus quel que soit l'âge "
            "du contrat. Le rachat permet de récupérer le capital. "
            "La fiscalité dépend également des sommes retirées."
        ),
        keywords=[
            "assurance-vie",
            "rachat",
            "fiscalité",
        ],
        vocabulary=[
            "rachat",
            "gain imposable",
        ],
        examples=[
            (
                "Un contrat de 10 ans génère 12 000 € de gains. "
                "Après abattement, les sommes restantes sont "
                "imposées à 7,5 %."
            ),
            (
                "Un contrat sans gains est totalement racheté. "
                "Aucun impôt n'est dû."
            ),
        ],
        legal_sources=[
            (
                "Dispositions fiscales relatives à l'imposition "
                "des gains issus des contrats d'assurance-vie."
            ),
            (
                "Conditions et modalités des rachats dans les "
                "contrats d'assurance-vie."
            ),
        ],
        prompt_hash="test",
    )


def build_valid_tax_topic() -> WrittenTopic:

    return WrittenTopic(
        id="assurance_vie_legal_tax_valid_test",
        title="Fiscalité du rachat en assurance-vie",
        summary=(
            "Lors d'un rachat d'assurance-vie, seule la fraction "
            "correspondant aux produits comprise dans le retrait "
            "entre dans le champ de l'imposition sur le revenu."
        ),
        description=(
            "Le régime fiscal dépend notamment de l'ancienneté du "
            "contrat et de la date de versement des primes. Pour les "
            "produits attachés aux primes versées à compter du "
            "27 septembre 2017, les règles du prélèvement forfaitaire "
            "prévu par le Code général des impôts doivent être "
            "distinguées du régime applicable aux versements "
            "antérieurs. Après huit ans, l'abattement annuel applicable "
            "aux produits doit être pris en compte avant l'imposition. "
            "L'analyse du taux applicable suppose également d'identifier "
            "le montant des primes concernées et les conditions prévues "
            "par le régime fiscal."
        ),
        keywords=[
            "assurance-vie",
            "rachat",
            "fiscalité",
        ],
        vocabulary=[
            "produits",
            "primes",
            "rachat partiel",
        ],
        examples=[
            (
                "Un souscripteur effectue un rachat partiel. La fraction "
                "de produits comprise dans le retrait est déterminée "
                "avant l'application du régime fiscal correspondant "
                "à la date des primes et à l'ancienneté du contrat."
            )
        ],
        legal_sources=[
            "Code général des impôts, article 125-0 A",
            "BOFiP, BOI-RPPM-RCM-20-10-20-50",
        ],
        prompt_hash="test",
    )


def print_report(
    title: str,
    report,
) -> None:

    print("=" * 60)
    print(title)
    print("=" * 60)

    print(f"Valide : {report.valid}")
    print(f"Problèmes : {len(report.issues)}")

    for issue in report.issues:

        print(
            f"- {issue.field}: "
            f"{issue.message}"
        )

    print()


def main():

    validator = TopicLegalTaxValidator()

    weak_report = validator.validate(
        build_weak_tax_topic()
    )

    valid_report = validator.validate(
        build_valid_tax_topic()
    )

    print_report(
        "TOPIC FISCAL FAIBLE",
        weak_report,
    )

    print_report(
        "TOPIC FISCAL ROBUSTE",
        valid_report,
    )


if __name__ == "__main__":

    main()
    