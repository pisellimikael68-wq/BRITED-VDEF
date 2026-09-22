from v2.knowledge.compiler.rule_seed import (
    RuleSeed,
)
from v2.knowledge.compiler.source_fragment import (
    SourceFragment,
)


class RuleSeedBuilder:
    """
    Construit des seeds de règles déterministes.

    Une entrée de la section `rules`
    constitue un noyau identitaire primaire.

    Les autres sections ne définissent pas
    l'identité de la règle.
    """

    PRIMARY_SECTION = "rules"

    def build(
        self,
        fragments: list[SourceFragment],
    ) -> list[RuleSeed]:

        primary_fragments = [
            fragment
            for fragment in fragments
            if fragment.section
            == self.PRIMARY_SECTION
        ]

        return [
            self._build_seed(
                primary=primary,
                fragments=fragments,
            )
            for primary in primary_fragments
        ]

    def _build_seed(
        self,
        *,
        primary: SourceFragment,
        fragments: list[SourceFragment],
    ) -> RuleSeed:

        supporting = (
            self._find_supporting_fragments(
                primary=primary,
                fragments=fragments,
            )
        )

        return RuleSeed(
            source_id=primary.source_id,
            primary_anchor=primary.anchor,
            primary_content=primary.text,
            supporting_anchors=[
                fragment.anchor
                for fragment in supporting
            ],
            supporting_contents=[
                fragment.text
                for fragment in supporting
            ],
        )

    def _find_supporting_fragments(
        self,
        *,
        primary: SourceFragment,
        fragments: list[SourceFragment],
    ) -> list[SourceFragment]:

        supporting_sections = {
            "protected_rules",
            "thresholds",
            "sensitive_dates",
            "examples",
            "attention_points",
            "key_points",
            "legal_references",
        }

        candidates = [
            fragment
            for fragment in fragments
            if (
                fragment.section
                in supporting_sections
                and fragment.source_id
                == primary.source_id
            )
        ]

        return [
            fragment
            for fragment in candidates
            if self._is_related(
                primary=primary,
                candidate=fragment,
            )
        ]

    @staticmethod
    def _is_related(
        *,
        primary: SourceFragment,
        candidate: SourceFragment,
    ) -> bool:

        primary_tokens = (
            RuleSeedBuilder._tokens(
                primary.text
            )
        )

        candidate_tokens = (
            RuleSeedBuilder._tokens(
                candidate.text
            )
        )

        if not primary_tokens:

            return False

        common_tokens = (
            primary_tokens
            & candidate_tokens
        )

        score = (
            len(common_tokens)
            / len(primary_tokens)
        )

        return score >= 0.20

    @staticmethod
    def _tokens(
        value: str,
    ) -> set[str]:

        normalized = (
            value.lower()
            .replace("'", " ")
            .replace("’", " ")
            .replace("-", " ")
            .replace(",", " ")
            .replace(".", " ")
            .replace(":", " ")
            .replace(";", " ")
            .replace("(", " ")
            .replace(")", " ")
        )

        stop_words = {
            "le",
            "la",
            "les",
            "un",
            "une",
            "des",
            "de",
            "du",
            "d",
            "et",
            "ou",
            "à",
            "au",
            "aux",
            "en",
            "pour",
            "par",
            "sur",
            "dans",
            "est",
            "sont",
            "être",
            "avec",
            "ce",
            "ces",
            "cette",
            "qui",
            "que",
            "lorsque",
            "selon",
        }

        return {
            token
            for token in normalized.split()
            if (
                len(token) >= 3
                and token not in stop_words
            )
        }
    