"""Construct and atomically persist static workflow snapshots."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, sha256_hex
from .derivation import revision_digest


class SnapshotError(ValueError):
    """Raised when snapshot lineage or persistence is invalid."""


def _projection(payload: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {key: payload[key] for key in keys}


def _ledger(payload: dict[str, Any]) -> dict[str, str]:
    return {
        payload["planRevision"]["id"]: revision_digest(
            "plan", [payload["planRevision"], *payload["phases"], *payload["families"]]
        ),
        payload["interimSpecRevision"]["id"]: revision_digest(
            "interim-spec", [payload["interimSpecRevision"], *payload["specSections"]]
        ),
    }


def build_snapshot(
    payload: dict[str, Any], prior: dict[str, Any] | None, bootstrap: bool
) -> dict[str, Any]:
    current_ledger = _ledger(payload)
    if prior is None:
        if not bootstrap:
            raise SnapshotError(
                "no admitted snapshot exists; pass --bootstrap only for first generation"
            )
        ledger = current_ledger
    else:
        prior_ledger = prior.get("payload", {}).get("revisionLedger")
        if not isinstance(prior_ledger, dict):
            raise SnapshotError("admitted snapshot has no revision ledger")
        for identifier, digest in current_ledger.items():
            previous = prior_ledger.get(identifier)
            if previous is not None and previous != digest:
                raise SnapshotError(
                    f"revision {identifier!r} was reused with different canonical content"
                )
        ledger = {**prior_ledger, **current_ledger}
    payload = {**payload, "revisionLedger": ledger}
    semantic_keys = (
        "schema",
        "algorithmVersions",
        "planRevision",
        "phases",
        "families",
        "interimSpecRevision",
        "specSections",
        "obligations",
        "fixtureManifests",
        "probes",
        "realizationSpecs",
    )
    semantic_digest = sha256_hex(canonical_json_bytes(_projection(payload, semantic_keys)))
    full_digest = sha256_hex(canonical_json_bytes(payload))
    return {
        "identity": {"fullDigest": full_digest, "semanticDigest": semantic_digest},
        "payload": payload,
    }


def load_snapshot(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    from .canonical import parse_authoritative_json

    value = parse_authoritative_json(path.read_bytes())
    if not isinstance(value, dict):
        raise SnapshotError("snapshot must be a JSON object")
    return value


def snapshot_bytes(snapshot: dict[str, Any]) -> bytes:
    return canonical_json_bytes(snapshot) + b"\n"


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
