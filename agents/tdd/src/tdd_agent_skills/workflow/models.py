"""Typed request, result, and failure boundaries for workflow planning."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class WorkflowPlanFailureKind(StrEnum):
    """Stable application failure categories for command adapters."""

    INVALID_REQUEST = "invalid-request"
    COMPILATION = "compilation"
    SNAPSHOT_DRIFT = "snapshot-drift"
    IO = "io"


class WorkflowPlanFailure(Exception):
    """A typed service failure that can be mapped by a CLI adapter."""

    def __init__(self, kind: WorkflowPlanFailureKind, message: str) -> None:
        super().__init__(message)
        self.kind = kind


@dataclass(frozen=True)
class WorkflowPlanRequest:
    """Input to the workflow-planning application service."""

    plan_path: Path
    fixture_specs_path: Path
    probes_path: Path
    realization_specs_path: Path
    output_path: Path | None = None
    check_path: Path | None = None


@dataclass(frozen=True)
class WorkflowPlanResult:
    """A successful workflow planning operation."""

    mode: str
    snapshot_path: Path
    full_digest: str
    semantic_digest: str
    written: bool
