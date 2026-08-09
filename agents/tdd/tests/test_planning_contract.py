from __future__ import annotations

import copy
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "contracts" / "planning" / "examples" / "normalized_sequence.cue"


def _cue(*arguments: str) -> subprocess.CompletedProcess[str]:
    executable = shutil.which("cue")
    assert executable is not None, "the CUE executable is required"
    return subprocess.run(
        [executable, *arguments],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )


def test_normalized_plan_is_an_executable_planning_contract() -> None:
    completed = _cue("export", str(EXAMPLE.relative_to(ROOT)), "-e", "normalizedPlan")
    assert completed.returncode == 0, completed.stderr
    plan = json.loads(completed.stdout)

    changes = plan["changes"]
    indexes = {change["id"]: index for index, change in enumerate(changes)}
    assert len(indexes) == len(changes)
    for change in changes:
        assert all(
            indexes[dependency] < indexes[change["id"]] for dependency in change["dependsOn"]
        )
        for artifact in change["generated"]:
            assert artifact["generator"]
            assert artifact["checkCommand"]
            assert artifact["manualEditing"] is False
        if change["implementation"]["runtimeCode"]:
            assert any(item["initialState"] == "failing" for item in change["acceptance"])

    reconciliation = changes[indexes["authority-reconciliation"]]
    assert reconciliation["implementation"]["runtimeCode"] is False
    assert indexes["observe-production"] < indexes["atomic-production"]

    release_proofs = changes[indexes["vertical-release-proof"]]["proof"]["required"]
    assert {
        "kind": "installed-entry-point",
        "entryPoint": "jj-agent",
    } in release_proofs

    topology = plan["cliTopology"]
    assert topology["applications"]["python-ppf"]["framework"] == "cyclopts"
    assert topology["applications"]["jj-agent"]["framework"] == "cyclopts"
    assert topology["shared"] == {
        "conventions": "shared-cyclopts",
        "requestDecoding": "generated-transport",
        "transportTypes": "generated-transport",
        "operationRegistry": "generated-registry",
        "errorEnvelope": "shared",
        "exitMapping": "shared",
    }
    assert set(topology["forbidden"]) == {
        "argparse",
        "entry-point-local request models",
        "entry-point-local operation registries",
        "implicit JSON coercion",
    }


def test_normalized_plan_validates_as_cue() -> None:
    completed = _cue("vet", "-c=false", str(EXAMPLE.relative_to(ROOT)))
    assert completed.returncode == 0, completed.stderr


def test_plan_contract_rejects_invariant_violations(tmp_path: Path) -> None:
    exported = _cue("export", str(EXAMPLE.relative_to(ROOT)), "-e", "normalizedPlan")
    assert exported.returncode == 0, exported.stderr
    valid = json.loads(exported.stdout)
    indexes = {change["id"]: index for index, change in enumerate(valid["changes"])}

    forward_dependency = copy.deepcopy(valid)
    forward_dependency["changes"][indexes["baseline"]]["dependsOn"] = ["authority-reconciliation"]

    manual_generated_artifact = copy.deepcopy(valid)
    specification = manual_generated_artifact["changes"][indexes["executable-specification"]]
    specification["generated"][0]["manualEditing"] = True

    runtime_reconciliation = copy.deepcopy(valid)
    runtime_reconciliation["changes"][indexes["authority-reconciliation"]]["implementation"][
        "runtimeCode"
    ] = True

    missing_installed_entry_point = copy.deepcopy(valid)
    release = missing_installed_entry_point["changes"][indexes["vertical-release-proof"]]
    release["proof"]["required"] = [
        proof for proof in release["proof"]["required"] if proof["kind"] != "installed-entry-point"
    ]

    no_initial_failing_proof = copy.deepcopy(valid)
    kernel = no_initial_failing_proof["changes"][indexes["pure-qualification-kernel"]]
    for criterion in kernel["acceptance"]:
        criterion["initialState"] = "passing"

    undeclared_change_field = copy.deepcopy(valid)
    undeclared_change_field["changes"][indexes["baseline"]]["parser"] = "argparse"

    invalid_plans = {
        "forward-dependency": forward_dependency,
        "manual-generated-artifact": manual_generated_artifact,
        "runtime-reconciliation": runtime_reconciliation,
        "missing-installed-entry-point": missing_installed_entry_point,
        "no-initial-failing-proof": no_initial_failing_proof,
        "undeclared-change-field": undeclared_change_field,
    }
    for name, plan in invalid_plans.items():
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        completed = _cue(
            "vet",
            str(EXAMPLE.relative_to(ROOT)),
            str(path),
            "-d",
            "planSchema",
        )
        assert completed.returncode != 0, name
