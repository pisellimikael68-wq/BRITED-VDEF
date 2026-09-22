from v2.agents.models import WrittenTopic
from v2.knowledge.validators.topic_legal_tax_validator import (
    TopicLegalTaxValidator,
)


def main() -> None:

    validator = TopicLegalTaxValidator()

    topic = WrittenTopic(
        id="assurance_vie_tax_date_source_leak_test",
        title="Fiscalité du rachat en assurance-vie",
        summary=(
            "La fiscalité d'un rachat en assurance-vie dépend "
            "notamment de l'ancienneté du contrat et du régime "
            "fiscal applicable aux produits compris dans le retrait."
        ),
        description=(
            "Après huit ans, certains produits peuvent relever "
            "d'un taux de 7,5 % selon les conditions fiscales "
            "applicables. Le souscripteur doit distinguer les "
            "primes versées du montant des produits compris dans "
            "le rachat. Le régime fiscal peut également dépendre "
            "du montant des primes et des caractéristiques du contrat."
        ),
        keywords=[
            "assurance-vie",
            "rachat",
            "fiscalité",
        ],
        vocabulary=[
            "produits",
            "primes versées",
        ],
        examples=[
            (
                "Un souscripteur effectue un rachat partiel "
                "comprenant une fraction de produits imposables."
            ),
        ],
        legal_sources=[
            (
                "Article 125-0 A du Code général des impôts : "
                "régime applicable aux primes versées à compter "
                "du 27 septembre 2017 et seuil de 150 000 €."
            ),
        ],
        prompt_hash="test",
    )

    report = validator.validate(topic)

    print("=" * 60)
    print("DATE PRÉSENTE UNIQUEMENT DANS LES SOURCES")
    print("=" * 60)

    print(f"Valide : {report.valid}")
    print(f"Problèmes : {len(report.issues)}")

    for issue in report.issues:
        print(
            f"- {issue.field}: "
            f"{issue.message}"
        )


if __name__ == "__main__":
    main()
    