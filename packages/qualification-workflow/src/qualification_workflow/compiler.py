"""High-level compiler from authored plan inputs to static snapshots."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, sha256_hex
from .cue_blocks import CueBlockError, export_block, export_expression
from .derivation import DerivationError, derive_obligations, validate_graph, validate_linkage
from .fixtures import FixtureError, derive_fixture_manifest
from .markdown import MarkdownPlanError, extract_plan
from .snapshot import SnapshotError, build_snapshot, load_snapshot, snapshot_bytes


class WorkflowCompileError(ValueError):
    """Raised when authored workflow inputs cannot form a static snapshot."""


def _component_root(plan_path: Path) -> Path:
    for parent in (plan_path.parent, *plan_path.parents):
        if (parent / "pyproject.toml").is_file():
            return parent
    raise WorkflowCompileError(f"could not find a component root above {plan_path}")


def _cue_module_root(plan_path: Path) -> Path:
    for parent in (plan_path.parent, *plan_path.parents):
        if (parent / "cue.mod" / "module.cue").is_file():
            return parent
    raise WorkflowCompileError(f"could not find a CUE module root above {plan_path}")


def _sidecar(repository_root: Path, path: Path, expression: str) -> list[dict[str, Any]]:
    value = export_expression(repository_root, path, expression)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise WorkflowCompileError(f"{path}: {expression} must export a list of records")
    return value


def compile_workflow(
    plan_path: Path,
    fixture_specs_path: Path,
    probes_path: Path,
    realization_specs_path: Path,
    output_path: Path | None = None,
    *,
    bootstrap: bool = False,
) -> dict[str, Any]:
    """Compile and validate a static workflow snapshot without executing probes."""
    try:
        plan_path = plan_path.resolve()
        component_root = _component_root(plan_path)
        cue_root = _cue_module_root(plan_path)
        extracted = extract_plan(plan_path)
        records: dict[str, list[dict[str, Any]]] = defaultdict(list)
        record_digests: dict[str, str] = {}
        source_blocks: list[dict[str, Any]] = []
        for block in extracted.blocks:
            record, record_digest = export_block(cue_root, block)
            identifier = record.get("id")
            if not isinstance(identifier, str):
                raise WorkflowCompileError(
                    f"{plan_path}:{block.line_start}: normative records require an id"
                )
            if identifier in record_digests:
                raise WorkflowCompileError(f"duplicate normative record ID {identifier!r}")
            record_digests[identifier] = record_digest
            records[block.kind].append(record)
            source_blocks.append(
                {
                    "kind": block.kind,
                    "lineStart": block.line_start,
                    "lineEnd": block.line_end,
                    "byteStart": block.byte_start,
                    "byteEnd": block.byte_end,
                    "sourceDigest": block.source_digest,
                    "recordDigest": record_digest,
                    "recordID": identifier,
                }
            )
        for kind in ("plan.revision", "plan.phase", "plan.family", "spec.revision", "spec.section"):
            records.setdefault(kind, [])
        validate_graph(records)

        fixture_specs = _sidecar(cue_root, fixture_specs_path.resolve(), "fixtureSpecs")
        probes = _sidecar(cue_root, probes_path.resolve(), "probeSpecs")
        realizations = _sidecar(cue_root, realization_specs_path.resolve(), "realizationSpecs")
        fixture_manifests = [
            derive_fixture_manifest(component_root, fixture) for fixture in fixture_specs
        ]
        obligations = derive_obligations(records, record_digests)
        validate_linkage(obligations, fixture_manifests, probes, realizations)

        relative_path = plan_path.relative_to(component_root).as_posix()
        normative_records: list[dict[str, Any]] = [
            {"kind": kind, "record": record}
            for kind, values in records.items()
            for record in values
        ]

        def normative_sort_key(item: dict[str, Any]) -> tuple[str, str]:
            record = item["record"]
            if not isinstance(record, dict):
                raise WorkflowCompileError("internal error: normative record is not an object")
            identifier = record.get("id")
            if not isinstance(identifier, str):
                raise WorkflowCompileError("internal error: normative record has no ID")
            return str(item["kind"]), identifier

        normative_records.sort(key=normative_sort_key)
        normative_digest = sha256_hex(
            canonical_json_bytes(
                {"schema": "workflow-plan-normative.v0", "records": normative_records}
            )
        )
        payload = {
            "schema": "workflow-snapshot/v0",
            "algorithmVersions": {
                "canonicalJson": "rfc8785-ijson.v0",
                "normativeProjection": "workflow-plan-normative.v0",
                "semanticSnapshot": "workflow-semantic-snapshot.v0",
                "obligationId": "workflow-obligation-id.v0",
                "fixtureTree": "workflow-fixture-tree.v0",
            },
            "planArtifactOccurrence": {
                "path": relative_path,
                "bytesDigest": extracted.bytes_digest,
                "normativeDigest": normative_digest,
            },
            "sourceBlocks": sorted(
                source_blocks, key=lambda value: (value["kind"], value["recordID"])
            ),
            "planRevision": records["plan.revision"][0],
            "phases": sorted(records["plan.phase"], key=lambda value: value["sequence"]),
            "families": sorted(
                records["plan.family"], key=lambda value: (value["phaseID"], value["sequence"])
            ),
            "interimSpecRevision": records["spec.revision"][0],
            "specSections": sorted(
                records["spec.section"], key=lambda value: (value["familyID"], value["sequence"])
            ),
            "obligations": obligations,
            "fixtureManifests": sorted(fixture_manifests, key=lambda value: value["fixtureID"]),
            "probes": sorted(probes, key=lambda value: value["id"]),
            "realizationSpecs": sorted(realizations, key=lambda value: value["id"]),
        }
        prior = load_snapshot(output_path) if output_path is not None else None
        return build_snapshot(payload, prior, bootstrap)
    except (
        CueBlockError,
        DerivationError,
        FixtureError,
        MarkdownPlanError,
        SnapshotError,
    ) as error:
        raise WorkflowCompileError(str(error)) from error


def compiled_bytes(**kwargs: Any) -> bytes:
    return snapshot_bytes(compile_workflow(**kwargs))
