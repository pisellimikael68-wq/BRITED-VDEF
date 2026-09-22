from v2.agents.architect.architect import ArchitectAgent
from v2.agents.planner.planner import PlannerAgent
from v2.agents.writer.writer import WriterAgent
from v2.agents.reviewer.reviewer import ReviewerAgent


class KnowledgeOrchestrator:

    def __init__(self):

        self.architect = ArchitectAgent()
        self.planner = PlannerAgent()
        self.writer = WriterAgent()
        self.reviewer = ReviewerAgent()

    def run(
        self,
        family: str,
    ):

        print("🏗 Architect...")

        plan = self.architect.design(family)

        print("📚 Planner...")

        plan = self.planner.plan(plan)

        print("✍️ Writer...")

        plan = self.writer.write(plan)

        print("🔍 Reviewer...")

        plan = self.reviewer.review(plan)

        print()

        print("✅ Pipeline terminée")

        return plan


if __name__ == "__main__":

    KnowledgeOrchestrator().run(
        "assurance_vie",
    )
    