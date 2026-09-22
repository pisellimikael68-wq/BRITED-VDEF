from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from v2.models.knowledge_models import Topic


TEMPLATE_DIR = Path(__file__).parent / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
)

template = env.get_template("topic.py.j2")


def write_chapter(
    output_dir: Path,
    module_name: str,
    variable_name: str,
    topics: list[Topic],
):
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{module_name}.py"

    content = template.render(
        variable_name=variable_name,
        topics=topics,
    )

    output_file.write_text(content, encoding="utf-8")

    print(f"      ✅ {output_file}")
    