from __future__ import annotations

import json
import shutil
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[3]


def _command(*arguments: str) -> subprocess.CompletedProcess[str]:
    executable = shutil.which("python-ppf")
    assert executable is not None, "the workspace python-ppf console script is required"
    return subprocess.run(
        [executable, *arguments],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )


def test_workflow_compile_cli_checks_snapshot_as_external_process() -> None:
    completed = _command(
        "workflow",
        "compile",
        "agents/tdd/docs/workflow-plan-example.md",
        "--fixtures",
        "fixtures/tdd/manifest.cue",
        "--probes",
        "fixtures/tdd/probes.cue",
        "--realizations",
        "fixtures/tdd/realization-specs.cue",
        "--check",
        "agents/tdd/generated/workflow/example.json",
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    result = json.loads(completed.stdout)
    assert result["operation"] == "workflow.compile"
    assert result["mode"] == "check"
    assert result["written"] is False


def test_public_console_surface_is_consolidated_in_ppf() -> None:
    ppf = tomllib.loads((ROOT / "packages/ppf/pyproject.toml").read_text())
    tdd = tomllib.loads((ROOT / "agents/tdd/pyproject.toml").read_text())
    assert ppf["project"]["scripts"]["python-ppf"] == "ppf.workflow_cli:main"
    assert "scripts" not in tdd["project"]
    workflow_help = _command("workflow", "--help")
    assert workflow_help.returncode == 0
    assert "plan" in workflow_help.stdout
    assert "compile" in workflow_help.stdout
