# OSCAL Agentic GitOps Controller

## Governed-project and controller profile proposal

| Field | Value |
|---|---|
| Status | Migrated and normalized for architecture review |
| Parent specification | Kernel Spec Model A |
| Profile namespaces | Governed project, controller, and binding |
| Original source | `fatb4f/cuestrap@main:docs/cuestrap-governed-repository-controller-proposal.md` |
| Original source blob | `9fe2cb6708d0c2a8a98f2d03cdaae2754c139f36` |
| Original title | Cuestrap Governed Repository Controller |

## 1. Migration decision

The original proposal incorrectly assigned the identity of the complete controller architecture to CUEstrap. CUEstrap is the upstream CUE-pattern qualification laboratory. The proposal actually contains:

```text
Model A semantic specification concepts
+ Model B and generated API concepts
+ compiler-kernel contracts
+ governed-repository project semantics
+ OSCAL agentic GitOps controller semantics
+ one controller/project binding
```

The base compiler concepts now belong to Kernel Spec. The controller-specific concepts are retained here as a downstream profile.

## 2. Profile decomposition

```text
Kernel Spec Model A
    ├── OSCALGovernedRepositoryProject
    ├── OSCALAgenticGitOpsController
    └── ControllerProjectBinding
```

### Governed project

The project owns:

- one shared OSCAL-centered typed semantic graph;
- immutable graph checkpoints and ordered transition events;
- normative, implementation, qualification, assessment, runtime, and governance partitions;
- findings, risks, remediation obligations, and authorization posture;
- OSCAL lifecycle projections;
- repository settlement and publication policy.

### Controller

The controller owns only qualified, bounded capabilities to:

- observe project and runtime state;
- normalize source records into event proposals;
- request deterministic graph folds;
- invoke qualified assessment procedures;
- derive technical posture under accountable authorization;
- propose admissible transitions;
- execute explicitly delegated one-use effects;
- collect receipts and reconcile outcomes;
- request constrained Git publication.

### Binding

The binding identifies exact project, controller, policy, procedure, evidence, operation, projection, and capability revisions. It narrows authority and cannot silently expand it.

## 3. Semantic center

The architectural center is one continuously revised typed semantic graph.

```text
qualified graph checkpoint
        +
ordered admitted transition events
        +
pinned policy, procedure, and kernel revisions
        ↓
deterministic graph fold
        ↓
next graph revision
        ├── implementation and control state
        ├── evidence and assessment state
        ├── findings, risks, and remediation
        ├── System A and System B conclusions
        ├── derived technical posture
        ├── delegated capability envelope
        └── OSCAL lifecycle projections
```

System A and System B are independently evidenced partitions of the same graph, not competing semantic universes.

## 4. Authority hierarchy

| Tier | Authority | Responsibility |
|---|---|---|
| 0 | Git OIDs and cryptographic digests | Exact source, checkpoint, event, artifact, receipt, and publication identity |
| 1 | Accountable authorization records and official OSCAL resources | Organizational authorization, risk acceptance, lifecycle identity, controls, assessments, risks, and remediation |
| 2 | Kernel Spec CUE contracts through a qualified implementation | Graph integrity, transition relations, assessment semantics, posture derivation, effect bounds, and projection requirements |
| 3 | Qualified operational evidence | Observations, receipts, attestations, tests, counterexamples, and assessment invocations |
| 4 | Canonical graph checkpoints and event ledger | Reproducible causal history and current semantic state |
| 5 | Materialized analytical projections | DuckDB, indexes, caches, metrics, and reactive views |
| 6 | Generated transports | Go/Python types, JSON Schema, OpenAPI, GraphQL, CLI, MCP, reports, and dashboards |

A derived tier may be regenerated or replaced. It may not redefine a lower tier.

## 5. Core invariants

1. Every authority-bearing fact is representable in one typed semantic graph.
2. Every causal graph change is an immutable ordered event.
3. Every authority-bearing candidate is normalized, frozen, and content-addressed before qualification.
4. Successful execution does not itself establish authorization, evidence, settlement, or conformance.
5. Reactive recomputation is non-effectful by default.
6. Authoritative conclusions require exact currently qualified procedures and evidence cutoffs.
7. Analytical and transport projections cannot become parallel authorities.
8. Composition preserves independent provenance.
9. Formal authorization remains with an accountable organizational authority.
10. Every effect requires a separate, narrowed, expiring capability.

## 6. Graph partitions

The graph exposes bounded partitions for:

- **normative** — controls, objectives, parameters, requirements, and policy relations;
- **implementation** — components, capabilities, resources, responsibilities, and target state;
- **qualification** — procedures, generators, witnesses, mutations, properties, and receipts;
- **System A** — target observations, objective results, findings, risks, and target conclusions;
- **System B** — proposals, admission, dispatch, runtime evidence, continuity, conformance, and attribution;
- **governance** — formal authorization, conditions, posture, delegated envelope, settlement, and publication.

Every node and relation retains authority owner, source coordinates, revision coordinates, and evidence status.

## 7. State and event model

The controller distinguishes:

- repository snapshots;
- graph checkpoints;
- operation bases;
- prior-settled checkpoints;
- candidate checkpoints;
- rebuildable projection checkpoints.

Raw runtime or repository records become canonical events only after deterministic normalization, source binding, identity reconciliation, structural validation, and transition admission.

The durable ledger uses immutable, checksummed, digest-chained event segments. Batch replay and incremental folding must produce equivalent graph revisions and conclusions.

## 8. Admission law

A bounded effect is admitted only when all applicable predicates hold:

```text
current graph and repository identities
∧ current policy and kernel identities
∧ current qualified procedures
∧ System A technical eligibility
∧ System B readiness and trusted continuity
∧ qualified tactical conclusion
∧ current posture permits the operation
∧ accountable authorization conditions remain valid
∧ exact parent decision authorizes the bundle
∧ requested effects fit the narrowed capability
∧ no unresolved identity, evidence, event, or projection conflict
```

Admission is prospective. Later success cannot repair missing initiation authority.

## 9. Effect and capability boundary

Effects use a closed mutation vocabulary rather than ambient tool access.

At minimum, Git capabilities distinguish:

- object construction;
- index or worktree mutation;
- commit construction;
- authoritative reference movement;
- remote publication.

A capability to construct a commit does not imply authority to move `main`. Every grant binds exact actor, operation, graph, policy, event cutoff, repository snapshot, authorization, parent decision, allowed effects, epoch, expiry, and maximum uses.

## 10. Authorization posture

Formal authorization and risk acceptance are externally accountable governance facts.

The controller derives a technical posture such as:

```text
authorized
conditional
suspended
revoked
indeterminate
```

Posture is derived from exact graph, policy, event, procedure, evidence, authorization, finding, risk, condition, and continuity coordinates. It constrains subsequent operations but never replaces the formal authorization record.

## 11. Evidence and qualification

Raw output becomes evidence through:

```text
immutable source reference
→ deterministic normalization
→ subject and claim binding
→ qualified procedure invocation
→ concrete invocation receipt
→ observation, finding, risk, remediation, or posture fact
```

Procedure qualification and concrete invocation are separate evidence classes. A successful invocation cannot qualify itself, and a qualification receipt cannot substitute for a concrete assessment result.

## 12. Continuous evaluation

The continuous loop is:

```text
new source record or time boundary
→ immutable capture
→ semantic event proposal
→ admission and graph fold
→ graph revision advancement
→ analytical materialization refresh
→ affected-subject invalidation
→ qualified assessment invocation
→ findings, risks, remediation, and posture update
→ OSCAL projection refresh
→ next bounded operation evaluation
```

Observation and recomputation continue even when no mutation is authorized.

The evaluator supports stateless, keyed stateful, windowed, and lifecycle/sequence evaluation through the same semantic kernel.

## 13. Runtime and analytical profiles

DuckDB may materialize revision-bound semantic, temporal, metric, assessment, risk, posture, and projection relations. Marimo may orchestrate a reactive DAG over those relations.

Neither owns semantic conclusions. Every authority-bearing DAG node and edge declares typed inputs, outputs, dependencies, preconditions, postconditions, failure behavior, and qualification evidence.

Alternative streaming or reactive runtimes may replace scheduling mechanics only if they preserve qualified batch, incremental, replay, and restart equivalence.

## 14. OSCAL projections

Official OSCAL resources remain portable governance and lifecycle representations:

- Catalog;
- Profile;
- Component Definition;
- System Security Plan;
- Assessment Plan;
- Assessment Results;
- POA&M;
- authorization package records.

OSCAL projectors preserve stable UUIDs, source links, graph and event coordinates, lineage, projector identity, source-set digest, artifact digest, and official-schema validation receipt.

CUE evaluates the bounded semantic profile. Official OSCAL schemas validate complete OSCAL artifacts.

## 15. Model B and generated adapters

The controller profile compiles through the Kernel Spec IR family.

```text
Model A closure
    ├── API IR / Model B
    ├── OSCAL lifecycle IR
    ├── evaluation IR
    ├── runtime/controller IR
    └── documentation IR
```

Generated transports include Go and Python types, JSON Schema, OpenAPI, GraphQL, CLI, MCP, database bindings, tests, reports, and dashboards. They record source and generator revisions and cannot be hand-edited as independent contract authorities.

LLM output is always untrusted candidate data constrained to closed schemas and revalidated through the semantic kernel. Model confidence is not evidence quality.

## 16. Settlement

Execution admission is not settlement.

```text
operation admitted
→ one-use effect execution
→ runtime record reconciliation
→ graph advancement
→ independent System A recapture
→ System B conformance and attribution assessment
→ finding, risk, metric, and posture recomputation
→ OSCAL validation
→ publication qualification
→ prior-settled checkpoint advancement
```

Settlement fails closed on stale identities, missing receipts, continuity gaps, unresolved conflicts, stale procedures, invalid projections, or publication races.

## 17. Conformance properties

The profile requires executable properties for:

1. deterministic graph folding;
2. batch/stream/replay equivalence;
3. event integrity;
4. provenance-preserving System A/System B composition;
5. procedure currentness;
6. qualification/invocation separation;
7. analytical incremental/rebuild equivalence;
8. reactive non-actuation;
9. DAG qualification and settlement;
10. posture traceability;
11. restriction monotonicity;
12. no unauthorized mutation;
13. freshness enforcement;
14. capability confinement;
15. evidence non-forgery;
16. continuity safety;
17. OSCAL projection traceability;
18. settlement monotonicity;
19. projection rebuildability;
20. negative-witness permanence;
21. publication isolation.

## 18. Implementation stages

The migrated proposal is now ordered under the Kernel Spec bootstrap:

1. base Model A vocabulary and normative object model;
2. project, controller, and binding semantics;
3. compiler, importer, and projection contracts;
4. shared graph vocabulary and revision identity;
5. immutable event-segment and graph-fold contracts;
6. qualified assessment procedure and invocation contracts;
7. analytical and reactive materialization profiles;
8. OSCAL lifecycle and authorization-posture projections;
9. runtime reconciliation and continuity contracts;
10. bounded transition, capability, settlement, and Git publication contracts;
11. generated adapters and model-runtime profiles.

## 19. Migration invariant

This profile no longer defines CUEstrap.

```text
CUEstrap
    qualifies reusable CUE patterns and minimal kernel primitives.

Kernel Spec
    defines the canonical machine-readable compiler specification.

OSCAL agentic GitOps profile
    instantiates Kernel Spec for one governed project and controller.
```

The original proposal remains recoverable through the CUEstrap Git history and the exact source blob recorded above.
