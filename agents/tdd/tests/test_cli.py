from __future__ import annotations

import json
import shutil
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def _command(*arguments: str) -> subprocess.CompletedProcess[str]:
    executable = shutil.which("python-ppf")
    assert executable is not None, "the installed python-ppf console script is required"
    return subprocess.run(
        [executable, *arguments],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )


def test_workflow_plan_cli_checks_snapshot_as_external_process() -> None:
    completed = _command(
        "workflow",
        "plan",
        "docs/workflow-plan-example.md",
        "--fixtures",
        "fixtures/manifest.cue",
        "--probes",
        "fixtures/probes.cue",
        "--realizations",
        "fixtures/realization-specs.cue",
        "--check",
        "generated/workflow/example.json",
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    result = json.loads(completed.stdout)
    assert result["operation"] == "workflow.plan"
    assert result["mode"] == "check"
    assert result["written"] is False


def test_public_console_surface_is_consolidated() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    scripts = project["scripts"]
    assert scripts == {"python-ppf": "tdd_agent_skills.cli:main"}
    root_help = _command("--help")
    assert root_help.returncode == 0
    assert "workflow" in root_help.stdout
    workflow_help = _command("workflow", "--help")
    assert workflow_help.returncode == 0
    assert "plan" in workflow_help.stdout
    assert "evaluate" not in workflow_help.stdout
