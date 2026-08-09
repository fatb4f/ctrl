# Contracts and generated transports

Define a closed, versioned CUE contract family for:

```text
RolloutSpec
RolloutIdentity
RolloutEpisode
LifecycleEvent
ToolInvocationObservation
PytestObservation
CPythonObservation
RationaleGroundingObservation
LLMBehaviorObservation
ClaimAdmission
ControlState
ControlAction
RepairDirective
BranchFork
RolloutResidual
ExternalEffectManifest
EvidenceManifest
QualificationVerdict
PromotionAuthorization
QualifiedInconclusiveResult
QualificationRejected
```

Every record carries the qualification schema identifier. `RolloutIdentity`
contains:

```text
rollout_id
parent_rollout_id?
thread_id
turn_id?
item_id?
event_sequence_id
repository_snapshot_before
repository_snapshot_after?
workspace_instance_id
environment_digest
model_configuration_digest
evaluation_spec_digest
policy_digest
provider_id?
provider_version?
cue_schema_digest
generator_version
admission_service_version
```

Digests are domain-tagged SHA-256 values over JSON encoded under the accepted
`canonicalization-profile/v0` or over canonical repository entries. Repository
snapshots include normalized paths, bytes, and executable modes while excluding
VCS metadata, virtual environments, caches, evidence logs, and runtime
artifacts.

`ClaimAdmission` is the only source of claim status:

```python
class ClaimAdmission(BaseModel):
    claim_id: str
    status: Literal["SATISFIED", "VIOLATED", "UNKNOWN"]
    applicability: Applicability
    freshness: Freshness
    provenance: Provenance
    admitted_observation_ids: tuple[str, ...]
    rejected_observation_ids: tuple[str, ...]
    cue_schema_digest: str
    admission_service_version: str
    validation_result_digest: str
```

Use these obligation classes in P0:

```text
HARD_EXECUTABLE
    hidden probe outcome
    CPython retention observation
    regression tests
    deterministic rationale-grounding predicates

ADVISORY_SEMANTIC
    LLM assessment of rationale quality

ADVISORY_DIAGNOSTIC
    additional CPython retention details
```

The deterministic grounding provider emits a neutral closed observation:

```cue
#RationaleGroundingObservation: close({
    references_hidden_probe:     bool
    references_retention_fact:   bool
    identifies_lifecycle_owner:  bool
    proposed_fix_targets_owner:  bool

    unsupported_fact_references: [...#FactID]

    rationale_artifact_digest: #Digest
    admitted_fact_ids:         [...#FactID]
    provider_id:               #ProviderID
    provider_version:          #Version
})

#SatisfiedRationaleGrounding:
    #RationaleGroundingObservation & {
        references_hidden_probe:     true
        references_retention_fact:   true
        identifies_lifecycle_owner:  true
        proposed_fix_targets_owner:  true
        unsupported_fact_references: []
    }
```

The admission service, not the provider, unifies the observation with
`SatisfiedRationaleGrounding`. Successful unification produces `SATISFIED`. A
structurally valid observation that does not unify because any predicate is
false or `unsupported_fact_references` is non-empty produces `VIOLATED`.
Missing or unavailable observations, provider failure, and structurally invalid
grounding candidates with no valid replacement produce `UNKNOWN`; invalid
candidates are retained in `rejected_observation_ids`.

The hard predicate verifies references to admitted facts; it does not score
prose quality. An `LLMBehaviorObservation` is advisory and cannot satisfy a hard
claim. A recorded judgment can be replayed deterministically as an immutable
observation. Re-running the judge creates a new evaluation episode with a new
identity.

Generated Pydantic models are frozen and reject extra fields. Providers cannot
author admissions, claims, residuals, controller state, transitions, or
verdicts. The generator validates CUE, exports deterministic JSON Schema,
generates the models, formats them with locked Ruff, and supports a byte-for-byte
check mode.
