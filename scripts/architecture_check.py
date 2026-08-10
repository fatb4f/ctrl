from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import tomllib
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.protocols import Validator
from pydantic import BaseModel, ValidationError
from qualification_workflow.generated import (
    QualificationPolicyTransport,
    QualificationResultTransport,
)

ROOT = Path(__file__).parents[1]
PROVENANCE_INPUT_DIRECTORIES = (
    "spec/core",
    "spec/repository",
    "spec/qualification",
    "spec/qualification/generate",
)
EXPECTED_PROVENANCE_OUTPUTS = {
    "spec/generated/qualification.schema.json",
    "packages/qualification-workflow/src/qualification_workflow/generated/qualification.py",
}
LAYERS = ("core", "repository", "qualification", "controller")
ALLOWED_IMPORTS = {
    "core": set(),
    "repository": {"core"},
    "qualification": {"core", "repository", "qualification"},
    "controller": {"core", "repository", "qualification", "controller"},
}
IMPORT_LAYER = re.compile(
    r"github\.com/fatb4f/ctrl/spec/(core|repository|qualification|controller)"
)


def fail(message: str) -> None:
    raise SystemExit(message)


def components() -> dict[str, dict[str, str]]:
    completed = subprocess.run(
        ["cue", "export", "./control", "-e", "components"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        fail(f"cannot load component manifest:\n{completed.stderr}")
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        fail("component manifest must export an object")
    return value


def project(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))["project"]


def dependency_name(requirement: object) -> str:
    if not isinstance(requirement, str):
        return ""
    return re.split(r"[ @<>=!~\[]", requirement, maxsplit=1)[0].lower().replace("_", "-")


def forbidden_cue_imports(layer: str, content: str) -> set[str]:
    return set(IMPORT_LAYER.findall(content)) - ALLOWED_IMPORTS[layer]


def expected_provenance_inputs() -> set[str]:
    paths = {"cue.mod/module.cue"}
    for directory in PROVENANCE_INPUT_DIRECTORIES:
        paths.update(path.relative_to(ROOT).as_posix() for path in (ROOT / directory).glob("*.cue"))
    return paths


def schema_validator(definition: str) -> Validator:
    schema = json.loads(
        (ROOT / "spec/generated/qualification.schema.json").read_text(encoding="utf-8")
    )
    projected = {
        "$schema": schema["$schema"],
        "$defs": schema["$defs"],
        "$ref": f"#/$defs/{definition}",
    }
    Draft202012Validator.check_schema(projected)
    return Draft202012Validator(projected)


def pydantic_accepts(model: type[BaseModel], value: dict) -> bool:
    try:
        model.model_validate(value, strict=True)
    except ValidationError:
        return False
    return True


def cue_accepts(definition: str, value: dict) -> bool:
    with tempfile.TemporaryDirectory(prefix="qualification-cue-fixture-") as directory:
        fixture = Path(directory) / "fixture.json"
        fixture.write_text(json.dumps(value), encoding="utf-8")
        completed = subprocess.run(
            [
                "cue",
                "vet",
                "-c=true",
                "-d",
                f"#{definition}",
                "./spec/qualification",
                str(fixture),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    return completed.returncode == 0


def require_boundary(
    name: str,
    value: dict,
    *,
    schema: Validator,
    model: type[BaseModel],
    structural_definition: str,
    semantic_definition: str,
    expected: tuple[bool, bool, bool, bool],
) -> None:
    actual = (
        schema.is_valid(value),
        pydantic_accepts(model, value),
        cue_accepts(structural_definition, value),
        cue_accepts(semantic_definition, value),
    )
    if actual != expected:
        fail(f"qualification boundary mismatch for {name}: expected {expected}, got {actual}")


def qualification_boundaries() -> None:
    fixtures = json.loads(
        (ROOT / "spec/tests/qualification-transport-fixtures.json").read_text(encoding="utf-8")
    )
    result_schema = schema_validator("QualificationResultTransport")
    result_cases = {
        "validQualified": (True, True, True, True),
        "missingRepository": (False, False, False, False),
        "missingClaims": (False, False, False, False),
        "missingViolations": (False, False, False, False),
        "componentsList": (False, False, False, False),
        "componentRootNotString": (False, False, False, False),
        "emptyComponentRoot": (False, False, False, False),
        "emptyReason": (False, False, False, False),
        "stringComplete": (False, False, False, False),
        "unknownField": (False, False, False, False),
        "unknownQualified": (True, True, True, False),
        "rejectedSatisfiedViolation": (True, True, True, False),
        "validRejectedComplete": (True, True, True, True),
        "validRejectedIncomplete": (True, True, True, True),
        "rejectedIncompleteWithoutUnknown": (True, True, True, False),
        "mixedInconclusive": (True, True, True, True),
        "inconclusiveWithoutUnknown": (True, True, True, False),
    }
    for name, expected in result_cases.items():
        require_boundary(
            name,
            fixtures["results"][name],
            schema=result_schema,
            model=QualificationResultTransport,
            structural_definition="QualificationResultTransport",
            semantic_definition="QualificationResult",
            expected=expected,
        )

    policy_schema = schema_validator("QualificationPolicyTransport")
    policy_cases = {
        "valid": (True, True, True, True),
        "unknownObligationRef": (True, True, True, False),
        "emptyDescription": (False, False, False, False),
    }
    for name, expected in policy_cases.items():
        require_boundary(
            f"policy.{name}",
            fixtures["policies"][name],
            schema=policy_schema,
            model=QualificationPolicyTransport,
            structural_definition="QualificationPolicyTransport",
            semantic_definition="QualificationPolicy",
            expected=expected,
        )


def generated_provenance() -> None:
    provenance = ROOT / "spec/generated/qualification.provenance.json"
    try:
        generated = json.loads(provenance.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read generated transport provenance: {error}")
    if generated.get("role") != "transport-only":
        fail("generated qualification transports must be transport-only")
    if not generated.get("inputs") or not generated.get("outputs") or not generated.get("tools"):
        fail("generated qualification transports must record inputs, outputs, and tools")
    recorded_inputs = {item["path"] for item in generated["inputs"]}
    expected_inputs = expected_provenance_inputs()
    if recorded_inputs != expected_inputs:
        fail(
            "generated provenance input closure mismatch: "
            f"missing={sorted(expected_inputs - recorded_inputs)}, "
            f"unexpected={sorted(recorded_inputs - expected_inputs)}"
        )
    recorded_outputs = {item["path"] for item in generated["outputs"]}
    if recorded_outputs != EXPECTED_PROVENANCE_OUTPUTS:
        fail(
            "generated provenance output closure mismatch: "
            f"missing={sorted(EXPECTED_PROVENANCE_OUTPUTS - recorded_outputs)}, "
            f"unexpected={sorted(recorded_outputs - EXPECTED_PROVENANCE_OUTPUTS)}"
        )
    if provenance.relative_to(ROOT).as_posix() in recorded_outputs:
        fail("generated provenance must not include its own digest")
    for section in ("inputs", "outputs"):
        for item in generated[section]:
            path = ROOT / item["path"]
            if not path.is_file():
                fail(f"generated provenance path does not exist: {item['path']}")
            actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            if item["digest"] != actual:
                fail(f"generated provenance digest mismatch: {item['path']}")


def main() -> None:
    manifest = components()
    roots: dict[str, Path] = {}
    for component_id, item in manifest.items():
        root = ROOT / item["root"]
        if not root.is_dir():
            fail(f"component root does not exist: {component_id}: {item['root']}")
        roots[component_id] = root

    document = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    members = document["tool"]["uv"]["workspace"]["members"]
    for member in members:
        if not (ROOT / member / "pyproject.toml").is_file():
            fail(f"workspace member does not exist: {member}")

    owners: dict[str, str] = {}
    script_owners: dict[str, list[str]] = {}
    for component_id, root in roots.items():
        pyproject = root / "pyproject.toml"
        if not pyproject.is_file() or root == ROOT / "spec":
            continue
        metadata = project(pyproject)
        distribution = metadata["name"].lower().replace("_", "-")
        if distribution in owners:
            fail(f"distribution {distribution!r} has multiple owners")
        owners[distribution] = component_id
        for script in metadata.get("scripts", {}):
            script_owners.setdefault(script, []).append(component_id)

    if script_owners.get("python-ppf") != ["ppf"]:
        fail(f"python-ppf must belong only to PPF: {script_owners.get('python-ppf')}")

    ppf = project(ROOT / "packages/ppf/pyproject.toml")
    ppf_runtime = {dependency_name(item) for item in ppf.get("dependencies", [])}
    if "tdd-agent-skills" in ppf_runtime:
        fail("PPF has a forbidden runtime dependency on TDD")
    if "qualification-workflow" not in ppf_runtime:
        fail("PPF must consume qualification-workflow")
    tdd = project(ROOT / "agents/tdd/pyproject.toml")
    if "qualification-workflow" not in {
        dependency_name(item) for item in tdd.get("dependencies", [])
    }:
        fail("TDD must consume qualification-workflow")

    for layer in LAYERS:
        for path in (ROOT / "spec" / layer).rglob("*.cue"):
            for imported in forbidden_cue_imports(layer, path.read_text(encoding="utf-8")):
                fail(f"forbidden CUE edge: {layer} -> {imported}: {path.relative_to(ROOT)}")

    nested_git = [path for path in ROOT.rglob(".git") if path != ROOT / ".git"]
    if nested_git:
        fail(f"nested .git directories are forbidden: {nested_git}")
    locks = [path for path in ROOT.rglob("uv.lock") if ".venv" not in path.parts]
    if locks != [ROOT / "uv.lock"]:
        fail(f"exactly one root uv.lock is required: {locks}")

    generated_provenance()
    qualification_boundaries()

    print(
        json.dumps(
            {
                "components": sorted(manifest),
                "distributions": owners,
                "status": "pass",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
