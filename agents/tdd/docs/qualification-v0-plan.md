# Qualification v0 Procedural Implementation Plan

## Status and relationship to other plans

This document is the procedural implementation revision for qualification v0. It refines
`docs/plan.md` and uses `docs/skill-plan.md` as the source of truth for the Jujutsu skill product
surface.

The accepted architecture is:

```text
Kattis PPF profile and local CUE contracts     authoritative authored data
                    ↓
generated Pydantic transports                  closed Python admission boundary
                    ↓
CPython evidence adapters                      bounded raw runtime observations
                    ↓
pure Python qualification kernel               authoritative policy and derivation
                    ↓
python-control projection                      non-authoritative replay and policy scoring
                    ↓
pydantic-graph                                 required typed orchestration
                    ↓
rollout producers and evidence adapters        observed execution and raw evidence
```

The v0 vertical proof qualifies the shipped `jj-agent observe` interface through the exact installed
production wheel. The remaining Jujutsu workflows continue to follow `docs/skill-plan.md`; they
consume the same contracts, generated-model conventions, adapters, and qualification interfaces,
but are not required to complete the first qualification proof.

All Python entry points use the same Cyclopts conventions, generated transport types, generated
operation registry, error envelope, and exit mapping. `python-ppf` is the product control plane;
`jj-agent` is a separate executable only because the proof must cross an installed external-adapter
boundary. It is not a separately designed CLI framework. The pure kernel imports neither Cyclopts
nor either CLI adapter. `contracts/planning/change_plan.cue` and its normalized sequence example are
the executable change-level planning contract for this procedure.

This revision adopts the existing project rather than creating a second Python package:

- distribution: `tdd-agent-skills`;
- import root: `tdd_agent_skills`;
- Python: `>=3.14,<3.15`, with `.python-version` remaining `3.14`;
- runtime dependencies: the existing `pydantic>=2.13,<3` and
  `pydantic-graph>=2.22,<3` constraints;
- planned control-evaluation dependency: the `control` distribution, pinned to the admitted
  python-control 0.10.x API and added through the uv workflow only when the control adapter slice is
  implemented;
- code generation: the existing `codegen` dependency group;
- command contract: `just`, as required by `AGENTS.md`;
- locked versions: whatever is committed in `uv.lock`, currently including Pydantic 2.13.4,
  pydantic-graph 2.22.0, pytest 9.1.1, datamodel-code-generator 0.71.0, Ruff 0.16.1, and ty 0.0.65.

Do not add `pytest-reportlog`, `pytest-agent-digest`, `pytest-agentcontract`, or
`pytest-skill-engineering` in v0. The project-owned pytest plugin must capture the required raw
evidence using pytest's public hooks. Optional presentation and agent-evaluation plugins remain
deferred until the core proof is complete.

---

## Completion target

Qualification v0 is complete when the repository can execute this content-addressed proof without
ever shipping the deliberately unsafe observer:

```text
safe production jj-observe exists from its first implementation
  → a separate proof-fixture repository models the observation contract
  → Plan₁ permits an apparently read-only fixture observer
  → its contract and test plan are approved
  → typed evaluations close Plan₁ obligations over exact probes, fixtures, validators, and evidence roles
  → a test-proposal attempt and rollout produce qualified red
  → a separate candidate attempt and rollout produce qualified green on declared positive probes
  → an adversarial attempt and rollout prove observation mutated repository state
  → CE₁ is admitted as a Plan₁ gap
  → Plan₂ adds an explicit non-mutation obligation and addresses CE₁
  → base_tree₂ = candidate_tree₁ and inherited accepted tests remain frozen
  → a Plan₂ test-proposal rollout reaches fresh qualified red
  → the exact production wheel is installed in the immutable artifact store
  → a repair rollout invokes that wheel through its installed jj-agent console entry point
  → production dispatch reaches the bound safe core and the target probe reaches qualified green
  → a separate regression rollout independently qualifies CE₁'s linked probe
  → CE₁ is derived as resolved for Plan₂
  → a promotion rollout independently qualifies the exact production artifact
  → every rollout is terminal, gap-free, closure-matched, and artifact-linked
  → the evidence package has complete plan-to-evaluation-to-rollout coverage with no orphan nodes
  → the complete adversarial campaign passes with stable operation and working-copy fingerprints
  → static wheel inspection and runtime dispatch identities agree
  → every blocking obligation is satisfied
  → behavioral, candidate, and release-artifact promotion are derived by the pure kernel
```

The unsafe candidate_tree₁ observer exists only in the proof-fixture repository or its test fixtures.
It is not located in or importable from the production package, exposed through `jj-agent`, or
referenced by production skills. Production `jj-observe` always uses `--ignore-working-copy`.

No authored `phase`, `satisfied`, `resolved`, `qualified`, or `promotion_ready` field may appear in
the authoritative root.

---

## Phase 0 — Preflight and authority reconciliation

### 0.1 Preserve the updated project baseline

Before editing, inspect and record:

```bash
rg --hidden --files -g '!.git' -g '!.jj' -g '!.venv'
nl -ba docs/skill-plan.md
nl -ba pyproject.toml
just tools-check
just check
```

Do not rewrite `pyproject.toml`, `.python-version`, or `uv.lock` to match earlier qualification
drafts. Add only the entry points and project-owned source needed by this plan. If dependency
constraints must change, update them through the existing uv workflow and commit the resulting lock
change in the same slice.

Do not edit `.venv`, `dist`, caches, or other generated/runtime files.

### 0.2 Reconcile normative documentation

Amend `docs/plan.md` so that its former graph deferral has a narrow exception for:

- the qualification lifecycle graph defined here; and
- the bounded per-skill Jujutsu transaction graphs defined by `docs/skill-plan.md`.

The amendment must retain these boundaries:

- CUE/PPF owns authored contracts;
- pure functions own classification, selection, evaluation, transitions, and promotion;
- graph nodes own orchestration only;
- graph state is not persisted as qualification authority;
- no generalized workflow engine is introduced.

Add links among the three plan documents so that their roles are unambiguous:

- `docs/plan.md`: qualification semantics and original obligations;
- `docs/qualification-v0-plan.md`: executable implementation procedure;
- `docs/skill-plan.md`: Jujutsu skill and `jj-agent` product behavior.

Produce an authority reconciliation record, completed skill-directory inventory,
command/interface compatibility matrix, deterministic manifest, and a missing-reference report with
zero unresolved entries. This phase may change documentation, contracts, skill artifacts, tests,
generators, and gates, but it may not change Python runtime behavior. Any conflict that cannot be
resolved under the precedence rules in `docs/plan.md` becomes an explicit decision record and blocks
implementation.

Validate that no active statement still rejects all graph usage:

```bash
rg -n "pydantic-graph|graph runtime|workflow graph" README.md docs contracts
```

### 0.3 Require the normative PPF inputs

The user will provide the four Kattis PPF 0.2.0 documents. Do not fabricate, reconstruct, or
silently download substitutes. Before Phase 1, verify these identifiers:

```text
urn:python-policy-ppf:generation-policy:0.2.0
urn:python-policy-ppf:implementation-policy-extension:0.2.0
urn:python-policy-ppf:extension:evaluation-workflow:0.2.0
urn:python-policy-ppf:composed:extensions:0.2.0
```

Stop and report a blocker if any source document, provenance URL, or license notice is missing.

### 0.4 Phase 0 gate

```bash
just check
just test-clean-locked
```

Commit only authority and documentation changes in this phase.

---

## Phase 1 — Shared CUE contracts and deterministic generation

### 1.0 Compile typed Markdown plans into static workflow snapshots

The procedural Markdown plan is an admitted source occurrence, not merely referenced prose. Its
authority is partitioned as follows:

```text
static contract authority:
    PlanArtifactOccurrence, PlanRevision, Obligation, EvaluationSpec, FixtureSpec, ProbeSpec,
    CampaignSpec, RealizationSpec

observed execution authority:
    Attempt, RolloutOccurrence, RolloutEvent, ArtifactProduction, ProbeObservation

derived authority:
    EvaluationOccurrence, EvaluationResult, EvidenceBinding, EvidenceCoverage, RolloutProjection,
    Qualification, CounterexampleResolution, Verdict, PromotionAuthorization
```

The compiler produces `Obligation` records from admitted normative blocks before execution; those
records are static contract authority, while satisfaction remains derived. `FixtureManifest` and
`WorkflowSnapshot` are deterministic static projections. `CampaignSpec` defines required probes and
policy before execution. `Campaign` stores observed rollout membership and purpose but no authored
red/green, completeness, qualification, or promotion claim.

Only fenced blocks with these exact info strings are normative:

```text
cue plan.revision
cue plan.phase
cue plan.family
cue spec.revision
cue spec.section
```

The compiler parses Markdown with a CommonMark AST, validates each CUE record in an isolated CUE
instance, and compiles obligations only from invariants, acceptance criteria, and failure modes.
Explanatory prose is not an obligation source.

Identity is deliberately split:

```text
bytesDigest      exact Markdown bytes; provenance and source drift
sourceDigest     exact fence bytes; audit
recordDigest     canonical exported CUE record; revision immutability
fullDigest       complete generated snapshot; byte-for-byte generation checks
semanticDigest   normative static graph; candidate and evidence binding
```

Consequently prose edits, source-block movement, and equivalent CUE formatting may change
provenance without invalidating runtime evidence. Evidence binds `semanticDigest`; generation
checks bind `fullDigest`.

Fixture specifications are authored, while fixture manifests are generated from
`fixtures/data/<fixture-id>/` using a versioned tree digest. A static realization specification
selects obligations and probes; a runtime realization attempt later binds the candidate,
semantic snapshot, selected probes, and fixture trees. `python-ppf workflow plan` only compiles and checks
the static snapshot. The existing `qualification` controller remains the only admission boundary
for attempts, rollout journals, and observations. Counterexample resolutions, qualifications,
verdicts, and promotion authorizations are produced only by the pure kernel.

Revision reuse fails closed: an admitted revision ID may only recur with the same aggregate
canonical digest. A changed plan or spec revision requires a new ID whose sequence is exactly one
greater than, and whose `supersedes` field names, its predecessor.

### 1.1 Use one shared generation architecture

Create these contract families:

```text
contracts/shared/           IDs, digests, artifacts, evidence, errors, canonical path types
contracts/qualification/    PPF bindings, snapshots, attempts, rollouts, observations, verdicts
contracts/jj/               jj-agent v0 requests, results, operation snapshots, skill operations
```

Commit exported schemas beneath:

```text
generated/schema/qualification-v0.schema.json
generated/schema/jj-agent-v0.schema.json
generated/schema/cpython-evidence-v0.schema.json
generated/schema/control-policy-evaluation-v0.schema.json
```

Commit generated transports beneath:

```text
src/tdd_agent_skills/generated/qualification.py
src/tdd_agent_skills/generated/jj_agent.py
src/tdd_agent_skills/generated/cpython_evidence.py
src/tdd_agent_skills/generated/control_policy.py
```

Do not create a separate `src/qualification` project. Do not hand-edit generated schema or Python
files.

### 1.2 Install and lock the supplied PPF documents

Place the exact supplied bytes beneath `contracts/qualification/ppf/0.2.0/`. Add a committed CUE
manifest containing, for each document:

- canonical identifier;
- version;
- local relative path;
- supplied upstream/provenance URL;
- media type;
- license identifier and notice path;
- lowercase SHA-256 of the exact bytes.

The generation check must fail before schema export if a PPF file is missing or its digest,
identifier, or version differs.

### 1.3 Define non-recursive snapshot identity

Define `RootPayload` as the authoritative payload. It contains authored entities and admitted raw
evidence but does not contain its own digest:

```python
class RootPayload(FrozenTransport):
    schema: Literal["kattis.ppf-root.v0"]
    intent: TaskIntent
    ppf_bindings: PPFBindings
    plan_revisions: FrozenMap[PlanID, PlanRevision]
    claims: FrozenMap[ClaimID, Claim]
    obligations: FrozenMap[ObligationID, Obligation]
    evaluation_specs: FrozenMap[EvaluationID, EvaluationSpec]
    fixture_specs: FrozenMap[FixtureID, FixtureSpec]
    fixture_manifests: FrozenMap[FixtureID, FixtureManifest]
    candidates: FrozenMap[CandidateID, Candidate]
    campaign_specs: FrozenMap[CampaignID, CampaignSpec]
    campaigns: FrozenMap[CampaignID, Campaign]
    probes: FrozenMap[ProbeID, ProbeSpec]
    validators: FrozenMap[ValidatorID, ValidatorSpec]
    admissions: FrozenMap[AdmissionID, Admission]
    approvals: FrozenMap[ApprovalID, Approval]
    attempts: FrozenMap[AttemptID, Attempt]
    rollouts: FrozenMap[RolloutID, RolloutOccurrence]
    rollout_events: FrozenMap[SHA256, RolloutEvent]
    artifact_productions: FrozenMap[ArtifactDigest, ArtifactProduction]
    observations: FrozenMap[ObservationID, ProbeObservation]
    counterexamples: FrozenMap[CounterexampleID, Counterexample]
    subject_bindings: FrozenMap[SubjectID, SubjectBinding]
    sandbox_profiles: FrozenMap[SandboxProfileID, SandboxProfile]
    repository_surface: RepositorySurfaceManifest
    execution_limits: ExecutionLimits
    artifacts: FrozenMap[ArtifactDigest, ArtifactRef]
```

Define the stored snapshot separately:

```python
class SnapshotEnvelope(FrozenTransport):
    workflow_id: WorkflowID
    revision: NonNegativeInt
    parent_snapshot_digest: SHA256 | None
    root: RootPayload
```

Rules:

- `snapshot_digest` is the content-addressed store key, not a field inside the hashed envelope;
- revision zero has no parent;
- revision `n` names the digest of revision `n - 1`;
- an attempt may bind the source snapshot because it predates that attempt;
- an observation binds its attempt and input closure, never the snapshot produced by admitting it.

Define the mutable store pointer independently:

```python
class WorkflowHead(FrozenTransport):
    workflow_id: WorkflowID
    revision: NonNegativeInt
    snapshot_digest: SHA256
```

Define the exact proof-to-production realization record:

```python
class SubjectBinding(FrozenTransport):
    subject_id: SubjectID
    proof_candidate_id: CandidateID
    proof_candidate_digest: SHA256
    production_distribution_digest: SHA256
    production_entry_point: NonEmptyString
    production_module: NonEmptyString
    production_callable: NonEmptyString
    shared_core_artifact_digest: SHA256
    production_adapter_artifact_digest: SHA256
```

The `subject_bindings` map is keyed by `subject_id`. V0 promotion requires exactly one binding for
the promoted subject, and that binding has no authority until an `Admission` names its exact digest.

### 1.4 Define canonical hashing

Use SHA-256 everywhere. Structured values use the RFC 8785 canonical JSON representation over a
restricted JSON domain; artifacts use their exact bytes.

The CUE contracts must prohibit normative floating-point values and restrict every integer to the
inclusive I-JSON range `[-9_007_199_254_740_991, 9_007_199_254_740_991]`. They may contain strings,
integers in that range, booleans, null, arrays, and objects only.

Every authoritative JSON byte boundary, including Jujutsu request references and the Jujutsu skill
manifest, must strictly decode UTF-8 and then use:

```python
json.loads(
    text,
    object_pairs_hook=reject_duplicates,
    parse_float=reject_float,
    parse_constant=reject_nonfinite,
)
```

Recursive validation admits only objects, arrays, strings, canonical-range integers, booleans, and
null. It rejects lone Unicode surrogate code points in keys and values and all unsupported values
before constructing an ordinary dictionary or invoking Pydantic. `FrozenMap` detects canonical-key
collisions after decoding; it cannot recover duplicate keys discarded by a normal JSON decoder.

Use explicit domain prefixes:

```text
kattis.ppf.snapshot.v0\0
kattis.ppf.closure.v0\0
kattis.ppf.evaluation.v0\0
kattis.ppf.evaluation-result.v0\0
kattis.ppf.evidence-coverage.v0\0
kattis.ppf.rollout.v0\0
kattis.ppf.rollout-event.v0\0
kattis.ppf.rollout-stream.v0\0
kattis.ppf.schema.v0\0
kattis.ppf.prompt.v0\0
kattis.ppf.artifact.v0\0
jj-agent.request.v0\0
jj-agent.result.v0\0
```

Normalize repository paths as UTF-8, NFC, POSIX-relative paths. Do not impose NFC normalization on
arbitrary JSON strings, command arguments, or raw artifacts.

### 1.5 Define the exact input closure

`InputClosure` must bind:

- source snapshot digest;
- plan revision ID and digest;
- selected evaluation-spec digests and their plan/obligation/probe/fixture/validator closure;
- subject and candidate digests;
- static campaign-spec and probe digests; the observed `Campaign` is excluded to avoid a digest
  cycle through its rollout IDs;
- validator-set digest;
- repository-surface digest;
- relevant `base_tree`, `approved_test_patch`, `accepted_test_tree`, `implementation_patch`, and
  `candidate_tree` IDs or digests;
- prompt digest when an agent produced the candidate;
- subject-binding, production-distribution, shared-core, and production-adapter artifact digests;
- qualification-controller, candidate-runner, fingerprint-adapter, and rollout-producer artifact
  digests, plus the rollout producer source-contract digest;
- toolchain, execution-environment, dependency-environment, invocation, and sandbox-profile digests.

A changed closure starts a new attempt lineage. Historical evidence remains inspectable but cannot
satisfy the changed lineage.

#### Canonical execution identity records

Define immutable records rather than accepting opaque caller-chosen digests:

```python
class InstalledDistributionIdentity(FrozenTransport):
    normalized_name: Pep503Name
    version: NonEmptyString
    source_artifact_digest: SHA256
    installed_record_closure_digest: SHA256


class DependencyEnvironmentIdentity(FrozenTransport):
    lockfile_digest: SHA256
    distributions: tuple[InstalledDistributionIdentity, ...]


class ExecutionEnvironmentIdentity(FrozenTransport):
    implementation: NonEmptyString
    version: NonEmptyString
    cache_tag: NonEmptyString
    abi_tag: NonEmptyString
    platform_tag: NonEmptyString
    python_runtime_artifact_digest: SHA256
    sanitized_environment: FrozenMap[NonEmptyString, str]
    working_directory_policy: Literal["outside-checkout"]
    sandbox_profile_digest: SHA256


class ComponentArtifactIdentity(FrozenTransport):
    role: Literal[
        "qualification_controller",
        "candidate_runner",
        "fingerprint_adapter",
        "rollout_producer",
    ]
    artifacts: tuple[ArtifactRef, ...]
```

Normalize distribution names with PEP 503 rules, sort by normalized name, and reject duplicates.
Every installed dependency must bind the exact locked wheel artifact used for installation. Derive
`installed_record_closure_digest` from canonical path/digest pairs for every regular file named by
that distribution's installed `RECORD`; resolve paths against the disposable environment root and
reject missing, extra, duplicate, absolute, outside-root, or symlink paths. Derive
`python_runtime_artifact_digest` from canonical path/digest pairs for the
resolved interpreter and its standard-library/runtime files, excluding site packages, caches, and
bytecode. Component identities use canonical repository- or wheel-relative path/digest pairs sorted
by path and reject missing, duplicate, symlink, or out-of-root entries. Hash each complete record
with its own domain prefix and bind those resulting structured digests in `InputClosure`.

### 1.6 Define typed evaluations and evidence coverage

Generate a closed `EvaluationSpec` transport with the semantic fields in `docs/plan.md`: exact plan
revision, obligations, probe, fixture, validators, campaign specification, purpose, expected outcome,
and required evidence roles. Bind it to the supplied Kattis PPF evaluation-workflow extension after
the exact upstream documents are installed; do not guess or locally impersonate the upstream wire
schema.

Extend `RealizationSpec` and `CampaignSpec` to select evaluation IDs. The selected evaluations close
over their probes, fixtures, validators, and obligations; attempts bind the resulting evaluation
closure digest. Existing probe-to-obligation and probe-to-fixture links must exactly agree with the
evaluation rather than defining a parallel coverage graph.

Derive these records without storing them as authored root fields:

```python
derive_evaluation_occurrence(root, evaluation_id, rollout_id)
derive_evidence_bindings(root, evaluation_id, rollout_id)
evaluate_typed_evaluation(root, evaluation_id, rollout_id)
derive_evidence_coverage(root)
```

`EvaluationOccurrence` pairs the rollout's matching `probe-started` and `probe-completed` events and
their observations. `EvidenceBinding` assigns a closed `EvidenceRole` from `docs/plan.md` to an exact
artifact and reachable event; roles outside the evaluation purpose are rejected. `EvaluationResult`
applies only admitted validators to complete observations and evidence bindings and returns
`supports`, `refutes`, or `indeterminate`. `EvidenceCoverage` closes the complete typed path:

```text
normative plan record
→ obligation
→ evaluation specification
→ probe + fixture manifest + validators
→ attempt closure
→ rollout and evaluation events
→ observation and artifact production
→ evaluation result
```

Evidence coverage stops at evaluation results. Qualification and verdict derivation consume that
complete acyclic graph; package and SBOM projections add the later decision-support edges.

Every applicable obligation must have evaluation coverage. A derived not-applicable disposition is
permitted only when the static applicability rule and all of its inputs are bound; it cannot be an
authored escape hatch. Every required evidence role must resolve to an exact artifact consumed or
produced by a reachable evaluation event. Orphan nodes, disagreement between evaluation/probe/
fixture relationships, fixture tree drift, missing roles, incomplete observations, or a result not
derived from the bound validators produce `indeterminate` and block promotion.

### 1.7 Define causal rollout lineage

Generate the `RolloutOccurrence`, `RolloutEvent`, `ArtifactProduction`, and rollout-linked
`ProbeObservation` transports specified by `docs/plan.md`. An attempt declares execution intent and
its complete `InputClosure`; its sole rollout records actual execution. A retry always creates a new
attempt and rollout rather than extending or replacing a terminal lineage.

The root transition API admits an open rollout with its first immutable event-stream prefix, appends
only by installing a new prefix and root revision, and seals only through these transitions:

```text
open → open
open → completed | failed | cancelled | indeterminate
```

Every prefix artifact contains the complete canonical ordered sequence from `first_event` through
`last_event`. Derive `event_id` with `kattis.ppf.rollout-event.v0` from canonical event content after
omitting the ID itself. Validate sequence contiguity, the immediate `previous_event_id` hash chain,
same-rollout earlier causal parents, unique event IDs, known actors, operation-contract bindings,
and all input/output artifact references. Derive `event_stream_digest` with
`kattis.ppf.rollout-stream.v0`; separately verify the exact stored bytes through
`event_stream_artifact`.

An `ArtifactProduction` must name an `artifact-produced` event that outputs its exact artifact. A
`ProbeObservation` must name the same attempt as its rollout, a terminal `probe-completed` event,
and an observed artifact in that event's outputs. Both probe events and the observation name the
same `evaluation_id`. Its `obligation_ids` must exactly match both the `EvaluationSpec` and static
mapping for its `ProbeSpec`; observations cannot expand or narrow probe coverage.

Treat the Runtime handoff contract as the first rollout-producer adapter. Map its bounded session,
paired operation/result events, running and terminal states, failures, validation projections, Git
tree identity, and deterministic canonical serialization into the shared rollout transports. Do not
add a Codex prompt/transcript parser to qualification. Raw prompts, tool payloads, and sensitive
terminal output remain private artifacts referenced by digest.

The Codex App Server JSON-RPC surface is the preferred adapter boundary. `turn/start` accepts a
`collaborationMode`; `collaborationMode/list` discovers presets but is experimental. In Plan Mode,
ingest the final `plan` item from `item/completed` as a proposed plan artifact. Ingest
`turn/plan/updated` records as stepped rollout events/projection inputs with their ordered step text
and `pending`, `inProgress`, or `completed` status. They do not become `PlanRevision`,
`EvaluationResult`, `Qualification`, or `Verdict` records. Preserve `item/*`, tool call/result, turn,
and failure lifecycles as the causal execution stream. `codex exec --json` may supply the same class
of noninteractive plan-update and item events through a separate versioned producer adapter.
Bind the implemented adapter to the exact protocol/schema version and verify behavior against the
official [Codex App Server](https://learn.chatgpt.com/docs/app-server.md) and
[non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md) contracts.

An attempt is eligible for latest-attempt selection only when it has exactly one terminal rollout
whose closure agrees with the attempt and whose complete stream validates. Invalid, incomplete, or
open rollout lineage produces an integrity-blocking result; it cannot be normalized as a failed
probe or recovered by an older successful attempt.

`completed` means controlled execution and journaling reached the expected end; it does not mean the
probe supported its claim. Only a completed rollout reaches the red/green/adversarial classifier.
`failed`, `cancelled`, and `indeterminate` are terminal blocking execution results. At seal, a
completed rollout has no operation left pending or running and pairs every tool/shell call with
exactly one later terminal result whose causal parent is that call; an unpaired call seals
indeterminate.

### 1.7A Bind CPython evidence and python-control projections

Add local CUE definitions for `CaptureIntegrity`, `SourceCoordinate`, the closed runtime
`Observation` union, the closed bounded `ValueProjection` union, `RuntimeEvidenceContent`, and
`ControlPolicyEvaluation`. Export their JSON Schemas through the shared generator and generate the
frozen Pydantic modules listed in section 1.1. The Pydantic models are the executable Python-side
transport realization; CUE and the pure kernel remain the structural and semantic authorities.

`ProbeObservation` remains the shared rollout-linked provenance envelope. A CPython adapter stores
one canonical `RuntimeEvidenceContent` artifact and places its provider ID, schema ID, capture
status, integrity projection, and artifact digest in the envelope. It does not emit a semantic
supports/refutes outcome. `EvaluationResult` is derived later from the admitted evaluation spec,
validators, evidence roles, complete raw artifact, and exact closure.

Use one wire naming convention: snake case in CUE, exported JSON Schema, generated Pydantic aliases,
canonical JSON, and pure-kernel selectors. Contract tests must fail on any alias drift between an
exported schema, generated serialization, and its CUE evaluator.

Runtime evidence must satisfy all of these laws:

- the content document excludes its own digest; exact canonical bytes are identified by the
  artifact store key and rollout `ArtifactProduction`;
- digest values are lowercase 64-character SHA-256 strings with their algorithm fixed by type;
- timestamps use normalized UTC RFC 3339 strings and are parsed for ordering checks;
- paths are repository-relative and bind source digests;
- every column names its coordinate unit and every bytecode offset binds a code identity;
- process, interpreter, thread, optional task, and event-order scope are explicit;
- scalar variants prohibit ambiguous type/value pairs, non-finite floats, and unsafe JSON numbers;
- mapping summaries use typed key/value entries and never stringify arbitrary keys;
- object identities are capture-local and have no cross-run identity authority;
- observation count, recursion depth, collection entries, string/byte lengths, and total canonical
  document bytes are bounded by the probe spec and execution limits;
- complete capture excludes truncation, loss, serialization failure, and instrumentation error;
  incomplete capture remains diagnostic evidence and cannot satisfy a promotion-grade role; and
- omitted optional values and explicit `null` follow distinct declared semantics.

Define the CPython adapter port without importing provider implementations into the pure kernel:

```python
class CPythonEvidenceAdapter(Protocol):
    provider_id: str

    def supports(self, spec: RuntimeProbeSpec) -> bool: ...

    def execute(
        self,
        spec: RuntimeProbeSpec,
        context: ProbeExecutionContext,
    ) -> RuntimeEvidenceContent: ...
```

Each authoritative runtime probe installs `sys.monitoring` or another collector inside the fresh
child interpreter that executes the target. The parent runner cannot claim child events from a
callback installed in the pytest/controller process. Monitoring callbacks enqueue bounded event
seeds only; normalization, disassembly, hashing, CUE evaluation, subprocess work, and controller
updates execute outside the callback.

The control adapter consumes a fixed-dimensional feature projection and keeps target state distinct
from belief state. The belief includes the complete fixed hypothesis posterior required for the
decision; entropy alone is not a sufficient state. Legal categorical actions come from the pure
kernel. Candidate probes or short sequences are enumerated outside python-control, which may replay
and score only those fixed candidates.

Because the authoritative JSON domain forbids floats, numpy arrays and raw python-control responses
remain non-authoritative exact-byte artifacts. A generated `ControlPolicyEvaluation` admits only
CUE-defined integer or tagged-decimal summaries and must bind:

- feature-schema, transition-model, observation-model, and policy artifact digests;
- the source evidence and belief-state projection digests;
- the exact legal candidate action sequence evaluated;
- accumulated cost, perturbation, residual-uncertainty, and trajectory-error projections;
- quantization, approximation, and error-bound metadata; and
- the python-control distribution/version and numerical dependency closure.

Control predictions can rank legal probes and qualify model fidelity against recorded episodes.
They cannot establish a CPython runtime fact, satisfy a runtime evidence role, override a CUE
verdict, or authorize promotion. Controllability and observability matrix results are local to the
named linearization and do not prove global workflow reachability or distinguishability.

### 1.8 Model approval and admission as evidence facts

Define immutable `Admission` and `Approval` entities that bind an entity ID, entity digest, evidence
artifact, and admitting/approving actor.

Rules:

- agent output is an artifact and proposal, never an approval;
- only an admitted exact digest may be evaluated;
- plans and test plans require approval records bound to their exact digests;
- changing an entity invalidates its former admission or approval;
- `PlanApproved` and `TestPlanApproved` are derived projections, not stored phases.

### 1.9 Define counterexample applicability and resolution

Every counterexample binds its exact plan, subject, candidate, campaign, probe, attempt, reproduction
observation, artifact, revision target, `regression_probe_id`, and
`expected_non_reproduction_matcher`.

For v0, `MatcherSpec` is a closed declarative conjunction of equality predicates over fields in the
typed raw-evidence schema. It permits no executable code, regular expressions, or arbitrary field
selectors. CE₁'s matcher requires equality of before/after operation ID, working-copy change ID, and
working-copy tree ID.

Add `addresses_counterexamples: frozenset[CounterexampleID]` to `PlanRevision`.

Derive in this order:

```text
fresh rollout-valid authoritative observations
  → individual probe qualification
  → regression_probe_qualified
  → counterexample_resolved_for(plan)
  → applicable open counterexamples
  → adversarial_campaign_qualified
  → obligations and promotion
```

`regression_probe_qualified(counterexample, plan)` requires the selected observation to use the
counterexample's exact regression probe, bind the exact plan and candidate closure, be fresh,
authoritative, terminal, and successful, and satisfy the non-reproduction matcher. It must not
consult counterexample openness, campaign qualification, obligations, or promotion.

`counterexample_resolved_for(plan)` additionally requires the plan to be in the applicable
descendant lineage and explicitly address the counterexample. Creating or approving Plan₂ does not
resolve CE₁. An adversarial campaign qualifies only after every required adversarial probe qualifies
and no applicable counterexample remains open after applying the independently derived regression
evidence. CE₁ remains stored as historical evidence.

`project_next_route` must preserve these four counterexample states:

```text
counterexample applies, not addressed
    → revision required
counterexample addressed, fresh regression absent
    → execute required regression probe
counterexample addressed, fresh regression failed
    → revision required
counterexample addressed, fresh regression qualified
    → resolved for descendant plan
```

An addressed counterexample awaiting fresh regression evidence remains unresolved, but it is not an
open-counterexample terminal blocker. Its required regression probe is selected before aggregate
campaign promotion or other incomplete-coverage routing.

### 1.10 Generate deeply immutable authoritative collections

Pydantic's `frozen=True` is shallow. Add one handwritten generic `FrozenMap` under the shared runtime
package and configure generated qualification models to use it for authoritative maps.

`FrozenMap` must:

- implement `collections.abc.Mapping`;
- store only an immutable tuple of canonical-key-sorted pairs;
- reject duplicate canonical keys;
- expose no mutable backing dictionary;
- validate from JSON objects through Pydantic core-schema hooks;
- serialize to JSON objects in canonical key order;
- provide copy-on-write `with_item`, `without`, and `merge` operations.

Use tuples and frozensets for other authoritative collections. Generated `jj-agent` request/result
models may use ordinary frozen transport fields where deep persistent mutation is not part of the
contract, but qualification root collections must use `FrozenMap`.

### 1.11 Define qualification and Jujutsu schemas

Qualification CUE must close and cross-check:

- plans, claims, obligations, prerequisites, and blocking policy;
- typed evaluation specifications and complete plan-to-obligation-to-evaluation provenance;
- candidates and contract/candidate subjects;
- static campaign specifications, observed campaign rollout membership, and required/permitted
  expectations;
- probes, validators, attempts, rollouts, rollout events, artifact productions, observations, and
  counterexamples;
- evaluation-to-probe/fixture/validator agreement, fixture-manifest identity, required evidence
  roles, and derived evidence-coverage closure;
- subject bindings, declarative matcher specifications, and proof-to-production cross-references;
- canonical execution, dependency, and component-artifact identity records;
- rollout-producer identity, event-chain integrity, event-stream custody, and observation-producing
  event relationships;
- admissions and approvals;
- repository surfaces and sandbox profiles;
- artifacts, execution limits, snapshots, and heads;
- Plan₁/Plan₂ parent, cause, and tree-lineage facts;
- the packaged operation registry, adapter-artifact manifest, static inspection evidence, and
  runtime dispatch evidence; and
- the exact adapter-role set, fixed wheel coverage scope, and exhaustive artifact-set derivation.

Jujutsu CUE must implement the envelopes and operations from `docs/skill-plan.md`, including stable
failure classes, command evidence, operation snapshots, change IDs, diff digests, and probe results.

### 1.12 Build one deterministic generator

Create one orchestration script for shared, qualification, and Jujutsu outputs. It must:

1. verify PPF sources and tool versions;
2. run CUE formatting checks without rewriting;
3. validate open definitions and concrete examples;
4. export both committed JSON Schemas;
5. export qualification and Jujutsu fixtures;
6. invoke the locked `datamodel-codegen` executable;
7. apply the shared frozen base and `FrozenMap` configuration;
8. format generated Python with the locked Ruff;
9. generate detailed skill request examples under `.codex/skills/*/references/`;
10. generate the packaged declarative operation registry and adapter-artifact manifest;
11. write a manifest of sources, commands, versions, and output digests;
12. under `--check`, generate into a temporary directory and compare byte-for-byte.

Add `just` recipes:

```text
just generate
just generate-check
just jj-generate-check
just qualification-generate-check
```

`jj-generate-check` and `qualification-generate-check` may select subsets, but both must delegate to
the same generator and manifest logic.

### 1.13 Phase 1 tests and gate

Add contract tests for:

- PPF identifier/digest mismatch;
- broken cross-references and map-key/entity-ID mismatch;
- `required` not contained by `permitted`;
- obligation cycles;
- unresolved approval/admission;
- self-referential or invalid snapshot lineage;
- normative plan records without obligations, applicable obligations without evaluations,
  evaluation/probe/fixture disagreement, missing validators or evidence roles, fixture tree drift,
  invalid not-applicable dispositions, and orphan evaluation evidence;
- duplicate rollouts for one attempt, illegal terminal-rollout extension, closure mismatch, event
  gaps, broken previous/causal links, unpaired completed calls, unclosed pending/running operations,
  caller-chosen event-ID disagreement, stream-digest mismatch, and unknown actors or operation
  contracts;
- observation events of the wrong kind, observation artifacts absent from event outputs, unexplained
  evidence artifacts, and probe/obligation mapping disagreement;
- canonicalization and domain separation;
- safe-integer boundaries and duplicate-key rejection before Pydantic parsing;
- deep immutability and deterministic serialization;
- noncanonical dependency names or ordering, lock/wheel/`RECORD` disagreement, runtime-closure drift,
  and missing, extra, escaping, duplicate, or symlink identity paths;
- subject-binding admission and proof/production cross-reference failures;
- malformed or ambiguous operation registries and adapter-artifact manifests;
- missing or duplicate adapter roles, manifest paths outside the fixed coverage set, omitted files,
  dynamic project-owned imports, and exhaustive adapter-digest drift;
- qualification and Jujutsu schema/model drift;
- closed-field rejection and Pydantic round trips.

Run:

```bash
just generate-check
just check
just test-clean-locked
```

---

## Phase 2 — Pure qualification kernel

Implement the kernel beneath `src/tdd_agent_skills/qualification/`. This phase must use authored
fixtures only; it must not invoke pytest, `jj`, agents, sandboxes, or `pydantic-graph`.

### 2.1 Canonicalization API

Implement and test:

```python
def parse_authoritative_json(data: bytes) -> JsonValue: ...
def canonical_json_bytes(value: JsonValue) -> bytes: ...
def digest_structured(domain: DigestDomain, value: JsonValue) -> SHA256: ...
def digest_artifact(data: bytes) -> SHA256: ...
def digest_snapshot(envelope: SnapshotEnvelope) -> SHA256: ...
def digest_input_closure(closure: InputClosure) -> SHA256: ...
```

Use published RFC 8785 test vectors restricted to the admitted JSON domain. Accept the inclusive
integer boundaries `-9_007_199_254_740_991` and `9_007_199_254_740_991`; reject adjacent values,
all floats, `NaN`, positive and negative infinity, invalid UTF-8, lone Unicode surrogate code points,
unsupported value types, and duplicate raw object keys. Validate Unicode scalar values recursively
in object keys and string values. All CLI, fixture, reference, manifest, store-object, and other
authoritative JSON ingestion must call `parse_authoritative_json` before Pydantic validation or
hashing. Arbitrary JSON strings are not NFC-normalized.

### 2.2 Repository-surface law

Implement a restricted rooted glob matcher rather than shell, `glob`, or Git pathspec semantics.
Support literal segments, `*`, `?`, and complete-segment `**` only.

Validate that:

- normalized patterns are unique;
- every tracked path and every path changed by a proposed transition matches exactly one class;
- the exactly matched class permits the active capability and is not protected;
- submodules are rejected;
- symlinks are classified by link path without following targets.

Classify additions, modifications, deletions, and renames. Normalize a rename to deletion plus
addition and reclassify both endpoints before admission. Revalidate the resulting tracked tree after
each accepted transition. Reject unclassified, multiply classified, protected, cross-capability, or
out-of-phase generated changes. V0 does not claim or attempt pairwise language-intersection analysis
for patterns whose overlap is never exercised by a tracked or transition path.

### 2.3 Total pytest classifiers

Define project-owned raw pytest types using collection and runtest hook output. Commands are argv
arrays and node IDs are explicit.

Apply this common precedence:

1. stale or mismatched closure;
2. repository or sandbox integrity failure;
3. timeout, signal, missing output, pytest internal error, or adapter failure;
4. collection error, duplicate probe ID, missing node, or unexpected node;
5. baseline failure;
6. role-specific expectation.

Red requires exact target collection, all declared baselines green under the same closure, a call
phase failure, and an exact stable failure code.

Green requires complete positive-probe coverage, call-phase success, no setup/teardown failure, no
baseline regression, accepted-test blob immutability, and no undeclared execution mutation.

These classifiers normalize raw probe facts only. A classifier output cannot qualify a probe until
`evaluate_typed_evaluation` binds it to the exact evaluation, fixture, validators, rollout events,
observation, and required evidence roles and `derive_evidence_coverage` finds no required gap.

Individual adversarial-probe qualification requires a fresh terminal authoritative result satisfying
that probe's expectation and integrity rules. A regression probe may qualify while its linked
counterexample is still provisionally open; individual probe classification must never consult
counterexample state.

Aggregate adversarial-campaign qualification requires every required adversarial probe to qualify,
no retryable result, complete coverage, and no applicable counterexample remaining open after
applying independently qualified regression evidence. Absence of an artifact alone is never a pass.

### 2.4 Latest-attempt selection

For each exact subject/campaign/probe/input-closure key:

- sequence starts at one and is contiguous;
- duplicate IDs or sequence numbers invalidate the campaign;
- each attempt has exactly one rollout and each rollout names exactly one attempt;
- only attempts with a completed, closure-matched, gap-free rollout reach probe classification;
- the highest sequence is authoritative;
- a newer non-completed terminal rollout yields its blocking result and cannot fall back to an older
  success;
- an invalid or nonterminal newer rollout is an integrity blocker, not permission to select older
  evidence;
- a changed closure starts a new lineage;
- exhausted limits produce a blocking result.

### 2.5 Campaign, obligation, and promotion algebra

Implement pure functions for:

```python
validate_root(root)
validate_rollout(root, rollout_id)
derive_rollout_projection(root, rollout_id)
derive_evaluation_occurrence(root, evaluation_id, rollout_id)
derive_evidence_bindings(root, evaluation_id, rollout_id)
evaluate_typed_evaluation(root, evaluation_id, rollout_id)
derive_evidence_coverage(root)
select_authoritative_attempts(root)
regression_probe_qualified(root, counterexample_id, plan_id)
counterexample_resolved_for(root, counterexample_id, plan_id)
evaluate_campaign(root, campaign_id)
evaluate_obligation(root, obligation_id)
is_counterexample_open(root, counterexample_id)
validate_subject_binding(root, subject_id)
evaluate_release_identity(root, subject_id)
derive_projection(root)
project_next_route(root)
```

Use this projection and routing precedence:

1. invalid/corrupt root;
2. stale closure, invalid rollout lineage, incomplete typed evaluation coverage, or integrity
   violation;
3. execution-limit exhaustion;
4. infrastructure failure;
5. invalid probe or validator;
6. baseline regression;
7. applicable counterexample that is unaddressed, or whose fresh regression semantically failed:
   revision required;
8. addressed counterexample without fresh regression evidence: execute its required regression
   probe;
9. other incomplete required coverage;
10. unsatisfied obligation;
11. qualified but promotion-incomplete;
12. promotion-ready.

Infrastructure and retryable regression-probe failures remain governed by the higher-priority
failure routes. An addressed counterexample cannot match item 7 merely because its regression probe
has not run.

### 2.6 Immutable transitions

Implement copy-on-write transitions for admission, approval, attempts, rollout opening, event
append, rollout sealing, observations, and counterexamples. Every transition must validate the
complete result, return a new `RootPayload`, and leave the input's canonical bytes unchanged.

Illegal transitions return a typed error and the unchanged root. They must not persist phase,
verdict, satisfaction, counterexample resolution, or promotion fields.

### 2.7 Phase 2 tests and gate

Use table-driven tests for every classifier result and route. Include:

- stale evidence;
- attempt/rollout closure mismatch, missing rollout, duplicate rollout, open rollout, failed event
  chain, event gap, invalid causal parent, and stream/artifact digest disagreement;
- observation without a reachable producing event or exact output artifact;
- wrong red failure code;
- baseline regression;
- setup/teardown failures;
- incomplete adversarial search;
- latest-failure/no-success-fallback behavior;
- Plan₁ CE₁ remaining open;
- Plan₂ approval not resolving CE₁;
- CE₁'s regression probe qualifying while CE₁ is provisionally open;
- Plan₂ addressing CE₁ without fresh evidence routing to the required regression probe;
- fresh regression reproduction routing Plan₂ to revision-required;
- fresh Plan₂ regression evidence resolving CE₁ for Plan₂;
- campaign qualification occurring only after counterexample resolution is derived;
- exact agreement between the four counterexample states and `project_next_route`;
- unsafe, behaviorally equivalent, and wrong-distribution subject substitutions;
- input roots remaining byte-identical after every transition.

Run:

```bash
just check
just test-clean-locked
```

---

## Phase 3 — `jj-observe` and raw evidence adapters

### 3.1 Implement `jj-agent` inside the existing package

Add the `jj-agent` console script to `pyproject.toml` and implement under
`src/tdd_agent_skills/jj_agent/`. Do not create a second distribution.

Implement this entry point with Cyclopts and the shared Python CLI adapter conventions. It must use
the generated request/result types, generated operation registry, shared error envelope, and shared
exit mapping; it may not introduce entry-point-local parsing, models, registries, coercion, or exit
semantics.

For v0, implement the public `observe` operation first:

```text
jj-agent --repo REPO observe REQUEST.json
```

Accept `-` for stdin. Emit exactly one typed JSON result to stdout. Send diagnostics to stderr. Use
the exit-code contract from `docs/skill-plan.md`.

Run argv arrays without a shell. Force noninteractive editor, pager, color, and prompt behavior.
Support only `jj >=0.43.0,<0.44.0`.

Package the generated closed operation registry at
`tdd_agent_skills/jj_agent/operations-v0.json`. Its `observe` entry identifies the shared safe core
module and callable. The production dispatcher must consume this resource directly; it may not
maintain a separate hard-coded operation map. Package the adapter-artifact manifest at
`tdd_agent_skills/jj_agent/adapter-artifacts-v0.json`; it covers the entry-point, request-decoding,
registry, dispatch, exception-normalization, serialization, stream, and exit-code implementation.

The manifest cannot choose its own coverage boundary. Schema v0 fixes these required roles exactly:

```text
entry_point
request_decoder
registry_loader
dispatcher
exception_normalizer
result_serializer
stream_router
exit_code_mapper
```

Each role maps to one existing regular wheel path; one path may implement multiple roles. The
inspector independently recomputes the exhaustive artifact set as the unique entry-point metadata,
the registry resource, the adapter manifest, the generated Jujutsu transport module, and every
regular entry beneath the fixed `tdd_agent_skills/jj_agent/` wheel prefix. The generated transport
path is exactly `tdd_agent_skills/generated/jj_agent.py`. The manifest must cover
every required role with paths inside that recomputed set and may name no path outside it. Production
adapter modules may import project-owned code only from that fixed prefix, the generated transport,
or the separately bound shared-core target; reject dynamic project-owned imports. Derive
`production_adapter_artifact_digest` from canonical sorted wheel-path/exact-byte-digest pairs for the
entire recomputed set, never merely from paths declared by the manifest.

### 3.2 Implement the observe graph

The bounded `jj-observe` graph must execute:

```text
validate request
→ check jj version
→ capture operation and working-copy fingerprints
→ execute typed observation with --ignore-working-copy
→ normalize conflict roots, change facts, and Git-format diff digest
→ capture fingerprints again
→ reject any mutation
→ return typed result
```

The graph decides no qualification state. Its result is raw subject evidence consumed by the
qualification kernel.

The shipped path is always:

```text
installed jj-agent console script
→ CLI/request decoding
→ packaged operation registry
→ observe dispatcher
→ shared safe core
→ result serialization
→ stdout/stderr and exit-code mapping
```

Every production result includes typed `RuntimeDispatchEvidence`: entry-point identity, operation
key, registry-resource digest, resolved core module/callable, shared-core artifact digest, and
production-adapter artifact digest. The dispatcher must confirm that the selected registry target is
callable and fail closed on a missing, ambiguous, malformed, or mismatched target.

Keep `jj-conflict-check` as a deprecated alias returning the same conflict observation type, as
required by the skill plan. Compatibility is directional: `conflicts → observe`. Decode the alias
into the canonical observe request before registry lookup and dispatch; do not give it a separate
handler.

Non-mutation requires two independent equality proofs: repository identity before and after the
external invocation, and a filesystem/Jujutsu state digest before and after it. A successful result,
matching operation ID alone, or matching working-copy change ID alone is insufficient.

### 3.3 Define the VCS trust boundary

Treat the Jujutsu adapter as a qualified primitive. It emits:

- adapter and `jj` versions;
- repository and invocation identities;
- operation ID before and after;
- working-copy change/tree ID before and after;
- selected revision/change IDs;
- Git-format patch or diff digest;
- changed paths and conflict roots;
- command evidence and bounded outputs.

The pure kernel validates declared identity equality, lineage consistency, surface rules, and
protected content. It does not claim to reconstruct Jujutsu ancestry from a tree ID alone.

### 3.4 Implement non-importing wheel-inspection primitives

Implement static wheel inspection as a pure bytes-to-evidence adapter. It must:

1. accept wheel bytes and an expected distribution digest supplied by its caller;
2. recompute and verify that digest;
3. read `.dist-info/entry_points.txt` without importing application modules;
4. verify the declared console entry point and module/callable;
5. parse and validate the packaged operation registry;
6. resolve the `observe` target to packaged source bytes;
7. derive the shared-core artifact digest;
8. derive the domain-separated production-adapter artifact digest from the manifest; and
9. emit immutable `ProductionSubjectInspection` evidence.

Static inspection must not import or execute wheel application code. Duplicate registry keys,
malformed metadata, ambiguous distributions, missing resources or targets, unsafe archive paths, and
digest disagreement fail closed.

Phase 3 does not retrieve from the qualification artifact store and does not inspect a newly built
production wheel. Phase 4 adds the store-integrated wrapper; Phase 5 performs the authoritative
inspection after `just test-clean-locked` and the content-addressed build handoff.

### 3.5 Implement project-owned pytest evidence

Add a pytest plugin inside `tdd_agent_skills` using public collection and runtest hooks. It must:

- register the qualification probe marker;
- reject missing or duplicate probe IDs;
- record exact collected node IDs;
- preserve setup/call/teardown outcomes;
- emit stable failure codes in report properties;
- write one structured raw-result artifact;
- expose probe start, probe completion, artifact production, and diagnostics as rollout-producer
  events without classifying them;
- never classify qualification state.

The subprocess adapter must capture exit code, signal, timeout, bounded stdout/stderr, raw-result
digest, and repository fingerprints before and after execution.

### 3.6 Sandbox and isolated runner primitives

Implement `trusted-local` for the vertical proof:

- disposable Jujutsu workspace or temporary repository;
- temporary home;
- explicit environment allowlist;
- fresh interpreter process for every authoritative production attempt;
- a supplied fixture wheel installed into a fresh disposable dependency environment for Phase 3
  tests; Phase 5 supplies the exact stored production wheel;
- invocation through the absolute generated `jj-agent` console-script path;
- checkout, user site, `PYTHONPATH`, `PYTHONHOME`, and unrelated Python variables excluded;
- a working directory outside the checkout and an empty initial application module cache;
- timeout and available resource limits;
- before/after repository-integrity checks;
- canonically derived interpreter/runtime, dependency, environment, controller, runner, and
  fingerprint-adapter identities;
- explicit evidence that host isolation was not provided.

Define the `linux-bwrap` interface but keep its implementation optional. A campaign marked
untrusted must block if a qualified bwrap-equivalent adapter is unavailable; it may not fall back to
trusted-local.

### 3.7 Phase 3 tests and gate

Fake-adapter graph tests must cover node order, failures, mutation detection, and JSON output.

Rollout-producer adapter tests must cover bounded session identity, deterministic mapping of paired
operation/result records, call-without-result failure, running-to-terminal state mapping, validation
projection and Git-tree identity preservation, sensitive payload artifact references, canonical
event serialization, and adapter-contract digest drift. Qualification must have no alternate Codex
transcript parser.

Codex App Server fixtures must cover Plan Mode selection, final `item/completed` plan authority over
streamed deltas, `turn/plan/updated` step/status mapping, item and turn failure lifecycles, and strict
separation between proposed plan artifacts, rollout projections, typed evaluation results, and
promotion authority. Unknown collaboration modes, step statuses, item variants, or protocol drift
fail closed.

Real temporary-repository tests must cover:

- observation with stable operation and working-copy fingerprints;
- a fixture-owned unsafe observer without `--ignore-working-copy` producing mutation evidence; the
  unsafe implementation must exist only in the proof-fixture repository or test fixtures and must
  never replace or impersonate the production adapter;
- conflict-root observations;
- unsupported Jujutsu versions;
- malformed input and stable exit codes;
- JSON-only stdout and diagnostics-only stderr;
- subprocess timeout and output bounds.

Structural tests must prove that unsafe candidate_tree₁ code cannot be imported from
`tdd_agent_skills`, is absent from the packaged operation registry and `jj-agent` CLI, and is not
referenced by production skills.
Safe-observer artifact assertions scan production files only so that the deliberate proof fixture
remains possible.

Inspector and runner primitive tests must cover:

- non-importing static inspection of generated valid and malformed fixture wheels;
- installation of a supplied fixture wheel into a fresh environment;
- execution through the absolute installed console script, never a direct core import;
- request decoding, operation selection, argument translation, exception normalization, result
  serialization, stream separation, and exit-code mapping;
- static inspection and runtime dispatch-evidence agreement for fixture identities;
- rejection of checkout or previously installed distribution resolution.

Do not build, retrieve, inspect, or execute the release-candidate wheel in the Phase 3 gate.

CPython evidence-adapter tests must additionally cover:

- child-owned monitoring installation and cleanup;
- bounded projection of recursive, effectful, oversized, non-string-keyed, and unsupported values;
- Unicode source coordinates across character, UTF-8-byte, and UTF-16 units;
- global versus per-stream ordering under multiple threads and interpreters;
- event loss, truncation, timeout, instrumentation error, and serialization failure;
- rejection of digest self-reference, alias drift, non-normalized timestamps, unsafe numbers, and
  contradictory integrity fields; and
- derivation of semantic results only after CUE admission and pure-kernel evaluation.

Control-adapter tests must cover fixed-sequence replay, complete-belief-state projection, rejection
of fractional or illegal actions, time/input shape agreement, deterministic recorded-corpus A/B
evaluation, explicit approximation bounds, and the inability of a model prediction to satisfy a
runtime evidence obligation.

Run:

```bash
just jj-generate-check
just check
just test-clean-locked
```

---

## Phase 4 — Snapshot store, qualification graph, and operator CLI

### 4.1 Store layout and compare-and-swap

Use this ignored runtime layout:

```text
.run/qualification/
├── objects/sha256/<digest>.json
├── artifacts/sha256/<digest>
├── heads/<workflow-id>.json
└── locks/<workflow-id>.lock
```

Objects and artifacts are immutable. Workflow heads are mutable pointers protected by a
per-workflow file lock.

Implement:

```python
put_snapshot(envelope) -> snapshot_digest
get_snapshot(snapshot_digest) -> SnapshotEnvelope
put_artifact(bytes) -> artifact_digest
get_artifact(artifact_digest) -> bytes
get_head(workflow_id) -> WorkflowHead
compare_and_swap(workflow_id, expected_revision, expected_digest, new_envelope) -> WorkflowHead
```

For mutable head updates, write a same-directory temporary file, flush and `fsync` it, atomically
replace the head, and `fsync` the directory. A stale revision or digest returns a typed concurrency
error. Re-putting identical immutable bytes is idempotent; a digest collision with different bytes
is corruption.

`compare_and_swap` must acquire the workflow lock, load and verify the current head and envelope,
and fail closed unless all of these hold:

```text
current.revision == expected_revision
current.snapshot_digest == expected_digest
new_envelope.workflow_id == current.workflow_id
new_envelope.revision == expected_revision + 1
new_envelope.parent_snapshot_digest == expected_digest
digest(stored new_envelope) == new WorkflowHead.snapshot_digest
```

Validate and canonically encode the new envelope before installation. Under the same lock, install
its immutable object, verify the returned digest, then atomically replace the head. Define revision
zero creation separately: it requires no existing head and `parent_snapshot_digest is None`.

### 4.2 Content-addressed release-artifact custody

Implement `inspect_stored_production_distribution(distribution_digest)` as the store-integrated
wrapper: retrieve and verify immutable bytes, then delegate to the Phase 3 bytes inspector. Test the
wrapper in Phase 4 with synthetic stored wheel artifacts only. The authoritative production-wheel
call remains a Phase 5 action after `just test-clean-locked`.

Phase 4 implements the custody mechanics with synthetic artifacts. Phase 5 executes this
authoritative sequence, and only after `just test-clean-locked` succeeds:

```text
wheel bytes
→ put_artifact
→ production_distribution_digest
→ create and admit SubjectBinding
→ static inspection from store
→ production-path proof from store
→ packaging checks from store
→ publication input identified by digest
```

After `put_artifact`, no qualification or release stage may consume the mutable `dist/` path.
Consumers retrieve the exact bytes with `get_artifact(production_distribution_digest)`, verify them,
and materialize a temporary file only when a downstream tool requires a pathname. The same filename
with different bytes is rejected; a rebuilt wheel requires a new binding, admission, and proof;
missing or corrupted stored bytes are a terminal integrity failure. Publication remains outside v0,
but any future release command must consume the qualified digest or a digest-verified materialization.

### 4.3 Export rollout-aware evidence packages and projections

Add a deterministic package exporter with this layout:

```text
qualification-package/
├── manifest/
├── plan/
│   ├── occurrences/
│   └── revisions/
├── obligations/
│   ├── records/
│   └── provenance/
├── evaluations/
│   ├── specifications/
│   ├── occurrences/
│   ├── results/
│   └── coverage/
├── fixtures/
│   ├── specifications/
│   ├── manifests/
│   └── materializations/
├── probes/
│   └── specifications/
├── candidates/
├── attempts/
├── rollouts/
│   ├── occurrences/
│   ├── event-streams/
│   ├── projections/
│   └── diagnostics/
├── observations/
├── evidence/
│   ├── bindings/
│   └── coverage/
├── artifacts/
├── counterexamples/
└── verdicts/
```

The manifest binds every included path and exact digest, binds the root digest of the derived
`EvidenceCoverage` graph, and distinguishes canonical observed facts from derived projections. The
package verifier requires complete typed paths from normative plan records through obligations,
evaluation specifications, probes, fixtures, validators, rollout occurrences/events, observations,
role-labeled evidence artifacts, evaluation results, and verdict support. Directory presence cannot
satisfy coverage.

A private complete package contains every event body and referenced evidence artifact required for
qualification. A public package or qualification SBOM may omit sensitive bodies but must retain
plan, obligation, evaluation, probe, fixture, rollout, producer, input-closure, event-stream,
artifact role, producing event, observation, result, and verdict relationships by digest. A public
projection is informational and cannot be re-admitted as complete private evidence.

Implement `RolloutProjection` as a pure derivation over a verified root. A marimo canvas may render
the plan, obligation graph, attempt configuration, live rollout, observation graph, qualification,
verdict, and promotion controls. It reads immutable journal prefixes after head advancement and has
no API for authoring events, observations, qualifications, or decisions. The same package and head
must rebuild a byte-identical machine projection after restart; UI layout bytes are not
authoritative.

Package and projection tests cover deterministic export, manifest/path and coverage-root digest
verification, every missing or orphan typed-coverage edge, fixture/probe/evaluation disagreement,
private-to-public redaction with relationship preservation, refusal to qualify from an incomplete
public projection, restart equivalence, and marimo-free kernel operation.

### 4.4 Qualification graph state

Use only identifiers and optimistic-concurrency data:

```python
class GraphState(BaseModel):
    workflow_id: WorkflowID
    root_digest: SHA256
    expected_revision: int
```

Every qualification node must:

1. load and verify the workflow head;
2. load the immutable snapshot;
3. verify that the node equals `project_next_route(root)`;
4. invoke exactly one effect;
5. normalize the raw result;
6. call exactly one pure transition;
7. store the new snapshot;
8. compare-and-swap the workflow head;
9. derive the next node.

Nodes may not assign phases or conclusions directly.

Execution uses a bounded rollout-ingestion subgraph whose nodes preserve the same one-effect,
one-transition rule:

```text
OpenRollout
  → NextRolloutEvent
  → NextRolloutEvent ...
  → SealRollout
  → AdmitObservation
```

`OpenRollout` creates or binds the producer session and admits the initial stream prefix.
`NextRolloutEvent` requests exactly one normalized producer event, verifies its identity and links,
stores its referenced artifacts, and appends exactly one event through copy-on-write transition.
`SealRollout` verifies the complete event window and performs the sole open-to-terminal transition.
`AdmitObservation` can run only after sealing and can admit only an observation derived from a named
reachable `probe-completed` event. Each transition installs a new snapshot and advances the head by
compare-and-swap, allowing a live projection without treating graph state as evidence.

Attempt state, rollout journal, immutable evidence artifacts, graph projections, and promotion
decisions are distinct representations. Persisted transition, attempt, or graph state is not
evidence and is never a decision. After restart, the controller reconstructs the route and every
decision from the verified immutable rollout journal and evidence plus the pure kernel; it does not
trust a partially persisted transition. An interrupted open rollout may resume only from its exact
validated stream prefix and bound producer session; otherwise it is sealed indeterminate and a new
attempt is required.

### 4.5 Qualification CLI

Add the `qualification` command group to the existing `python-ppf` Cyclopts application:

```text
python-ppf qualify run PACKAGE --workflow WORKFLOW [--max-steps N]
```

Rules:

- `qualify run` will perform CUE admission, create revision zero, execute graph nodes until its
  terminal projection or step limit, and report the derived projection;
- its proof mode will retrieve the exact stored wheel and run the deterministic `jj-observe`
  two-cycle proof through its installed production entry point;
- machine JSON goes to stdout and diagnostics to stderr.

### 4.6 Graph equivalence and restart tests

Test:

- stale graph state losing compare-and-swap;
- graph route disagreement failing closed;
- direct-kernel and graph execution producing byte-identical final roots;
- interrupted execution resuming from the persisted head;
- interrupted rollout resuming only from an exact producer session and event prefix;
- rollout open, append, seal, and observation nodes each applying exactly one transition;
- terminal rollout extension, event replay, event omission, and post-hoc observation fabrication
  failing closed;
- adapter failures becoming raw classified evidence;
- immutable snapshot objects never being overwritten;
- wrong workflow ID, skipped revision, wrong parent digest, and stored-object/head digest mismatch;
- same-name synthetic wheel replacement not affecting digest-selected inspection or proof;
- store-integrated inspection delegating to the bytes inspector for synthetic artifacts;
- evaluation performing no writes.

Run:

```bash
just generate-check
just check
just test-clean-locked
```

---

## Phase 5 — Concrete Plan₁ to Plan₂ proof

### 5.1 Separate the controller from the proof subject

The shipped subject is `jj-agent observe`, but the qualification implementation must never regress
it deliberately. Keep the controller, safe production adapter, fingerprint adapter, and immutable
artifact store in the main project. Materialize a separate temporary Jujutsu proof repository from
committed source and patch fixtures; do not commit its `.jj` state. Unsafe candidate_tree₁ code
exists only in
that repository or its test fixtures: it is outside and not importable from the production package,
absent from the packaged registry and CLI, and unreferenced by production skills.

Use these terms exclusively:

```text
base_tree₁                       base tree
approved_test_patch₁             approved test delta
accepted_test_tree₁              resulting accepted-test tree
implementation_patch₁           implementation delta
candidate_tree₁                  resulting unsafe candidate tree

base_tree₂ = candidate_tree₁     exact second-cycle base tree
approved_test_patch₂             approved regression-test delta
accepted_test_tree₂              resulting accepted-test tree
implementation_patch₂           implementation delta
candidate_tree₂                  resulting production-path harness tree
```

Plan₁ requires valid typed observation output but omits the non-mutation invariant.
`implementation_patch₁` therefore adds fixture-owned unsafe observation code without
`--ignore-working-copy`. Its positive probes pass, while CE₁'s adversarial fingerprint probe
reproduces operation and working-copy mutation. The unsafe fixture cannot serve as, replace, or
impersonate the production adapter.

Plan₂ has Plan₁ as parent, names CE₁ as its revision cause, includes CE₁ in
`addresses_counterexamples`, adds the blocking non-mutation obligation, and binds CE₁ to its exact
`regression_probe_id` and equality matcher. It starts from exact
`base_tree₂ = candidate_tree₁` and preserves all inherited accepted-test blobs.
`implementation_patch₂` produces `candidate_tree₂` as a harness that constructs fixture paths and
requests but never imports or calls the safe core directly.

### 5.2 Bind the exact production wheel

Only after `just test-clean-locked` succeeds:

1. build the wheel;
2. read its exact bytes and call `put_artifact`;
3. discard the mutable build pathname from all subsequent qualification decisions;
4. derive `production_distribution_digest` from the store key;
5. statically inspect the stored wheel without importing application modules;
6. construct `SubjectBinding` for exact candidate_tree₂, wheel, entry point, shared core, and adapter
   digests; and
7. admit that binding by its exact canonical digest.

The binding pins four independently checked identities: source revision, wheel digest, installed
distribution metadata, and the absolute invoked executable path. The proof fails if that path is a
source-tree shim, belongs to another environment, or does not match the bound installation metadata.

The stored wheel contains the generated declarative operation registry used by production dispatch.
Independent static inspection proves:

```text
stored wheel digest matches binding
∧ console entry-point metadata matches binding
∧ the observe registry entry resolves to shared core S
∧ packaged S bytes match shared_core_artifact_digest
∧ packaged adapter artifacts match production_adapter_artifact_digest
```

These are identity facts only; direct core inspection or invocation is never qualifying behavior.

### 5.3 Execute candidate_tree₂ through the shipped path

Retrieve the wheel by digest, materialize it in a temporary location, and install it with the bound
locked dependencies into a fresh disposable environment. Invoke the absolute installed console
script:

```text
candidate_tree₂ harness
→ exact stored wheel
→ installed jj-agent console entry point
→ CLI/request decoding
→ packaged operation registry
→ observe dispatcher
→ shared safe core S
→ result serialization
→ stdout/stderr and exit-code mapping
```

The process uses a fresh interpreter, controlled import path, empty initial application module
cache, checkout and user site excluded, sanitized environment, and before/after integrity
fingerprints. The candidate runner records the exact argv, executable, environment, dependency,
controller, runner, and fingerprint-adapter identities.

Runtime `RuntimeDispatchEvidence` must match the independent static inspection, admitted
`SubjectBinding`, and `InputClosure`. A successful direct call to S cannot satisfy the
candidate_tree₂ probe.

### 5.4 Construct authoritative proof data

Commit CUE values, source fixtures, typed evaluation specifications, approved patches, and expected
relations for Plan₁, CE₁, Plan₂, and the subject binding. Every normative acceptance criterion,
invariant, and failure mode maps through an obligation to at least one evaluation that closes over an
exact probe, fixture manifest, validator set, expected outcome, and evidence-role set. Runtime-derived
tree IDs are admitted as evidence rather than hard-coded when Jujutsu does not guarantee stable
identifiers.

Authoritative red, green, adversarial, inspection, dispatch, and promotion evidence must be generated
fresh by `qualification prove-v0` in separate test-proposal, candidate, adversarial, repair,
regression, and promotion rollouts. Static raw observations and rollout journals may exist only as
explicitly non-authoritative pure-kernel fixtures. No fixture may author a verdict, resolution,
qualification, or promotion field.

### 5.5 Assert every lifecycle and release gate

The vertical test must assert:

1. Plan₁ and `approved_test_patch₁` are admitted and approved by exact digest.
2. `approved_test_patch₁` touches only test-authoring surfaces and
   `accepted_test_tree₁ = apply(base_tree₁, approved_test_patch₁)`.
3. accepted_test_tree₁ produces qualified red with baselines green.
4. `candidate_tree₁ = apply(accepted_test_tree₁, implementation_patch₁)` and inherited accepted
   tests are unchanged.
5. candidate_tree₁ reaches qualified green on declared positive probes.
6. CE₁'s exact adversarial probe reproduces repository mutation.
7. CE₁ is open and Plan₁ projects revision-required.
8. Creating and approving Plan₂ does not itself resolve CE₁.
9. Addressing CE₁ without fresh regression evidence routes to its required regression probe rather
   than a terminal open-counterexample result.
10. `base_tree₂ = candidate_tree₁` by exact tree identity and inherited test blobs remain unchanged.
11. Plan₁ observations are stale for Plan₂.
12. `accepted_test_tree₂ = apply(base_tree₂, approved_test_patch₂)` and produces fresh qualified
    red.
13. `candidate_tree₂ = apply(accepted_test_tree₂, implementation_patch₂)` and identifies the exact
    proof candidate in SubjectBinding.
14. The exact wheel is retrieved by digest and static inspection matches the binding.
15. candidate_tree₂ runs every qualifying probe through the absolute installed console entry point.
16. Request decoding, registry selection, dispatch, S execution, serialization, streams, and exit
    mapping satisfy the public contract.
17. CE₁'s regression probe qualifies while CE₁ is still provisionally open.
18. That evidence derives CE₁ as resolved for Plan₂.
19. Every required adversarial probe qualifies and the aggregate campaign then qualifies.
20. Runtime dispatch, shared-core, production-adapter, environment, dependency, controller, runner,
    and fingerprint-adapter identities match the closure.
21. Every attempt has exactly one distinct terminal rollout with matching closure, contiguous event
    sequence, valid hash/causal links, and explained evidence artifacts.
22. Every observation names a reachable `probe-completed` event that produced its exact artifact.
23. Baseline/test-proposal, candidate/repair, adversarial, regression, and release campaign
    memberships are distinct and their required ordering is derived from exact lineage.
24. The derived coverage graph contains every normative plan-to-obligation-to-evaluation edge, exact
    probe and fixture identity, evaluation event, observation, and required evidence-role binding.
25. All blocking obligations qualify and behavioral, candidate, and release-artifact promotion are
    derived.

### 5.6 Required negative proofs

Each case must fail at its intended gate:

- reuse a Plan₁ observation for Plan₂ or select an older success after a newer failure;
- remove a plan-to-obligation source edge, leave an applicable obligation without an evaluation,
  substitute a probe or fixture outside its evaluation, omit a validator or evidence role, or add an
  orphan result or artifact;
- omit a rollout, attach two rollouts to one attempt, reuse one rollout for two campaign phases, or
  mismatch attempt and rollout closures;
- leave a rollout open, extend a terminal rollout, skip or replay an event, break a previous-event or
  causal-parent link, change canonical event content without changing its ID, or mismatch the stream
  artifact and canonical stream digest;
- attach an observation to an absent or unreachable event, a non-probe event, or an artifact that
  the event did not produce; leave any qualifying evidence artifact unexplained by reachable events;
- use the wrong regression probe, plan, candidate, closure, or non-reproduction matcher result;
- omit CE₁ from `addresses_counterexamples` or claim resolution before fresh regression evidence;
- select addressed CE₁ as a terminal open-counterexample blocker before executing its required
  regression probe, or reproduce CE₁ freshly without routing to revision-required;
- use a base_tree₂ other than candidate_tree₁, alter an inherited test blob, or omit a required
  adversarial probe;
- substitute unsafe candidate_tree₁ for the production core;
- substitute an independent safe reimplementation with different bytes;
- package the correct core in a different wheel;
- let candidate_tree₂ call S directly rather than enter through the installed console script;
- break entry-point wiring, request decoding, operation selection, argument translation, exception
  normalization, serialization, stream separation, or exit-code mapping;
- make the runtime dispatcher disagree with the packaged registry;
- omit an adapter role or in-scope wheel file from the manifest, add an out-of-scope path, or use a
  dynamic project-owned import;
- resolve application code from the checkout, user site, or a previously installed distribution;
- change the lockfile, dependency wheel, installed `RECORD` closure, interpreter/runtime closure,
  sanitized environment, controller, runner, or fingerprint-adapter bytes;
- replace a mutable build-path wheel with the same filename after proof;
- tamper with or remove the stored content-addressed wheel or snapshot;
- resume with a stale graph revision or violate any compare-and-swap semantic invariant; or
- run an untrusted campaign under `trusted-local`.

### 5.7 Phase 5 and final gate

The documentation and skill-reconciliation slice does not extend the runtime proof. During this
slice, `just qualify` remains the repository's existing qualification gate and passing it does not
claim that `jj-agent` or the vertical runtime proof has been implemented.

When the deferred runtime implementation lands, extend the `just` contract so:

- `just check` runs formatting, typing, contract, fake-adapter, pure-kernel, CLI, graph, registry,
  static-inspection, and identity tests;
- `just test-clean-locked` proves the locked test group in isolation before any new artifact is
  inspected;
- `just qualify` builds and stores the wheel, runs the temporary-repository two-cycle proof through
  the installed production entry point, runs packaging checks from stored bytes, and executes every
  required mutation and identity-substitution proof.

Run in order:

```bash
just tools-check
just generate-check
just check
just test-clean-locked
just qualify
```

Do not inspect, qualify, or publish new build artifacts until `just test-clean-locked` succeeds, per
`AGENTS.md`. Publication remains outside this plan's execution authority.

---

## Public interfaces added by this plan

### Commands

```text
jj-agent --repo REPO observe REQUEST.json
python-ppf workflow plan PLAN --fixtures MANIFEST --probes PROBES --evaluations EVALUATIONS --realizations REALIZATIONS --output SNAPSHOT
python-ppf workflow plan PLAN --fixtures MANIFEST --probes PROBES --evaluations EVALUATIONS --realizations REALIZATIONS --check SNAPSHOT
python-ppf qualify run PACKAGE --workflow WORKFLOW [--max-steps N]
python-ppf qualify export PACKAGE --workflow WORKFLOW [--public]
```

The other `jj-agent` commands remain governed by `docs/skill-plan.md` and may be implemented after
the qualification-v0 proof without changing qualification contracts.

### Pure kernel API

```python
validate_root(root)
parse_authoritative_json(data)
canonical_json_bytes(value)
digest_snapshot(envelope)
digest_input_closure(closure)
digest_evaluation_spec(evaluation)
digest_evaluation_result(result)
digest_evidence_coverage(coverage)
digest_rollout_event(event)
digest_rollout_stream(events)
validate_rollout(root, rollout_id)
derive_rollout_projection(root, rollout_id)
derive_evaluation_occurrence(root, evaluation_id, rollout_id)
derive_evidence_bindings(root, evaluation_id, rollout_id)
evaluate_typed_evaluation(root, evaluation_id, rollout_id)
derive_evidence_coverage(root)
validate_surface_manifest(manifest, tracked_paths)
classify_changed_paths(manifest, capability, changes)
classify_red(root, attempt, raw_result, integrity)
classify_green(root, attempt, raw_result, integrity)
classify_adversarial_probe(root, attempt, raw_result, integrity)
select_authoritative_attempts(root)
regression_probe_qualified(root, counterexample_id, plan_id)
counterexample_resolved_for(root, counterexample_id, plan_id)
evaluate_campaign(root, campaign_id)
evaluate_obligation(root, obligation_id)
is_counterexample_open(root, counterexample_id)
validate_subject_binding(root, subject_id)
evaluate_release_identity(root, subject_id)
derive_projection(root)
project_next_route(root)
apply_transition(root, cause)
```

Rollout transition causes are closed transports for opening an occurrence, appending exactly one
event, sealing an occurrence, and admitting an event-linked observation. Package export and SBOM
projection are read-only pure operations over a verified root and artifact store.

### Store API

```python
put_snapshot(envelope)
get_snapshot(snapshot_digest)
put_artifact(data)
get_artifact(artifact_digest)
get_head(workflow_id)
compare_and_swap(workflow_id, expected_revision, expected_digest, new_envelope)
```

### Evidence-package API

```python
export_qualification_package(root, artifact_store, destination, disclosure_policy)
derive_qualification_sbom(root, disclosure_policy)
verify_qualification_package(package)
```

### Production-artifact API

```python
inspect_distribution_bytes(wheel_bytes, expected_distribution_digest)
inspect_stored_production_distribution(distribution_digest)
derive_production_adapter_artifact_digest(manifest, wheel_entries)
materialize_artifact(artifact_digest, destination)
validate_runtime_dispatch(inspection, dispatch_evidence, subject_binding, closure)
derive_dependency_environment_identity(lockfile, installed_distributions)
derive_execution_environment_identity(interpreter, environment, sandbox_profile)
derive_component_artifact_identity(role, artifacts)
```

---

## Implementation sequencing and change boundaries

Update `contracts/planning/examples/normalized_sequence.cue` before runtime implementation so its
executable sequence includes the rollout contracts and producer adapter. Its safety order is:

```text
baseline
→ authority-and-skill reconciliation
→ executable specification
→ typed evaluation and evidence-coverage contracts
→ rollout contracts and pure lineage validation
→ pure qualification kernel
→ Runtime handoff rollout-producer adapter
→ observe adapter vertical
→ qualification orchestration
→ installed-wheel release proof
→ atomic
→ split
→ resolve-conflict
→ workspace.prepare
→ workspace.collect
→ workspace.dispose
```

Each change names exactly one externally observable capability or reconciliation result and declares
its earlier dependency edges, authority references, included and excluded paths, inputs, authored
and generated outputs, prohibitions, acceptance criteria, gates, allowed implementation effects,
and immutable proof evidence. Generated outputs name one generator and drift check and forbid manual
editing. The adapter-artifact manifest is a generated projection of the operation registry, never a
parallel authority.

Within every change:

1. declare the initial observable failing proof before production runtime code;
2. implement only the minimum current slice;
3. regenerate only through the declared generator recipe;
4. run the slice-specific gate and `just check`;
5. record immutable evidence required for promotion;
6. reject independently reversible capabilities combined in one change; and
7. do not introduce a parser, transport model, registry, error envelope, or exit taxonomy at an
   entry-point boundary.

Dependencies must reference earlier changes. `authority-reconciliation` is runtime-free,
`observe-production` precedes every repository-mutating workflow, and `vertical-release-proof`
must invoke the installed `jj-agent` entry point. Run `just planning-contract-check` to enforce the
machine-checkable portion of these rules.

No remote, push, bookmark integration, global `jj op restore`, or destructive workspace cleanup is
authorized by this plan.

---

## Deferred scope

- remaining destructive Jujutsu workflows beyond the interfaces in `docs/skill-plan.md`;
- live agent SDK execution;
- generalized trajectory interception;
- distributed workers, leases, or multi-writer workflows;
- generalized event sourcing or a generalized artifact database beyond the bounded qualification
  rollout journal;
- recursive validator qualification;
- mutation testing as a normative obligation;
- generalized Hypothesis state machines;
- python-control as a workflow-legality, evidence-admission, or promotion authority;
- AI-authored normative tests without explicit PPF admission;
- Marimo as an execution runtime;
- mandatory bwrap implementation when the v0 proof declares trusted-local.

---

## Acceptance checklist

```text
[ ] docs/plan.md, docs/skill-plan.md, and this procedure have no authority conflict
[ ] current pyproject dependency ranges and uv.lock remain the dependency authority
[ ] one shared CUE-to-schema-to-Pydantic generation path serves qualification and jj-agent
[ ] generated CPython evidence and control-policy transports use the same CUE authority and naming
[ ] runtime evidence artifacts are bounded, digest-external, coordinate-explicit, and integrity-safe
[ ] CPython monitoring is installed in the child interpreter and callbacks emit bounded seeds only
[ ] ProbeObservation contains raw capture provenance and never authors a semantic evaluation result
[ ] python-control scores only pure-kernel-admitted discrete actions over complete belief projections
[ ] numerical traces remain non-authoritative artifacts and admitted summaries contain no floats
[ ] exact user-supplied PPF documents are bound by identifier, provenance, license, and digest
[ ] snapshot identity has no digest self-reference
[ ] canonical structured hashing is domain-separated, safe-integer bounded, and duplicate preserving
[ ] execution, dependency, controller, runner, and fingerprint identities have canonical derivations
[ ] authoritative root maps are deeply immutable
[ ] approval and admission are stored as evidence facts, never derived phases
[ ] typed evaluation specs bind plan revisions, obligations, probes, fixtures, validators, purposes,
    expected outcomes, and evidence roles
[ ] every normative plan record and applicable obligation has complete typed evaluation coverage
[ ] evidence coverage reaches exact rollout events, observations, and role-labeled artifacts
[ ] attempts declare exact execution intent and each attempt has exactly one rollout
[ ] rollout streams are append-only, content-addressed, gap-free, hash-linked, and closure-matched
[ ] Runtime handoff is adapted as a rollout producer without a second Codex transcript parser
[ ] Codex Plan Mode items remain proposals and stepped plan updates remain rollout projections
[ ] observations bind reachable probe-completed events and artifacts produced by those events
[ ] unexplained evidence artifacts and nonterminal or invalid rollouts block qualification
[ ] workflow-head compare-and-swap enforces workflow, revision, parent, and digest invariants
[ ] counterexample resolution is probe-linked, closure-scoped, acyclic, and purely derived
[ ] addressed counterexamples without fresh regression evidence route to their required probe
[ ] repository surfaces are exclusive over tracked and transition paths and fail closed
[ ] pytest hooks emit raw structured facts without qualification policy
[ ] production jj-observe always uses --ignore-working-copy and proves fingerprint equality
[ ] VCS derivation is treated as a qualified adapter primitive
[ ] trusted-local is disclosed and never described as host isolation
[ ] latest-attempt selection never falls back to older success
[ ] graph routes exactly equal pure-kernel projections
[ ] rollout open, append, seal, and observation nodes preserve one-effect/one-transition semantics
[ ] campaign phases use distinct rollouts and red/green/regression/release claims are derived
[ ] Plan₁'s fixture-owned candidate_tree₁ reaches green but produces counterexample CE₁
[ ] unsafe candidate_tree₁ code is absent from the production package, CLI, registry, and skills
[ ] CE₁'s regression probe can qualify before aggregate counterexample closure
[ ] the wheel is stored and retrieved by digest after test-clean-locked
[ ] static wheel inspection imports no application modules
[ ] adapter-artifact coverage is exhaustive over its fixed wheel scope and required roles
[ ] candidate_tree₂ invokes the absolute console entry point installed from the exact stored wheel
[ ] runtime registry, shared-core, adapter, environment, and closure identities agree
[ ] direct-core, safe-analogue, unsafe-core, and wrong-wheel substitutions fail
[ ] Plan₂ produces fresh red, green, complete adversarial, candidate, and release evidence
[ ] private evidence-package export contains complete rollout journals and relationships
[ ] evidence-package verification fails on every orphan or missing typed-coverage edge
[ ] public package and SBOM projections preserve digests and relationships while omitting private
    bodies
[ ] marimo, when present, rebuilds only a derived rollout and qualification projection
[ ] generated artifacts reproduce byte-for-byte
[ ] just check passes
[ ] just test-clean-locked passes
[ ] just qualify passes
```

## Assumptions

- The user supplies the exact Kattis PPF 0.2.0 documents before Phase 1.
- Linux with case-sensitive paths is the v0 execution platform.
- Jujutsu 0.43.x is the only supported v0 family.
- The v0 proof may use `trusted-local`, and its report records that trust assumption.
- The wheel is the executable v0 release artifact; the sdist remains subject to packaging checks but
  does not establish runtime execution identity.
- The declarative registry is generated, packaged, inspected without import, and used directly by
  production dispatch.
- One process is the active writer for a qualification workflow; compare-and-swap still protects
  against stale graph resumption.
- V0 admits one rollout per attempt; retries and distinct campaign purposes create new attempts and
  rollouts.
- Runtime handoff is the first rollout-producer adapter and is consumed through its versioned
  deterministic contract.
- Existing packaging, license, metadata, and release checks remain mandatory and are not replaced by
  qualification tests.
- Until the deferred runtime lands, `just qualify` is the existing repository gate and makes no
  claim that the vertical `jj-agent` proof has run.
