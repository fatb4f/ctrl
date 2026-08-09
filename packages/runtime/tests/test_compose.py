from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest
from conftest import issue_snapshot, slice_document, write_handoff

import runtime_promptgen.compose as compose_module
from runtime_promptgen.compose import compose_prompt
from runtime_promptgen.jsonio import (
    ISSUE_SNAPSHOT_MAX_BYTES,
    SLICE_MANIFEST_MAX_BYTES,
)


def test_compose_validates_and_atomically_publishes(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = write_handoff(tmp_path / "handoff.json", repository)
    slice_value = slice_document()
    monkeypatch.setattr(
        compose_module,
        "_fetch_issue",
        lambda repository, issue, workspace: issue_snapshot(
            json.dumps(slice_value), number=issue
        ),
    )
    output = tmp_path / "nested/prompt.json"
    path = compose_prompt(
        slice_repository="fatb4f/runtime",
        slice_issue=7,
        handoff_path=handoff,
        output_path=output,
    )
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["schema"] == "runtime.prompt.v0"
    assert document["control"]["resolveMutationTargetsBeforeEachWrite"] is True
    assert document["slice"] == slice_value
    assert path.read_bytes().endswith(b"\n")
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_output_collision_fails_before_issue_fetch(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = write_handoff(tmp_path / "handoff.json", repository)

    def unexpected_fetch(*args, **kwargs):
        pytest.fail("issue fetch occurred before output collision rejection")

    monkeypatch.setattr(compose_module, "_fetch_issue", unexpected_fetch)
    with pytest.raises(ValueError, match="cannot replace"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=handoff,
        )


def test_duplicate_handoff_key_is_rejected(
    repository: Path,
    tmp_path: Path,
) -> None:
    handoff = tmp_path / "handoff.json"
    handoff.write_bytes(b'{"schema":"codex.handoff.v0","schema":"codex.handoff.v0"}')
    with pytest.raises(ValueError, match="duplicate key"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=tmp_path / "prompt.json",
        )


def test_duplicate_issue_snapshot_key_is_rejected(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = write_handoff(tmp_path / "handoff.json", repository)
    monkeypatch.setattr(
        compose_module,
        "_fetch_issue",
        lambda *args: b'{"number":7,"number":7}',
    )
    with pytest.raises(ValueError, match="duplicate key"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=tmp_path / "prompt.json",
        )


def test_duplicate_slice_key_is_rejected(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = write_handoff(tmp_path / "handoff.json", repository)
    body = '{"schema":"runtime.slice.v0","schema":"runtime.slice.v0"}'
    monkeypatch.setattr(
        compose_module,
        "_fetch_issue",
        lambda repository, issue, workspace: issue_snapshot(body, number=issue),
    )
    with pytest.raises(ValueError, match="duplicate key"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=tmp_path / "prompt.json",
        )


def test_issue_snapshot_limit_precedes_decode(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = write_handoff(tmp_path / "handoff.json", repository)
    monkeypatch.setattr(
        compose_module,
        "_fetch_issue",
        lambda *args: b" " * (ISSUE_SNAPSHOT_MAX_BYTES + 1),
    )
    with pytest.raises(ValueError, match="snapshot exceeds"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=tmp_path / "prompt.json",
        )


def test_slice_body_limit_precedes_decode(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = write_handoff(tmp_path / "handoff.json", repository)
    body = " " * (SLICE_MANIFEST_MAX_BYTES + 1)
    monkeypatch.setattr(
        compose_module,
        "_fetch_issue",
        lambda repository, issue, workspace: issue_snapshot(body, number=issue),
    )
    with pytest.raises(ValueError, match="slice manifest exceeds"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=tmp_path / "prompt.json",
        )


def test_parent_repository_must_match_slice_repository(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    handoff = write_handoff(tmp_path / "handoff.json", repository)
    body = json.dumps(slice_document(repository="fatb4f/other"))
    monkeypatch.setattr(
        compose_module,
        "_fetch_issue",
        lambda repository, issue, workspace: issue_snapshot(body, number=issue),
    )
    with pytest.raises(ValueError, match="parent repository"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=tmp_path / "prompt.json",
        )


def test_symlink_escape_in_manifest_is_rejected(
    repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (repository / "linked").symlink_to(outside, target_is_directory=True)
    handoff = write_handoff(tmp_path / "handoff.json", repository)
    slice_value = slice_document()
    slice_value["allowedMutationPaths"] = ["linked/file.txt"]
    monkeypatch.setattr(
        compose_module,
        "_fetch_issue",
        lambda repository, issue, workspace: issue_snapshot(
            json.dumps(slice_value), number=issue
        ),
    )
    with pytest.raises(ValueError, match="escapes repository"):
        compose_prompt(
            slice_repository="fatb4f/runtime",
            slice_issue=7,
            handoff_path=handoff,
            output_path=tmp_path / "prompt.json",
        )
