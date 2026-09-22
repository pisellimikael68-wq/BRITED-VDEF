from legacy.core.orchestrator import BritedOrchestrator

subject = input("Sujet de la vidéo : ")

orchestrator = BritedOrchestrator()

context = orchestrator.run(subject)

print("\n")
print("=" * 60)
print("SCRIPT FINAL")
print("=" * 60)
print()

print(context.script)

print("\n")
print("=" * 60)
print("REVIEW")
print("=" * 60)
print()

print(context.review)
