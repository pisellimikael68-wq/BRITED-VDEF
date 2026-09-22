from pathlib import Path


def generate_family_init(folder: Path):

    """
    Génère automatiquement le __init__.py d'une famille.
    """

    modules = []

    for file in sorted(folder.glob("*.py")):

        if file.name == "__init__.py":
            continue

        if file.name.startswith("_"):
            continue

        modules.append(file.stem)

    imports = []

    variables = []

    for module in modules:

        variable = f"{module.upper()}_TOPICS"

        imports.append(
            f"from .{module} import {variable}"
        )

        variables.append(variable)

    family_name = folder.name.upper()

    lines = []

    lines.extend(imports)

    lines.append("")
    lines.append("")

    lines.append(f"{family_name}_TOPICS = (")

    for variable in variables:

        lines.append(f"    {variable}")

        if variable != variables[-1]:
            lines.append("    +")

    lines.append(")")

    (folder / "__init__.py").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
    