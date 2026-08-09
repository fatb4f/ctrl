# Qualification Package v0 Semantic Authority

## Authority and architecture

This document owns the qualification laws and obligation model. The executable implementation
procedure is `docs/qualification-v0-plan.md`; the Jujutsu skill and `jj-agent` product contract is
`docs/skill-plan.md`. Procedural details may refine this document but may not weaken its laws.

The three authorities have distinct, non-interchangeable roles:

| Authority | Owns |
| --- | --- |
| `docs/plan.md` | Semantic product intent and invariants |
| `docs/qualification-v0-plan.md` | Qualification lifecycle and implementation sequencing |
| `docs/skill-plan.md` | Skill packaging, references, manifests, and skill-facing interfaces |

Reconciliation obeys these precedence rules:

1. semantic invariants cannot be weakened by procedural documents;
2. procedural sequencing cannot silently alter product interfaces;
3. skill packaging cannot introduce runtime behavior absent from the semantic or procedural plans;
   and
4. an irreconcilable conflict requires an explicit decision record, and implementation must not
   choose implicitly.

`contracts/planning/change_plan.cue` makes change ordering, authority references, scope, generation,
acceptance, gates, implementation effects, and promotion evidence executable. Its normalized plan is
`contracts/planning/examples/normalized_sequence.cue` and is checked by
`just planning-contract-check`.

The authority chain is:

```text
Kattis PPF profile and local CUE contracts     authoritative authored data
                    ↓
pure Python qualification kernel               authoritative policy and derivation
                    ↓
pydantic-graph                                 bounded typed orchestration
                    ↓
rollout producers and evidence adapters        observed execution and raw evidence
```

CUE owns authored structure. Pure functions own classification, attempt selection, counterexample
resolution, obligation evaluation, transitions, and promotion. Graph nodes invoke effects and apply
one pure transition; graph state is never qualification authority. The qualification lifecycle graph
and the bounded per-skill graphs in `docs/skill-plan.md` are the only v0 graph-runtime exceptions. No
general workflow engine is introduced.

All Python CLI entry points use shared Cyclopts conventions, generated transport types, the generated
operation registry, one error-envelope model, and one exit-code mapping. `jj-agent` is a separate
executable boundary so qualification can exercise an installed external adapter; it is not a second
CLI architecture. The pure qualification kernel remains independent of Cyclopts and every CLI
adapter.

## Authoritative state and evidence

Qualification evaluates this matrix:

```text
candidate × campaign × probe × attempt × rollout → observation
```

The immutable root contains task intent, PPF bindings, plans, claims, obligations, typed evaluation
specifications, candidates, campaign specifications and observed campaigns, probes, fixtures,
validators, approvals, admissions, attempts, rollouts, rollout events, artifact productions,
observations, counterexamples, subject bindings, sandbox profiles, repository surfaces, execution
limits, and artifact references. It must not contain authored `phase`, `satisfied`, `resolved`,
`qualified`, or `promotion_ready` fields.

Authority is partitioned by provenance:

```text
static contract authority
    PlanArtifactOccurrence, PlanRevision, Obligation, EvaluationSpec, FixtureSpec, ProbeSpec,
    CampaignSpec, RealizationSpec

observed execution authority
    Attempt, RolloutOccurrence, RolloutEvent, ArtifactProduction, ProbeObservation

derived authority
    EvaluationOccurrence, EvaluationResult, EvidenceBinding, EvidenceCoverage, RolloutProjection,
    Qualification, CounterexampleResolution, Verdict, PromotionAuthorization
```

An `Obligation` is deterministically compiled from admitted normative plan/specification blocks and
then becomes part of the static contract. Its satisfaction is never authored. `CampaignSpec`
defines required probes and campaign policy before execution; an attempt binds its digest. A
`Campaign` records observed rollout membership and purpose without changing that closure. Campaign
completeness and every red/green, resolution, qualification, verdict, and promotion claim are
derived by the pure kernel.

Plans and test plans require approvals bound to their exact digests. Every evaluated entity and
subject binding requires admission by exact digest. Agent output is an artifact and proposal, never
an approval. A changed entity invalidates its former approval or admission.

Observations bind exact input closures, attempts, rollout events, raw reports, and provenance.
Pytest, Jujutsu, and Runtime handoff adapters emit raw facts only. Freshness is identity- and
digest-based, not timestamp-based. For each exact subject/campaign/probe/closure lineage, the newest
completed attempt with one valid terminal rollout is authoritative; a newer failure can never fall
back to an older success.

## Typed evaluations and evidence coverage

The Kattis PPF-style package is a typed proof graph, not a directory convention. Static
`EvaluationSpec` records define how admitted normative plan records and obligations are exercised by
exact probes, fixtures, validators, and campaign policy without authoring the result:

```python
EvidenceRole = Literal[
    "fixture-input",
    "state-before",
    "candidate-artifact",
    "probe-result",
    "validator-result",
    "state-after",
    "release-artifact",
    "diagnostic",
]


class EvaluationSpec(FrozenTransport):
    evaluation_id: EvaluationID
    plan_revision_id: PlanRevisionID
    obligation_ids: tuple[ObligationID, ...]

    probe_id: ProbeID
    fixture_id: FixtureID
    validator_ids: tuple[ValidatorID, ...]
    campaign_spec_id: CampaignID

    purpose: Literal[
        "baseline",
        "red",
        "candidate",
        "repair",
        "adversarial",
        "regression",
        "release",
    ]
    expected_outcome: Literal["supports", "refutes"]
    required_evidence_roles: tuple[EvidenceRole, ...]


class EvidenceBinding(FrozenTransport):
    evaluation_id: EvaluationID
    evidence_role: EvidenceRole
    artifact_digest: ArtifactDigest
    rollout_id: RolloutID
    event_id: SHA256
    observation_id: ObservationID | None
```

The exact wire binding to the supplied Kattis evaluation-workflow extension is generated only from
the admitted upstream PPF documents; local contracts must not fabricate an incompatible upstream
shape. The semantic requirements above remain mandatory regardless of the generated field names.

`EvaluationOccurrence` is derived from matching `probe-started` and `probe-completed` rollout events
that name the same evaluation, plus their event-linked observations. `EvidenceBinding` assigns an
allowed semantic role to an exact artifact at a reachable event; the role vocabulary is closed and
an evaluation may require only roles applicable to its purpose. `EvaluationResult` is derived by
applying the evaluation's validators and expected outcome to those observations and bindings. None
of these records is authored or accepted directly from an adapter.

`EvidenceCoverage` is the derived transitive closure:

```text
normative PlanArtifactOccurrence record
  → compiled Obligation
  → EvaluationSpec
  → ProbeSpec + FixtureSpec + FixtureManifest + ValidatorSpec
  → Attempt.input_closure
  → RolloutOccurrence
  → probe-started/probe-completed RolloutEvents
  → ProbeObservation
  → exact evidence ArtifactProduction
  → EvaluationResult
```

`EvidenceCoverage` stops at evaluation results so derivation remains acyclic. Qualification and
verdicts consume only complete coverage and the package manifest then records their support edges.

Coverage is complete only when:

- every admitted normative invariant, acceptance criterion, and failure mode maps to at least one
  obligation;
- every applicable obligation maps to at least one typed evaluation, or has a purely derived
  not-applicable disposition with its applicability inputs bound;
- every evaluation closes over existing, admitted plan, obligation, probe, fixture, validator, and
  campaign-spec identities and is bound by the attempt's input closure;
- the probe's obligation and fixture references exactly agree with its evaluation;
- the fixture materialized in the rollout matches the bound `FixtureManifest.tree_digest`;
- every required evidence role resolves to an exact artifact consumed or produced by a reachable
  event in that evaluation occurrence; and
- every evaluation result is derived from complete event-linked observations under the bound
  validators.

An orphan plan requirement, obligation, evaluation, probe, fixture, observation, evidence artifact,
or result is a coverage gap. Required coverage gaps derive `indeterminate` and block verdict and
promotion; presence of files in the package never implies semantic coverage.

## Rollout lineage

The qualification lifecycle is:

```text
plan
  → obligations
  → candidate
  → attempt
  → rollout
  → observations
  → verdict
```

An attempt declares execution intent: its candidate, selected obligations and probes, environment,
controller, and complete `InputClosure`. A rollout is the causal record of the actual execution of
that intent: operations, tool invocations, fixture materialization, candidate and probe execution,
artifact production, failures, and diagnostics. Attempt state, graph state, controller logs, and
marimo cell state are not substitutes for a rollout journal.

The initial transport contract is:

```python
class RolloutOccurrence(FrozenTransport):
    rollout_id: RolloutID
    attempt_id: AttemptID
    input_closure_digest: SHA256

    producer: ComponentArtifactIdentity
    producer_session_id: NonEmptyString
    source_contract_digest: SHA256

    first_event: NonNegativeInt
    last_event: NonNegativeInt

    event_stream_artifact: ArtifactDigest
    event_stream_digest: SHA256

    status: Literal[
        "open",
        "completed",
        "failed",
        "cancelled",
        "indeterminate",
    ]


class RolloutEvent(FrozenTransport):
    rollout_id: RolloutID
    sequence: NonNegativeInt

    event_id: SHA256
    previous_event_id: SHA256 | None
    causal_parent_id: SHA256 | None

    kind: Literal[
        "agent-message",
        "tool-call",
        "tool-result",
        "shell-call",
        "shell-result",
        "artifact-produced",
        "probe-started",
        "probe-completed",
        "diagnostic",
    ]

    actor: ComponentArtifactIdentity
    operation_contract_digest: SHA256 | None
    evaluation_id: EvaluationID | None

    input_artifacts: tuple[ArtifactDigest, ...]
    output_artifacts: tuple[ArtifactDigest, ...]

    outcome: Literal[
        "pending",
        "running",
        "succeeded",
        "failed",
        "indeterminate",
    ]


class ArtifactProduction(FrozenTransport):
    artifact_digest: ArtifactDigest
    rollout_id: RolloutID
    producing_event_id: SHA256
    media_type: NonEmptyString
    schema_digest: SHA256 | None


class ProbeObservation(FrozenTransport):
    observation_id: ObservationID
    evaluation_id: EvaluationID
    attempt_id: AttemptID
    rollout_id: RolloutID
    producing_event_id: SHA256

    probe_id: ProbeID
    obligation_ids: tuple[ObligationID, ...]

    observed_artifact_digest: ArtifactDigest
    outcome: Literal["supports", "refutes", "indeterminate"]
```

`ComponentArtifactIdentity` includes a rollout-producer role in addition to the controller, runner,
and fingerprint-adapter roles. `source_contract_digest` binds the exact producer-to-rollout adapter
contract; per-event `operation_contract_digest` binds the invoked operation contract when one
exists. Runtime handoff is the first producer adapter: qualification consumes its bounded sessions,
paired operation/result events, states, failures, validation projections, Git tree identities, and
canonical serialization rather than introducing another Codex transcript parser.

For a Codex App Server producer, the final Plan Mode `plan` item is a proposed plan artifact and may
enter the normal plan admission/approval path. `turn/plan/updated` notifications are observed stepped
plan updates for the rollout journal and `RolloutProjection`; they are never a `PlanRevision`, an
evaluation result, or evidence of obligation satisfaction. Tool/result and item lifecycle events
remain the causal execution surface.

Every event ID is derived, never caller-chosen, from domain-separated canonical event content with
the `event_id` field omitted. Event sequences are contiguous from `first_event` through
`last_event`; the first event has no previous event, every later event names the immediately prior
event, and any causal parent names an earlier event in the same rollout. The event-stream artifact
digest identifies exact stored bytes, while `event_stream_digest` is the domain-separated digest of
the canonical ordered event sequence. Both must validate independently.

Rollout journals are append-only. An open `RolloutOccurrence` identifies the immutable stream prefix
visible in its containing snapshot; appending or sealing creates a new content-addressed root
revision and never overwrites an older prefix. Only these transitions are legal:

```text
open → open
open → completed | failed | cancelled | indeterminate
```

Terminal occurrences cannot gain events or change status. V0 admits at most one rollout per
attempt; a retry creates a new attempt and rollout. `ArtifactProduction` must name an
`artifact-produced` event that outputs the exact artifact. An observation must name a terminal
`probe-completed` event whose outputs contain its exact observed artifact, and its obligation IDs
must exactly equal the static probe-to-obligation mapping.

`probe-started` and `probe-completed` events require `evaluation_id`; all other event kinds leave it
null unless their operation is explicitly part of that evaluation. The observation's evaluation ID
must match its producing event and `EvaluationSpec`.

Rollout status describes execution-record integrity, not the candidate or probe result. `completed`
means the controlled journal reached its expected end even when a probe refuted a claim; that is how
fresh red remains qualifying evidence. `failed`, `cancelled`, and `indeterminate` identify producer,
infrastructure, or control failures and route to blocking results. At seal, a completed rollout has
no operation left pending or running: every tool or shell call has exactly one later causally linked
terminal result. An unpaired call forces an indeterminate rollout.

A verdict requires all of the following:

```text
attempt.input_closure_digest == rollout.input_closure_digest
the rollout is terminal and is the sole rollout for the attempt
the admitted event window is contiguous and its hash and causal links validate
every observation references an admitted reachable rollout event
every evidence artifact is consumed or produced by a reachable rollout event
every observation artifact is produced by its named probe-completed event
every applicable obligation has a complete typed EvaluationResult
the EvidenceCoverage graph has no required missing or orphan node or edge
```

Missing events, unexplained artifacts, identity disagreement, a nonterminal rollout, or an invalid
stream makes the lineage indeterminate and blocks qualification. A completed process exit alone
does not make an invalid rollout admissible.

## Campaign rollout structure

A complete TDD campaign preserves distinct execution contexts rather than flattening them into one
session:

```python
class Campaign(FrozenTransport):
    campaign_id: CampaignID
    plan_revision_id: PlanRevisionID

    baseline_rollout_ids: tuple[RolloutID, ...]
    candidate_rollout_ids: tuple[RolloutID, ...]
    adversarial_rollout_ids: tuple[RolloutID, ...]
    regression_rollout_ids: tuple[RolloutID, ...]
    release_rollout_ids: tuple[RolloutID, ...]
```

Rollout IDs are unique across the campaign tuples and tuple order is execution order.
`baseline_rollout_ids` contains test-proposal and fresh-red executions;
`candidate_rollout_ids` contains initial candidate and later repair executions;
`adversarial_rollout_ids`, `regression_rollout_ids`, and `release_rollout_ids` contain their named
purposes. Each rollout binds its own attempt and closure, and every attempt binds the static
`CampaignSpec` rather than the post-execution `Campaign`; this avoids a digest cycle through rollout
membership. The kernel derives, rather than trusts, fresh red before implementation, candidate green
after implementation, reproducible counterexamples, independent regression closure, and equality
between the qualified candidate and production artifact.

## Deterministic identity laws

Use SHA-256 with explicit domain prefixes. Structured values use RFC 8785 canonical JSON restricted
to strings, booleans, null, arrays, objects, and integers in this inclusive range:

```text
-9_007_199_254_740_991 <= integer <= 9_007_199_254_740_991
```

All floating-point values and non-finite numbers are forbidden. Authoritative JSON byte ingress
strictly decodes UTF-8, preserves object pairs, rejects duplicate keys, rejects floats through
`parse_float`, and rejects `NaN` and infinities through `parse_constant` before Pydantic receives a
mapping. Recursive validation admits only objects, arrays, strings, canonical-range integers,
booleans, and null; it rejects lone Unicode surrogate code points in keys and values and all
unsupported values. `FrozenMap` provides deep immutability and rejects canonical-key collisions
after decoding; it cannot substitute for raw-key duplicate detection. NFC normalization applies to
repository paths only, never to arbitrary JSON strings.

Snapshot identity is non-recursive: a `SnapshotEnvelope` does not contain its own digest. Revision
zero has no parent; revision `n` names the digest of revision `n - 1`. An observation binds its
attempt and source closure, never the snapshot created by admitting that observation.

Repository paths are UTF-8, NFC, POSIX-relative paths. The v0 rooted glob grammar supports literal
segments, `*`, `?`, and complete-segment `**`. Exclusivity is operational rather than a claim about
whole pattern languages: every tracked path and every path changed by a proposed transition must
match exactly one class. Renames are deletion plus addition, and both endpoints are reclassified
before admission. Unclassified, multiply classified, protected, cross-capability, or out-of-phase
generated changes fail closed.

Use distinct tree and delta identities throughout:

```text
base_tree₁             base tree
approved_test_patch₁   approved test delta
accepted_test_tree₁    resulting accepted-test tree
implementation_patch₁ implementation delta
candidate_tree₁        resulting candidate tree
```

The same naming law applies to the second cycle. `base_tree₂ = candidate_tree₁` means exact tree
identity, not behavioral or patch equivalence.

## Counterexample and promotion algebra

Each counterexample binds its reproduction evidence and exactly one v0 `regression_probe_id` plus a
closed declarative `expected_non_reproduction_matcher`. Matcher selectors are limited to fields in
the typed raw-evidence schema; executable code and arbitrary selectors are forbidden.

Derive qualification in this acyclic order:

```text
fresh rollout-valid authoritative observations
  → EvaluationOccurrence and EvidenceBinding
  → EvaluationResult
  → complete EvidenceCoverage
  → individual probe qualification
  → regression_probe_qualified
  → counterexample_resolved_for(plan)
  → applicable open counterexamples
  → adversarial_campaign_qualified
  → obligations
  → candidate promotion
  → release-artifact promotion
```

`regression_probe_qualified(counterexample, plan)` requires the selected observation to use the
counterexample's exact regression probe, bind the exact plan and candidate closure, be fresh,
authoritative, terminal, and successful, and satisfy the non-reproduction matcher. It must not
consult counterexample openness, campaign qualification, obligations, or promotion.

A counterexample is resolved for a plan only when the plan is in the applicable descendant lineage,
explicitly addresses it, and its regression probe qualifies. An adversarial campaign qualifies only
when every required adversarial probe qualifies and no applicable counterexample remains open after
deriving regression resolutions. Counterexamples remain stored as historical evidence.

`project_next_route` must preserve the distinction between counterexample resolution and missing
regression coverage:

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
open-counterexample terminal route. The required regression probe is selected before aggregate
campaign promotion or other incomplete-coverage routing.

Relational satisfaction remains separate from evidence qualification. Infrastructure, execution,
resource, integrity, stale-closure, baseline, or incomplete-coverage results block qualification
even if an authored permitted/required relation is otherwise satisfied. Promotion is derived only
after every blocking obligation has fresh qualifying evidence.

## Subject-to-production realization

Behavioral qualification is not release qualification. Every promoted subject must have one
admitted `SubjectBinding` that binds the exact proof candidate, production wheel, console entry
point, shared observation core, and complete production adapter artifact set:

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

The wheel must contain a generated, declarative operation registry used directly by runtime
dispatch. Static inspection reads wheel metadata, the registry, and packaged bytes without importing
application modules. It verifies the entry point, the `observe` target, the shared-core digest, and a
domain-separated digest of the adapter artifacts responsible for request decoding, dispatch,
exception normalization, serialization, stream separation, and exit-code mapping.

The adapter manifest cannot define its own coverage. V0 fixes the required semantic roles and wheel
scope: unique entry-point metadata, `tdd_agent_skills/jj_agent/operations-v0.json`,
`tdd_agent_skills/jj_agent/adapter-artifacts-v0.json`,
`tdd_agent_skills/generated/jj_agent.py`, and every regular file beneath
`tdd_agent_skills/jj_agent/`. Static inspection recomputes that complete set from wheel contents,
requires every role to resolve inside it, rejects dynamic project-owned imports outside the fixed
scope and separately bound core, and hashes canonical sorted wheel-path/exact-byte-digest pairs. A
manifest that omits a file or role is invalid.

The qualified candidate_tree₂ is a production-path harness. It may supply fixture paths and requests,
but must execute the absolute console script installed from the exact bound wheel:

```text
candidate_tree₂ harness
  → installed console entry point
  → CLI/request decoding
  → declarative operation registry
  → observe dispatcher
  → shared safe core S
  → result serialization
  → stdout/stderr and exit-code mapping
```

Direct core comparison is identity evidence only; it is never the qualifying execution path.
Runtime dispatch evidence must agree with independent static inspection, the subject binding, and
the input closure.

Release-artifact promotion requires the exact wheel, entry point, production-path execution,
registry target, shared core, production adapter, candidate_tree₂, controller, runner, fingerprint
adapter, environment, and dependency identities to match the closure, in addition to all probe,
counterexample, campaign, and obligation gates.

Environment equality is canonical rather than caller-declared. The execution identity binds the
implementation/version/ABI/platform tuple, exact interpreter and standard-library/runtime file
closure, sanitized environment, working-directory policy, and sandbox profile. The dependency
identity binds the exact lockfile and a PEP-503-name-sorted set of installed distributions, each with
version, source-wheel digest, and digest of every regular installed file named by `RECORD`.
Controller, runner, and fingerprint-adapter identities are sorted path/exact-byte-digest manifests.
Paths are resolved against their declared repository, wheel, or disposable-environment root;
missing, duplicate, outside-root, extra, or symlink entries fail closed.

## Persistence and artifact custody

Snapshots and artifacts are immutable content-addressed objects. Workflow heads are mutable pointers
protected by a per-workflow lock. `compare_and_swap` must reject unless:

```text
new_envelope.workflow_id == current.workflow_id
new_envelope.revision == expected_revision + 1
new_envelope.parent_snapshot_digest == expected_digest
digest(stored new_envelope) == new_head.snapshot_digest
```

The current head must match the expected revision and digest before anything is replaced. Head
updates use same-directory temporary files, flush and `fsync`, atomic replacement, and directory
`fsync`.

After `just test-clean-locked`, release custody is:

```text
wheel bytes
  → put_artifact
  → production_distribution_digest
  → admitted SubjectBinding
  → static inspection from store
  → production-path proof from store
  → packaging checks from store
  → publication input by digest
```

No later stage may trust a mutable build-directory pathname. Rebuilt or replaced bytes require a new
digest, binding, admission, and proof. Publication is outside v0 implementation authority, but any
future release command must consume the qualified digest or a digest-verified materialization.

The exportable evidence package includes rollout identity, journals, projections, and diagnostics:

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

The canonical package binds the typed chain from normative plan records through obligations,
evaluation specifications, probes, fixtures, attempts, causal rollouts, observations, exact evidence,
evaluation results, and derived decisions. The manifest includes a digest of the complete
`EvidenceCoverage` projection and rejects any orphan or required missing node or edge. Detailed
prompts, tool payloads, and terminal output may remain private content-addressed artifacts, but their
digests, evidence roles, evaluation bindings, and required relationships remain in the manifest so
privacy does not weaken lineage validation.

Marimo is an optional reactive projection over the canonical journal:

```text
canonical rollout journal
  → live RolloutProjection
  → observation and obligation projections
  → verdict and promotion controls
```

A new event may update active operations, generated artifacts, probe state, failures, observation
availability, obligation status, and campaign completeness. Marimo never creates canonical events,
observations, qualifications, or decisions; rebuilding the canvas from the same admitted package
must produce the same projection.

The derived qualification SBOM may expose only the rollout digest, producer identity, input-closure
digest, event-stream digest, terminal status, artifact relationships, and observation relationships:

```text
Attempt executedAs Rollout
Rollout used ControllerArtifact
Rollout ranIn ExecutionEnvironment
Rollout consumed BaseState
Rollout produced CandidateState
Rollout produced EvidenceArtifact
Observation derivedFrom RolloutEvent
Evaluation exercised Obligation
Evaluation used Probe
Evaluation used Fixture
EvaluationResult supportedBy EvidenceArtifact
Verdict supportedBy Observation
Verdict supportedBy EvaluationResult
```

Omitting private event bodies from the public SBOM is a disclosure policy, not permission to omit
them from the private canonical evidence package used for qualification.

## Execution trust and proof obligation

Authoritative production attempts run in a fresh disposable interpreter environment with a
controlled import path, empty initial application module cache, checkout and user site excluded,
sanitized environment, bound dependencies, and before/after integrity fingerprints. `trusted-local`
is permitted for the v0 proof only when evidence explicitly states that host isolation was not
provided. An untrusted campaign must block without a qualified stronger sandbox.

The vertical proof uses a dedicated proof-fixture repository, never a deliberately regressed
production adapter. The unsafe candidate_tree₁ observer exists only in that repository or its test
fixtures: it is outside the production package, cannot be imported from the production package, is
not exposed through `jj-agent`, and is not referenced by production skills. Production `jj-observe`
uses the safe core from its first implementation.

```text
proof fixture repository
  base_tree₁ + approved_test_patch₁             → accepted_test_tree₁
  accepted_test_tree₁ + implementation_patch₁   → candidate_tree₁ unsafe fixture
  base_tree₂ = candidate_tree₁
  base_tree₂ + approved_test_patch₂             → accepted_test_tree₂
  accepted_test_tree₂ + implementation_patch₂  → candidate_tree₂ production-path harness

qualification project
  safe production adapter
    ← invoked through the installed production path by candidate_tree₂
```

Plan₁ reaches red and positive green in the proof fixture before CE₁ reproduces the mutation gap.
Plan₂ addresses CE₁, starts from exact `base_tree₂ = candidate_tree₁`, preserves inherited
accepted-test blobs, and reaches fresh red and safe green. Candidate_tree₂ invokes the stored wheel
through its absolute installed console entry point; it never imports or calls the shared core
directly. Promotion requires fresh regression evidence, complete adversarial coverage, exact subject
realization, and release-artifact identity.

## Assumptions and deferred scope

- Python 3.14 and Jujutsu 0.43.x are the v0 compatibility families.
- The wheel is the executable release artifact; the sdist retains packaging checks but does not
  establish runtime execution identity.
- Exact supplied Kattis PPF 0.2.0 inputs are required before contract implementation.
- Distributed workers, leases, multi-writer workflows, generalized event-sourcing infrastructure,
  generalized workflow runtimes, live agent SDK execution, and publication remain deferred. The
  bounded rollout journal required by qualification is not deferred.
- A marimo execution runtime is deferred; a marimo view, when present, is a derived projection only.
- Existing packaging, licensing, metadata, lockfile, and `just` checks remain mandatory.
- Until the deferred `jj-agent` runtime and vertical proof are implemented, `just qualify` remains
  the repository's existing qualification gate and does not itself establish this future proof.

## Semantic acceptance

- No authored or adapter-produced conclusion can bypass the pure kernel.
- Counterexample resolution has no dependency on aggregate campaign qualification.
- Counterexample routing selects missing required regression evidence instead of treating an
  addressed counterexample as a terminal open-counterexample blocker.
- Canonical JSON, repository surfaces, snapshots, and store transitions fail closed.
- Every qualifying observation has a valid attempt, rollout, producing event, and exact artifact
  lineage; broken, incomplete, or nonterminal rollouts block qualification.
- Typed evaluations close normative plan records over obligations, probes, fixtures, validators,
  rollouts, observations, and role-labeled evidence; orphan or missing coverage blocks promotion.
- Campaign phases remain separate rollout lineages, and red/green ordering is derived rather than
  authored.
- Unsafe proof code is structurally absent from the production package, CLI, and skills.
- candidate_tree₂ qualification traverses the complete installed production entry point.
- Static inspection executes no wheel application code.
- Every release consumer retrieves or verifies the wheel by its admitted digest.
- The evidence package and public SBOM preserve rollout and artifact relationships without requiring
  disclosure of private event bodies.
- Codex proposed-plan items and stepped plan updates retain proposal and rollout-projection authority
  respectively and cannot bypass plan admission or evaluation derivation.
- Behavioral, candidate, and release-artifact qualification are separately derived and all required
  for promotion.
