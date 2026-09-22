import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable

from v2.agents.models import WrittenTopic
from v2.knowledge.sources.academic_models import (
    ProtectedRule,
)


@dataclass(slots=True)
class ProtectedRuleIssue:
    """
    Anomalie détectée par le Protected Rules Gate.
    """

    field: str
    message: str

    rule_id: str = ""
    validator_key: str = ""


@dataclass(slots=True)
class ProtectedRulesReport:
    """
    Rapport produit par le Protected Rules Gate.
    """

    issues: list[ProtectedRuleIssue] = field(
        default_factory=list
    )

    @property
    def valid(self) -> bool:
        return not self.issues

    @property
    def issue_count(self) -> int:
        return len(self.issues)


class ProtectedRulesValidator:
    """
    Contrôle les règles Knowledge protégées applicables
    à un topic généré.

    Chaque validator_key est reliée à une fonction
    déterministe.

    Les contrôles négatifs sont effectués phrase par phrase
    afin de distinguer une affirmation interdite de sa
    négation explicite.
    """

    def __init__(self):

        self.validators: dict[
            str,
            Callable[
                [str, ProtectedRule],
                ProtectedRuleIssue | None,
            ],
        ] = {
            "av_rachat_total_formula": (
                self._validate_av_rachat_total_formula
            ),
            "av_rachat_partiel_formula": (
                self._validate_av_rachat_partiel_formula
            ),
            "av_rachats_successifs": (
                self._validate_av_rachats_successifs
            ),
            "av_post_2017_rate_75": (
                self._validate_av_post_2017_rate_75
            ),
            "av_post_2017_rate_128": (
                self._validate_av_post_2017_rate_128
            ),
            "av_150k_not_global_128": (
                self._validate_av_150k_not_global_128
            ),
            "av_150k_not_exemption": (
                self._validate_av_150k_not_exemption
            ),
        }

    def validate(
        self,
        *,
        topic: WrittenTopic,
        protected_rules: list[ProtectedRule],
    ) -> ProtectedRulesReport:

        report = ProtectedRulesReport()

        content = self._normalize(
            self._build_content(topic)
        )

        for rule in protected_rules:

            validator_key = rule.validator_key.strip()

            if not validator_key:
                continue

            validator = self.validators.get(
                validator_key
            )

            if validator is None:

                report.issues.append(
                    ProtectedRuleIssue(
                        field="protected_rules",
                        message=(
                            "Aucun validateur déterministe "
                            "n'est enregistré pour la règle "
                            f"'{rule.id}' "
                            f"(validator_key='{validator_key}')."
                        ),
                        rule_id=rule.id,
                        validator_key=validator_key,
                    )
                )

                continue

            issue = validator(
                content,
                rule,
            )

            if issue is not None:
                report.issues.append(issue)

        return report

    # ==========================================================
    # ASSURANCE-VIE — RACHAT TOTAL
    # ==========================================================

    def _validate_av_rachat_total_formula(
        self,
        content: str,
        rule: ProtectedRule,
    ) -> ProtectedRuleIssue | None:

        if "rachat total" not in content:

            return self._issue(
                rule,
                "La règle du rachat total n'est pas exposée.",
            )

        correct_patterns = (
            (
                r"valeur de rachat.{0,120}"
                r"(?:moins|diminuee de|deduction de|difference)"
                r".{0,120}primes versees"
            ),
            (
                r"difference.{0,120}"
                r"valeur de rachat.{0,120}"
                r"primes versees"
            ),
            (
                r"valeur de rachat\s*-\s*"
                r"(?:total des )?primes versees"
            ),
        )

        if not self._matches_any(
            content,
            correct_patterns,
        ):

            return self._issue(
                rule,
                (
                    "La formule du rachat total n'est pas "
                    "restituée conformément à la règle protégée : "
                    "produits imposables = valeur de rachat "
                    "- total des primes versées."
                ),
            )

        return None

    # ==========================================================
    # ASSURANCE-VIE — RACHAT PARTIEL
    # ==========================================================

    def _validate_av_rachat_partiel_formula(
        self,
        content: str,
        rule: ProtectedRule,
    ) -> ProtectedRuleIssue | None:

        if "rachat partiel" not in content:

            return self._issue(
                rule,
                "La règle du rachat partiel n'est pas exposée.",
            )

        required_terms = (
            "montant du rachat",
            "primes versees",
            "valeur de rachat",
        )

        if not all(
            term in content
            for term in required_terms
        ):

            return self._issue(
                rule,
                (
                    "La formule du rachat partiel ne contient "
                    "pas les trois composantes protégées : "
                    "montant du rachat, primes versées et "
                    "valeur de rachat."
                ),
            )

        correct_patterns = (
            (
                r"primes versees.{0,120}"
                r"(?:x|×|multipliees par).{0,120}"
                r"montant du rachat.{0,80}"
                r"(?:/|divise par|rapport).{0,80}"
                r"valeur de rachat"
            ),
            (
                r"quote-part de primes.{0,180}"
                r"proportion"
            ),
            (
                r"part de primes.{0,180}"
                r"proportion"
            ),
        )

        has_correct_structure = self._matches_any(
            content,
            correct_patterns,
        )

        example_formula_pattern = (
            r"primes.{0,80}"
            r"(?:=|est de|sont de).{0,80}"
            r"\d[\d\s]*.{0,40}"
            r"(?:x|×).{0,40}"
            r"\d[\d\s]*.{0,20}"
            r"/.{0,20}"
            r"\d[\d\s]*"
        )

        has_formula_example = bool(
            re.search(
                example_formula_pattern,
                content,
                flags=re.IGNORECASE | re.DOTALL,
            )
        )

        if not (
            has_correct_structure
            or has_formula_example
        ):

            return self._issue(
                rule,
                (
                    "La formule protégée du rachat partiel "
                    "n'est pas correctement identifiable. "
                    "La quote-part de primes doit être calculée "
                    "à partir des primes versées multipliées par "
                    "le rapport montant du rachat / valeur de "
                    "rachat totale à la date du rachat."
                ),
            )

        inverted_patterns = (
            (
                r"montant du rachat.{0,100}"
                r"(?:x|×|multiplie par).{0,100}"
                r"valeur de rachat.{0,80}"
                r"(?:/|divise par).{0,80}"
                r"primes"
            ),
            (
                r"rapport entre la valeur.{0,100}"
                r"et.{0,100}primes"
            ),
        )

        if self._matches_any(
            content,
            inverted_patterns,
        ):

            return self._issue(
                rule,
                (
                    "Une inversion potentielle de la formule "
                    "du rachat partiel a été détectée."
                ),
            )

        return None

    # ==========================================================
    # ASSURANCE-VIE — RACHATS SUCCESSIFS
    # ==========================================================

    def _validate_av_rachats_successifs(
        self,
        content: str,
        rule: ProtectedRule,
    ) -> ProtectedRuleIssue | None:

        successif_context = (
            "rachats successifs" in content
            or "rachat ulterieur" in content
            or "rachats anterieurs" in content
        )

        if not successif_context:

            return self._issue(
                rule,
                (
                    "Le traitement des rachats partiels "
                    "successifs n'est pas exposé."
                ),
            )

        adjustment_markers = (
            "primes deja remboursees",
            "primes deja reputees remboursees",
            "primes rachetees",
            "capital deja rembourse",
            "retranchees des primes",
            "deduire des primes",
            "primes restantes",
        )

        if not any(
            marker in content
            for marker in adjustment_markers
        ):

            return self._issue(
                rule,
                (
                    "Le topic ne précise pas que les primes "
                    "déjà réputées remboursées doivent être "
                    "retranchées pour les rachats successifs."
                ),
            )

        return None

    # ==========================================================
    # ASSURANCE-VIE — TAUX 7,5 %
    # ==========================================================

    def _validate_av_post_2017_rate_75(
        self,
        content: str,
        rule: ProtectedRule,
    ) -> ProtectedRuleIssue | None:

        required_markers = (
            "27 septembre 2017",
            "7,5 %",
            "150 000",
        )

        if not all(
            marker in content
            for marker in required_markers
        ):

            return self._issue(
                rule,
                (
                    "Le taux de 7,5 % n'est pas correctement "
                    "articulé avec la date du 27 septembre 2017 "
                    "et le seuil de 150 000 euros."
                ),
            )

        duration_context = (
            "plus de huit ans" in content
            or "plus de 8 ans" in content
            or "au-dela de huit ans" in content
            or "au-dela de 8 ans" in content
        )

        if not duration_context:

            return self._issue(
                rule,
                (
                    "Le taux de 7,5 % n'est pas contextualisé "
                    "par rapport à un contrat de plus de huit ans."
                ),
            )

        return None

    # ==========================================================
    # ASSURANCE-VIE — TAUX 12,8 %
    # ==========================================================

    def _validate_av_post_2017_rate_128(
        self,
        content: str,
        rule: ProtectedRule,
    ) -> ProtectedRuleIssue | None:

        required_markers = (
            "27 septembre 2017",
            "12,8 %",
            "150 000",
        )

        if not all(
            marker in content
            for marker in required_markers
        ):

            return self._issue(
                rule,
                (
                    "Le taux de 12,8 % n'est pas correctement "
                    "articulé avec la date du 27 septembre 2017 "
                    "et le seuil de 150 000 euros."
                ),
            )

        excess_markers = (
            "depassant 150 000",
            "excedant 150 000",
            "au-dela de 150 000",
            "exces au-dela de 150 000",
            "part de primes depassant",
            "fraction des produits",
            "fraction des gains",
        )

        if not any(
            marker in content
            for marker in excess_markers
        ):

            return self._issue(
                rule,
                (
                    "Le taux de 12,8 % n'est pas rattaché "
                    "à la fraction correspondant aux primes "
                    "excédant le seuil de 150 000 euros."
                ),
            )

        return None

    # ==========================================================
    # ASSURANCE-VIE — PAS DE 12,8 % GLOBAL
    # ==========================================================

    def _validate_av_150k_not_global_128(
        self,
        content: str,
        rule: ProtectedRule,
    ) -> ProtectedRuleIssue | None:

        protective_patterns = (
            (
                r"ne conduit.{0,80}pas.{0,120}"
                r"(?:12,8 %).{0,120}"
                r"(?:integralite|totalite|ensemble)"
            ),
            (
                r"ne conduit.{0,80}pas.{0,120}"
                r"(?:integralite|totalite|ensemble)"
                r".{0,120}12,8 %"
            ),
            (
                r"12,8 %.{0,120}"
                r"uniquement.{0,120}"
                r"(?:fraction|part)"
            ),
            (
                r"uniquement.{0,120}"
                r"(?:fraction|part).{0,120}"
                r"12,8 %"
            ),
            (
                r"12,8 %.{0,160}"
                r"au prorata"
            ),
            (
                r"au prorata.{0,160}"
                r"12,8 %"
            ),
            (
                r"fraction des produits correspondant"
            ),
            (
                r"fraction des gains correspondant"
            ),
            (
                r"part de primes depassant"
            ),
        )

        has_protective_statement = self._matches_any(
            content,
            protective_patterns,
        )

        forbidden_patterns = (
            (
                r"(?:depasse|superieur a|au-dela de)"
                r".{0,80}150 000"
                r".{0,180}"
                r"(?:integralite|totalite|ensemble)"
                r".{0,100}12,8 %"
            ),
            (
                r"12,8 %"
                r".{0,100}"
                r"(?:integralite|totalite|ensemble)"
                r".{0,180}"
                r"(?:depasse|superieur a|au-dela de)"
                r".{0,80}150 000"
            ),
        )

        for sentence in self._split_sentences(content):

            if self._matches_any(
                sentence,
                protective_patterns,
            ):
                continue

            if self._matches_any(
                sentence,
                forbidden_patterns,
            ):

                return self._issue(
                    rule,
                    (
                        "Le topic semble appliquer le taux de "
                        "12,8 % à l'intégralité des produits lors "
                        "du dépassement du seuil de 150 000 euros."
                    ),
                )

        if not has_protective_statement:

            return self._issue(
                rule,
                (
                    "Le topic ne protège pas explicitement "
                    "contre l'application globale du taux de "
                    "12,8 % à l'intégralité des produits."
                ),
            )

        return None

    # ==========================================================
    # ASSURANCE-VIE — PAS D'EXONÉRATION SOUS 150 K€
    # ==========================================================

    def _validate_av_150k_not_exemption(
        self,
        content: str,
        rule: ProtectedRule,
    ) -> ProtectedRuleIssue | None:

        protective_patterns = (
            (
                r"ne constitue.{0,100}pas.{0,120}"
                r"(?:exoneration|exonere)"
            ),
            (
                r"ne correspond.{0,100}pas.{0,120}"
                r"(?:exoneration|exonere)"
            ),
            (
                r"ne signifie.{0,100}pas.{0,120}"
                r"(?:exoneration|exonere)"
            ),
            (
                r"pas une exonération"
            ),
            (
                r"pas une exoneration"
            ),
            (
                r"n'entraine pas.{0,120}"
                r"(?:exoneration|absence d'impot)"
            ),
        )

        forbidden_patterns = (
            (
                r"(?:inferieur|en dessous|sous)"
                r".{0,80}150 000"
                r".{0,180}"
                r"(?:exonere|exoneration|aucun impot|non imposable)"
            ),
            (
                r"(?:exonere|exoneration|aucun impot|non imposable)"
                r".{0,180}"
                r"(?:inferieur|en dessous|sous)"
                r".{0,80}150 000"
            ),
        )

        for sentence in self._split_sentences(content):

            if self._matches_any(
                sentence,
                protective_patterns,
            ):
                continue

            if self._matches_any(
                sentence,
                forbidden_patterns,
            ):

                return self._issue(
                    rule,
                    (
                        "Le topic présente potentiellement le seuil "
                        "de 150 000 euros comme une exonération "
                        "générale d'impôt sur le revenu."
                    ),
                )

        return None

    # ==========================================================
    # HELPERS
    # ==========================================================

    @staticmethod
    def _build_content(
        topic: WrittenTopic,
    ) -> str:

        return "\n".join(
            [
                topic.title,
                topic.summary,
                topic.description,
                *topic.keywords,
                *topic.vocabulary,
                *topic.examples,
                *topic.legal_sources,
            ]
        )

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:
        """
        Normalise le contenu pour les contrôles déterministes.
        """

        value = value.lower()

        value = unicodedata.normalize(
            "NFKD",
            value,
        )

        value = "".join(
            character
            for character in value
            if not unicodedata.combining(character)
        )

        value = value.replace(
            "\u00a0",
            " ",
        )

        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        return value.strip()

    @staticmethod
    def _split_sentences(
        content: str,
    ) -> list[str]:
        """
        Découpe le contenu en unités de contrôle.

        Les affirmations interdites sont analysées localement
        afin qu'une négation explicite ne soit pas interprétée
        comme l'affirmation qu'elle réfute.
        """

        return [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?;])\s+",
                content,
            )
            if sentence.strip()
        ]

    @staticmethod
    def _matches_any(
        content: str,
        patterns: tuple[str, ...],
    ) -> bool:

        return any(
            re.search(
                pattern,
                content,
                flags=re.IGNORECASE | re.DOTALL,
            )
            for pattern in patterns
        )

    @staticmethod
    def _issue(
        rule: ProtectedRule,
        message: str,
    ) -> ProtectedRuleIssue:

        return ProtectedRuleIssue(
            field="protected_rules",
            message=message,
            rule_id=rule.id,
            validator_key=rule.validator_key,
        )
    