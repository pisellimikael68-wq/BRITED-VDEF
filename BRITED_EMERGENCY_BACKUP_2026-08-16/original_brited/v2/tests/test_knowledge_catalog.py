from v2.knowledge.io.knowledge_catalog import (
    KnowledgeCatalog,
)

catalog = KnowledgeCatalog()

print()

print("Familles :")
print(catalog.families())

print()

print("Chapitres assurance_vie :")
print(catalog.chapters("assurance_vie"))

print()

print(
    "Rachats existe :",
    catalog.exists(
        "assurance_vie",
        "rachats",
    ),
)
