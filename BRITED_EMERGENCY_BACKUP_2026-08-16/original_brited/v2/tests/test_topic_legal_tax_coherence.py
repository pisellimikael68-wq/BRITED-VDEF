from v2.agents.models import WrittenTopic
from v2.knowledge.validators.topic_legal_tax_validator import (
    TopicLegalTaxValidator,
)


def build_topic(
    *,
    description: str,
) -> WrittenTopic:

    return WrittenTopic(
        id="assurance_vie_fiscalite_coherence_test",
        title="Fiscalité du rachat en assurance-vie",
        summary=(
            "La fiscalité du rachat en assurance-vie dépend "
            "du régime fiscal applicable aux produits générés "
            "par le contrat et des caractéristiques du rachat."
        ),
        description=description,
        keywords=[
            "assurance-vie",
            "rachat",
            "fiscalité",
        ],
        vocabulary=[
            "produits imposables",
            "primes versées",
        ],
        examples=[
            (
                "Un souscripteur réalise un rachat partiel "
                "comprenant une fraction de produits imposables."
            )
        ],
        legal_sources=[
            "Article 125-0 A du Code général des impôts (CGI)",
            (
                "BOFiP-Impôts, BOI-RPPM-RCM-10-10-80, "
                "revenus de capitaux mobiliers et assurance-vie"
            ),
        ],
        prompt_hash="test-hash",
    )


def display_report(
    title: str,
    report,
) -> None:

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"Valide : {report.valid}")
    print(f"Problèmes : {len(report.issues)}")

    for issue in report.issues:
        print(
            f"- {issue.field}: "
            f"{issue.message}"
        )


def main():

    validator = TopicLegalTaxValidator()

    # --------------------------------------------------
    # TEST 1
    # 27 septembre 2017 mal relié à la souscription
    # --------------------------------------------------

    topic_wrong_date_link = build_topic(
        description=(
            "La fiscalité du rachat dépend de la date de "
            "souscription du contrat. Depuis le 27 septembre "
            "2017, les contrats sont soumis au prélèvement "
            "forfaitaire unique. Le traitement des produits "
            "dépend également de la durée du contrat et des "
            "modalités du rachat effectué par le souscripteur."
        )
    )

    report_wrong_date_link = validator.validate(
        topic_wrong_date_link
    )

    display_report(
        "DATE 27 SEPTEMBRE 2017 MAL RELIÉE",
        report_wrong_date_link,
    )

    # --------------------------------------------------
    # TEST 2
    # 7,5 % sans seuil de 150 000 €
    # --------------------------------------------------

    topic_missing_threshold = build_topic(
        description=(
            "Pour les primes versées à compter du "
            "27 septembre 2017, les produits attachés au "
            "contrat peuvent relever du prélèvement forfaitaire. "
            "Après huit ans, le taux de 7,5 % peut s'appliquer "
            "aux gains imposables après prise en compte de "
            "l'abattement annuel applicable."
        )
    )

    report_missing_threshold = validator.validate(
        topic_missing_threshold
    )

    display_report(
        "TAUX DE 7,5 % SANS SEUIL DE 150 000 €",
        report_missing_threshold,
    )

    # --------------------------------------------------
    # TEST 3
    # Formulation fiscale absolue
    # --------------------------------------------------

    topic_absolute_statement = build_topic(
        description=(
            "Pour les primes versées à compter du "
            "27 septembre 2017, le régime fiscal dépend des "
            "conditions prévues par l'article 125-0 A du CGI. "
            "Les prélèvements sociaux de 17,2 % s'appliquent "
            "systématiquement aux revenus du contrat, quelle "
            "que soit sa durée. Le souscripteur doit distinguer "
            "les primes versées des produits générés."
        )
    )

    report_absolute_statement = validator.validate(
        topic_absolute_statement
    )

    display_report(
        "FORMULATION FISCALE ABSOLUE",
        report_absolute_statement,
    )


if __name__ == "__main__":
    main()
    