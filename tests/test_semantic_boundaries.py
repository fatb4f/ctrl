from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError
from qualification_workflow.generated import (
    QualificationPolicyTransport,
    QualificationResultTransport,
)

ROOT = Path(__file__).parents[1]
FIXTURES = json.loads(
    (ROOT / "spec/tests/qualification-transport-fixtures.json").read_text(encoding="utf-8")
)


def test_transport_models_do_not_claim_semantic_validity() -> None:
    transport = QualificationResultTransport.model_validate(
        FIXTURES["results"]["unknownQualified"], strict=True
    )
    assert transport.verdict == "QUALIFIED"
    assert transport.complete is True

    policy = QualificationPolicyTransport.model_validate(
        FIXTURES["policies"]["unknownObligationRef"], strict=True
    )
    assert policy.applicability.obligationRefs == ["missing-obligation"]


@pytest.mark.parametrize(
    "fixture",
    [
        "missingRepository",
        "missingClaims",
        "missingViolations",
        "componentsList",
        "componentRootNotString",
        "emptyComponentRoot",
        "emptyReason",
        "stringComplete",
        "unknownField",
    ],
)
def test_transport_models_enforce_strict_structure(fixture: str) -> None:
    with pytest.raises(ValidationError):
        QualificationResultTransport.model_validate(FIXTURES["results"][fixture], strict=True)


def test_transport_models_preserve_non_empty_evidence_descriptions() -> None:
    with pytest.raises(ValidationError):
        QualificationPolicyTransport.model_validate(
            FIXTURES["policies"]["emptyDescription"], strict=True
        )


def test_generated_transport_provenance_is_complete_and_non_self_referential() -> None:
    provenance_path = ROOT / "spec/generated/qualification.provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))

    assert provenance["role"] == "transport-only"
    assert provenance["tools"]["cue"]["version"]
    assert provenance["tools"]["datamodel-code-generator"]["version"] == "0.71.0"
    assert "cue.mod/module.cue" in {item["path"] for item in provenance["inputs"]}
    assert provenance_path.relative_to(ROOT).as_posix() not in {
        item["path"] for item in provenance["outputs"]
    }
    for section in ("inputs", "outputs"):
        for item in provenance[section]:
            content = (ROOT / item["path"]).read_bytes()
            assert item["digest"] == "sha256:" + hashlib.sha256(content).hexdigest()


def test_generated_check_mode_does_not_rewrite_outputs() -> None:
    outputs = [
        ROOT / "spec/generated/qualification.schema.json",
        ROOT
        / "packages/qualification-workflow/src/qualification_workflow/generated/qualification.py",
        ROOT / "spec/generated/qualification.provenance.json",
    ]
    before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in outputs}
    subprocess.run(
        [sys.executable, "scripts/generate_qualification_transports.py", "--check"],
        cwd=ROOT,
        check=True,
    )
    after = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in outputs}
    assert after == before
