# Diagnostics-Aligned Assurance Runtime v0

> Repository publication note: this document is the versioned runtime successor for the
> qualification architecture. It preserves the existing `workflow-snapshot/v0` contract and
> introduces `assurance-runtime-release/v0` as a separate composite release boundary. The
> existing qualification P0 remains authoritative and is not replaced by this document.


## 1. Canonical formulation

> The system is a diagnostics-aligned assurance runtime governed by immutable CUE-authored workflow and ontology releases. It records agent and probe activity in a lossless append-only journal, normalizes those records into typed facts, executes admitted diagnostic workflows through a deterministic controller, and produces independently adjudicated qualification verdicts.

The runtime may expose generated interfaces through Xonsh, the Codex app-server, SDK clients, marimo, or other adapters. These interfaces are projections over the same pinned workflow snapshot. They do not independently define obligations, evidence sufficiency, legal transitions, or verdict semantics.

```text
Markdown plan + normative CUE
              │
              ▼
       workflow-snapshot/v0
              │
              ▼
   assurance-runtime-release/v0
              │
       generated transports
              │
              ▼
     typed capability registry
              │
    ┌─────────┼───────────┐
    ▼         ▼           ▼
app-server   graph       Xonsh
 / SDK     controller   operator shell
    │         │           │
    └─────────┴───────────┘
              │
              ▼
      authorized operations
              │
              ▼
    pinned diagnostic runtime
              │
              ▼
    append-only JSONL journal
              │
        normalization
              │
              ▼
       canonical facts
              │
    qualification kernel
              │
              ▼
     realization verdict
              │
    ┌─────────┼───────────┐
    ▼         ▼           ▼
 DuckDB      OTel       marimo
analytics  correlation   replay
```

---

## 2. Authority partition

| Layer | Responsibility | Explicit non-responsibility |
|---|---|---|
| **CUE sources** | Authored structural constraints, closed local vocabulary, obligation definitions and evidence-policy shape | Runtime execution and verdict derivation |
| **Admission service** | Validate and publish immutable workflow, ontology, policy and capability releases | Discover semantics implicitly from runtime behavior |
| **Workflow snapshot** | Bind plans, obligations, probes, functions, skills and release digests into one executable contract | Mutable episode state |
| **Generated Pydantic models** | Typed request, result and state transports | Independent schema authority |
| **Capability registry** | Bind typed operations to authorized adapters | Determine evidence sufficiency |
| **Controller** | Execute admitted workflow transitions deterministically | Create ontology relations from execution edges |
| **Adapters and probes** | Observe or actuate the subject through explicit contracts | Issue qualification verdicts |
| **JSONL journal** | Preserve ordered canonical envelopes and references to exact private artifacts | Analytical querying or sole storage of sensitive bytes |
| **Qualification kernel** | Evaluate admitted evidence against pinned policies | Collect raw observations |
| **DuckDB** | Reproducible analytical projection | Canonical evidence storage |
| **OpenTelemetry** | Cross-component correlation and timing projection | Sole copy of evidence-bearing events |
| **marimo** | Replay, comparison, inspection and shadow evaluation | Persistent workflow engine |
| **python-control** | Shadow estimation, simulation and policy comparison | Direct episode actuation |
| **Xonsh** | Optional generated operator shell and bounded diagnostic adapter | Validation authority, sandbox or primary evidence store |
| **`configparser`** | Ingest user-facing or legacy INI configuration | Semantic validation |
| **Startup/bootstrap files** | Install explicit, digested diagnostic helpers | Ambient hidden initialization |

The governing invariant is:

```text
runtime event
    = source observation

normalized record
    = canonical fact candidate

admitted evidence
    = fact accepted under a pinned policy

verdict
    = deterministic evaluation result

projection
    = replaceable view over retained records
```

---

## 3. Canonical identities

Every episode and derived artifact must bind the versions that determine its interpretation:

```text
subjectSnapshotDigest
workflowSnapshotDigest
ontologyReleaseDigest
evaluationPolicyDigest
schemaVersion
providerVersions
interpreterProfileDigest
capabilitySetDigest
journalHeadDigest
```

Published workflow, ontology and policy releases are immutable.

A later release must not silently reinterpret an earlier verdict. Re-evaluation requires an explicit requalification episode with its own identity and decision record.

Timestamps may be retained operationally, but freshness-sensitive timestamps must either:

1. be explicit decision inputs; or
2. be excluded from semantic identity.

---

## 4. Workflow snapshot and runtime release

The existing `workflow-snapshot/v0` remains the immutable static-plan artifact. It contains
normative Markdown occurrences, plan/spec revisions, obligations, fixture manifests, probes and
realization specifications. Its closed contract is not expanded with mutable runtime state or
capability bindings.

The runtime composes that artifact into a separate immutable release:

```python
class AssuranceRuntimeRelease(BaseModel):
    schema: Literal["assurance-runtime-release/v0"]

    workflow_snapshot_digest: str
    workflow_semantic_digest: str

    ontology_release_digest: str
    evaluation_policy_digest: str
    development_graph_digest: str
    capability_set_digest: str
    generated_manifest_digest: str

    provider_requirements: tuple[str, ...]
    release_digest: str
```

The release builder verifies every referenced artifact and emits a non-self-referential,
canonical digest. A digest mismatch between the source, snapshot, release, generated package and
loaded runtime fails closed before execution.

Static development units and prerequisite edges belong to the referenced development-graph
artifact. Their runtime status is a derived projection and never appears in the immutable
workflow snapshot or release payload.

The generation pipeline is:

```text
Markdown plan
→ parse normative fenced records
→ validate CUE
→ export canonical values
→ derive obligations
→ compose sidecars
→ emit workflow-snapshot/v0
→ build assurance-runtime-release/v0
→ generate runtime transports and capability registry
→ verify generated artifact digests
```

## 5. Episode context

Runtime consumers receive a read-only context rather than direct mutable controller state:

```python
class EpisodeContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    episode_id: str

    thread_id: str | None
    turn_id: str | None
    item_id: str | None

    subject_snapshot_digest: str
    workflow_snapshot_digest: str
    ontology_release_digest: str
    evaluation_policy_digest: str

    graph_state_id: str
    graph_state_digest: str

    ready_obligations: tuple[str, ...]
    satisfied_obligations: tuple[str, ...]
    residual_obligations: tuple[str, ...]

    capability_set_digest: str
    journal_head_digest: str
```

State changes occur only through admitted typed commands:

```python
EvaluateEvidence(
    obligation_id="obligation.import-resolution",
    evidence_ids=(
        "evidence.interpreter-identity",
        "evidence.import-resolution",
    ),
)
```

The mutable internal state of the graph or qualification kernel is never exposed as a general shell object.

---

## 6. Obligation and development graph

Long-horizon work is represented by immutable development-unit specifications connected by
admitted prerequisite edges. Runtime status is derived separately.

```cue
#DevelopmentUnitSpec: close({
    id:           #NodeID
    obligation:   #ObligationID
    scope: {
        files?:   [...#Path]
        symbols?: [...#SymbolID]
    }
    tests: [...#TestID]
})

#PrerequisiteEdge: close({
    from: #NodeID
    to:   #NodeID
    relation:
        "history_precedes" |
        "defines_symbol_used_by" |
        "produces_interface_used_by" |
        "extends_schema_or_type"
    supporting_facts: [...#FactID]
})
```

The graph is an evaluation contract, not a claim that development has one optimal total order.
Statuses such as `ready`, `satisfied`, and `regressed` are derived episode projections.
Previously satisfied units remain active regression obligations after later mutations.

```text
turn completed
    ≠
development unit satisfied
    ≠
realization qualified
```

## 7. Lossless event journal

Runtime events are first retained in an append-only journal.

```json
{
  "journalSchema": "assurance-event-envelope/v0",
  "sequence": 184,
  "collectorRunId": "run_...",
  "observedAt": "2026-08-06T14:31:22.184Z",

  "source": "codex-app-server",
  "episodeId": "episode_...",
  "threadId": "thread_...",
  "turnId": "turn_...",
  "itemId": "item_...",

  "method": "item/completed",
  "payloadSchema": "provider-protocol/version",
  "payloadArtifact": {
    "digest": "sha256:...",
    "mediaType": "application/json",
    "byteLength": 0,
    "privacy": "private"
  },

  "previousRecordDigest": "sha256:...",
  "recordDigest": "sha256:..."
}
```

The collector retains every received public event at its producer boundary. Exact App Server
payload bytes are stored as private content-addressed artifacts; the Python SDK producer stores
the complete public notification representation together with its SDK and runtime versions.
The record digest excludes its own digest field.

The collector retains:

```text
thread lifecycle
turn lifecycle
item lifecycle
commands
tool calls
approvals
file changes
errors
warnings
diagnostic operations
probe observations
graph transitions
evaluation decisions
```

Intermediate transitions remain available:

```text
item/started
item/delta
item/completed
```

Evidence derivation normally uses the reconciled terminal object. Intermediate events remain available for timing, lifecycle analysis and controller debugging.

A session-end event does not seal the journal. Sealing belongs to an external collector after terminal-event reconciliation. Crash recovery may explicitly mark unresolved started objects.

---

## 8. Canonical projections

The journal is normalized into project-owned facts:

```text
raw_events
threads
turns
items
commands
file_changes
approvals
tool_calls
diagnostic_invocations
probe_observations
graph_transitions
evaluation_decisions
lifecycle_anomalies
event_correlations
```

Each normalized fact retains:

```text
source record identity
provider identity and version
subject snapshot
episode identity
normalizer version
raw payload digest
canonical fact digest
```

DuckDB relations are rebuildable from the journal. Deleting the DuckDB database must not change qualification outcomes.

---

## 9. Typed capability registry

Every operation available to an agent, graph, shell or workbook is registered through a generated specification.

```python
class FunctionSpec(BaseModel):
    function_id: str
    adapter_id: str
    operation: str

    request_schema: str
    result_schema: str

    requires_obligations: tuple[str, ...] = ()
    emits_observation_kinds: tuple[str, ...] = ()
    emits_artifact_kinds: tuple[str, ...] = ()

    effect_class: Literal[
        "read",
        "probe",
        "mutation",
        "external",
        "control",
    ]

    authorization_policy: str
```

Callable contract:

```python
RequestT = TypeVar("RequestT", bound=BaseModel)
ResultT = TypeVar("ResultT", bound=BaseModel)


class TypedFunction(Protocol[RequestT, ResultT]):
    spec: FunctionSpec

    def __call__(
        self,
        request: RequestT,
        *,
        context: EpisodeContext,
    ) -> ResultT: ...
```

Initial registry:

```text
runtime.current_turn
runtime.current_items

graph.inspect_state
graph.dispatch

obligations.inspect
obligations.ready

git.resolve_revision
git.committed_snapshot
git.workspace_diff

cpython.interpreter_identity
cpython.path_configuration
cpython.import_resolution
cpython.distribution_metadata
cpython.exception_chain
cpython.audit_probe

pytest.collect
pytest.run_nodeids
pytest.run_fixture_probe
pytest.run_regression_set

control.encode_state
control.estimate_state
control.rank_probe
control.compare_policies
```

The same function is callable through the SDK, app-server, graph, Xonsh, marimo, pytest evaluations and replay infrastructure.

---

## 10. Xonsh boundary

Xonsh is a later-phase optional generated operational interface with two bounded roles:

1. **Operator shell:** inspect the current episode, graph and obligation projections.
2. **Diagnostic adapter:** execute admitted probes that combine Python reflection and subprocess activity.

It is not a first-class Pydantic integration. Generated Pydantic models work in Xonsh because Xonsh executes Python.

Generated aliases remain adapters over the typed registry:

```xonsh
turn
graph-state
obligations
git-snapshot
py-identity
py-import
pytest-collect
pytest-run
```

Each alias must:

1. parse shell arguments;
2. construct a generated request model;
3. inject the current immutable context;
4. call a registered function;
5. validate the returned transport;
6. return the typed invocation/result to the central collector, which appends the journal records;
7. render a human-readable projection.

Aliases do not contain independent operational semantics.

Xonsh must run as an ephemeral, pinned and sandboxed process with:

```text
explicit executable
explicit working directory
declared environment
declared bootstrap
declared capability set
timeout
effect authorization
journal correlation identifiers
```

It must not inherit ambient startup files or silently qualify evidence based on interactive session state.

---

## 11. Interpreter profile

The evaluated interpreter is part of the subject identity.

```python
class InterpreterProfile(BaseModel):
    profile_id: str

    executable: str
    implementation: Literal["cpython"]
    version_constraint: str

    virtual_environment: str | None
    isolated: bool

    bootstrap_module: str | None
    bootstrap_digest: str | None

    allowed_imports: tuple[str, ...]
    environment: dict[str, str]

    profile_digest: str
```

The probe runner records at minimum:

```text
sys.executable
sys.implementation
sys.version
sys.prefix
sys.base_prefix
sys.path
sys.flags
sysconfig paths
installed distributions
platform
working directory
selected environment variables
```

The default invocation is the exact repository interpreter:

```bash
/path/to/repository/.venv/bin/python \
  -m assurance_runtime.probe_runner \
  probe-request.json
```

### Bootstrap policy

Avoid invisible global behavior through:

```text
shell-wide PYTHONPATH
ambient PYTHONSTARTUP
sitecustomize
undeclared .pth execution
host user startup files
```

Use an explicit generated prelude:

```python
from assurance_runtime import (
    capture_exception,
    capture_import,
    compare_environment,
    emit_observation,
    probe,
)
```

Record:

```text
bootstrap module
bootstrap version
bootstrap digest
imported helper names
```

A later embedded implementation may use an isolated CPython initialization profile, but the external sandbox and launcher remain the security boundary.

Python-level audit hooks are diagnostic instrumentation, not authorization enforcement.

---

## 12. Diagnostic probe model

A static probe targets an explicit hypothesis and requested observation. An execution request binds
that specification to one exact subject, interpreter profile, capability set and episode.

```cue
#DiagnosticProbeSpec: close({
    id:                     #ProbeID
    hypothesis:              #HypothesisID
    requested_observation:  #ObservationKind
    actuator:                #AuthorizedActuator
    timeout_seconds:        #SafeInteger
})

#DiagnosticProbeRequest: close({
    request_id:              #ID
    probe_id:                #ProbeID
    subject_snapshot_digest: #Digest
    interpreter_profile_digest: #Digest
    working_directory:       #Path
    module?:                 #NonEmptyString
})
```

The adapter emits raw observations only. The pure kernel derives eliminated hypotheses, remaining
hypotheses, causal claims, residuals and any information-gain projection. No provider-authored
hypothesis result or floating-point score can satisfy an obligation.

Mutation may be conditionally blocked until required runtime diagnosis is available, but a
universal diagnosis-before-editing rule is too rigid. Authorization policy therefore determines
when diagnostic evidence is mandatory:

```text
read-only inspection
→ normally permitted

low-cost diagnostic probe
→ preferred where uncertainty is material

mutation
→ permitted only when its prerequisite evidence policy is satisfied

emergency or trivial correction path
→ may use a separate admitted policy
```

## 13. Causal claims

A root-cause conclusion is represented as a refutable claim rather than an unqualified label.

```cue
#CausalClaim: close({
    cause:  #FactOrStateID
    effect: #FactOrStateID

    assumptions: [...#Predicate]
    confounders: [...#FactOrStateID]

    interventions: [...#InterventionID]
    refutations:   [...#RefutationID]

    status:
        "supported" |
        "refuted" |
        "unsupported"
})
```

The system prefers `unsupported` over fragile causal attribution.

Diagnostic conclusions should identify:

```text
root-cause step or state
fault classification
supporting observations
source locations
corrective strategy
remaining uncertainty
refutation attempts
```

Trajectory length or token count alone is not a reliable diagnostic quality signal. Structural behaviors—such as acquiring relevant context before mutation and performing verification—are more suitable evaluation candidates.

---

## 14. Controller

The evidence-core slice uses a deterministic application service and pure transition functions.
`pydantic-graph` or an equivalent typed graph runtime may implement the operational episode
controller in the later graph phase:

```text
MaterializeSubject
→ StartTurn
→ CollectLifecycleEvents
→ NormalizeObservations
→ EvaluateEvidence
    ├─ sufficient → ProduceVerdict
    ├─ ambiguous  → SelectProbe
    └─ invalid    → RejectEpisode
                         │
                         ▼
                    ExecuteProbe
                         │
                         ▼
                CollectObservation
```

Its execution edges are not ontology edges.

The controller receives state and admitted observations, then produces deterministic transition decisions:

```python
def select_transition(state: DiagnosticState) -> TransitionDecision:
    if state.subject_identity_invalid:
        return RejectEpisode(reason="invalid_subject")

    if state.evidence_sufficient:
        return Qualify()

    if state.remaining_budget <= 0:
        return Inconclusive(reason="budget_exhausted")

    return ExecuteProbe(
        probe=rank_legal_probes(state)[0],
    )
```

Repeated records with the same semantic digest are idempotent no-ops. A duplicate rejection is reserved for conflicting records that share a logical identity.

---

## 15. OpenTelemetry projection

This is a later-phase projection. It is not required for evidence-core qualification.

OpenTelemetry provides a correlation plane:

```text
episode
└── agent thread
    └── turn
        ├── model interaction
        ├── command execution
        ├── file mutation
        ├── diagnostic probe
        ├── pytest execution
        └── evidence evaluation
```

Project-owned correlation attributes include:

```text
assurance.episode.id
assurance.subject.digest
assurance.workflow.digest
assurance.ontology.release_digest
assurance.policy.digest
codex.thread.id
codex.turn.id
codex.item.id
diagnostic.request.id
probe.id
hypothesis.id
observation.id
evidence.id
```

Span-tree evaluations may confirm that required verification or diagnostic steps occurred.

The span remains a telemetry projection. It is not the sole retained representation of an evidence-bearing event.

---

## 16. marimo workbench

This is a later-phase operator projection. It is not required for evidence-core qualification.

marimo is the operator and research surface:

```text
01 Select episode
02 Inspect subject identity
03 Reconstruct lifecycle
04 Show command and mutation timeline
05 Inspect diagnostic facts
06 Compare hypotheses before and after probes
07 Replay controller transitions
08 Execute candidate policy in shadow mode
09 Compare expected and actual verdicts
10 Export evaluation artifact
```

marimo may:

```text
query DuckDB
invoke replay APIs
render timelines
run evaluation cases
compare policy revisions
export review artifacts
```

It may not:

```text
mutate canonical journal records
issue authoritative verdicts directly
hide runtime dependencies
become the persistent episode controller
```

---

## 17. `python-control` shadow model

This is a later-phase advisory projection. It is not required for evidence-core qualification.

`python-control` is initially an advisory analytical layer.

Possible state vector:

```text
unresolved hypotheses
evidence coverage
observation freshness
confidence dispersion
remaining budget
regression exposure
```

Possible control inputs:

```text
inspect
search
execute test
run probe
mutate
revert
terminate
```

Observed outputs:

```text
new facts
hypothesis reduction
test-state changes
policy violations
cost
```

Normalized flow:

```text
recorded episodes
→ identify an approximate transition model
→ simulate alternate probe-selection policies
→ compare information gain, cost and stability
→ propose bounded deterministic policy changes
→ admit a policy revision independently
```

A control recommendation must pass through:

```text
legal-transition filter
→ effect authorization
→ budget constraints
→ deterministic tie-breaking
→ TransitionDecision
```

The model never directly actuates an episode.

---

## 18. Skills

A skill compiles into a typed capability manifest rather than remaining only prose.

```python
class SkillSpec(BaseModel):
    skill_id: str
    version: str

    input_schema: str
    output_schema: str

    required_capabilities: tuple[str, ...]
    required_obligations: tuple[str, ...]
    permitted_functions: tuple[str, ...]

    produced_claims: tuple[str, ...]
    produced_evidence: tuple[str, ...]

    termination_conditions: tuple[str, ...]
    policy_digest: str
```

Trajectory corpora, failed episodes and agent-generated revisions may propose skill changes.

Admission remains:

```text
trajectory feedback
→ candidate revision
→ replay and independent validation
→ admitted immutable revision
```

Not:

```text
trajectory feedback
→ automatic authoritative mutation
```

---

## 19. Repository retrieval

Repository context acquisition should use deterministic or structural providers as the default evidence source.

```text
agent
  ↓ typed query
repository provider
  ↓ evidence bundle
optional exploratory subagent
```

A retrieval result should expose:

```text
query
repository and revision
scope
selected artifacts
coverage
omissions
provenance
abstention or uncertainty
```

Exploratory subagent output must not be the sole context source because planner-to-subagent handoffs can silently lose scope or constraints.

Counterfactual wrong-repository and no-gold controls should be available for retrieval evaluation.

---

## 20. Configuration ingestion

Configuration precedence is explicit:

```text
built-in CUE defaults
→ repository diagnostic profile
→ scenario profile
→ episode overrides

Observed runtime environment is captured separately as subject evidence; it does not override
resolved configuration.
```

`configparser` may ingest INI sources:

```ini
[interpreter]
executable = .venv/bin/python
isolated = true
bootstrap_module = assurance_runtime.bootstrap

[capabilities]
functions =
    cpython.interpreter_identity
    cpython.import_resolution
    pytest.collect
    pytest.run_nodeids

[telemetry]
jsonl = .artifacts/runtime/events.jsonl
otel = true
```

The resulting mapping must pass through generated models and CUE-governed admission before becoming an immutable interpreter or diagnostic profile.

Every resolved value retains its source and precedence.

---

## 21. Thin vertical slice

The first successor realization covers one scenario:

```text
pytest collection raises ModuleNotFoundError
```

The existing qualification P0 configuration-key episode remains the prerequisite authority-chain
proof. This successor slice adds diagnostic evidence and does not replace that episode.

### Required operations

```text
1. Build and verify an assurance-runtime-release/v0.
2. Ingest one App Server event stream and one Python SDK event stream through their producer ports.
3. Retain exact source-boundary payload artifacts and seal the journal.
4. Normalize thread, turn, item, command and terminal lifecycle facts.
5. Identify the exact requested Python interpreter and environment.
6. Record sys.path and selected environment identity.
7. Inspect project installation and distribution state.
8. Resolve the target module specification.
9. Reproduce the import in the pinned environment.
10. Re-run pytest collection.
11. Evaluate the import-resolution obligation set in the pure kernel.
12. Produce satisfied, inconclusive or rejected diagnostic status.
13. Verify deterministic journal replay and projection independence.
```

### Initial capability set

```text
repository.committed_snapshot

cpython.interpreter_identity
cpython.import_resolution
cpython.distribution_metadata

pytest.collect
pytest.run_nodeids
```

### Initial generated artifacts

```text
generated_runtime/
├── models.py
├── runtime_release.py
├── function_specs.py
├── registry.py
└── manifest.json
```

Xonsh aliases, graph commands, OpenAPI output, DuckDB, OTel and marimo are later-phase artifacts.

## 22. Core evaluation matrix

| Evaluation | Required invariant |
|---|---|
| Journal integrity | Every record has valid sequence and digest linkage |
| Journal replay | The same sealed journal produces the same canonical facts |
| Adapter equivalence | SDK and app-server representations normalize equivalently |
| Lifecycle closure | Every started object is terminal or explicitly unresolved |
| Subject identity | All evidence binds to the requested repository snapshot |
| Interpreter identity | Probe evidence binds to the requested executable and environment |
| Bootstrap visibility | Every injected helper is declared, versioned and digested |
| Function authorization | Every invocation was permitted by its capability and effect policy |
| Graph determinism | The same state and admitted observations produce the same transition |
| Evidence idempotency | Replayed identical facts do not change state |
| Projection reproducibility | DuckDB rebuilds to equivalent relations |
| Trace correlation | Every derived span links to source records or probe identifiers |
| Verdict independence | Removing DuckDB, OTel or marimo does not change the verdict |
| Regression retention | Earlier satisfied units remain active after later mutations |
| Unsupported-claim safety | Insufficient causal evidence produces `unsupported` or `inconclusive` |
| Controller shadowing | Optimized recommendations never directly actuate the runtime |

---

## 23. Adoption order

### Prerequisite — existing qualification P0

```text
workflow contracts
→ generated transports
→ pure qualification kernel
→ current configuration-key authority-chain episode
```

### AR0 — evidence core

```text
workflow-snapshot/v0
→ assurance-runtime-release/v0
→ JSONL journal plus private artifact store
→ direct App Server producer
→ Python SDK producer
→ pinned CPython import probe
→ deterministic evidence evaluation
```

Normal repository gates use committed protocol fixtures. Authenticated live producer smoke tests are
explicit and non-gating.

### AR1 — operational projections

```text
pydantic-graph controller
Xonsh operator/diagnostic adapter
DuckDB projection
OpenTelemetry correlation
marimo replay
configuration and skill projections
```

### AR2 — advisory optimization

```text
episode corpus
→ python-control state estimation
→ shadow probe-selection policies
→ policy comparison and independent admission
```

## 24. Final normalized boundary

The canonical architecture is not:

```text
Xonsh + Pydantic
or
DuckDB + OTel
or
pydantic-graph + python-control
```

It is:

```text
CUE-authored semantic authority
→ immutable workflow snapshot
→ generated typed capabilities
→ authorized deterministic execution
→ lossless evidence journal
→ canonical fact normalization
→ independent qualification
→ replaceable analytical and operator projections
```

Xonsh, Pydantic, DuckDB, OpenTelemetry, marimo, `pydantic-graph` and `python-control` are valuable because they occupy distinct bounded roles inside that architecture. None becomes authoritative merely because it is convenient, stateful, typed, observable or mathematically expressive.
