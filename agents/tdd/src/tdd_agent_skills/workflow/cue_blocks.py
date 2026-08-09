"""Isolated CUE validation for extracted records and authored sidecars."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, parse_authoritative_json, sha256_hex
from .markdown import ExtractedBlock

_TYPE_BY_KIND = {
    "plan.revision": "#PlanRevision",
    "plan.phase": "#PlanPhase",
    "plan.family": "#DeliverableFamily",
    "spec.revision": "#InterimSpecRevision",
    "spec.section": "#SpecSection",
}
_FORBIDDEN = re.compile(r"^\s*(?:package\b|import\b|#[_A-Za-z]|_[_A-Za-z]|for\b)", re.MULTILINE)


class CueBlockError(ValueError):
    """Raised for CUE validation or export failures."""


def _run(argv: list[str], cwd: Path) -> bytes:
    environment = {key: value for key, value in os.environ.items() if key in {"PATH", "SYSTEMROOT"}}
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        message = completed.stderr.decode("utf-8", "replace").strip()
        raise CueBlockError(message or f"CUE command failed: {' '.join(argv)}")
    return completed.stdout


def export_block(repository_root: Path, block: ExtractedBlock) -> tuple[dict[str, Any], str]:
    if _FORBIDDEN.search(block.body):
        raise CueBlockError(
            f"{block.kind} at line {block.line_start}: non-record CUE syntax is forbidden"
        )
    cue_type = _TYPE_BY_KIND[block.kind]
    temporary = Path(tempfile.mkdtemp(prefix="workflow-cue-"))
    try:
        wrapper = temporary / "record.cue"
        wrapper.write_text(
            "package extracted\n\n"
            'import planning "github.com/fatb4f/ctrl/agents/tdd/contracts/planning"\n\n'
            f"record: planning.{cue_type} & {{\n{block.body}\n}}\n",
            encoding="utf-8",
        )
        _run(["cue", "vet", "-c", str(wrapper)], repository_root)
        raw = _run(
            ["cue", "export", "-e", "record", "--out", "json", str(wrapper)], repository_root
        )
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    value = parse_authoritative_json(raw)
    if not isinstance(value, dict):
        raise CueBlockError(
            f"{block.kind} at line {block.line_start}: CUE record did not export an object"
        )
    return value, sha256_hex(canonical_json_bytes(value))


def export_expression(repository_root: Path, path: Path, expression: str) -> Any:
    raw = _run(["cue", "export", "-e", expression, "--out", "json", str(path)], repository_root)
    return parse_authoritative_json(raw)
