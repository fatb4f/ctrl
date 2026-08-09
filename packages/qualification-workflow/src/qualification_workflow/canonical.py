"""Strict JSON and deterministic hashing for workflow identities."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

SAFE_INTEGER_MIN = -(2**53) + 1
SAFE_INTEGER_MAX = (2**53) - 1


class CanonicalizationError(ValueError):
    """Raised when a value cannot participate in an authoritative digest."""


def _reject_constant(value: str) -> None:
    raise CanonicalizationError(f"non-finite JSON number is not allowed: {value}")


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalizationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def parse_authoritative_json(data: bytes) -> Any:
    """Parse JSON while preserving duplicate-key and I-JSON failures."""
    try:
        text = data.decode("utf-8", "strict")
        value = json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_constant=_reject_constant,
            parse_float=lambda value: (_ for _ in ()).throw(
                CanonicalizationError(f"floating-point JSON number is not allowed: {value}")
            ),
        )
    except UnicodeDecodeError as error:
        raise CanonicalizationError("JSON input is not UTF-8") from error
    except json.JSONDecodeError as error:
        raise CanonicalizationError(f"invalid JSON: {error.msg}") from error
    validate_json_value(value)
    return value


def validate_json_value(value: Any) -> None:
    """Reject values outside the project-owned I-JSON subset."""
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        if not SAFE_INTEGER_MIN <= value <= SAFE_INTEGER_MAX:
            raise CanonicalizationError("integer is outside the I-JSON safe range")
        return
    if isinstance(value, float):
        raise CanonicalizationError("floating-point values are not allowed")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError("JSON object keys must be strings")
            validate_json_value(item)
        return
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        for item in value:
            validate_json_value(item)
        return
    raise CanonicalizationError(f"unsupported authoritative value: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize the supported I-JSON subset deterministically.

    Floats are prohibited, so CPython's JSON string and integer encoding is sufficient for the
    RFC 8785 subset used by this project.
    """
    validate_json_value(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def domain_digest(domain: str, payload: bytes) -> str:
    return sha256_hex(domain.encode("utf-8") + b"\0" + payload)
