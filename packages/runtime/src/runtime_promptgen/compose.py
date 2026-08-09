from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated, Any, Literal

from handoff import Handoff
from handoff.model import HANDOFF_MAX_BYTES
from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    StrictInt,
    StrictStr,
)

from .contracts import validate_prompt, validate_slice
from .jsonio import (
    ISSUE_SNAPSHOT_MAX_BYTES,
    SLICE_MANIFEST_MAX_BYTES,
    decode_object,
    read_bounded,
)
from .paths import (
    resolve_input_and_output,
    resolve_repository_root,
    validate_mutation_paths,
)


class IssueSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    number: Annotated[StrictInt, Field(ge=1)]
    title: StrictStr
    body: StrictStr
    state: Literal["OPEN"]
    url: HttpUrl
    updatedAt: AwareDatetime


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fetch_issue(repository: str, issue: int, workspace: Path) -> bytes:
    snapshot = workspace / "issue.json"
    stderr = workspace / "gh.stderr"
    with snapshot.open("wb") as stdout, stderr.open("wb") as error_output:
        try:
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "view",
                    str(issue),
                    "--repo",
                    repository,
                    "--json",
                    "number,title,body,state,url,updatedAt",
                ],
                stdout=stdout,
                stderr=error_output,
                check=False,
            )
        except FileNotFoundError as error:
            raise ValueError("gh is required") from error
    if result.returncode != 0:
        detail = read_bounded(stderr, limit=8192, label="gh stderr").decode(
            "utf-8", errors="replace"
        )
        raise ValueError(f"failed to acquire slice issue {repository}#{issue}: {detail.strip()}")
    return read_bounded(
        snapshot,
        limit=ISSUE_SNAPSHOT_MAX_BYTES,
        label="GitHub issue snapshot",
    )


def _publish(path: Path, data: bytes, *, protected_source: Path) -> None:
    _, resolved_path = resolve_input_and_output(protected_source, path)
    if resolved_path != path:
        raise ValueError("--output path changed during prompt composition")
    directory = path.parent
    directory.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".prompt.", dir=directory)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        os.chmod(path, 0o600)
        directory_descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary.unlink(missing_ok=True)
        raise


def compose_prompt(
    *,
    slice_repository: str,
    slice_issue: int,
    handoff_path: Path,
    output_path: Path,
) -> Path:
    source, destination = resolve_input_and_output(handoff_path, output_path)
    handoff_data = read_bounded(
        source,
        limit=HANDOFF_MAX_BYTES,
        label="handoff",
    )
    decode_object(handoff_data, label="handoff")
    handoff = Handoff.model_validate_json(handoff_data)
    repository_root = resolve_repository_root(handoff.repository.root)

    with tempfile.TemporaryDirectory(prefix="promptgen.") as temporary:
        issue_data = _fetch_issue(
            slice_repository,
            slice_issue,
            Path(temporary),
        )
    if len(issue_data) > ISSUE_SNAPSHOT_MAX_BYTES:
        raise ValueError(f"GitHub issue snapshot exceeds {ISSUE_SNAPSHOT_MAX_BYTES} bytes")
    issue_document = decode_object(issue_data, label="GitHub issue snapshot")
    issue = IssueSnapshot.model_validate(issue_document)
    if issue.number != slice_issue:
        raise ValueError(
            f"slice issue number mismatch: expected {slice_issue}, observed {issue.number}"
        )

    slice_data = issue.body.encode("utf-8")
    if len(slice_data) > SLICE_MANIFEST_MAX_BYTES:
        raise ValueError(f"slice manifest exceeds {SLICE_MANIFEST_MAX_BYTES} bytes")
    slice_document = decode_object(slice_data, label="slice manifest")
    slice_projection = validate_slice(slice_document)
    if slice_projection.parent.repository != slice_repository:
        raise ValueError("slice parent repository must equal the repository containing the slice")
    validate_mutation_paths(
        repository_root,
        [
            *slice_document["allowedMutationPaths"],
            *slice_document["forbiddenMutationPaths"],
        ],
    )

    prompt: dict[str, Any] = {
        "schema": "runtime.prompt.v0",
        "sources": {
            "handoff": {
                "sessionID": handoff.session.session_id,
                "path": str(source),
                "sha256": _sha256(handoff_data),
            },
            "slice": {
                "repository": slice_repository,
                "issue": issue.number,
                "url": str(issue.url),
                "updatedAt": issue.updatedAt.isoformat().replace("+00:00", "Z"),
                "bodySha256": _sha256(slice_data),
            },
        },
        "handoff": handoff.model_dump(mode="json", by_alias=True, exclude_none=False),
        "slice": slice_document,
        "control": {
            "executeOnlyDeclaredSlice": True,
            "respectMutationBoundaries": True,
            "resolveMutationTargetsBeforeEachWrite": True,
            "runDeclaredValidation": True,
            "treatHandoffAsPriorSessionEvidence": True,
            "doNotMutateGitHubIssues": True,
            "produceHandoffBeforeContinuing": True,
        },
    }
    validate_prompt(prompt)
    data = (
        json.dumps(prompt, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    _publish(destination, data, protected_source=source)
    return destination
