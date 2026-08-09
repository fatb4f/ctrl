from __future__ import annotations

import os
from pathlib import Path

import pytest

from runtime_promptgen.paths import (
    resolve_input_and_output,
    resolve_mutation_target,
    resolve_repository_root,
)


def test_symlink_escape_is_rejected(repository: Path, tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (repository / "linked").symlink_to(outside, target_is_directory=True)
    root = resolve_repository_root(repository)
    with pytest.raises(ValueError, match="escapes repository"):
        resolve_mutation_target(root, "linked/file.txt")


def test_in_repository_symlink_is_allowed(repository: Path) -> None:
    target = repository / "target"
    target.mkdir()
    (repository / "linked").symlink_to(target, target_is_directory=True)
    root = resolve_repository_root(repository)
    assert resolve_mutation_target(root, "linked/file.txt") == target / "file.txt"


def test_output_symlink_alias_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "handoff.json"
    source.write_text("{}", encoding="utf-8")
    output = tmp_path / "prompt.json"
    output.symlink_to(source)
    with pytest.raises(ValueError, match="cannot replace"):
        resolve_input_and_output(source, output)


def test_output_hardlink_alias_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "handoff.json"
    source.write_text("{}", encoding="utf-8")
    output = tmp_path / "prompt.json"
    os.link(source, output)
    with pytest.raises(ValueError, match="cannot alias"):
        resolve_input_and_output(source, output)
