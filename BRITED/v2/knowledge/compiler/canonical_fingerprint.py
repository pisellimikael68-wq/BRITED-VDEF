import hashlib
import json

from v2.knowledge.compiler.canonical_models import (
    CanonicalRule,
)


class CanonicalRuleFingerprintBuilder:
    """
    Construit l'empreinte stable d'une règle canonique.

    Le fingerprint représente le contenu métier
    canonique de la règle.

    Il ne dépend pas :
    - de l'identifiant de la règle ;
    - de la source documentaire ;
    - de l'ordre initial des collections.

    Il dépend :
    - de la famille ;
    - du chapitre ;
    - du type de règle ;
    - du statement canonique ;
    - des conditions ;
    - des éléments nécessaires ;
    - des contresens interdits ;
    - des références juridiques.
    """

    @classmethod
    def build(
        cls,
        rule: CanonicalRule,
    ) -> str:
        """
        Produit un SHA-256 déterministe.
        """

        payload = {
            "family": rule.family,
            "chapter": rule.chapter,
            "rule_type": rule.rule_type,
            "statement": rule.statement,
            "keywords": sorted(
                rule.keywords
            ),
            "conditions": sorted(
                rule.conditions
            ),
            "required_elements": sorted(
                rule.required_elements
            ),
            "forbidden_interpretations": sorted(
                rule.forbidden_interpretations
            ),
            "legal_references": sorted(
                rule.legal_references
            ),
        }

        serialized = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            serialized.encode("utf-8")
        ).hexdigest()
    