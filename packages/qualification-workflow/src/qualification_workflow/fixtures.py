"""Derive fixture manifests from declared fixture roots."""

from __future__ import annotations

import os
import stat
import unicodedata
from pathlib import Path
from typing import Any

from .canonical import sha256_hex


class FixtureError(ValueError):
    """Raised when fixture bytes cannot be admitted."""


def _file_digest(path: Path) -> tuple[str, int]:
    digest = __import__("hashlib").sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def _entry_bytes(entry: dict[str, Any]) -> bytes:
    return (
        entry["path"].encode("utf-8")
        + b"\0"
        + entry["mode"].encode("ascii")
        + b"\0"
        + str(entry["byteLength"]).encode("ascii")
        + b"\0"
        + entry["fileDigest"].encode("ascii")
        + b"\0"
    )


def derive_fixture_manifest(repository_root: Path, fixture_spec: dict[str, Any]) -> dict[str, Any]:
    fixture_id = fixture_spec["id"]
    root = repository_root / "fixtures" / "data" / fixture_id
    if not root.is_dir():
        raise FixtureError(f"fixture {fixture_id!r} root does not exist: {root}")

    entries: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in list(dirnames):
            candidate = directory_path / name
            if candidate.is_symlink():
                raise FixtureError(f"fixture {fixture_id!r} contains symlink directory {candidate}")
        for name in filenames:
            candidate = directory_path / name
            metadata = candidate.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                raise FixtureError(f"fixture {fixture_id!r} contains symlink {candidate}")
            if not stat.S_ISREG(metadata.st_mode):
                raise FixtureError(f"fixture {fixture_id!r} contains non-regular file {candidate}")
            relative = candidate.relative_to(root).as_posix()
            normalized = unicodedata.normalize("NFC", relative)
            if (
                relative != normalized
                or "\\" in relative
                or any(part in {"", ".", ".."} for part in relative.split("/"))
            ):
                raise FixtureError(f"fixture {fixture_id!r} has non-canonical path {relative!r}")
            if relative in seen_paths:
                raise FixtureError(f"fixture {fixture_id!r} has duplicate path {relative!r}")
            seen_paths.add(relative)
            executable = bool(metadata.st_mode & 0o111)
            other_bits = stat.S_IMODE(metadata.st_mode) & ~0o755
            if other_bits:
                raise FixtureError(
                    f"fixture {fixture_id!r} has unsupported permissions on {relative!r}"
                )
            mode = "100755" if executable else "100644"
            file_digest, size = _file_digest(candidate)
            entries.append(
                {
                    "path": relative,
                    "mode": mode,
                    "byteLength": size,
                    "fileDigest": file_digest,
                }
            )

    entries.sort(key=lambda entry: entry["path"].encode("utf-8"))
    payload = b"workflow-fixture-tree.v0\0" + b"".join(_entry_bytes(entry) for entry in entries)
    return {"fixtureID": fixture_id, "entries": entries, "treeDigest": sha256_hex(payload)}
