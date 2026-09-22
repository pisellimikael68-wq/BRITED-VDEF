import sys

from v2.core.factory import PipelineFactory


def main():

    if len(sys.argv) < 3:

        print("\n===================================")
        print("           BRITED V2")
        print("===================================")

        print("\nGénérateur de contenu patrimonial IA")

        print("\nUsage :")
        print('  python3 brited.py instagram "assurance-vie"')

        print("\nPipelines disponibles :")
        print("  • instagram")

        print("\nExemples :")
        print('  python3 brited.py instagram "SCI"')
        print('  python3 brited.py instagram "assurance-vie"')
        print('  python3 brited.py instagram "private equity"')

        return

    mode = sys.argv[1]
    subject = sys.argv[2]

    try:

        pipeline = PipelineFactory.create(mode)

    except ValueError as e:

        print(f"\n❌ {e}")
        return

    context = pipeline.run(subject)

    print("\n===================================")
    print(f"         {mode.upper()}")
    print("===================================")

    print("\nTitre")
    print("-----------------------------------")
    print(context.script.title)

    print("\nHook")
    print("-----------------------------------")
    print(context.script.hook)

    print("\nScript")
    print("-----------------------------------")
    print(context.script.body)

    print("\nCTA")
    print("-----------------------------------")
    print(context.script.cta)

    print("\n===================================")
    print("REVIEW")
    print("===================================")

    print(f"\nScore : {context.review.score}/100")


if __name__ == "__main__":
    main()