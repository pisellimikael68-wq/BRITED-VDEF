"""
brited.runtime.loader
=====================

BRITED configuration loader.

This module is responsible for discovering and loading every
configuration file inside the .brited directory.

It performs no validation and no orchestration.

Responsibilities
----------------

- Discover the .brited directory
- Load YAML files
- Build an in-memory representation
- Expose loaded objects

Validation is handled by validator.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ==========================================================
# Runtime Configuration
# ==========================================================


@dataclass(slots=True)
class RuntimeConfiguration:
    """Represents the loaded BRITED configuration."""

    root: Path

    project: dict[str, Any] = field(default_factory=dict)

    architecture: dict[str, Any] = field(default_factory=dict)

    components: dict[str, Any] = field(default_factory=dict)

    conventions: dict[str, Any] = field(default_factory=dict)

    roadmap: dict[str, Any] = field(default_factory=dict)

    decisions: dict[str, Any] = field(default_factory=dict)

    agents: dict[str, dict[str, Any]] = field(default_factory=dict)

    protocols: dict[str, dict[str, Any]] = field(default_factory=dict)

    artifacts: dict[str, dict[str, Any]] = field(default_factory=dict)

    rules: dict[str, dict[str, Any]] = field(default_factory=dict)

    skills: dict[str, dict[str, Any]] = field(default_factory=dict)


# ==========================================================
# Loader
# ==========================================================


class Loader:
    """
    Loads every BRITED configuration file.
    """

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:

        if project_root is None:
            project_root = Path.cwd()

        self.project_root = Path(project_root)

        self.brited_root = self.project_root / ".brited"

        self.configuration = RuntimeConfiguration(
            root=self.brited_root
        )

    # ------------------------------------------------------

    def load(self) -> RuntimeConfiguration:
        """
        Load the entire BRITED configuration.
        """

        self._check_structure()

        self.configuration.project = self._load_yaml(
            "project.yml"
        )

        self.configuration.architecture = self._load_yaml(
            "architecture.yml"
        )

        self.configuration.components = self._load_yaml(
            "components.yml"
        )

        self.configuration.conventions = self._load_yaml(
            "conventions.yml"
        )

        self.configuration.roadmap = self._load_yaml(
            "roadmap.yml"
        )

        self.configuration.decisions = self._load_yaml(
            "decisions.yml"
        )

        self.configuration.agents = self._load_directory(
            "agents"
        )

        self.configuration.protocols = self._load_directory(
            "protocols"
        )

        self.configuration.artifacts = self._load_directory(
            "artifacts"
        )

        self.configuration.rules = self._load_directory(
            "rules"
        )

        self.configuration.skills = self._load_directory(
            "skills"
        )

        return self.configuration

    # ------------------------------------------------------

    def _check_structure(self) -> None:

        if not self.brited_root.exists():
            raise FileNotFoundError(
                ".brited directory not found."
            )

    # ------------------------------------------------------

    def _load_yaml(
        self,
        filename: str,
    ) -> dict[str, Any]:

        path = self.brited_root / filename

        if not path.exists():
            return {}

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return yaml.safe_load(file) or {}

    # ------------------------------------------------------

    def _load_directory(
        self,
        directory: str,
    ) -> dict[str, dict[str, Any]]:

        root = self.brited_root / directory

        result: dict[str, dict[str, Any]] = {}

        if not root.exists():
            return result

        for file in sorted(root.glob("*.yml")):

            with file.open(
                "r",
                encoding="utf-8",
            ) as stream:

                result[file.stem] = (
                    yaml.safe_load(stream) or {}
                )

        return result

    # ------------------------------------------------------

    @property
    def loaded(self) -> bool:

        return bool(self.configuration.project)

    # ------------------------------------------------------

    def summary(self) -> dict[str, int]:
        """
        Returns a summary of the loaded configuration.
        """

        return {

            "agents": len(self.configuration.agents),

            "protocols": len(
                self.configuration.protocols
            ),

            "artifacts": len(
                self.configuration.artifacts
            ),

            "rules": len(
                self.configuration.rules
            ),

            "skills": len(
                self.configuration.skills
            ),
        }
    