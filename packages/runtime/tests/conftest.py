from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repository,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test")
    (root / "tracked.txt").write_text("one\n", encoding="utf-8")
    git(root, "add", "tracked.txt")
    git(root, "commit", "-qm", "initial")
    return root


def handoff_document(repository: Path) -> dict:
    oid = git(repository, "rev-parse", "HEAD")
    return {
        "schema": "codex.handoff.v0",
        "createdAt": "2026-07-29T19:00:00Z",
        "repository": {
            "root": str(repository),
            "head": oid,
            "branch": "main",
            "upstream": None,
            "ahead": None,
            "behind": None,
            "indexTree": oid,
            "staged": [],
            "numstat": [],
        },
        "session": {
            "rollout": "/tmp/rollout.jsonl",
            "sessionId": "session-1",
            "firstEvent": 0,
            "lastEvent": 0,
        },
        "objective": None,
        "completed": [],
        "currentOperation": None,
        "nextOperation": None,
        "completionCriteria": [],
        "operations": [],
        "validation": [],
        "failures": [],
        "openQuestions": [],
        "diagnostics": [],
    }


def write_handoff(path: Path, repository: Path) -> Path:
    path.write_text(json.dumps(handoff_document(repository)), encoding="utf-8")
    return path


def slice_document(*, repository: str = "fatb4f/runtime") -> dict:
    return {
        "schema": "runtime.slice.v0",
        "sliceID": "slice-1",
        "parent": {"repository": repository, "issue": 1},
        "predecessor": None,
        "next": None,
        "objective": "Implement the slice",
        "inputs": [],
        "allowedMutationPaths": ["src/"],
        "forbiddenMutationPaths": [".git/"],
        "focusedValidation": [{"kind": "argv", "argv": ["pytest", "-q"]}],
        "closureValidation": [],
        "completionCriteria": ["Tests pass"],
        "nonGoals": [],
    }


def issue_snapshot(body: str, *, number: int = 7) -> bytes:
    return json.dumps(
        {
            "number": number,
            "title": "Slice",
            "body": body,
            "state": "OPEN",
            "url": f"https://github.com/fatb4f/runtime/issues/{number}",
            "updatedAt": "2026-07-29T19:00:00Z",
        },
        separators=(",", ":"),
    ).encode("utf-8")
