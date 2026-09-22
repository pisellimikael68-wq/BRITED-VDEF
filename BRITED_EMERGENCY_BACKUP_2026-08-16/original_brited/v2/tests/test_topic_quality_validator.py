from v2.agents.models import WrittenTopic
from v2.knowledge.validators.topic_quality_validator import (
    TopicQualityValidator,
)


def main():

    validator = TopicQualityValidator()

    bad_topic = WrittenTopic(
        id="quality_bad_test",
        title="Test faible",
        summary="Résumé trop court.",
        description="Description trop courte.",
        keywords=["test"],
        vocabulary=["mot"],
        examples=[],
        legal_sources=[],
    )

    good_topic = WrittenTopic(
        id="quality_good_test",
        title="Fiscalité du rachat en assurance-vie",
        summary=(
            "Le rachat d'un contrat d'assurance-vie entraîne une "
            "imposition limitée à la quote-part de produits comprise "
            "dans la somme retirée par le souscripteur."
        ),
        description=(
            "Lorsqu'un souscripteur effectue un rachat partiel sur son "
            "contrat d'assurance-vie, la totalité de la somme retirée "
            "ne constitue pas un revenu imposable. Le rachat comprend "
            "une fraction correspondant au capital initialement versé "
            "et une fraction représentative des produits accumulés sur "
            "le contrat. Seule cette quote-part de produits entre dans "
            "l'assiette de l'impôt sur le revenu selon les règles "
            "fiscales applicables au contrat et à la date des versements."
        ),
        keywords=[
            "assurance-vie",
            "rachat",
            "fiscalité",
        ],
        vocabulary=[
            "rachat partiel",
            "produits",
        ],
        examples=[
            (
                "Un contrat valorisé 120 000 euros pour 100 000 euros "
                "de versements comporte 20 000 euros de produits."
            )
        ],
        legal_sources=[
            "CGI, article 125-0 A",
        ],
    )

    print("=" * 60)
    print("TOPIC FAIBLE")
    print("=" * 60)

    bad_report = validator.validate(bad_topic)

    print(f"Valide : {bad_report.valid}")
    print(f"Problèmes : {bad_report.issue_count}")

    for issue in bad_report.issues:
        print(f"- {issue.field}: {issue.message}")

    print()

    print("=" * 60)
    print("TOPIC VALIDE")
    print("=" * 60)

    good_report = validator.validate(good_topic)

    print(f"Valide : {good_report.valid}")
    print(f"Problèmes : {good_report.issue_count}")

    for issue in good_report.issues:
        print(f"- {issue.field}: {issue.message}")


if __name__ == "__main__":
    main()
    