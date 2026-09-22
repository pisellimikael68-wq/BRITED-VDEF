from v2.studio.models.script import Script


def main():

    script = Script(
        title="Qu'est-ce qu'une assurance-vie ?",
        format="carousel",
        hook="L'assurance-vie est souvent mal comprise."
    )

    script.add_section(
        "Définition",
        "Une assurance-vie est une enveloppe d'investissement."
    )

    script.add_section(
        "Exemple",
        "Julie ouvre un contrat pour préparer sa retraite."
    )

    script.conclusion = (
        "L'assurance-vie est avant tout une enveloppe fiscale."
    )

    script.call_to_action = (
        "Enregistrez cette publication."
    )

    script.display()


if __name__ == "__main__":
    main()
    