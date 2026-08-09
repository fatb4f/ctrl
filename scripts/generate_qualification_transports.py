from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCHEMA = ROOT / "spec/generated/qualification.schema.json"
PROVENANCE = ROOT / "spec/generated/qualification.provenance.json"
PYDANTIC = (
    ROOT / "packages/qualification-workflow/src/qualification_workflow/generated/qualification.py"
)

PINNED_CUE_VERSION = "v0.18.0-0.dev.0.20260713132914-0c547ba896a5"
PINNED_DATAMODEL_CODEGEN_VERSION = "0.71.0"

CUE_ARGV = [
    "cue",
    "def",
    "./spec/qualification/generate",
    "--out",
    "jsonschema",
    "-e",
    "#QualificationTransportBundle",
]
CODEGEN_ARGV = [
    "datamodel-codegen",
    "--input",
    "spec/generated/qualification.schema.json",
    "--input-file-type",
    "jsonschema",
    "--output",
    "packages/qualification-workflow/src/qualification_workflow/generated/qualification.py",
    "--output-model-type",
    "pydantic_v2.BaseModel",
    "--target-python-version",
    "3.14",
    "--strict-nullable",
    "--use-standard-collections",
    "--use-union-operator",
    "--use-default-kwarg",
    "--enum-field-as-literal",
    "all",
    "--collapse-root-models",
    "--extra-fields",
    "forbid",
    "--disable-timestamp",
    "--formatters",
    "builtin",
    "--class-name",
    "QualificationTransportBundle",
]


def digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def generation_inputs() -> list[Path]:
    paths = [ROOT / "cue.mod/module.cue"]
    for directory in (
        ROOT / "spec/core",
        ROOT / "spec/repository",
        ROOT / "spec/qualification",
        ROOT / "spec/qualification/generate",
    ):
        paths.extend(sorted(directory.glob("*.cue")))
    return sorted(set(paths))


def command_version(argv: list[str]) -> str:
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.splitlines()[0].strip()


def tool_environment() -> tuple[dict[str, str], str, str, str]:
    environment = os.environ.copy()
    cue_binary = environment.get("CTRL_CUE_BIN", "cue")
    cue_version = command_version([cue_binary, "version"])
    expected_cue = f"cue version {PINNED_CUE_VERSION}"
    if cue_version != expected_cue:
        raise SystemExit(f"expected {expected_cue!r}, got {cue_version!r}")

    codegen_version = command_version(["datamodel-codegen", "--version"])
    expected_codegen = f"datamodel-codegen {PINNED_DATAMODEL_CODEGEN_VERSION}"
    if codegen_version != expected_codegen:
        raise SystemExit(f"expected {expected_codegen!r}, got {codegen_version!r}")
    return environment, cue_binary, cue_version, codegen_version


def render() -> dict[Path, bytes]:
    environment, cue_binary, cue_version, codegen_version = tool_environment()
    cue_command = [cue_binary, *CUE_ARGV[1:]]
    exported = subprocess.run(
        cue_command,
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    schema = json_bytes(json.loads(exported.stdout))

    with tempfile.TemporaryDirectory(prefix="qualification-transports-") as directory:
        temporary_root = Path(directory)
        temporary_schema = temporary_root / SCHEMA.relative_to(ROOT)
        temporary_python = temporary_root / PYDANTIC.relative_to(ROOT)
        temporary_schema.parent.mkdir(parents=True, exist_ok=True)
        temporary_python.parent.mkdir(parents=True, exist_ok=True)
        temporary_schema.write_bytes(schema)
        subprocess.run(CODEGEN_ARGV, cwd=temporary_root, env=environment, check=True)
        python = temporary_python.read_bytes()
        public_bundle = b"class QualificationTransportBundle(BaseModel):"
        private_bundle = b"class _QualificationTransportBundle(BaseModel):"
        if python.count(public_bundle) != 1:
            raise SystemExit("generated Python did not contain the expected bundle root")
        python = python.replace(public_bundle, private_bundle)

    inputs = [
        {
            "digest": digest(path.read_bytes()),
            "path": path.relative_to(ROOT).as_posix(),
        }
        for path in generation_inputs()
    ]
    outputs = [
        {"digest": digest(schema), "path": SCHEMA.relative_to(ROOT).as_posix()},
        {"digest": digest(python), "path": PYDANTIC.relative_to(ROOT).as_posix()},
    ]
    provenance = {
        "inputs": inputs,
        "outputs": outputs,
        "role": "transport-only",
        "tools": {
            "cue": {
                "argv": CUE_ARGV,
                "version": cue_version.removeprefix("cue version "),
            },
            "datamodel-code-generator": {
                "argv": CODEGEN_ARGV,
                "version": codegen_version.removeprefix("datamodel-codegen "),
            },
        },
    }
    return {SCHEMA: schema, PYDANTIC: python, PROVENANCE: json_bytes(provenance)}


def write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        Path(temporary).replace(path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    rendered = render()
    if arguments.check:
        stale = [
            path.relative_to(ROOT)
            for path, content in rendered.items()
            if not path.is_file() or path.read_bytes() != content
        ]
        if stale:
            raise SystemExit(f"generated qualification transports are stale: {stale}")
        return
    for path, content in rendered.items():
        write_atomic(path, content)


if __name__ == "__main__":
    main()
