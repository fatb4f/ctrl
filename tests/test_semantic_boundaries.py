from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qualification_workflow.generated import QualificationResultTransport

ROOT = Path(__file__).parents[1]


def test_transport_models_do_not_claim_semantic_validity() -> None:
    transport = QualificationResultTransport(
        claims={},
        complete=False,
        verdict="QUALIFIED",
        violations=[],
    )
    assert transport.verdict == "QUALIFIED"
    assert transport.complete is False


def test_generated_transport_provenance_binds_canonical_cue() -> None:
    provenance = json.loads(
        (ROOT / "spec/generated/qualification.provenance.json").read_text(encoding="utf-8")
    )
    source = ROOT / provenance["authoritativeInputs"][0]["path"]
    digest = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
    assert provenance["authoritativeInputs"][0]["digest"] == digest
    assert provenance["role"] == "transport-only"
