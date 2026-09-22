from dataclasses import dataclass, field

from v2.knowledge.sources.academic_models import (
    ProtectedRule,
)


@dataclass(slots=True, frozen=True)
class KnowledgeContext:
    """
    Contexte Knowledge transmis au Writer.

    Il représente une sélection contrôlée de connaissances
    pertinentes pour la rédaction d'un topic.

    Les règles protégées sont transportées séparément
    du contenu académique général.

    Elles restent structurées afin de pouvoir être :
    - injectées dans les prompts ;
    - contrôlées par des validateurs déterministes ;
    - tracées par leur identifiant.
    """

    topic_id: str

    academic_content: str = ""

    protected_rules: list[ProtectedRule] = field(
        default_factory=list
    )

    source_ids: list[str] = field(
        default_factory=list
    )

    source_types: list[str] = field(
        default_factory=list
    )

    def is_empty(self) -> bool:
        """
        Indique si aucune connaissance exploitable
        n'est disponible.
        """

        return (
            not self.academic_content.strip()
            and not self.protected_rules
        )

    def render_protected_rules(self) -> str:
        """
        Construit le bloc textuel des règles protégées
        destiné aux prompts du Writer.

        Les métadonnées techniques ne sont pas exposées
        au modèle.
        """

        if not self.protected_rules:
            return ""

        return "\n".join(
            f"- {rule.statement}"
            for rule in self.protected_rules
        )

    def get_protected_rule_ids(self) -> list[str]:
        """
        Retourne les identifiants des règles protégées.
        """

        return [
            rule.id
            for rule in self.protected_rules
        ]

    def get_validator_keys(self) -> list[str]:
        """
        Retourne les clés des validateurs déterministes
        associés aux règles protégées.
        """

        return [
            rule.validator_key
            for rule in self.protected_rules
            if rule.validator_key
        ]
    