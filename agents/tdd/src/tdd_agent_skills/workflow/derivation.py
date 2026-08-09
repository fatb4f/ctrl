"""Pure derivation and linkage for static workflow records."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .canonical import canonical_json_bytes, sha256_hex


class DerivationError(ValueError):
    """Raised for invalid authored graph relationships."""


def _id_payload(*values: str) -> bytes:
    chunks = [b"workflow-obligation-id.v0\0"]
    for value in values:
        encoded = value.encode("utf-8")
        chunks.extend((str(len(encoded)).encode("ascii"), b"\0", encoded))
    return b"".join(chunks)


def obligation_id(spec_revision_id: str, section_id: str, source_type: str, source_id: str) -> str:
    return "obligation.h" + sha256_hex(
        _id_payload(spec_revision_id, section_id, source_type, source_id)
    )


def effective_baseline_policy(source: dict[str, Any]) -> str:
    intent = source["changeIntent"]
    policy = source.get("baselinePolicy")
    if policy is None:
        if intent == "introduce":
            return "must-fail"
        if intent == "preserve":
            return "must-pass"
        raise DerivationError("modify source element requires an explicit baselinePolicy")
    default = {"introduce": "must-fail", "preserve": "must-pass"}.get(intent)
    if (
        policy == "unconstrained" or (default is not None and policy != default)
    ) and not source.get("baselineRationale"):
        raise DerivationError(
            "non-default or unconstrained baseline policy requires baselineRationale"
        )
    return policy


def _validate_sequences(records: list[dict[str, Any]], owner: str) -> None:
    values = sorted(record["sequence"] for record in records)
    if values != list(range(len(records))):
        raise DerivationError(f"{owner} sequences must be contiguous from zero")


def validate_graph(records: dict[str, list[dict[str, Any]]]) -> None:
    revisions = records["plan.revision"]
    spec_revisions = records["spec.revision"]
    if len(revisions) != 1 or len(spec_revisions) != 1:
        raise DerivationError("a compiled plan must contain exactly one plan and one spec revision")
    plan = revisions[0]
    spec = spec_revisions[0]
    if spec["planRevisionID"] != plan["id"]:
        raise DerivationError("interim spec revision must bind the current plan revision")

    phases = records["plan.phase"]
    families = records["plan.family"]
    sections = records["spec.section"]
    _validate_sequences(phases, "phase")
    phase_by_id = {phase["id"]: phase for phase in phases}
    if len(phase_by_id) != len(phases):
        raise DerivationError("phase IDs must be unique")
    families_by_phase: dict[str, list[dict[str, Any]]] = defaultdict(list)
    family_by_id: dict[str, dict[str, Any]] = {}
    for family in families:
        if family["planRevisionID"] != plan["id"] or family["phaseID"] not in phase_by_id:
            raise DerivationError(f"family {family['id']!r} does not belong to this plan and phase")
        if family["id"] in family_by_id:
            raise DerivationError(f"duplicate family ID {family['id']!r}")
        family_by_id[family["id"]] = family
        families_by_phase[family["phaseID"]].append(family)
    for phase_id, phase_families in families_by_phase.items():
        _validate_sequences(phase_families, f"family in phase {phase_id}")

    sections_by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for section in sections:
        if section["specRevisionID"] != spec["id"] or section["familyID"] not in family_by_id:
            raise DerivationError(
                f"section {section['id']!r} has no current spec revision or family"
            )
        sections_by_family[section["familyID"]].append(section)
    for family_id, family_sections in sections_by_family.items():
        _validate_sequences(family_sections, f"section in family {family_id}")
    if set(sections_by_family) != set(family_by_id):
        raise DerivationError("every deliverable family requires at least one spec section")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(family_id: str) -> None:
        if family_id in visited:
            return
        if family_id in visiting:
            raise DerivationError("deliverable family dependencies contain a cycle")
        visiting.add(family_id)
        family = family_by_id[family_id]
        phase = phase_by_id[family["phaseID"]]
        for dependency_id in family["dependsOn"]:
            dependency = family_by_id.get(dependency_id)
            if dependency is None:
                raise DerivationError(
                    f"family {family_id!r} references unknown dependency {dependency_id!r}"
                )
            dependency_phase = phase_by_id[dependency["phaseID"]]
            if (dependency_phase["sequence"], dependency["sequence"]) >= (
                phase["sequence"],
                family["sequence"],
            ):
                raise DerivationError(f"family {family_id!r} depends on a later or equal family")
            visit(dependency_id)
        visiting.remove(family_id)
        visited.add(family_id)

    for family_id in family_by_id:
        visit(family_id)


def derive_obligations(
    records: dict[str, list[dict[str, Any]]], record_digests: dict[str, str]
) -> list[dict[str, Any]]:
    spec_revision_id = records["spec.revision"][0]["id"]
    obligations: list[dict[str, Any]] = []
    for section in sorted(records["spec.section"], key=lambda value: value["id"]):
        contract = section["contract"]
        sources: list[tuple[str, str, dict[str, Any]]] = []
        sources.extend(("invariant", "invariant", source) for source in contract["invariants"])
        sources.extend(
            ("criterion", "capability" if source["kind"] == "positive" else "rejection", source)
            for source in section["acceptance"]
        )
        sources.extend(
            ("failureMode", "failure", source) for source in contract.get("failureModes", [])
        )
        for source_type, kind, source in sources:
            source_id = source["id"]
            obligations.append(
                {
                    "id": obligation_id(spec_revision_id, section["id"], source_type, source_id),
                    "kind": kind,
                    "subject": section["subject"],
                    "statement": source["statement"],
                    "blocking": source.get("blocking", True),
                    "effectiveBaselinePolicy": effective_baseline_policy(source),
                    "source": {
                        "planRevisionID": records["plan.revision"][0]["id"],
                        "familyID": section["familyID"],
                        "specRevisionID": spec_revision_id,
                        "specSectionID": section["id"],
                        "sourceElementType": source_type,
                        "sourceElementID": source_id,
                        "sourceRecordDigest": record_digests[section["id"]],
                    },
                }
            )
    return sorted(obligations, key=lambda obligation: obligation["id"])


def validate_linkage(
    obligations: list[dict[str, Any]],
    fixtures: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    realizations: list[dict[str, Any]],
) -> None:
    obligation_ids = {obligation["id"] for obligation in obligations}
    fixture_ids = {fixture["fixtureID"] for fixture in fixtures}
    probe_by_id = {probe["id"]: probe for probe in probes}
    if len(probe_by_id) != len(probes):
        raise DerivationError("probe IDs must be unique")
    for probe in probes:
        if probe["fixtureID"] not in fixture_ids:
            raise DerivationError(f"probe {probe['id']!r} references unknown fixture")
        unknown = set(probe["obligationIDs"]) - obligation_ids
        if unknown:
            raise DerivationError(
                f"probe {probe['id']!r} references unknown obligations: {sorted(unknown)}"
            )
        if len(probe["obligationIDs"]) != len(set(probe["obligationIDs"])):
            raise DerivationError(f"probe {probe['id']!r} repeats an obligation ID")
    covered = {obligation_id for probe in probes for obligation_id in probe["obligationIDs"]}
    missing = [
        obligation["id"]
        for obligation in obligations
        if obligation["blocking"] and obligation["id"] not in covered
    ]
    if missing:
        raise DerivationError(f"blocking obligations have no probe: {missing}")
    for realization in realizations:
        unknown_probes = set(realization["probeIDs"]) - set(probe_by_id)
        if unknown_probes:
            raise DerivationError(f"realization {realization['id']!r} references unknown probes")
        unknown_obligations = set(realization["obligationIDs"]) - obligation_ids
        if unknown_obligations:
            raise DerivationError(
                f"realization {realization['id']!r} references unknown obligations"
            )
        selected = {
            item
            for probe_id in realization["probeIDs"]
            for item in probe_by_id[probe_id]["obligationIDs"]
        }
        if not set(realization["obligationIDs"]) <= selected:
            raise DerivationError(
                f"realization {realization['id']!r} does not cover all declared obligations"
            )


def revision_digest(kind: str, records: list[dict[str, Any]]) -> str:
    return sha256_hex(
        canonical_json_bytes(
            {"kind": kind, "records": sorted(records, key=lambda value: value["id"])}
        )
    )
