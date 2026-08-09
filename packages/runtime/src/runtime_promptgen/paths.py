from __future__ import annotations

import os
import subprocess
from collections.abc import Iterable
from pathlib import Path


def resolve_repository_root(value: str | Path) -> Path:
    root = Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"handoff repository root is not a directory: {root}")
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(f"handoff repository root is not a Git repository: {root}")
    try:
        observed = Path(result.stdout.decode("utf-8").strip()).resolve(strict=True)
    except (UnicodeDecodeError, OSError) as error:
        raise ValueError("cannot resolve the Git repository root") from error
    if observed != root:
        raise ValueError(
            f"handoff repository root is not canonical: expected {root}, observed {observed}"
        )
    return root


def resolve_mutation_target(repository_root: Path, declared_path: str) -> Path:
    target = (repository_root / declared_path.rstrip("/")).resolve(strict=False)
    try:
        target.relative_to(repository_root)
    except ValueError as error:
        raise ValueError(
            f"mutation path escapes repository through symlinks: {declared_path}"
        ) from error
    return target


def validate_mutation_paths(
    repository_root: Path,
    declared_paths: Iterable[str],
) -> None:
    for declared_path in declared_paths:
        resolve_mutation_target(repository_root, declared_path)


def resolve_input_and_output(input_path: Path, output_path: Path) -> tuple[Path, Path]:
    source = input_path.expanduser().resolve(strict=True)
    destination = output_path.expanduser().resolve(strict=False)
    if source == destination:
        raise ValueError("--output cannot replace the input handoff")
    if destination.exists() and os.path.samefile(source, destination):
        raise ValueError("--output cannot alias the input handoff")
    return source, destination
