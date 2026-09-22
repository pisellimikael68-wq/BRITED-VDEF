from dataclasses import dataclass, field

from v2.agents.models import WrittenTopic


@dataclass(slots=True)
class QualityIssue:
    """
    Représente un problème de qualité détecté
    sur un topic généré.
    """

    field: str
    message: str


@dataclass(slots=True)
class TopicQualityReport:
    """
    Rapport du contrôle qualité d'un topic.
    """

    issues: list[QualityIssue] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.issues

    @property
    def issue_count(self) -> int:
        return len(self.issues)


class TopicQualityValidator:
    """
    Contrôle la qualité éditoriale minimale
    d'un WrittenTopic avant son export.
    """

    MIN_SUMMARY_LENGTH = 80
    MIN_DESCRIPTION_LENGTH = 250

    MIN_KEYWORDS = 3
    MIN_VOCABULARY = 2
    MIN_EXAMPLES = 1
    MIN_LEGAL_SOURCES = 1

    GENERIC_EXPRESSIONS = (
        "il est important de noter",
        "il convient de noter",
        "dans le monde d'aujourd'hui",
        "de nos jours",
        "en conclusion",
        "pour conclure",
    )

    def validate(
        self,
        topic: WrittenTopic,
    ) -> TopicQualityReport:

        report = TopicQualityReport()

        self._validate_summary(
            topic=topic,
            report=report,
        )

        self._validate_description(
            topic=topic,
            report=report,
        )

        self._validate_keywords(
            topic=topic,
            report=report,
        )

        self._validate_vocabulary(
            topic=topic,
            report=report,
        )

        self._validate_examples(
            topic=topic,
            report=report,
        )

        self._validate_legal_sources(
            topic=topic,
            report=report,
        )

        self._validate_generic_content(
            topic=topic,
            report=report,
        )

        return report

    def _validate_summary(
        self,
        *,
        topic: WrittenTopic,
        report: TopicQualityReport,
    ) -> None:

        summary = topic.summary.strip()

        if len(summary) < self.MIN_SUMMARY_LENGTH:
            report.issues.append(
                QualityIssue(
                    field="summary",
                    message=(
                        "Résumé trop court "
                        f"({len(summary)} caractères, "
                        f"minimum {self.MIN_SUMMARY_LENGTH})."
                    ),
                )
            )

    def _validate_description(
        self,
        *,
        topic: WrittenTopic,
        report: TopicQualityReport,
    ) -> None:

        description = topic.description.strip()

        if len(description) < self.MIN_DESCRIPTION_LENGTH:
            report.issues.append(
                QualityIssue(
                    field="description",
                    message=(
                        "Description trop courte "
                        f"({len(description)} caractères, "
                        f"minimum {self.MIN_DESCRIPTION_LENGTH})."
                    ),
                )
            )

    def _validate_keywords(
        self,
        *,
        topic: WrittenTopic,
        report: TopicQualityReport,
    ) -> None:

        keywords = {
            keyword.strip().lower()
            for keyword in topic.keywords
            if keyword.strip()
        }

        if len(keywords) < self.MIN_KEYWORDS:
            report.issues.append(
                QualityIssue(
                    field="keywords",
                    message=(
                        "Nombre insuffisant de mots-clés "
                        f"({len(keywords)}, "
                        f"minimum {self.MIN_KEYWORDS})."
                    ),
                )
            )

    def _validate_vocabulary(
        self,
        *,
        topic: WrittenTopic,
        report: TopicQualityReport,
    ) -> None:

        vocabulary = {
            word.strip().lower()
            for word in topic.vocabulary
            if word.strip()
        }

        if len(vocabulary) < self.MIN_VOCABULARY:
            report.issues.append(
                QualityIssue(
                    field="vocabulary",
                    message=(
                        "Vocabulaire insuffisant "
                        f"({len(vocabulary)}, "
                        f"minimum {self.MIN_VOCABULARY})."
                    ),
                )
            )

    def _validate_examples(
        self,
        *,
        topic: WrittenTopic,
        report: TopicQualityReport,
    ) -> None:

        examples = [
            example.strip()
            for example in topic.examples
            if example.strip()
        ]

        if len(examples) < self.MIN_EXAMPLES:
            report.issues.append(
                QualityIssue(
                    field="examples",
                    message=(
                        "Aucun exemple exploitable "
                        "n'a été généré."
                    ),
                )
            )

    def _validate_legal_sources(
        self,
        *,
        topic: WrittenTopic,
        report: TopicQualityReport,
    ) -> None:

        legal_sources = [
            source.strip()
            for source in topic.legal_sources
            if source.strip()
        ]

        if len(legal_sources) < self.MIN_LEGAL_SOURCES:
            report.issues.append(
                QualityIssue(
                    field="legal_sources",
                    message=(
                        "Aucune source juridique ou fiscale "
                        "n'a été fournie."
                    ),
                )
            )

    def _validate_generic_content(
        self,
        *,
        topic: WrittenTopic,
        report: TopicQualityReport,
    ) -> None:

        content = (
            f"{topic.summary}\n"
            f"{topic.description}"
        ).lower()

        detected_expressions = [
            expression
            for expression in self.GENERIC_EXPRESSIONS
            if expression in content
        ]

        if detected_expressions:
            report.issues.append(
                QualityIssue(
                    field="content",
                    message=(
                        "Expressions éditoriales génériques détectées : "
                        + ", ".join(detected_expressions)
                    ),
                )
            )
            