"""Application service for workflow plan compilation and drift checking."""

from __future__ import annotations

from .compiler import WorkflowCompileError, compile_workflow
from .models import (
    WorkflowPlanFailure,
    WorkflowPlanFailureKind,
    WorkflowPlanRequest,
    WorkflowPlanResult,
)
from .snapshot import SnapshotError, atomic_write, snapshot_bytes


def compile_workflow_plan(request: WorkflowPlanRequest) -> WorkflowPlanResult:
    """Compile or check a static workflow plan behind a typed application boundary."""
    if (request.output_path is None) == (request.check_path is None):
        raise WorkflowPlanFailure(
            WorkflowPlanFailureKind.INVALID_REQUEST,
            "supply exactly one of output_path or check_path",
        )
    snapshot_path = request.output_path or request.check_path
    assert snapshot_path is not None
    try:
        if request.output_path is not None:
            snapshot = compile_workflow(
                plan_path=request.plan_path,
                fixture_specs_path=request.fixture_specs_path,
                probes_path=request.probes_path,
                realization_specs_path=request.realization_specs_path,
                output_path=snapshot_path,
                bootstrap=not snapshot_path.exists(),
            )
            atomic_write(snapshot_path, snapshot_bytes(snapshot))
            mode = "output"
            written = True
        else:
            if not snapshot_path.exists():
                raise WorkflowPlanFailure(
                    WorkflowPlanFailureKind.SNAPSHOT_DRIFT,
                    f"snapshot does not exist: {snapshot_path}",
                )
            snapshot = compile_workflow(
                plan_path=request.plan_path,
                fixture_specs_path=request.fixture_specs_path,
                probes_path=request.probes_path,
                realization_specs_path=request.realization_specs_path,
                output_path=snapshot_path,
                bootstrap=False,
            )
            if snapshot_bytes(snapshot) != snapshot_path.read_bytes():
                raise WorkflowPlanFailure(
                    WorkflowPlanFailureKind.SNAPSHOT_DRIFT,
                    "compiled workflow differs from committed snapshot",
                )
            mode = "check"
            written = False
    except WorkflowPlanFailure:
        raise
    except (WorkflowCompileError, SnapshotError) as error:
        raise WorkflowPlanFailure(WorkflowPlanFailureKind.COMPILATION, str(error)) from error
    except OSError as error:
        raise WorkflowPlanFailure(WorkflowPlanFailureKind.IO, str(error)) from error
    return WorkflowPlanResult(
        mode=mode,
        snapshot_path=snapshot_path,
        full_digest=snapshot["identity"]["fullDigest"],
        semantic_digest=snapshot["identity"]["semanticDigest"],
        written=written,
    )
