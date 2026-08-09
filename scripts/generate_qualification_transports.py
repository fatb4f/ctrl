from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "spec/qualification/kernel.cue"
SCHEMA = ROOT / "spec/generated/qualification.schema.json"
PROVENANCE = ROOT / "spec/generated/qualification.provenance.json"
PYDANTIC = (
    ROOT / "packages/qualification-workflow/src/qualification_workflow/generated/qualification.py"
)


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def outputs() -> dict[Path, bytes]:
    source_digest = "sha256:" + hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/fatb4f/ctrl/spec/generated/qualification.schema.json",
        "$comment": (
            "Transport structure only. Canonical CUE evaluates applicability, references, "
            "relations, verdicts, and promotion predicates."
        ),
        "title": "Qualification transport",
        "type": "object",
        "additionalProperties": False,
        "required": ["claims", "complete", "verdict", "violations"],
        "properties": {
            "claims": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/claimAdmission"},
            },
            "complete": {"type": "boolean"},
            "verdict": {"enum": ["QUALIFIED", "INCONCLUSIVE", "REJECTED"]},
            "violations": {"type": "array", "items": {"type": "string"}},
        },
        "$defs": {
            "claimAdmission": {
                "type": "object",
                "additionalProperties": False,
                "required": ["claimID", "observationID", "status", "reason"],
                "properties": {
                    "claimID": {"type": "string"},
                    "observationID": {"type": "string"},
                    "status": {"enum": ["SATISFIED", "VIOLATED", "UNKNOWN"]},
                    "reason": {"type": "string"},
                },
            }
        },
    }
    provenance = {
        "artifactPaths": [
            "spec/generated/qualification.schema.json",
            "packages/qualification-workflow/src/qualification_workflow/generated/qualification.py",
        ],
        "authoritativeInputs": [
            {
                "digest": source_digest,
                "path": "spec/qualification/kernel.cue",
            }
        ],
        "generator": "scripts/generate_qualification_transports.py",
        "role": "transport-only",
    }
    model = dedent(
        f'''\
        """Generated structural transports; canonical CUE owns semantic validity."""

        from typing import Literal

        from pydantic import BaseModel, ConfigDict

        AUTHORITATIVE_INPUT = "spec/qualification/kernel.cue"
        AUTHORITATIVE_INPUT_DIGEST = (
            "{source_digest}"
        )


        class ClaimAdmissionTransport(BaseModel):
            """Representable claim-admission structure without semantic evaluation."""

            model_config = ConfigDict(extra="forbid")

            claimID: str
            observationID: str
            status: Literal["SATISFIED", "VIOLATED", "UNKNOWN"]
            reason: str


        class QualificationResultTransport(BaseModel):
            """Representable result structure without CUE cross-record predicates."""

            model_config = ConfigDict(extra="forbid")

            claims: dict[str, ClaimAdmissionTransport]
            complete: bool
            verdict: Literal["QUALIFIED", "INCONCLUSIVE", "REJECTED"]
            violations: list[str]
        '''
    ).encode()
    return {SCHEMA: json_bytes(schema), PROVENANCE: json_bytes(provenance), PYDANTIC: model}


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
    rendered = outputs()
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
