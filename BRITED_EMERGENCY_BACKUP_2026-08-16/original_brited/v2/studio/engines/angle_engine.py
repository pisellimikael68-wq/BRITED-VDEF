from v2.models.knowledge_models import Topic

from v2.studio.editorial.editorial_types import EditorialAngle


class AngleEngine:
    """
    Sélectionne automatiquement le meilleur angle éditorial.
    """

    def select(
        self,
        topic: Topic,
    ) -> EditorialAngle:

        chapter = topic.chapter.lower()
        title = topic.title.lower()

        # ==================================================
        # CHAPITRES
        # ==================================================

        if chapter == "erreurs":
            return EditorialAngle.MISTAKE

        if chapter == "comparaisons":
            return EditorialAngle.COMPARISON

        if chapter == "questions_clients":
            return EditorialAngle.FAQ

        if chapter == "cas_particuliers":
            return EditorialAngle.CASE_STUDY

        if chapter in [
            "fiscalite",
            "transmission",
            "clause_beneficiaire",
        ]:
            return EditorialAngle.REGULATION

        # ==================================================
        # CONTENU
        # ==================================================

        if topic.misconceptions:
            return EditorialAngle.MYTH

        if topic.common_mistakes:
            return EditorialAngle.MISTAKE

        if topic.client_questions:
            return EditorialAngle.QUESTION

        # ==================================================
        # TITRE
        # ==================================================

        if " ou " in title:
            return EditorialAngle.COMPARISON

        if title.startswith("comment"):
            return EditorialAngle.EXPLANATION

        if title.startswith("pourquoi"):
            return EditorialAngle.EXPLANATION

        if title.startswith("qu'est-ce"):
            return EditorialAngle.EXPLANATION

        if title.startswith("peut-on"):
            return EditorialAngle.FAQ

        # ==================================================
        # PAR DÉFAUT
        # ==================================================

        return EditorialAngle.EXPLANATION

        