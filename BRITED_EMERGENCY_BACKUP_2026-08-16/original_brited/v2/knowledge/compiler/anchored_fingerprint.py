import hashlib

from v2.knowledge.compiler.models import (
    CompiledRule,
)


class AnchoredRuleFingerprint:
    """
    Construit l'identité déterministe d'une règle
    à partir de sa provenance source.

    Le fingerprint ne dépend volontairement pas :
    - de l'identifiant produit par le LLM ;
    - du statement ;
    - du type de règle ;
    - de la sévérité ;
    - des conditions ;
    - des formulations éditoriales.

    L'identité repose uniquement sur :
    - l'identifiant stable de la source ;
    - les anchors des fragments fondant la règle.
    """

    @staticmethod
    def build(
        *,
        source_id: str,
        rule: CompiledRule,
    ) -> str:

        anchors = sorted(
            set(
                anchor.strip()
                for anchor in rule.source_anchors
                if anchor.strip()
            )
        )

        if not anchors:

            raise ValueError(
                "Impossible de construire un fingerprint "
                "ancré pour une règle sans source_anchors : "
                f"{rule.id}"
            )

        payload = "\n".join(
            [
                source_id.strip(),
                *anchors,
            ]
        )

        return hashlib.sha256(
            payload.encode(
                "utf-8"
            )
        ).hexdigest()
    