"""The single public Cyclopts application for python-ppf."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from cyclopts import App

from .workflow.models import WorkflowPlanFailure, WorkflowPlanRequest
from .workflow.service import compile_workflow_plan

app = App(name="python-ppf")
workflow = App(name="workflow")
app.command(workflow)


@workflow.command(name="plan")
def plan_workflow(
    plan: Path,
    *,
    fixtures: Path,
    probes: Path,
    realizations: Path,
    output: Path | None = None,
    check: Path | None = None,
) -> None:
    """Compile a typed Markdown workflow plan or check its committed snapshot."""
    result = compile_workflow_plan(
        WorkflowPlanRequest(
            plan_path=plan,
            fixture_specs_path=fixtures,
            probes_path=probes,
            realization_specs_path=realizations,
            output_path=output,
            check_path=check,
        )
    )
    print(
        json.dumps(
            {
                "operation": "workflow.plan",
                "mode": result.mode,
                "snapshotPath": result.snapshot_path.as_posix(),
                "fullDigest": result.full_digest,
                "semanticDigest": result.semantic_digest,
                "written": result.written,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def main() -> int:
    """Run the root application and map typed service failures to an application exit status."""
    try:
        app()
    except WorkflowPlanFailure as error:
        print(
            json.dumps(
                {"error": error.kind, "message": str(error)},
                separators=(",", ":"),
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1
    return 0
