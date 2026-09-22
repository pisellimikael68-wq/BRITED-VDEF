from v2.knowledge.compiler.models import (
    CompiledKnowledge,
    CompiledRule,
)
from v2.knowledge.compiler.rule_seed import (
    RuleSeed,
)
from v2.knowledge.compiler.rule_seed_builder import (
    RuleSeedBuilder,
)
from v2.knowledge.compiler.seed_condition_policy import (
    SeedConditionPolicy,
)
from v2.knowledge.compiler.seed_schemas import (
    SeedCompiledRuleSchema,
)
from v2.knowledge.compiler.seed_semantic_policy import (
    SeedSemanticPolicy,
)
from v2.knowledge.compiler.seed_severity_policy import (
    SeedSeverityPolicy,
)
from v2.knowledge.compiler.seed_statement_policy import (
    SeedStatementPolicy,
)
from v2.knowledge.compiler.source_fragment_builder import (
    SourceFragmentBuilder,
)
from v2.knowledge.sources.academic_models import (
    AcademicKnowledge,
)
from v2.llm.factory import LLMFactory
from v2.prompts.loader import PromptLoader
from v2.prompts.renderer import PromptRenderer


class SeedKnowledgeCompiler:
    """
    Compile les règles Knowledge seed par seed.

    La structure métier de chaque règle est déterminée
    par les différentes SeedPolicies.

    Le LLM ne complète plus que les informations
    difficilement déterministes.
    """

    def __init__(self):

        self.llm = LLMFactory.create()

        self.fragment_builder = (
            SourceFragmentBuilder()
        )

        self.seed_builder = (
            RuleSeedBuilder()
        )

        self.semantic_policy = (
            SeedSemanticPolicy()
        )

        self.severity_policy = (
            SeedSeverityPolicy()
        )

        self.statement_policy = (
            SeedStatementPolicy()
        )

        self.condition_policy = (
            SeedConditionPolicy()
        )

    def compile(
        self,
        knowledge: AcademicKnowledge,
    ) -> CompiledKnowledge:

        fragments = self.fragment_builder.build(
            knowledge
        )

        seeds = self.seed_builder.build(
            fragments
        )

        compiled_rules = [
            self.compile_seed(
                family=knowledge.family,
                chapter=knowledge.chapter,
                seed=seed,
            )
            for seed in seeds
        ]

        return CompiledKnowledge(
            source_id=knowledge.id,
            family=knowledge.family,
            chapter=knowledge.chapter,
            rules=compiled_rules,
        )

    def compile_seed(
        self,
        *,
        family: str,
        chapter: str,
        seed: RuleSeed,
    ) -> CompiledRule:

        rule_type = self.semantic_policy.classify(
            seed
        )

        severity = self.severity_policy.classify(
            seed=seed,
            rule_type=rule_type,
        )

        statement = self.statement_policy.build(
            seed
        )

        conditions = self.condition_policy.build(
            seed
        )

        prompt = PromptLoader.load(
            "knowledge/compile_rule_seed.md"
        )

        rendered_prompt = PromptRenderer.render(
            prompt,
            family=family,
            chapter=chapter,
            source_id=seed.source_id,
            primary_anchor=seed.primary_anchor,
            primary_content=seed.primary_content,
            supporting_content=self._render_supporting_content(
                seed
            ),
        )

        result = self.llm.generate(
            prompt=rendered_prompt,
            response_model=SeedCompiledRuleSchema,
        )

        return CompiledRule(
            id=seed.stable_id,
            statement=statement,
            rule_type=rule_type,
            severity=severity,
            source_anchors=[
                seed.primary_anchor,
                *seed.supporting_anchors,
            ],
            conditions=conditions,
            required_elements=self._normalize_values(
                result.required_elements
            ),
            forbidden_interpretations=self._normalize_values(
                result.forbidden_interpretations
            ),
            legal_references=self._normalize_values(
                result.legal_references
            ),
        )

    @staticmethod
    def _render_supporting_content(
        seed: RuleSeed,
    ) -> str:

        if not seed.supporting_anchors:
            return "Aucun fragment complémentaire."

        return "\n\n".join(
            (
                f"ANCHOR: {anchor}\n"
                f"TEXT: {content}"
            )
            for anchor, content in zip(
                seed.supporting_anchors,
                seed.supporting_contents,
                strict=True,
            )
        )

    @staticmethod
    def _normalize_values(
        values: list[str],
    ) -> list[str]:

        return [
            value.strip()
            for value in values
            if value.strip()
        ]
    