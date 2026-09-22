from v2.knowledge.compiler.corpus_models import (
    KnowledgeCorpus,
)
from v2.knowledge.compiler.rule_canonicalizer import (
    RuleCanonicalizer,
)
from v2.knowledge.compiler.rule_deduplicator import (
    RuleDeduplicator,
)
from v2.knowledge.compiler.seed_knowledge_compiler import (
    SeedKnowledgeCompiler,
)
from v2.knowledge.sources.academic_models import (
    AcademicKnowledge,
)


class CorpusCompiler:
    """
    Compile un ensemble de cours académiques
    en un corpus canonique unique.

    Pipeline :

        AcademicKnowledge
                ↓
        SeedKnowledgeCompiler
                ↓
        CompiledKnowledge
                ↓
        RuleCanonicalizer
                ↓
        CanonicalRule
                ↓
        RuleDeduplicator
                ↓
        KnowledgeCorpus
    """

    def __init__(self):

        self.seed_compiler = (
            SeedKnowledgeCompiler()
        )

        self.canonicalizer = (
            RuleCanonicalizer()
        )

        self.deduplicator = (
            RuleDeduplicator()
        )

    def compile(
        self,
        knowledges: list[AcademicKnowledge],
    )   -> KnowledgeCorpus:

        canonical_rules = []

        for     knowledge in knowledges:

            compiled = (
                self.seed_compiler.compile(
                knowledge
                )
            )

            canonical = (
                self.canonicalizer.canonicalize(
                compiled
                )
            )

            canonical_rules.extend(
                canonical.rules
            )

        canonical_rules = (
            self.deduplicator.deduplicate(
                canonical_rules
            )
        )

        return KnowledgeCorpus(
            rules=canonical_rules
        )