from v2.planning.markdown_plan_loader import MarkdownPlanLoader

loader = MarkdownPlanLoader()

family = loader.load("assurance_vie")

print()

print(f"Famille : {family.name}")

print(f"Chapitres : {len(family.chapters)}")

for chapter in family.chapters:

    print()

    print(chapter.name)

    print(len(chapter.topics))
    