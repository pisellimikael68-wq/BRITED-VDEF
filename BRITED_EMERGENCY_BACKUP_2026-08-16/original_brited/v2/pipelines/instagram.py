from config import MIN_REVIEW_SCORE

from v2.agents.leveria.agent import LeveriaAgent
from v2.agents.editorial.agent import EditorialAgent
from v2.agents.angle.agent import AngleAgent
from v2.agents.writer.agent import WriterAgent
from v2.agents.review.agent import ReviewAgent
from v2.agents.rewrite.agent import RewriteAgent

from v2.core.context import BritedContext

from v2.knowledge.engine import KnowledgeEngine

from v2.exporters.export_manager import ExportManager
from v2.history.history_manager import HistoryManager

from v2.services.logger import PipelineLogger


class InstagramPipeline:

    def run(self, subject: str) -> BritedContext:

        context = BritedContext(subject=subject)

        # ==========================================
        # KNOWLEDGE ENGINE
        # ==========================================

        context.editorial_brief = KnowledgeEngine().build(
            context.subject
        )

        # ==========================================
        # LEVERIA
        # ==========================================

        PipelineLogger.section("LEVERIA")

        context = LeveriaAgent().run(context)

        # ==========================================
        # EDITORIAL
        # ==========================================

        PipelineLogger.section("EDITORIAL")

        context = EditorialAgent().run(context)

        # ==========================================
        # ANGLE
        # ==========================================

        PipelineLogger.section("ANGLE")

        context = AngleAgent().run(context)

        # ==========================================
        # WRITER
        # ==========================================

        PipelineLogger.section("WRITER")

        context = WriterAgent().run(context)

        # ==========================================
        # REVIEW
        # ==========================================

        PipelineLogger.section("REVIEW")

        context = ReviewAgent().run(context)

        self.print_quality_report(context)

        PipelineLogger.info(
            f"Score initial : {context.review.score}/100"
        )

        if context.review.score < MIN_REVIEW_SCORE:

            PipelineLogger.warning(
                f"Score insuffisant : {context.review.score}/100"
            )

            PipelineLogger.info(
                "Lancement du RewriteAgent..."
            )

            context = RewriteAgent().run(context)

            PipelineLogger.section(
                "REVIEW APRÈS RÉÉCRITURE"
            )

            context = ReviewAgent().run(context)

            self.print_quality_report(context)

            PipelineLogger.info(
                f"Score après réécriture : {context.review.score}/100"
            )

            if context.review.score >= MIN_REVIEW_SCORE:

                PipelineLogger.success(
                    "Script validé après réécriture."
                )

            else:

                PipelineLogger.warning(
                    "Le script reste perfectible."
                )

        else:

            PipelineLogger.success(
                "Script validé dès la première version."
                )

        # ==========================================
        # EXPORT
        # ==========================================

        PipelineLogger.section("EXPORT")

        exported_files = ExportManager().export(context)

        for path in exported_files:

            PipelineLogger.info(f"Export : {path}")

        PipelineLogger.success(
            "Exports générés avec succès."
        )

        # ==========================================
        # HISTORY
        # ==========================================

        PipelineLogger.section("HISTORY")

        history_file = HistoryManager().save(context)

        PipelineLogger.info(
            f"Historique mis à jour : {history_file}"
        )

        PipelineLogger.success(
            "Historique enregistré."
        )

        return context

    def print_quality_report(
        self,
        context: BritedContext,
    ):

        review = context.review

        PipelineLogger.section("QUALITY REPORT")

        print(f"Global         : {review.score}/100")
        print()

        print(
            f"Patrimonial    : {review.patrimonial_score}/30"
        )

        print(
            f"Pédagogie      : {review.pedagogy_score}/20"
        )

        print(
            f"Instagram      : {review.instagram_score}/20"
        )

        print(
            f"Hook           : {review.hook_score}/10"
        )

        print(
            f"CTA            : {review.cta_score}/10"
        )

        print(
            f"Compliance     : {review.compliance_score}/10"
        )

        print()

        if review.strengths:

            print("Points forts")

            for point in review.strengths:

                print(f"  • {point}")

            print()

        if review.weaknesses:

            print("Faiblesses")

            for point in review.weaknesses:

                print(f"  • {point}")

            print()

        if review.rewrite_needed:

            print("Réécriture nécessaire")

            for instruction in review.rewrite_instructions:

                print(f"  • {instruction}")

            print()