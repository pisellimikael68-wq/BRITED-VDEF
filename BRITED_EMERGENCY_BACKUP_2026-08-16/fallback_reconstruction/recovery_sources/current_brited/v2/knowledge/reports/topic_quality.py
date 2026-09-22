from dataclasses import dataclass, field


@dataclass
class TopicQualityReport:
    """
    Rapport de validation d'un Topic.
    """

    score: int = 0

    grade: str = "Draft"

    is_gold: bool = False

    passed_rules: list[str] = field(default_factory=list)

    failed_rules: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    suggestions: list[str] = field(default_factory=list)

    def add_success(self, rule: str):
        self.passed_rules.append(rule)

    def add_failure(self, rule: str, suggestion: str | None = None):
        self.failed_rules.append(rule)

        if suggestion:
            self.suggestions.append(suggestion)
            