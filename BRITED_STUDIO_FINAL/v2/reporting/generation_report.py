from pathlib import Path

from v2.core.context import BritedContext


class GenerationReport:

    def __init__(self, context: BritedContext):

        self.context = context

    def display(self):

        review = self.context.review
        script = self.context.script
        angle = self.context.selected_angle

        print()
        print("=" * 60)
        print("                 BRITED V1.0")
        print("=" * 60)
        print()

        print(f"Sujet       : {self.context.subject}")
        print("Pipeline    : Instagram")

        if angle:
            print(f"Angle       : {angle.title}")

        print(f"Titre       : {script.title}")

        print(f"Score       : {review.score}/100")

        print()

        print("-" * 60)
        print("QUALITÉ")
        print("-" * 60)

        print(f"Patrimonial : {review.patrimonial_score}/30")
        print(f"Pédagogie   : {review.pedagogy_score}/20")
        print(f"Instagram   : {review.instagram_score}/20")
        print(f"Hook        : {review.hook_score}/10")
        print(f"CTA         : {review.cta_score}/10")
        print(f"Compliance  : {review.compliance_score}/10")

        print()

        if review.strengths:

            print("Points forts")

            for point in review.strengths:
                print(f"  ✓ {point}")

            print()

        if review.weaknesses:

            print("Faiblesses")

            for point in review.weaknesses:
                print(f"  • {point}")

            print()

        export_root = Path("exports")

        if export_root.exists():

            print("-" * 60)
            print("EXPORTS")
            print("-" * 60)

            for path in sorted(export_root.rglob("*")):

                if path.is_file():

                    print(f"✓ {path}")

            print()

        history = Path("history/history.json")

        if history.exists():

            print("-" * 60)
            print("HISTORIQUE")
            print("-" * 60)

            print(f"✓ {history}")

            print()

        print("=" * 60)
        print("        Génération terminée avec succès")
        print("=" * 60)
        print()
        