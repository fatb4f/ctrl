from __future__ import annotations

import pytest

from qualification_workflow.canonical import (
    CanonicalizationError,
    canonical_json_bytes,
    parse_authoritative_json,
)
from qualification_workflow.derivation import DerivationError, effective_baseline_policy


def test_authoritative_json_rejects_duplicate_keys_and_floats() -> None:
    with pytest.raises(CanonicalizationError, match="duplicate JSON key"):
        parse_authoritative_json(b'{"a": 1, "a": 2}')
    with pytest.raises(CanonicalizationError, match="floating-point"):
        parse_authoritative_json(b'{"a": 1.5}')


def test_canonical_json_sorts_object_keys() -> None:
    assert canonical_json_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}'


def test_baseline_policy_defaults_and_modify_requirement() -> None:
    assert effective_baseline_policy({"changeIntent": "introduce"}) == "must-fail"
    assert effective_baseline_policy({"changeIntent": "preserve"}) == "must-pass"
    with pytest.raises(DerivationError, match="requires an explicit"):
        effective_baseline_policy({"changeIntent": "modify"})
