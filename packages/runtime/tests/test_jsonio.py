from __future__ import annotations

import pytest
from runtime_promptgen.jsonio import decode_object


@pytest.mark.parametrize(
    "data,key",
    [
        (b'{"a":1,"a":2}', "a"),
        (b'{"outer":{"a":1,"a":2}}', "a"),
    ],
)
def test_duplicate_keys_are_rejected_at_every_depth(data: bytes, key: str) -> None:
    with pytest.raises(ValueError, match=f"duplicate key '{key}'"):
        decode_object(data, label="input")


def test_multiple_documents_are_rejected() -> None:
    with pytest.raises(ValueError, match="exactly one JSON document"):
        decode_object(b"{} {}", label="input")


def test_non_object_root_is_rejected() -> None:
    with pytest.raises(ValueError, match="must be a JSON object"):
        decode_object(b"[]", label="input")


def test_invalid_utf8_is_rejected() -> None:
    with pytest.raises(ValueError, match="UTF-8"):
        decode_object(b'{"value":"\xff"}', label="input")
