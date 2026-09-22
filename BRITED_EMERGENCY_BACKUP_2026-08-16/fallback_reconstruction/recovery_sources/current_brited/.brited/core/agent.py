"""
brited.core.agent
=================

Core abstraction for every BRITED agent.

An Agent is an executable unit capable of performing one task
within a protocol.

Concrete agents (Planner, Builder, Reviewer...) inherit from
this class.

The runtime is responsible for loading the agent definition
from .brited/agents/*.yml.

This module intentionally contains no provider-specific logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from time import perf_counter
from typing import Any

from .artifact import Artifact


# ==========================================================
# Agent State
# ==========================================================


class AgentState(str, Enum):
    """Lifecycle state of an agent."""

    IDLE = "idle"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DISABLED = "disabled"


# ==========================================================
# Agent Metrics
# ==========================================================


@dataclass(slots=True)
class AgentMetrics:
    """Runtime execution metrics."""

    started_at: datetime | None = None
    finished_at: datetime | None = None

    duration: float = 0.0

    executions: int = 0

    failures: int = 0


# ==========================================================
# Agent Result
# ==========================================================


@dataclass(slots=True)
class AgentResult:
    """Result returned by every agent."""

    success: bool

    message: str = ""

    artifact: Artifact | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Agent
# ==========================================================


class Agent(ABC):
    """
    Base class for every BRITED agent.

    Concrete implementations only implement run().
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str = "",
    ) -> None:

        self.id = agent_id
        self.name = name
        self.description = description

        self.state = AgentState.IDLE

        self.capabilities: list[str] = []

        self.metrics = AgentMetrics()

    # ------------------------------------------------------

    @property
    def enabled(self) -> bool:
        return self.state != AgentState.DISABLED

    # ------------------------------------------------------

    def enable(self) -> None:
        self.state = AgentState.READY

    def disable(self) -> None:
        self.state = AgentState.DISABLED

    # ------------------------------------------------------

    def execute(
        self,
        context: dict[str, Any],
    ) -> AgentResult:
        """
        Execute the agent lifecycle.

        before_run()
            ↓
           run()
            ↓
        after_run()
        """

        if not self.enabled:
            return AgentResult(
                success=False,
                message="Agent is disabled.",
            )

        self.metrics.executions += 1

        self.metrics.started_at = datetime.now(UTC)

        started = perf_counter()

        self.state = AgentState.RUNNING

        try:

            self.before_run(context)

            result = self.run(context)

            self.after_run(context, result)

            self.state = AgentState.COMPLETED

            return result

        except Exception as exc:

            self.metrics.failures += 1

            self.state = AgentState.FAILED

            return AgentResult(
                success=False,
                message=str(exc),
            )

        finally:

            self.metrics.finished_at = datetime.now(UTC)

            self.metrics.duration = (
                perf_counter() - started
            )

    # ------------------------------------------------------

    def before_run(
        self,
        context: dict[str, Any],
    ) -> None:
        """
        Hook executed before run().
        """

    # ------------------------------------------------------

    @abstractmethod
    def run(
        self,
        context: dict[str, Any],
    ) -> AgentResult:
        """
        Agent implementation.

        Must be implemented by subclasses.
        """

    # ------------------------------------------------------

    def after_run(
        self,
        context: dict[str, Any],
        result: AgentResult,
    ) -> None:
        """
        Hook executed after run().
        """

    # ------------------------------------------------------

    def supports(
        self,
        capability: str,
    ) -> bool:
        return capability in self.capabilities

    # ------------------------------------------------------

    def add_capability(
        self,
        capability: str,
    ) -> None:

        if capability not in self.capabilities:
            self.capabilities.append(capability)

    # ------------------------------------------------------

    def remove_capability(
        self,
        capability: str,
    ) -> None:

        if capability in self.capabilities:
            self.capabilities.remove(capability)

    # ------------------------------------------------------

    def reset(self) -> None:
        """
        Reset runtime state.
        """

        self.state = AgentState.IDLE

    # ------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"id='{self.id}', "
            f"state='{self.state.value}')"
        )
    