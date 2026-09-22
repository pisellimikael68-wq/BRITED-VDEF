from pathlib import Path


def generate_family_init(
    family_dir: Path,
):
    """
    Génère automatiquement le __init__.py d'une famille.
    """

    modules = []

    for file in sorted(family_dir.glob("*.py")):

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

    family_variable = f"{family_dir.name.upper()}_TOPICS"

    lines = []

    if imports:
        lines.extend(imports)
        lines.append("")
        lines.append("")

    lines.append(f"{family_variable} = (")

    if variables:
        lines.append(f"    {variables[0]}")

        for variable in variables[1:]:
            lines.append(f"    + {variable}")

    else:
        lines.append("    []")

    lines.append(")")
    lines.append("")

    (family_dir / "__init__.py").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"      📦 {family_dir.name}/__init__.py")
    