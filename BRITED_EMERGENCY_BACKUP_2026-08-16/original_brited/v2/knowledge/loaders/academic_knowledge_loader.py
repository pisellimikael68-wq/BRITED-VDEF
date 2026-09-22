import json
from dataclasses import fields
from pathlib import Path

from v2.knowledge.sources.academic_models import (
    AcademicKnowledge,
    ProtectedRule,
)


class AcademicKnowledgeLoader:
    """
    Charge le corpus académique structuré de BRITED.

    Les fichiers JSON représentent le socle de connaissance
    issu des notes personnelles utilisées par Leveria.

    Le loader assure également la compatibilité avec
    l'ancien format des règles protégées.
    """

    def __init__(
        self,
        base_dir: str = "data/knowledge/academic",
    ):

        self.base_dir = Path(base_dir)

    def load_file(
        self,
        path: Path,
    ) -> AcademicKnowledge:
        """
        Charge un fichier JSON académique.
        """

        if not path.is_file():

            raise FileNotFoundError(
                f"Fichier Knowledge introuvable : {path}"
            )

        try:

            data = json.loads(
                path.read_text(
                    encoding="utf-8",
                )
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                f"JSON Knowledge invalide : {path}"
            ) from exc

        if not isinstance(data, dict):

            raise ValueError(
                "La racine du fichier Knowledge "
                f"doit être un objet JSON : {path}"
            )

        allowed_fields = {
            field.name
            for field in fields(AcademicKnowledge)
        }

        unknown_fields = (
            set(data)
            - allowed_fields
        )

        if unknown_fields:

            raise ValueError(
                "Champs inconnus dans "
                f"{path} : "
                + ", ".join(
                    sorted(unknown_fields)
                )
            )

        data["protected_rules"] = (
            self._load_protected_rules(
                data.get(
                    "protected_rules",
                    [],
                ),
                path=path,
            )
        )

        try:

            return AcademicKnowledge(
                **data
            )

        except TypeError as exc:

            raise ValueError(
                "Structure Knowledge incompatible "
                f"dans {path}"
            ) from exc

    @staticmethod
    def _load_protected_rules(
        raw_rules,
        *,
        path: Path,
    ) -> list[ProtectedRule]:
        """
        Convertit les règles protégées JSON
        en objets ProtectedRule.

        Deux formats sont acceptés.

        Ancien format :
        [
            "Règle métier"
        ]

        Nouveau format :
        [
            {
                "id": "...",
                "statement": "...",
                "validator_key": "..."
            }
        ]

        L'ancien format reste chargeable mais ne possède
        pas de validateur déterministe associé.
        """

        if raw_rules is None:

            return []

        if not isinstance(raw_rules, list):

            raise ValueError(
                "Le champ protected_rules doit être "
                f"une liste dans {path}"
            )

        protected_rules: list[ProtectedRule] = []

        for index, raw_rule in enumerate(
            raw_rules,
            start=1,
        ):

            if isinstance(raw_rule, str):

                statement = raw_rule.strip()

                if not statement:

                    raise ValueError(
                        "Règle protégée vide dans "
                        f"{path} à l'index {index}"
                    )

                protected_rules.append(
                    ProtectedRule(
                        id=(
                            "LEGACY_PROTECTED_RULE_"
                            f"{index}"
                        ),
                        statement=statement,
                        validator_key="",
                    )
                )

                continue

            if not isinstance(raw_rule, dict):

                raise ValueError(
                    "Règle protégée invalide dans "
                    f"{path} à l'index {index}"
                )

            allowed_rule_fields = {
                "id",
                "statement",
                "validator_key",
            }

            unknown_rule_fields = (
                set(raw_rule)
                - allowed_rule_fields
            )

            if unknown_rule_fields:

                raise ValueError(
                    "Champs inconnus dans une règle "
                    f"protégée de {path} à l'index "
                    f"{index} : "
                    + ", ".join(
                        sorted(unknown_rule_fields)
                    )
                )

            missing_fields = (
                allowed_rule_fields
                - set(raw_rule)
            )

            if missing_fields:

                raise ValueError(
                    "Champs manquants dans une règle "
                    f"protégée de {path} à l'index "
                    f"{index} : "
                    + ", ".join(
                        sorted(missing_fields)
                    )
                )

            rule_id = raw_rule["id"]
            statement = raw_rule["statement"]
            validator_key = raw_rule["validator_key"]

            if (
                not isinstance(rule_id, str)
                or not rule_id.strip()
            ):

                raise ValueError(
                    "Identifiant de règle protégée "
                    f"invalide dans {path} "
                    f"à l'index {index}"
                )

            if (
                not isinstance(statement, str)
                or not statement.strip()
            ):

                raise ValueError(
                    "Statement de règle protégée "
                    f"invalide dans {path} "
                    f"à l'index {index}"
                )

            if (
                not isinstance(validator_key, str)
                or not validator_key.strip()
            ):

                raise ValueError(
                    "validator_key de règle protégée "
                    f"invalide dans {path} "
                    f"à l'index {index}"
                )

            protected_rules.append(
                ProtectedRule(
                    id=rule_id.strip(),
                    statement=statement.strip(),
                    validator_key=(
                        validator_key.strip()
                    ),
                )
            )

        AcademicKnowledgeLoader._validate_rule_uniqueness(
            protected_rules,
            path=path,
        )

        return protected_rules

    @staticmethod
    def _validate_rule_uniqueness(
        protected_rules: list[ProtectedRule],
        *,
        path: Path,
    ) -> None:
        """
        Vérifie l'unicité des identifiants
        de règles protégées dans un bloc Knowledge.
        """

        seen_ids: set[str] = set()

        for rule in protected_rules:

            if rule.id in seen_ids:

                raise ValueError(
                    "Identifiant de règle protégée "
                    f"dupliqué dans {path} : "
                    f"{rule.id}"
                )

            seen_ids.add(
                rule.id
            )

    def load_family(
        self,
        family: str,
    ) -> list[AcademicKnowledge]:
        """
        Charge tous les blocs Knowledge d'une famille.
        """

        family_dir = (
            self.base_dir
            / family
        )

        if not family_dir.is_dir():

            return []

        knowledge_blocks = [
            self.load_file(path)
            for path in sorted(
                family_dir.glob("*.json")
            )
        ]

        return knowledge_blocks

    def load_all(
        self,
    ) -> list[AcademicKnowledge]:
        """
        Charge l'ensemble du corpus académique.
        """

        if not self.base_dir.is_dir():

            return []

        return [
            self.load_file(path)
            for path in sorted(
                self.base_dir.glob("*/*.json")
            )
        ]
    