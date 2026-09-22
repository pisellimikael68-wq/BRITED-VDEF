from pathlib import Path


FONDAMENTAUX_TOPICS = [

    ("definition", "Définition de l'assurance-vie"),
    ("historique", "Historique de l'assurance-vie"),
    ("objectifs", "Objectifs patrimoniaux"),
    ("acteurs", "Les acteurs du contrat"),
    ("souscripteur", "Le souscripteur"),
    ("assure", "L'assuré"),
    ("beneficiaire", "Le bénéficiaire"),
    ("contrat_individuel", "Le contrat individuel"),
    ("contrat_collectif", "Le contrat collectif"),
    ("fonctionnement_general", "Fonctionnement général"),
    ("capitalisation", "Principe de capitalisation"),
    ("duree", "Durée du contrat"),
    ("liquidite", "Liquidité"),
    ("avantages", "Avantages"),
    ("inconvenients", "Limites et inconvénients"),
    ("cadre_juridique", "Cadre juridique"),
    ("cadre_fiscal", "Cadre fiscal"),
    ("vocabulaire", "Vocabulaire essentiel"),
    ("cas_usage", "Cas d'utilisation"),
    ("points_attention", "Points de vigilance"),
]


def generate_topics(
    family: str,
    chapter: str,
    topics: list[tuple[str, str]],
):

    path = (
        Path("v2")
        / "knowledge"
        / "plans"
        / "v2"
        / "knowledge"
        / family
        / f"{chapter}.md"
    )

    if not path.exists():

        raise FileNotFoundError(path)

    lines = []

    lines.append("---")
    lines.append("pillar: epargne")
    lines.append(f"family: {family}")
    lines.append(f"chapter: {chapter}")
    lines.append("---")
    lines.append("")

    for order, (slug, title) in enumerate(topics, start=1):

        lines.extend(
            [
                f"## {family}_{chapter}_{slug}",
                "",
                f"title: {title}",
                f"editorial_order: {order}",
                "difficulty: beginner",
                "priority: 50",
                "",
                "keywords:",
                "",
                "vocabulary:",
                "",
                "description:",
                "",
                "examples:",
                "",
                "legal_sources:",
                "",
                "---",
                "",
            ]
        )

    path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"✅ {path}")


if __name__ == "__main__":

    generate_topics(
        family="assurance_vie",
        chapter="fondamentaux",
        topics=FONDAMENTAUX_TOPICS,
    )
    