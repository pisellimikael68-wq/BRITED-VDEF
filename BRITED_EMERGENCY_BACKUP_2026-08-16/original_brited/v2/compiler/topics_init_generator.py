from pathlib import Path


def generate_topics_init(topics_dir: Path):
    """
    Génère automatiquement v2/knowledge/topics/__init__.py.
    Compatible avec les familles dont le nom est un mot réservé Python,
    comme "or".
    """

    families = []

    for folder in sorted(topics_dir.iterdir()):

        if not folder.is_dir():
            continue

        if folder.name.startswith("_"):
            continue

        if not (folder / "__init__.py").exists():
            continue

        families.append(folder.name)

    lines = []

    lines.append("from importlib import import_module")
    lines.append("")
    lines.append("")
    lines.append("def _load_family_topics(family: str, variable: str):")
    lines.append("    module = import_module(f'.{family}', __name__)")
    lines.append("    return getattr(module, variable)")
    lines.append("")
    lines.append("")

    variables = []

    for family in families:

        variable = f"{family.upper()}_TOPICS"
        variables.append(variable)

        lines.append(
            f'{variable} = _load_family_topics("{family}", "{variable}")'
        )

    lines.append("")
    lines.append("")
    lines.append("ALL_TOPICS = (")

    if variables:

        lines.append(f"    {variables[0]}")

        for variable in variables[1:]:
            lines.append(f"    + {variable}")

    else:
        lines.append("    []")

    lines.append(")")
    lines.append("")

    (topics_dir / "__init__.py").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("📚 topics/__init__.py généré")
    