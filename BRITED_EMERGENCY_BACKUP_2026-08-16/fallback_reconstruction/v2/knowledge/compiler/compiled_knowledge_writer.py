import json
from pathlib import Path

from v2.knowledge.compiler.models import (
    CompiledKnowledge,
)


class CompiledKnowledgeWriter:
    """
    Persiste les résultats du Knowledge Compiler.

    Le format de sortie est indépendant de la famille
    patrimoniale compilée.
    """

    def __init__(
        self,
        output_dir: str = "data/knowledge/compiled",
    ) -> None:

        self.output_dir = Path(output_dir)

    def write(
        self,
        knowledge: CompiledKnowledge,
    ) -> Path:
        """
        Écrit un CompiledKnowledge au format JSON.
        """

        output = (
            self.output_dir
            / knowledge.family
            / f"{knowledge.chapter}.json"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = {
            "source_id": knowledge.source_id,
            "family": knowledge.family,
            "chapter": knowledge.chapter,
            "rules": [
                {
                    "id": rule.id,
                    "statement": rule.statement,
                    "rule_type": rule.rule_type.value,
                    "severity": rule.severity.value,
                    "source_anchors": rule.source_anchors,
                    "conditions": rule.conditions,
                    "required_elements": (
                        rule.required_elements
                    ),
                    "forbidden_interpretations": (
                        rule.forbidden_interpretations
                    ),
                    "legal_references": (
                        rule.legal_references
                    ),
                }
                for rule in knowledge.rules
            ],
        }

        output.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        return output
        