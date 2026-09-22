import re

from collections import defaultdict

from v2.knowledge.compiler.models import (
    RuleType,
)
from v2.knowledge.compiler.rule_seed import (
    RuleSeed,
)


class SeedSemanticPolicy:
    """
    Politique déterministe de classification sémantique
    des RuleSeed.

    Principe architectural :

    - le primary_content porte l'identité sémantique
      principale de la règle ;

    - les signatures sémantiques fortes déterminent
      prioritairement le type lorsqu'une formulation
      normative caractéristique est détectée ;

    - le scoring lexical primaire intervient lorsque
      aucune signature forte n'est reconnue ;

    - les supporting_contents ne servent qu'à
      départager une ambiguïté résiduelle ;

    - aucun appel LLM n'intervient dans la
      classification.

    La classification doit donc être stable pour
    un même RuleSeed.
    """

    TYPE_PRIORITY = (
        RuleType.EXCEPTION,
        RuleType.FORMULA,
        RuleType.TAX_RATE,
        RuleType.SENSITIVE_DATE,
        RuleType.THRESHOLD,
        RuleType.CONDITION,
        RuleType.LEGAL_RULE,
        RuleType.DEFINITION,
        RuleType.OTHER,
    )

    def classify(
        self,
        seed: RuleSeed,
    ) -> RuleType:
        """
        Classifie un RuleSeed.

        Ordre de décision :

        1. signature sémantique forte sur le fragment
           primaire ;

        2. scoring du seul fragment primaire ;

        3. scoring combiné avec les fragments de support
           uniquement en cas d'ambiguïté primaire.
        """

        strong_type = (
            self._classify_strong_signature(
                seed
            )
        )

        if strong_type is not None:
            return strong_type

        primary_scores = self._score_primary(
            seed
        )

        best_primary_score = max(
            primary_scores.values()
        )

        primary_candidates = [
            rule_type
            for rule_type, score
            in primary_scores.items()
            if score == best_primary_score
        ]

        if (
            best_primary_score > 0
            and len(primary_candidates) == 1
        ):
            return primary_candidates[0]

        combined_scores = self.score(
            seed
        )

        return max(
            self.TYPE_PRIORITY,
            key=lambda rule_type: (
                combined_scores[rule_type],
                -self.TYPE_PRIORITY.index(
                    rule_type
                ),
            ),
        )

    def _classify_strong_signature(
        self,
        seed: RuleSeed,
    ) -> RuleType | None:
        """
        Détecte une signature normative forte dans le
        seul primary_content.

        Les signatures sont évaluées dans un ordre
        volontairement métier.

        Une exception doit notamment être détectée avant
        un taux ou un seuil, car une règle corrective
        peut elle-même citer un taux ou un seuil.
        """

        text = self._normalize(
            seed.primary_content
        )

        if self._is_strong_exception(
            text
        ):
            return RuleType.EXCEPTION

        if self._is_strong_formula(
            text
        ):
            return RuleType.FORMULA

        if self._is_strong_tax_rate(
            text
        ):
            return RuleType.TAX_RATE

        if self._is_strong_sensitive_date(
            text
        ):
            return RuleType.SENSITIVE_DATE

        if self._is_strong_threshold(
            text
        ):
            return RuleType.THRESHOLD

        return None

    @staticmethod
    def _is_strong_exception(
        text: str,
    ) -> bool:
        """
        Détecte une règle corrective ou une
        anti-interprétation.

        Ces formulations expriment qu'un fait ne produit
        pas automatiquement une conséquence donnée.
        """

        patterns = (
            r"\bne constitue pas\b",
            r"\bne signifie pas\b",
            r"\bne conduit pas\b",
            r"\bn'entraîne pas\b",
            r"\bn'entraine pas\b",
            r"\bne doit pas être\b",
            r"\bne doit pas etre\b",
            r"\bne s'applique pas\b",
            r"\bne s'applique pas\b",
            r"\bsans que\b",
            r"\bpas automatiquement\b",
        )

        return any(
            re.search(
                pattern,
                text,
            )
            for pattern in patterns
        )

    @staticmethod
    def _is_strong_formula(
        text: str,
    ) -> bool:
        """
        Détecte une règle définissant directement un
        calcul, une assiette ou un mécanisme quantitatif.
        """

        patterns = (
            r"\bcorrespond à la différence entre\b",
            r"\bcorrespond au montant\b",
            r"\bmultiplié par le rapport\b",
            r"\bmultipliée par le rapport\b",
            r"\bcalcul de l'assiette taxable\b",
            r"\bcalcul de l'assiette\b",
            r"\bpour les calculs ultérieurs\b",
            r"\bsolde des primes versées\b",
            (
                r"\bprimes à prendre en compte "
                r"pour le calcul\b"
            ),
            (
                r"\bsont augmentées des nouveaux "
                r"versements\b"
            ),
            (
                r"\bsont augmentes des nouveaux "
                r"versements\b"
            ),
        )

        return any(
            re.search(
                pattern,
                text,
            )
            for pattern in patterns
        )

    @staticmethod
    def _is_strong_tax_rate(
        text: str,
    ) -> bool:
        """
        Détecte une règle dont l'objet normatif principal
        est l'application d'un taux d'imposition.

        La présence simultanée d'un langage de taux ou
        d'imposition forfaitaire et d'un pourcentage est
        exigée.
        """

        rate_patterns = (
            r"\btaux forfaitaire\b",
            r"\bimposition forfaitaire\b",
            r"\btaux de\b",
        )

        has_rate_language = any(
            re.search(
                pattern,
                text,
            )
            for pattern in rate_patterns
        )

        has_percentage = bool(
            re.search(
                r"\b\d+(?:[,.]\d+)?\s*%",
                text,
            )
        )

        return (
            has_rate_language
            and has_percentage
        )

    @staticmethod
    def _is_strong_sensitive_date(
        text: str,
    ) -> bool:
        """
        Détecte une règle organisant une distinction de
        régime autour d'une date pivot.

        La seule présence d'une date ne suffit pas.
        Une logique explicite de distinction normative
        doit également être présente.
        """

        date_patterns = (
            (
                r"\bavant le 27 septembre 2017\b"
            ),
            (
                r"\bà compter du "
                r"27 septembre 2017\b"
            ),
            (
                r"\ba compter du "
                r"27 septembre 2017\b"
            ),
        )

        distinction_patterns = (
            r"\bdoit être distingué\b",
            r"\bdoit etre distingue\b",
            r"\bdoit être distinguée\b",
            r"\bdoit etre distinguee\b",
            r"\brégime fiscal distinct\b",
            r"\bregime fiscal distinct\b",
            r"\brégimes fiscaux distincts\b",
            r"\bregimes fiscaux distincts\b",
            r"\brelèvent de régimes\b",
            r"\brelevent de regimes\b",
        )

        has_sensitive_date = any(
            re.search(
                pattern,
                text,
            )
            for pattern in date_patterns
        )

        has_regime_distinction = any(
            re.search(
                pattern,
                text,
            )
            for pattern in distinction_patterns
        )

        return (
            has_sensitive_date
            and has_regime_distinction
        )

    @staticmethod
    def _is_strong_threshold(
        text: str,
    ) -> bool:
        """
        Détecte une règle définissant directement un
        montant d'abattement ou une limite quantitative.

        La simple présence du mot 'seuil' ne suffit pas :
        un seuil peut n'être qu'une condition d'une règle
        de taux ou d'une exception.
        """

        has_allowance_language = bool(
            re.search(
                r"\babattements? annuels?\b",
                text,
            )
        )

        has_amount = bool(
            re.search(
                r"\b\d[\d\s]*\s+euros\b",
                text,
            )
        )

        return (
            has_allowance_language
            and has_amount
        )

    def _score_primary(
        self,
        seed: RuleSeed,
    ) -> dict[RuleType, int]:
        """
        Calcule les scores sémantiques sur le seul
        primary_content.

        Aucun supporting content n'intervient ici.
        """

        scores: dict[
            RuleType,
            int,
        ] = defaultdict(int)

        self._score_text(
            text=self._normalize(
                seed.primary_content
            ),
            scores=scores,
            weight=1,
        )

        return {
            rule_type: scores[rule_type]
            for rule_type in RuleType
        }

    def score(
        self,
        seed: RuleSeed,
    ) -> dict[RuleType, int]:
        """
        Calcule les scores sémantiques combinés.

        Le primary content conserve un poids supérieur
        aux supporting contents.

        Cette méthode est principalement utilisée pour
        départager une ambiguïté primaire et pour les
        diagnostics de test.

        Les scores exposés ne constituent pas
        nécessairement la décision finale lorsqu'une
        signature sémantique forte est détectée.
        """

        scores: dict[
            RuleType,
            int,
        ] = defaultdict(int)

        self._score_text(
            text=self._normalize(
                seed.primary_content
            ),
            scores=scores,
            weight=3,
        )

        for content in seed.supporting_contents:
            self._score_text(
                text=self._normalize(
                    content
                ),
                scores=scores,
                weight=1,
            )

        return {
            rule_type: scores[rule_type]
            for rule_type in RuleType
        }

    def _score_text(
        self,
        *,
        text: str,
        scores: dict[RuleType, int],
        weight: int,
    ) -> None:
        """
        Applique les règles de scoring déterministes
        à un texte normalisé.
        """

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.FORMULA,
            patterns=(
                r"\bassiette taxable\b",
                r"\bproduit imposable\b",
                r"\bproduits imposables\b",
                r"\bcorrespond à\b",
                r"\bdifférence entre\b",
                r"\bdiminué du\b",
                r"\bdiminuée du\b",
                r"\bmultiplié par\b",
                r"\bmultipliée par\b",
                r"\brapport entre\b",
                r"\bprorata\b",
                r"\bcalcul\b",
                r"\bcalculs\b",
                r"\bsolde des primes\b",
                r"\bcapital déjà remboursé\b",
                (
                    r"\baugmentées des nouveaux "
                    r"versements\b"
                ),
                (
                    r"\baugmenté des nouveaux "
                    r"versements\b"
                ),
            ),
            weight=weight,
        )

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.TAX_RATE,
            patterns=(
                r"\btaux forfaitaire\b",
                r"\bimposition forfaitaire\b",
                r"\b12[,.]8\s*%\b",
                r"\b7[,.]5\s*%\b",
                r"\bbarème progressif\b",
                r"\btaux de\b",
                r"\btaux\b",
                r"\bimposition\b",
                r"\bimposé\b",
                r"\bimposés\b",
            ),
            weight=weight,
        )

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.THRESHOLD,
            patterns=(
                r"\bseuil\b",
                r"\b150\s*000\s+euros\b",
                r"\binférieur à\b",
                r"\binférieure à\b",
                r"\bsupérieur à\b",
                r"\bsupérieure à\b",
                r"\ben dessous du seuil\b",
                r"\bau-dessus du seuil\b",
                r"\bau dessus du seuil\b",
                r"\bdépasse le seuil\b",
                r"\bdépassant le seuil\b",
                r"\bau-delà de huit ans\b",
                r"\bau delà de huit ans\b",
                r"\b4\s*600\s+euros\b",
                r"\b9\s*200\s+euros\b",
                r"\babattement annuel\b",
                r"\babattements annuels\b",
            ),
            weight=weight,
        )

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.SENSITIVE_DATE,
            patterns=(
                (
                    r"\b\d{1,2}\s+"
                    r"(?:janvier|février|mars|avril|mai|juin|"
                    r"juillet|août|septembre|octobre|novembre|"
                    r"décembre)"
                    r"\s+\d{4}\b"
                ),
                r"\bau 31 décembre\b",
                r"\bannée n-1\b",
                r"\bà compter du\b",
                r"\bavant le\b",
                r"\baprès le\b",
                r"\bdate de versement\b",
                r"\bdate d'entrée en vigueur\b",
            ),
            weight=weight,
        )

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.EXCEPTION,
            patterns=(
                r"\bne constitue pas\b",
                r"\bne signifie pas\b",
                r"\bne conduit pas\b",
                r"\bn'entraîne pas\b",
                r"\bn'entraine pas\b",
                r"\bne doit pas\b",
                r"\bsans que\b",
                r"\bpas automatiquement\b",
                r"\bne [^.]* pas\b",
                (
                    r"\bne constitue pas une "
                    r"exonération\b"
                ),
                (
                    r"\bne signifie pas que "
                    r"la totalité\b"
                ),
                (
                    r"\bne conduit pas à appliquer "
                    r"automatiquement\b"
                ),
            ),
            weight=weight,
        )

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.CONDITION,
            patterns=(
                r"\ben cas de\b",
                r"\blorsque\b",
                r"\bsi\b",
                r"\bsous réserve\b",
                r"\bà condition\b",
                r"\bdoit être\b",
                r"\bdoivent être\b",
                r"\bdépend\b",
                r"\bdépend de\b",
            ),
            weight=weight,
        )

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.LEGAL_RULE,
            patterns=(
                r"\brégime fiscal\b",
                r"\bimpôt sur le revenu\b",
                r"\bimposition commune\b",
                r"\bdoit être distingué\b",
                r"\bdoit être distinguée\b",
                r"\bapplicable\b",
                r"\brégime applicable\b",
            ),
            weight=weight,
        )

        self._apply_patterns(
            text=text,
            scores=scores,
            rule_type=RuleType.DEFINITION,
            patterns=(
                r"\best défini comme\b",
                r"\best définie comme\b",
                r"\bdésigne\b",
                r"\bon entend par\b",
                r"\bcorrespond au sens de\b",
                r"\bconstitue la définition\b",
            ),
            weight=weight,
        )

    @staticmethod
    def _apply_patterns(
        *,
        text: str,
        scores: dict[RuleType, int],
        rule_type: RuleType,
        patterns: tuple[str, ...],
        weight: int,
    ) -> None:
        """
        Ajoute le poids de chaque pattern trouvé.

        Un pattern n'est comptabilisé qu'une fois par
        texte analysé.
        """

        for pattern in patterns:
            if re.search(
                pattern,
                text,
            ):
                scores[rule_type] += weight

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:
        """
        Normalisation légère et déterministe.

        Les accents sont volontairement conservés afin
        de préserver les expressions juridiques et
        fiscales françaises utilisées dans les patterns.
        """

        return " ".join(
            value.lower()
            .replace("’", "'")
            .replace("\n", " ")
            .replace("\t", " ")
            .split()
        )
    