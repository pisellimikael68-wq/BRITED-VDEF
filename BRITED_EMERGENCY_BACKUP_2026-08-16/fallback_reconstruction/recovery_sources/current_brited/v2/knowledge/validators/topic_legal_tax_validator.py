import re
from dataclasses import dataclass, field

from v2.agents.models import WrittenTopic


@dataclass
class LegalTaxIssue:
    """
    Anomalie juridique ou fiscale détectée.
    """

    field: str
    message: str


@dataclass
class LegalTaxReport:
    """
    Rapport produit par le Legal & Tax Gate.
    """

    valid: bool
    issues: list[LegalTaxIssue] = field(
        default_factory=list
    )


class TopicLegalTaxValidator:
    """
    Contrôle la robustesse juridique et fiscale
    minimale d'un topic patrimonial.

    Ce validateur ne prétend pas vérifier la vérité
    juridique d'une affirmation.

    Il détecte notamment :
    - les sources vagues,
    - l'absence de références juridiques identifiables,
    - les taux et seuils fiscaux insuffisamment contextualisés,
    - les affirmations fiscales absolues,
    - certaines dates fiscales sensibles non contextualisées.
    """

    VAGUE_SOURCE_PATTERNS = (
        "dispositions fiscales",
        "dispositions juridiques",
        "réglementation applicable",
        "législation applicable",
        "textes applicables",
        "conditions et modalités",
        "règles fiscales",
        "règles juridiques",
        "doctrine fiscale",
    )

    LEGAL_REFERENCE_PATTERNS = (
           r"\bCGI\b",
        r"\bCode général des impôts\b",
        r"\bCode civil\b",
        r"\bCode des assurances\b",
        r"\bBOI-[A-Z0-9\-]+",
        r"\bBOFiP\b",
        r"\barticle\s+[A-Z]?\s*\d+",
        r"\bart\.\s*[A-Z]?\s*\d+",
        r"\bL\.\s*\d+",
        r"\bR\.\s*\d+",
        r"\binstruction fiscale\b",
        r"\b\d+\s*[A-Z]\s*-\s*\d+\s*-\s*\d+\b",
    )

    ABSOLUTE_TAX_PATTERNS = (
        r"\btoujours impos",
        r"\bjamais impos",
        r"\baucun impôt n['’]est dû\b",
        r"\bexonéré dans tous les cas\b",
        r"\bsystématiquement impos",
        r"\bs['’]appliquent systématiquement\b",
        r"\bquel que soit\b",
    )

    SENSITIVE_DATE_PATTERNS = (
        r"27 septembre 2017",
        r"26 septembre 2017",
    )

    def validate(
        self,
        topic: WrittenTopic,
    ) -> LegalTaxReport:

        issues: list[LegalTaxIssue] = []

        content = self._build_content(topic)

        self._validate_sources(
            topic=topic,
            issues=issues,
        )

        self._validate_tax_rates(
            content=content,
            issues=issues,
        )

        self._validate_tax_thresholds(
            content=content,
            issues=issues,
        )

        self._validate_absolute_statements(
            content=content,
            issues=issues,
        )

        self._validate_sensitive_dates(
            content=content,
            issues=issues,
        )

        return LegalTaxReport(
            valid=not issues,
            issues=issues,
        )

    def _validate_sources(
        self,
        *,
        topic: WrittenTopic,
        issues: list[LegalTaxIssue],
    ) -> None:

        if not topic.legal_sources:

            issues.append(
                LegalTaxIssue(
                    field="legal_sources",
                    message=(
                        "Aucune source juridique ou fiscale "
                        "n'a été fournie."
                    ),
                )
            )

            return

        sources_text = " ".join(
            topic.legal_sources
        )

        sources_lower = sources_text.lower()

        vague_sources = [
            pattern
            for pattern in self.VAGUE_SOURCE_PATTERNS
            if pattern in sources_lower
        ]

        if vague_sources:

            issues.append(
                LegalTaxIssue(
                    field="legal_sources",
                    message=(
                        "Sources juridiques ou fiscales trop "
                        "génériques : "
                        + ", ".join(vague_sources)
                    ),
                )
            )

        has_identifiable_reference = any(
            re.search(
                pattern,
                sources_text,
                flags=re.IGNORECASE,
            )
            for pattern in self.LEGAL_REFERENCE_PATTERNS
        )

        if not has_identifiable_reference:

            issues.append(
                LegalTaxIssue(
                    field="legal_sources",
                    message=(
                        "Aucune référence juridique ou fiscale "
                        "précisément identifiable n'a été détectée "
                        "(article, code, CGI ou BOFiP)."
                    ),
                )
            )

    @staticmethod
    def _validate_tax_rates(
        *,
        content: str,
        issues: list[LegalTaxIssue],
    ) -> None:

        rates = re.findall(
            r"\b\d+(?:[,.]\d+)?\s*%",
            content,
        )

        if not rates:

            return

        contextual_markers = (
            "avant",
            "après",
            "depuis",
            "jusqu'au",
            "jusqu’au",
            "date",
            "durée",
            "prime",
            "versement",
            "seuil",
            "option",
            "sous condition",
        )

        content_lower = content.lower()

        if not any(
            marker in content_lower
            for marker in contextual_markers
        ):

            issues.append(
                LegalTaxIssue(
                    field="tax_rates",
                    message=(
                        "Des taux fiscaux sont mentionnés "
                        f"({', '.join(sorted(set(rates)))}) "
                        "sans contexte fiscal temporel, "
                        "conditionnel ou quantitatif identifiable."
                    ),
                )
            )

    @staticmethod
    def _validate_tax_thresholds(
        *,
        content: str,
        issues: list[LegalTaxIssue],
    ) -> None:

        fiscal_terms = (
            "fiscal",
            "impôt",
            "imposition",
            "abattement",
            "prélèvement",
            "taxe",
            "exonération",
        )

        content_lower = content.lower()

        if not any(
            term in content_lower
            for term in fiscal_terms
        ):

            return

        monetary_amounts = re.findall(
            r"\b\d[\d\s]*(?:[,.]\d+)?\s*€",
            content,
        )

        if monetary_amounts:

            threshold_markers = (
                "seuil",
                "abattement",
                "limite",
                "plafond",
                "fraction",
                "montant",
                "prime",
                "versement",
                "gain",
                "produit",
            )

            if not any(
                marker in content_lower
                for marker in threshold_markers
            ):

                issues.append(
                    LegalTaxIssue(
                        field="tax_thresholds",
                        message=(
                            "Des montants fiscaux sont mentionnés "
                            "sans qualification suffisante de leur "
                            "nature ou de leur fonction."
                        ),
                    )
                )

        post_reform_life_insurance_context = (
            (
                "assurance-vie" in content_lower
                or "assurance vie" in content_lower
            )
            and (
                "7,5 %" in content_lower
                or "7.5 %" in content_lower
            )
            and "27 septembre 2017" in content_lower
        )

        if post_reform_life_insurance_context:

            threshold_150k_patterns = (
                r"150[\s\u00a0]*000\s*€",
                r"150[\s\u00a0]*000\s*euros",
            )

            has_150k_threshold = any(
                re.search(
                    pattern,
                    content,
                    flags=re.IGNORECASE,
                )
                for pattern in threshold_150k_patterns
            )

            if not has_150k_threshold:

                issues.append(
                    LegalTaxIssue(
                        field="tax_thresholds",
                        message=(
                            "Le taux de 7,5 % est présenté dans "
                            "un contexte de fiscalité postérieure "
                            "au 27 septembre 2017 sans mention du "
                            "seuil de 150 000 € de primes, "
                            "nécessaire pour contextualiser "
                            "l'application du régime."
                        ),
                    )
                )

    def _validate_absolute_statements(
        self,
        *,
        content: str,
        issues: list[LegalTaxIssue],
    ) -> None:

        detected = []

        for pattern in self.ABSOLUTE_TAX_PATTERNS:

            match = re.search(
                pattern,
                content,
                flags=re.IGNORECASE,
            )

            if match:

                detected.append(
                    match.group(0)
                )

        if detected:

            issues.append(
                LegalTaxIssue(
                    field="legal_tax_content",
                    message=(
                        "Formulations fiscales ou juridiques "
                        "absolues détectées : "
                        + ", ".join(
                            sorted(set(detected))
                        )
                        + ". Vérifier les conditions, exceptions "
                        "et limites du régime."
                    ),
                )
            )

    def _validate_sensitive_dates(
        self,
        *,
        content: str,
        issues: list[LegalTaxIssue],
    ) -> None:

        content_lower = content.lower()

        insurance_life_context = (
            "assurance-vie" in content_lower
            or "assurance vie" in content_lower
        )

        post_reform_terms = (
            "pfu",
            "prélèvement forfaitaire unique",
            "12,8 %",
            "12.8 %",
            "7,5 %",
            "7.5 %",
        )

        has_post_reform_tax_content = any(
            term in content_lower
            for term in post_reform_terms
        )

        if not (
            insurance_life_context
            and has_post_reform_tax_content
        ):

            return

        has_sensitive_date = any(
            re.search(
                pattern,
                content,
                flags=re.IGNORECASE,
            )
            for pattern in self.SENSITIVE_DATE_PATTERNS
        )

        if not has_sensitive_date:

            issues.append(
                LegalTaxIssue(
                    field="tax_dates",
                    message=(
                        "Le topic traite de la fiscalité "
                        "forfaitaire de l'assurance-vie sans "
                        "mentionner la date charnière du "
                        "27 septembre 2017."
                    ),
                )
            )

            return

        premium_date_patterns = (
            (
                r"primes?\s+vers[ée]es?\s+avant\s+"
                r"(?:le\s+)?27 septembre 2017"
            ),
            (
                r"primes?\s+vers[ée]es?\s+[àa]\s+compter\s+"
                r"du\s+27 septembre 2017"
            ),
            (
                r"versements?\s+effectu[ée]s?\s+avant\s+"
                r"(?:le\s+)?27 septembre 2017"
            ),
            (
                r"versements?\s+effectu[ée]s?\s+[àa]\s+compter\s+"
                r"du\s+27 septembre 2017"
            ),
        )

        has_premium_date_context = any(
            re.search(
                pattern,
                content,
                flags=re.IGNORECASE,
            )
            for pattern in premium_date_patterns
        )

        if not has_premium_date_context:

            issues.append(
                LegalTaxIssue(
                    field="tax_dates",
                    message=(
                        "La date du 27 septembre 2017 n'est pas "
                        "suffisamment contextualisée par rapport "
                        "aux primes versées avant ou à compter "
                        "de cette date."
                    ),
                )
            )

    @staticmethod
    def _build_content(
        topic: WrittenTopic,
    ) -> str:

        return "\n".join(
            [
                topic.title,
                topic.summary,
                topic.description,
                *topic.examples,
                *topic.legal_sources,
            ]
        )
    