from __future__ import annotations

from pathlib import Path

from qualification_workflow.compiler import compile_workflow
from qualification_workflow.snapshot import snapshot_bytes
from tdd_agent_skills.workflow.compiler import compile_workflow as compatibility_compile

ROOT = Path(__file__).parents[1]


def test_compatibility_compiler_produces_byte_identical_snapshot(tmp_path: Path) -> None:
    arguments = (
        ROOT / "docs/workflow-plan-example.md",
        ROOT / "fixtures/manifest.cue",
        ROOT / "fixtures/probes.cue",
        ROOT / "fixtures/realization-specs.cue",
    )
    direct = compile_workflow(*arguments, tmp_path / "direct.json", bootstrap=True)
    compatibility = compatibility_compile(
        *arguments,
        tmp_path / "compatibility.json",
        bootstrap=True,
    )
    expected = (ROOT / "generated/workflow/example.json").read_bytes()
    assert snapshot_bytes(direct) == snapshot_bytes(compatibility) == expected
