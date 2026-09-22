from v2.knowledge.compiler.models import (
    CompiledKnowledge,
    CompiledRule,
    RuleSeverity,
    RuleType,
)
from v2.knowledge.compiler.rule_deduplicator import (
    RuleDeduplicator,
)
from v2.knowledge.compiler.schemas import (
    CompiledKnowledgeSchema,
)
from v2.knowledge.compiler.source_fragment import (
    SourceFragment,
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


class KnowledgeCompiler:
    """
    Compile un bloc Knowledge académique en règles
    métier structurées et ancrées dans la source.
    """

    def __init__(self):

        self.llm = LLMFactory.create()

        self.fragment_builder = (
            SourceFragmentBuilder()
        )

        self.deduplicator = RuleDeduplicator()

    def compile(
        self,
        knowledge: AcademicKnowledge,
    ) -> CompiledKnowledge:

        fragments = self.fragment_builder.build(
            knowledge
        )

        prompt = PromptLoader.load(
            "knowledge/compile_rules.md"
        )

        rendered_prompt = PromptRenderer.render(
            prompt,
            family=knowledge.family,
            chapter=knowledge.chapter,
            source_id=knowledge.id,
            source_fragments=(
                self._render_fragments(
                    fragments
                )
            ),
        )

        result = self.llm.generate(
            prompt=rendered_prompt,
            response_model=CompiledKnowledgeSchema,
        )

        valid_anchors = {
            fragment.anchor
            for fragment in fragments
        }

        compiled_rules = [
            self._to_compiled_rule(
                rule=rule,
                valid_anchors=valid_anchors,
            )
            for rule in result.rules
        ]

        compiled_rules = self.deduplicator.deduplicate(
            compiled_rules
        )

        return CompiledKnowledge(
            source_id=knowledge.id,
            family=knowledge.family,
            chapter=knowledge.chapter,
            rules=compiled_rules,
        )

    @staticmethod
    def _to_compiled_rule(
        *,
        rule,
        valid_anchors: set[str],
    ) -> CompiledRule:

        source_anchors = [
            value.strip()
            for value in rule.source_anchors
            if value.strip()
        ]

        invalid_anchors = [
            anchor
            for anchor in source_anchors
            if anchor not in valid_anchors
        ]

        if invalid_anchors:

            raise ValueError(
                "Source anchors invalides produits "
                "par le Knowledge Compiler : "
                + ", ".join(
                    sorted(set(invalid_anchors))
                )
            )

        return CompiledRule(
            id=rule.id.strip(),
            statement=rule.statement.strip(),
            rule_type=RuleType(rule.rule_type),
            severity=RuleSeverity(rule.severity),
            source_anchors=sorted(
                set(source_anchors)
            ),
            conditions=[
                value.strip()
                for value in rule.conditions
                if value.strip()
            ],
            required_elements=[
                value.strip()
                for value in rule.required_elements
                if value.strip()
            ],
            forbidden_interpretations=[
                value.strip()
                for value
                in rule.forbidden_interpretations
                if value.strip()
            ],
            legal_references=[
                value.strip()
                for value in rule.legal_references
                if value.strip()
            ],
        )

    @staticmethod
    def _render_fragments(
        fragments: list[SourceFragment],
    ) -> str:

        return "\n\n".join(
            (
                f"ANCHOR: {fragment.anchor}\n"
                f"SECTION: {fragment.section}\n"
                f"TEXT: {fragment.text}"
            )
            for fragment in fragments
        )
    