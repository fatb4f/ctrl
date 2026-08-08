from __future__ import annotations

import json
from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis_jsonschema import from_schema
from runtime_promptgen.contracts import (
    SLICE_SCHEMA,
    SliceManifestProjection,
    validate_prompt,
    validate_slice,
)


def test_every_valid_fixture_projects_through_pydantic() -> None:
    fixtures = sorted((Path(__file__).parent / "fixtures/slices/valid").glob("*.json"))
    assert fixtures
    for fixture in fixtures:
        document = json.loads(fixture.read_text(encoding="utf-8"))
        assert isinstance(validate_slice(document), SliceManifestProjection)


@settings(
    max_examples=25,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
@given(from_schema(SLICE_SCHEMA))
def test_schema_valid_samples_project_through_pydantic(document: dict) -> None:
    assert isinstance(validate_slice(document), SliceManifestProjection)


@pytest.mark.parametrize(
    "path",
    [
        "/etc/passwd",
        "../../etc",
        "src/../etc",
        "src//file",
        ".",
    ],
)
def test_schema_rejects_unsafe_mutation_paths(path: str) -> None:
    fixture = Path(__file__).parent / "fixtures/slices/valid/minimal.json"
    document = json.loads(fixture.read_text(encoding="utf-8"))
    document["allowedMutationPaths"] = [path]
    with pytest.raises(ValueError, match="violates its schema"):
        validate_slice(document)


def test_prompt_schema_is_closed() -> None:
    with pytest.raises(ValueError, match="violates its schema"):
        validate_prompt({"schema": "runtime.prompt.v0", "unknown": True})
