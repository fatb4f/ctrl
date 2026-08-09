"""One-release compatibility aliases for :mod:`qualification_workflow`."""

from __future__ import annotations

import importlib
import sys

from qualification_workflow import (
    WorkflowPlanFailure,
    WorkflowPlanFailureKind,
    WorkflowPlanRequest,
    WorkflowPlanResult,
    compile_workflow_plan,
)

_MODULES = (
    "canonical",
    "compiler",
    "cue_blocks",
    "derivation",
    "fixtures",
    "markdown",
    "models",
    "service",
    "snapshot",
)
for _module in _MODULES:
    sys.modules[f"{__name__}.{_module}"] = importlib.import_module(
        f"qualification_workflow.{_module}"
    )

__all__ = [
    "WorkflowPlanFailure",
    "WorkflowPlanFailureKind",
    "WorkflowPlanRequest",
    "WorkflowPlanResult",
    "compile_workflow_plan",
]
