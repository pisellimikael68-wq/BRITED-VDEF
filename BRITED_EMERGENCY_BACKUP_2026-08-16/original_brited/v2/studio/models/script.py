from dataclasses import dataclass, field


# ==========================================================
# SCRIPT SECTION
# ==========================================================

@dataclass
class ScriptSection:
    """
    Représente une section du script.
    Exemple :
    - Définition
    - Explication
    - Exemple
    - À retenir
    """

    title: str

    content: str


# ==========================================================
# SCRIPT
# ==========================================================

@dataclass
class Script:
    """
    Représente le script complet d'une publication.

    Il est généré par le ScriptEngine à partir
    d'une Publication.
    """

    # ==========================================================
    # IDENTITÉ
    # ==========================================================

    title: str

    format: str

    # ==========================================================
    # INTRODUCTION
    # ==========================================================

    hook: str

    # ==========================================================
    # CONTENU
    # ==========================================================

    sections: list[ScriptSection] = field(default_factory=list)

    # ==========================================================
    # CONCLUSION
    # ==========================================================

    conclusion: str = ""

    call_to_action: str = ""

    # ==========================================================
    # SOURCES
    # ==========================================================

    legal_sources: list[str] = field(default_factory=list)

    vocabulary: list[str] = field(default_factory=list)

    # ==========================================================
    # MÉTADONNÉES
    # ==========================================================

    notes: list[str] = field(default_factory=list)

    # ==========================================================
    # HELPERS
    # ==========================================================

    def add_section(
        self,
        title: str,
        content: str,
    ) -> None:

        self.sections.append(
            ScriptSection(
                title=title,
                content=content,
            )
        )

    def display(self) -> None:

        print("\n" + "=" * 60)
        print("📝 SCRIPT")
        print("=" * 60)

        print(f"\nTitre : {self.title}")

        print(f"\nFormat : {self.format}")

        print(f"\nHook :\n{self.hook}")

        print("\n--- CONTENU ---")

        for section in self.sections:

            print(f"\n### {section.title}")

            print(section.content)

        if self.conclusion:

            print("\n--- CONCLUSION ---")

            print(self.conclusion)

        if self.call_to_action:

            print("\n--- CTA ---")

            print(self.call_to_action)

        if self.legal_sources:

            print("\n--- SOURCES ---")

            for source in self.legal_sources:

                print(f"- {source}")
                