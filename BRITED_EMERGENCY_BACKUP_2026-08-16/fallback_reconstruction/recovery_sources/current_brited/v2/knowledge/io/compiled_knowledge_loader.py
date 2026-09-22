import json
from pathlib import Path
from typing import Any

from v2.knowledge.compiler.models import (
    CompiledKnowledge,
    CompiledRule,
    RuleSeverity,
    RuleType,
)


class CompiledKnowledgeLoader:
    """
    Charge un corpus Knowledge compilé depuis un fichier JSON.

    Le format attendu correspond à celui produit par
    CompiledKnowledgeWriter.
    """

    def __init__(
        self,
        input_dir: str = "data/knowledge/compiled",
    ) -> None:
        self.input_dir = Path(input_dir)

    def load(
        self,
        family: str,
        chapter: str,
    ) -> CompiledKnowledge:
        """
        Charge un CompiledKnowledge à partir de sa famille
        et de son chapitre.
        """

        input_path = (
            self.input_dir
            / family
            / f"{chapter}.json"
        )

        if not input_path.exists():
            raise FileNotFoundError(
                "Corpus compilé introuvable : "
                f"{input_path}"
            )

        try:
            raw_data = json.loads(
                input_path.read_text(
                    encoding="utf-8",
                )
            )
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Le fichier compilé contient un JSON invalide : "
                f"{input_path}"
            ) from exc

        return self._build_knowledge(
            raw_data,
            source_path=input_path,
        )

    def _build_knowledge(
        self,
        data: dict[str, Any],
        *,
        source_path: Path,
    ) -> CompiledKnowledge:
        """
        Reconstruit un CompiledKnowledge depuis un dictionnaire.
        """

        required_fields = {
            "source_id",
            "family",
            "chapter",
            "rules",
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            missing = ", ".join(
                sorted(missing_fields)
            )

            raise ValueError(
                "Champs manquants dans le corpus compilé "
                f"{source_path} : {missing}"
            )

        rules_data = data["rules"]

        if not isinstance(rules_data, list):
            raise ValueError(
                "Le champ 'rules' doit être une liste dans "
                f"{source_path}"
            )

        rules = [
            self._build_rule(
                rule_data,
                source_path=source_path,
                rule_index=index,
            )
            for index, rule_data in enumerate(
                rules_data
            )
        ]

        return CompiledKnowledge(
            source_id=str(data["source_id"]),
            family=str(data["family"]),
            chapter=str(data["chapter"]),
            rules=rules,
        )

    def _build_rule(
        self,
        data: dict[str, Any],
        *,
        source_path: Path,
        rule_index: int,
    ) -> CompiledRule:
        """
        Reconstruit une CompiledRule depuis un dictionnaire.
        """

        if not isinstance(data, dict):
            raise ValueError(
                "Chaque règle doit être un objet JSON dans "
                f"{source_path}. Index invalide : {rule_index}"
            )

        required_fields = {
            "id",
            "statement",
            "rule_type",
            "severity",
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            missing = ", ".join(
                sorted(missing_fields)
            )

            raise ValueError(
                "Champs manquants pour la règle "
                f"{rule_index} dans {source_path} : {missing}"
            )

        try:
            rule_type = RuleType(
                data["rule_type"]
            )
        except ValueError as exc:
            raise ValueError(
                "Type de règle invalide pour la règle "
                f"{rule_index} dans {source_path} : "
                f"{data['rule_type']}"
            ) from exc

        try:
            severity = RuleSeverity(
                data["severity"]
            )
        except ValueError as exc:
            raise ValueError(
                "Sévérité invalide pour la règle "
                f"{rule_index} dans {source_path} : "
                f"{data['severity']}"
            ) from exc

        return CompiledRule(
            id=str(data["id"]),
            statement=str(data["statement"]),
            rule_type=rule_type,
            severity=severity,
            source_anchors=self._read_string_list(
                data,
                "source_anchors",
                source_path=source_path,
                rule_index=rule_index,
            ),
            conditions=self._read_string_list(
                data,
                "conditions",
                source_path=source_path,
                rule_index=rule_index,
            ),
            required_elements=self._read_string_list(
                data,
                "required_elements",
                source_path=source_path,
                rule_index=rule_index,
            ),
            forbidden_interpretations=(
                self._read_string_list(
                    data,
                    "forbidden_interpretations",
                    source_path=source_path,
                    rule_index=rule_index,
                )
            ),
            legal_references=self._read_string_list(
                data,
                "legal_references",
                source_path=source_path,
                rule_index=rule_index,
            ),
        )

    @staticmethod
    def _read_string_list(
        data: dict[str, Any],
        field_name: str,
        *,
        source_path: Path,
        rule_index: int,
    ) -> list[str]:
        """
        Lit un champ optionnel contenant une liste de chaînes.
        """

        value = data.get(
            field_name,
            [],
        )

        if not isinstance(value, list):
            raise ValueError(
                f"Le champ '{field_name}' de la règle "
                f"{rule_index} doit être une liste dans "
                f"{source_path}"
            )

        if not all(
            isinstance(item, str)
            for item in value
        ):
            raise ValueError(
                f"Le champ '{field_name}' de la règle "
                f"{rule_index} doit contenir uniquement "
                f"des chaînes dans {source_path}"
            )

        return value
        