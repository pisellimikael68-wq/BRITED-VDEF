from dataclasses import dataclass, field


@dataclass(slots=True)
class GenerationOptions:
    """
    Options de génération utilisées par les pipelines.
    """

    force: bool = False

    chapters: list[str] | None = None

    verbose: bool = True

    dry_run: bool = False

    parallel: bool = False

    overwrite: bool = False

    stop_on_error: bool = False

    max_topics: int | None = None

    tags: list[str] = field(default_factory=list)
    