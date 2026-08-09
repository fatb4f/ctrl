from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ISSUE_SNAPSHOT_MAX_BYTES = 2 * 1024 * 1024
SLICE_MANIFEST_MAX_BYTES = 1024 * 1024


def read_bounded(path: Path, *, limit: int, label: str) -> bytes:
    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"{label} exceeds {limit} bytes")
    return data


def decode_object(data: bytes, *, label: str) -> dict[str, Any]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{label} is not valid UTF-8") from error

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{label} is not exactly one JSON document: {error.msg}"
        ) from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")  # noqa: TRY004
    return value
