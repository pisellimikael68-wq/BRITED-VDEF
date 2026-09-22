from v2.core.factory import PipelineFactory
from v2.exporters.markdown import MarkdownExporter


def main():

    pipeline = PipelineFactory.create("instagram")

    subject = input("Sujet : ")
    
    context = pipeline.run(subject)

    path = MarkdownExporter().export(context)

    print(f"\n📄 Export terminé : {path}")


if __name__ == "__main__":
    main()