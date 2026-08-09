"""Extraction of normative CUE records from Markdown source occurrences."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from markdown_it import MarkdownIt

from .canonical import sha256_hex

_INFO = re.compile(
    r"^cue (plan\.revision|plan\.phase|plan\.family|spec\.revision|spec\.section)[ \t]*$"
)
_CUE_PREFIX = re.compile(r"^cue(?:[ \t].*)?$")


class MarkdownPlanError(ValueError):
    """Raised when a Markdown plan has invalid normative block structure."""


@dataclass(frozen=True)
class ExtractedBlock:
    kind: str
    body: str
    line_start: int
    line_end: int
    byte_start: int
    byte_end: int
    source_digest: str


@dataclass(frozen=True)
class ExtractedPlan:
    path: Path
    data: bytes
    blocks: tuple[ExtractedBlock, ...]

    @property
    def bytes_digest(self) -> str:
        return sha256_hex(self.data)


def _line_offsets(data: bytes) -> list[int]:
    offsets = [0]
    for index, byte in enumerate(data):
        if byte == 10:
            offsets.append(index + 1)
    return offsets


def _line_end_offset(data: bytes, offsets: list[int], end_line_exclusive: int) -> int:
    if end_line_exclusive < len(offsets):
        return offsets[end_line_exclusive]
    return len(data)


def extract_plan(path: Path) -> ExtractedPlan:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise MarkdownPlanError(f"{path}: Markdown must be UTF-8") from error

    offsets = _line_offsets(data)
    parser = MarkdownIt("commonmark")
    blocks: list[ExtractedBlock] = []
    for token in parser.parse(text):
        if token.type != "fence":
            continue
        info = token.info
        match = _INFO.fullmatch(info)
        if match is None:
            if _CUE_PREFIX.fullmatch(info):
                raise MarkdownPlanError(f"{path}: unsupported normative block type {info!r}")
            continue
        if token.map is None:
            raise MarkdownPlanError(f"{path}: parser did not provide fence location")
        start_line, end_line = token.map
        byte_start = offsets[start_line]
        byte_end = _line_end_offset(data, offsets, end_line)
        source = data[byte_start:byte_end]
        if not source:
            raise MarkdownPlanError(f"{path}: empty fenced source at line {start_line + 1}")
        blocks.append(
            ExtractedBlock(
                kind=match.group(1),
                body=token.content,
                line_start=start_line + 1,
                line_end=end_line,
                byte_start=byte_start,
                byte_end=byte_end,
                source_digest=sha256_hex(source),
            )
        )
    return ExtractedPlan(path=path, data=data, blocks=tuple(blocks))
