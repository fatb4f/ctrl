from __future__ import annotations

import os
import re
import sys
from collections.abc import Sequence
from pathlib import Path

from cyclopts import App
from cyclopts.exceptions import CycloptsError
from pydantic import ValidationError

from .compose import compose_prompt
from .contracts import ContractDriftError

_REPOSITORY = re.compile(r"^[^/\s]+/[^/\s]+$")
_SESSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,255}$")

app = App(
    help="Compose one validated runtime.prompt.v0 document",
    exit_on_error=False,
    print_error=False,
    result_action=lambda result: result,
)


@app.default
def promptgen(
    *,
    slice_repo: str,
    slice_issue: int,
    handoff_session: str | None = None,
    handoff_file: Path | None = None,
    handoff_root: Path | None = None,
    output: Path = Path("prompt.json"),
) -> None:
    """Bind a GitHub slice manifest to trusted prior-session evidence."""
    if _REPOSITORY.fullmatch(slice_repo) is None:
        raise ValueError("--slice-repo must use OWNER/REPO form")
    if slice_issue < 1:
        raise ValueError("--slice-issue must be a positive integer")
    if (handoff_session is None) == (handoff_file is None):
        raise ValueError("exactly one of --handoff-session or --handoff-file is required")
    if handoff_session is not None:
        if _SESSION.fullmatch(handoff_session) is None:
            raise ValueError("--handoff-session is invalid")
        root = handoff_root
        if root is None:
            state = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
            root = state / "handoff"
        handoff_file = root / handoff_session / "handoff.json"
    assert handoff_file is not None
    path = compose_prompt(
        slice_repository=slice_repo,
        slice_issue=slice_issue,
        handoff_path=handoff_file,
        output_path=output,
    )
    print(path)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        app(list(argv) if argv is not None else None)
    except (
        ContractDriftError,
        CycloptsError,
        OSError,
        ValidationError,
        ValueError,
    ) as error:
        print(f"promptgen failed: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
