"""
brited.core.artifact
====================

Base artifact model used by the BRITED runtime.

Every artifact exchanged between agents inherits from this class.

Artifacts are immutable data contracts that can be:

- validated
- serialized
- versioned
- hashed
- traced

This module intentionally contains no business logic.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
import hashlib
import json
from typing import Any
from uuid import uuid4


# ==========================================================
# Artifact Status
# ==========================================================


class ArtifactStatus(str, Enum):
    """Lifecycle of an artifact."""

    DRAFT = "draft"
    VALIDATED = "validated"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


# ==========================================================
# Metadata
# ==========================================================


@dataclass(slots=True)
class Metadata:
    """Metadata attached to every artifact."""

    id: str = field(default_factory=lambda: str(uuid4()))

    version: str = "1.0.0"

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    author: str = "system"

    status: ArtifactStatus = ArtifactStatus.DRAFT


# ==========================================================
# Artifact
# ==========================================================


@dataclass(slots=True)
class Artifact(ABC):
    """
    Base class for every artifact.

    All exchanged objects inside BRITED must inherit from this class.
    """

    name: str

    description: str = ""

    metadata: Metadata = field(default_factory=Metadata)

    payload: dict[str, Any] = field(default_factory=dict)

    tags: list[str] = field(default_factory=list)

    references: list[str] = field(default_factory=list)

    # ------------------------------------------------------

    @property
    def id(self) -> str:
        return self.metadata.id

    @property
    def version(self) -> str:
        return self.metadata.version

    @property
    def status(self) -> ArtifactStatus:
        return self.metadata.status

    # ------------------------------------------------------

    def validate(self) -> bool:
        """
        Validate artifact integrity.

        Runtime-specific validation rules are implemented elsewhere.
        """

        if not self.name.strip():
            return False

        if self.metadata is None:
            return False

        return True

    # ------------------------------------------------------

    def touch(self) -> None:
        """Update modification timestamp."""

        self.metadata.updated_at = datetime.now(UTC)

    # ------------------------------------------------------

    def approve(self) -> None:
        self.metadata.status = ArtifactStatus.APPROVED
        self.touch()

    def reject(self) -> None:
        self.metadata.status = ArtifactStatus.REJECTED
        self.touch()

    def archive(self) -> None:
        self.metadata.status = ArtifactStatus.ARCHIVED
        self.touch()

    # ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize artifact."""

        return asdict(self)

    # ------------------------------------------------------

    def to_json(self) -> str:
        """Serialize artifact as JSON."""

        return json.dumps(
            self.to_dict(),
            default=str,
            indent=2,
            ensure_ascii=False,
        )

    # ------------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Artifact":
        """
        Instantiate artifact from dictionary.

        Concrete subclasses may override this method.
        """

        return cls(**data)

    # ------------------------------------------------------

    def fingerprint(self) -> str:
        """
        Compute deterministic SHA256 fingerprint.

        Useful for cache, traceability and change detection.
        """

        raw = json.dumps(
            self.to_dict(),
            sort_keys=True,
            default=str,
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    # ------------------------------------------------------

    def clone(self) -> "Artifact":
        """
        Create a deep copy preserving payload.

        New artifact receives a fresh identifier.
        """

        data = self.to_dict()

        data["metadata"]["id"] = str(uuid4())

        data["metadata"]["created_at"] = datetime.now(UTC)

        data["metadata"]["updated_at"] = datetime.now(UTC)

        return self.from_dict(data)

    # ------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self.fingerprint())

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"status={self.status.value})"
        )
    