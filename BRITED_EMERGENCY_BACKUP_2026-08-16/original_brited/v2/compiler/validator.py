from .models import RawChapter


VALID_DIFFICULTIES = {
    "Débutant",
    "Intermédiaire",
    "Avancé",
    "Expert",
}


def validate_chapter(chapter: RawChapter) -> list[str]:
    """
    Valide un chapitre et retourne la liste des erreurs.
    """

    errors = []

    ids = set()
    editorial_orders = set()

    for topic in chapter.topics:

        # -----------------------------
        # ID unique
        # -----------------------------

        if topic.id in ids:
            errors.append(
                f"ID dupliqué : {topic.id}"
            )

        ids.add(topic.id)

        # -----------------------------
        # Editorial order unique
        # -----------------------------

        if topic.editorial_order in editorial_orders:
            errors.append(
                f"Editorial order dupliqué : {topic.editorial_order}"
            )

        editorial_orders.add(topic.editorial_order)

        # -----------------------------
        # Difficulté valide
        # -----------------------------

        if topic.difficulty not in VALID_DIFFICULTIES:
            errors.append(
                f"Difficulté invalide : {topic.difficulty}"
            )

        # -----------------------------
        # Priorité
        # -----------------------------

        if not (1 <= topic.priority <= 10):
            errors.append(
                f"Priorité invalide ({topic.priority}) pour {topic.id}"
            )

    # -----------------------------
    # Vérifie la continuité
    # -----------------------------

    expected = list(range(1, len(chapter.topics) + 1))

    if sorted(editorial_orders) != expected:

        errors.append(
            f"Editorial order attendu : {expected} "
            f"mais obtenu : {sorted(editorial_orders)}"
        )

    return errors
