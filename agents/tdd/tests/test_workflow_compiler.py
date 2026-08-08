from __future__ import annotations

from pathlib import Path

import pytest

from tdd_agent_skills.workflow.compiler import compile_workflow
from tdd_agent_skills.workflow.fixtures import derive_fixture_manifest
from tdd_agent_skills.workflow.snapshot import (
    SnapshotError,
    atomic_write,
    build_snapshot,
    snapshot_bytes,
)

ROOT = Path(__file__).parents[3]
PLAN = ROOT / "agents/tdd/docs/workflow-plan-example.md"
FIXTURES = ROOT / "fixtures/tdd/manifest.cue"
PROBES = ROOT / "fixtures/tdd/probes.cue"
REALIZATIONS = ROOT / "fixtures/tdd/realization-specs.cue"


def test_example_plan_compiles_to_static_snapshot(tmp_path: Path) -> None:
    output = tmp_path / "workflow.json"
    snapshot = compile_workflow(
        plan_path=PLAN,
        fixture_specs_path=FIXTURES,
        probes_path=PROBES,
        realization_specs_path=REALIZATIONS,
        output_path=output,
        bootstrap=True,
    )
    payload = snapshot["payload"]
    assert payload["planArtifactOccurrence"]["path"] == "agents/tdd/docs/workflow-plan-example.md"
    assert len(payload["obligations"]) == 2
    assert payload["fixtureManifests"][0]["fixtureID"] == "fixture.workflow-example"
    assert snapshot["identity"]["semanticDigest"]


def test_existing_snapshot_is_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "workflow.json"
    first = compile_workflow(
        PLAN,
        FIXTURES,
        PROBES,
        REALIZATIONS,
        output,
        bootstrap=True,
    )
    atomic_write(output, snapshot_bytes(first))
    second = compile_workflow(
        PLAN,
        FIXTURES,
        PROBES,
        REALIZATIONS,
        output,
    )
    assert snapshot_bytes(first) == snapshot_bytes(second)


def test_fixture_manifest_changes_when_bytes_change(tmp_path: Path) -> None:
    root = tmp_path / "fixtures" / "data" / "fixture.example"
    root.mkdir(parents=True)
    target = root / "input.txt"
    target.write_text("first", encoding="utf-8")
    first = derive_fixture_manifest(tmp_path, {"id": "fixture.example"})
    target.write_text("second", encoding="utf-8")
    second = derive_fixture_manifest(tmp_path, {"id": "fixture.example"})
    assert first["treeDigest"] != second["treeDigest"]


def test_reused_revision_id_with_changed_section_is_rejected(tmp_path: Path) -> None:
    output = tmp_path / "workflow.json"
    snapshot = compile_workflow(
        PLAN,
        FIXTURES,
        PROBES,
        REALIZATIONS,
        output,
        bootstrap=True,
    )
    changed_payload = dict(snapshot["payload"])
    changed_sections = [dict(section) for section in changed_payload["specSections"]]
    changed_sections[0]["title"] = "Changed without a revision"
    changed_payload["specSections"] = changed_sections
    with pytest.raises(SnapshotError, match="reused with different canonical content"):
        build_snapshot(changed_payload, snapshot, bootstrap=False)
