from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Never, cast

OID = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_SOURCES = {"kernel-spec", "ppf", "runtime", "tdd-seed", "sdk-feedback"}


def fail(message: str) -> Never:
    raise SystemExit(message)


def verify(manifest_path: Path, *, require_cutover_ready: bool) -> None:
    root = manifest_path.resolve().parents[2]
    data: dict[str, Any] = json.loads(manifest_path.read_text())
    raw_sources = data.get("sources")
    if not isinstance(raw_sources, list) or not all(
        isinstance(source, dict) for source in raw_sources
    ):
        fail("migration manifest has no source list")
    sources = cast(list[dict[str, Any]], raw_sources)
    ids: set[str] = set()
    urls: set[str] = set()
    for source in sources:
        identifier = source.get("id")
        if not isinstance(identifier, str):
            fail("migration manifest contains a source without a string ID")
        ids.add(identifier)
        url = source.get("url")
        if not isinstance(url, str) or url in urls:
            fail(f"invalid or duplicate source URL: {identifier}")
        urls.add(url)
        for key in ("terminalCommit", "terminalTree"):
            if not isinstance(source.get(key), str) or OID.fullmatch(source[key]) is None:
                fail(f"invalid {key}: {identifier}")
        destination = source.get("destinationPath")
        if not isinstance(destination, str) or not (root / destination).exists():
            fail(f"materialized destination is missing: {identifier}: {destination}")
        refs = source.get("refs")
        if not isinstance(refs, dict) or not isinstance(refs.get("heads"), dict):
            fail(f"source refs are missing: {identifier}")
        default_name = source["defaultRef"].removeprefix("refs/heads/")
        if default_name not in refs["heads"]:
            fail(f"default branch tip is missing: {identifier}")
        for namespace in ("heads", "tags"):
            for name, oid in refs.get(namespace, {}).items():
                if not name or not isinstance(oid, str) or OID.fullmatch(oid) is None:
                    fail(f"invalid {namespace} ref: {identifier}: {name}")
        if source.get("license") not in {"MIT", "NOASSERTION"}:
            fail(f"invalid source license declaration: {identifier}")
    if ids != REQUIRED_SOURCES or len(sources) != len(ids):
        fail(f"migration manifest source set is invalid: {sorted(ids)}")

    issue_path = root / data["issues"]["mappingArchive"]
    issue_data = json.loads(issue_path.read_text())
    if not isinstance(issue_data.get("openIssues"), list) or not isinstance(
        issue_data.get("closedIssueArchive"), list
    ):
        fail("issue migration archive is invalid")

    cutover_ready = data.get("cutoverReady") is True
    if require_cutover_ready and not cutover_ready:
        blockers = data.get("blockers", [])
        fail("cutover is not ready:\n- " + "\n- ".join(blockers))
    if cutover_ready:
        if data["rewrite"].get("status") != "complete":
            fail("cutover-ready manifest requires a completed history rewrite")
        for source in sources:
            mapping = source["import"].get("commitMap")
            if not isinstance(mapping, str) or not (root / mapping).is_file():
                fail(f"commit map is missing: {source['id']}")
            if source["freeze"].get("status") != "complete":
                fail(f"freeze is incomplete: {source['id']}")
            if source["validation"].get("status") != "pass":
                fail(f"native validation is incomplete: {source['id']}")

    state = "cutover-ready" if cutover_ready else "prepared; operator blockers recorded"
    print(f"migration manifest: pass ({state})")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("manifest", type=Path)
    verify_parser.add_argument("--require-cutover-ready", action="store_true")
    arguments = parser.parse_args()
    if arguments.command == "verify":
        verify(arguments.manifest, require_cutover_ready=arguments.require_cutover_ready)


if __name__ == "__main__":
    main()
