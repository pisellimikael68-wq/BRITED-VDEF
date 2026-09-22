import re

from legacy.core.context import BritedContext

from legacy.agents.leveria_agent import search_leveria
from legacy.agents.angle_agent import choose_angle
from legacy.agents.writer_agent import write_script
from legacy.agents.review_agent import review_script


class BritedOrchestrator:

    def run(self, subject: str):

        context = BritedContext(subject=subject)

        print("\n========================")
        print("ÉTAPE 1 : LEVERIA")
        print("========================")

        context.knowledge = search_leveria(subject)

        print("\n========================")
        print("ÉTAPE 2 : ANGLE")
        print("========================")

        context.angles = choose_angle(
            context.subject,
            context.knowledge
        )

        print("\n========================")
        print("ÉTAPE 3 : WRITER")
        print("========================")

        context.script = write_script(
            context.subject,
            context.knowledge,
            context.angles
        )

        print("\n========================")
        print("ÉTAPE 4 : REVIEW")
        print("========================")

        context.review = review_script(
            context.subject,
            context.script
        )

        match = re.search(r"Total\s*:\s*(\d+)/50", context.review)

        if match:
            context.score = int(match.group(1))
            context.needs_rewrite = context.score < 46

        print("\n========================")
        print("SCORE")
        print("========================")
        print(context.score)

        print("\nRewrite nécessaire :", context.needs_rewrite)

        if context.needs_rewrite:

            print("\n========================")
            print("RÉÉCRITURE AUTOMATIQUE")
            print("========================")

            context.rewrite_count += 1

            context.script = write_script(
                context.subject,
                context.knowledge,
                context.angles,
                context.review
            )

            context.review = review_script(
                context.subject,
                context.script
            )

            match = re.search(r"Total\s*:\s*(\d+)/50", context.review)

            if match:
                context.score = int(match.group(1))
                context.needs_rewrite = context.score < 46

        return context
