from v2.agents.models import WrittenTopic
from v2.knowledge.validators.topic_legal_tax_validator import (
    TopicLegalTaxValidator,
)


def print_report(
    title: str,
    topic: WrittenTopic,
) -> None:

    validator = TopicLegalTaxValidator()

    report = validator.validate(topic)

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(f"Valide : {report.valid}")
    print(f"Problèmes : {len(report.issues)}")

    for issue in report.issues:

        print(
            f"- {issue.field}: {issue.message}"
        )


def main() -> None:

    reform_date_topic = WrittenTopic(
        id="insurance_life_reform_date_valid",
        title="Fiscalité du rachat en assurance-vie",
        summary=(
            "La fiscalité des produits d'assurance-vie "
            "dépend notamment de la date à laquelle les "
            "primes ont été versées sur le contrat."
        ),
        description=(
            "Pour l'imposition des produits attachés aux "
            "primes versées, la date du 27 septembre 2017 "
            "constitue une date charnière. Les produits "
            "afférents aux primes versées avant cette date "
            "et ceux afférents aux primes versées à compter "
            "de cette date relèvent de règles fiscales "
            "distinctes. La date de souscription du contrat "
            "ne doit donc pas être confondue avec la date "
            "des versements prise en compte pour articuler "
            "ces régimes."
        ),
        keywords=[
            "assurance-vie",
            "rachat",
            "fiscalité",
        ],
        vocabulary=[
            "primes versées",
            "produits",
        ],
        examples=[
            (
                "Un contrat souscrit avant 2017 peut recevoir "
                "des primes versées à compter du "
                "27 septembre 2017."
            ),
        ],
        legal_sources=[
            (
                "Article 125-0 A du Code général "
                "des impôts (CGI)"
            ),
        ],
        prompt_hash="test",
    )

    threshold_topic = WrittenTopic(
        id="insurance_life_threshold_valid",
        title="Taux de 7,5 % en assurance-vie",
        summary=(
            "Le taux de 7,5 % applicable à certains produits "
            "d'assurance-vie doit être présenté avec les "
            "conditions prévues par le régime fiscal."
        ),
        description=(
            "Pour les primes versées à compter du "
            "27 septembre 2017, la présentation du taux "
            "de 7,5 % doit notamment tenir compte du seuil "
            "de 150 000 € de primes prévu pour apprécier "
            "le régime applicable. L'analyse dépend également "
            "de la durée du contrat et des conditions prévues "
            "par l'article 125-0 A du CGI. Le taux ne peut "
            "donc pas être présenté isolément comme un taux "
            "uniforme applicable à tous les rachats."
        ),
        keywords=[
            "assurance-vie",
            "7,5 %",
            "150 000 €",
        ],
        vocabulary=[
            "primes",
            "seuil fiscal",
        ],
        examples=[
            (
                "L'analyse d'un rachat après huit ans suppose "
                "de qualifier les primes concernées et "
                "d'apprécier le seuil de 150 000 €."
            ),
        ],
        legal_sources=[
            (
                "Article 125-0 A du Code général "
                "des impôts (CGI)"
            ),
        ],
        prompt_hash="test",
    )

    prudent_statement_topic = WrittenTopic(
        id="prudent_tax_statement_valid",
        title="Prélèvements sociaux et assurance-vie",
        summary=(
            "Le traitement social des produits issus d'un "
            "contrat d'assurance-vie dépend du support et "
            "des modalités de constatation des produits."
        ),
        description=(
            "Les prélèvements sociaux peuvent être appliqués "
            "selon des modalités différentes en fonction "
            "notamment de la nature du support et du moment "
            "auquel les produits sont constatés. Une analyse "
            "du contrat et du régime applicable reste donc "
            "nécessaire avant de présenter les conséquences "
            "sociales d'un rachat."
        ),
        keywords=[
            "assurance-vie",
            "prélèvements sociaux",
            "rachat",
        ],
        vocabulary=[
            "produits",
            "support",
        ],
        examples=[
            (
                "Le traitement d'un fonds en euros et celui "
                "d'unités de compte peuvent nécessiter une "
                "analyse distincte."
            ),
        ],
        legal_sources=[
            (
                "Article L. 136-7 du Code de la "
                "sécurité sociale"
            ),
        ],
        prompt_hash="test",
    )

    print_report(
        "DATE 27 SEPTEMBRE 2017 BIEN CONTEXTUALISÉE",
        reform_date_topic,
    )

    print_report(
        "TAUX DE 7,5 % AVEC SEUIL DE 150 000 €",
        threshold_topic,
    )

    print_report(
        "FORMULATION FISCALE PRUDENTE",
        prudent_statement_topic,
    )


if __name__ == "__main__":

    main()
    