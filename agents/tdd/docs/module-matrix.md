# Required module and namespace matrix

This is a provisional implementation boundary. Generated namespaces and PPF
wire shapes remain provisional until the exact supplied PPF 0.2.0 documents are
inspected and recorded with provenance and digests.

## Namespace rules

```text
tdd_agent_skills.generated.*   frozen transports, enums, and registries
tdd_agent_skills.planning.*    Markdown/source input adapters
tdd_agent_skills.model.*       Model A/B, controls, effects, and transition vocabulary
tdd_agent_skills.runtime.*     pure graph coordinates, snapshots, deltas, and identities
tdd_agent_skills.mutation.*    mutation planning, authorization, occurrence, and evaluation
tdd_agent_skills.semantic.*    pure derivation and validation
tdd_agent_skills.profiles.*    pure PPF decoding, projection, and equivalence
tdd_agent_skills.ports.*       effect-interface protocols
tdd_agent_skills.adapters.*    concrete external-system effects
tdd_agent_skills.evidence_adapters.* tool-specific rollout and observation producers
tdd_agent_skills.control_eval.*     non-authoritative numeric replay and policy scoring
tdd_agent_skills.artifacts.*   canonical bytes, manifests, and identities
tdd_agent_skills.projections.* derived interaction and exchange surfaces
tdd_agent_skills.application.* typed use-case orchestration
tdd_agent_skills.bootstrap.*   concrete dependency assembly
tdd_agent_skills.cli.*         Cyclopts-only command adapters
```

`A → B` means module `A` may import module `B`:

```text
cli
  → bootstrap
  → application

bootstrap
  → application
  → adapters
  → evidence_adapters
  → control_eval
  → generated

application
  → planning
  → model
  → mutation
  → semantic
  → ports
  → profiles
  → generated

planning
  → model
  → generated

model
  → generated

mutation
  → model
  → runtime
  → semantic
  → generated

semantic
  → model
  → generated.mutation
  → generated

profiles
  → model
  → generated

ports
  → model
  → generated

adapters
  → ports
  → profiles
  → artifacts
  → generated

artifacts
  → generated

evidence_adapters
  → ports
  → generated

control_eval
  → model
  → ports
  → artifacts
  → generated

projections
  → generated

generated
  → standard library
  → Pydantic only
```

Concrete adapter construction belongs in `bootstrap`; application modules do
not import concrete adapters. `semantic` may import generated mutation
transports, never mutation orchestration, so the pure packages do not form an
import cycle.

## Module boundaries

| Namespace | Owns | I/O |
| --- | --- | ---: |
| `generated` | Frozen transports, enums, and registries | No |
| `planning` | Markdown parsing and source occurrences | Input adapter only |
| `model` | Model A/B vocabulary, controls, operations, effects, and legal transitions | No |
| `runtime` | Repository coordinates, materialized snapshots, graph deltas, and identities | No |
| `mutation` | Mutation plans, qualification, authorization, occurrences, and decisions | No |
| `semantic` | Pure derivation, reference resolution, and evaluation | No |
| `profiles` | Pure PPF decoding, projection, and equivalence | No |
| `ports` | Protocols for required effects | No |
| `adapters` | Filesystem, subprocess, CUE, and external-tool effects | Yes |
| `evidence_adapters` | Tool-specific rollout, event, and raw-observation production | Yes |
| `control_eval` | Numeric feature projection, replay, and candidate-policy scoring | Through injected ports |
| `artifacts` | Canonical bytes, manifests, and identities | Pure except store adapters |
| `projections` | Derived interaction and portable exchange surfaces | No |
| `application` | Use-case coordination over functions and ports | Through injected ports |
| `bootstrap` | Concrete dependency assembly | During construction |
| `cli` | Cyclopts request/result adaptation | Stdin/stdout/stderr only |

## Core generated contracts

| Module | Principal contents |
| --- | --- |
| `generated/common.py` | Digests, artifact references, source anchors, semantic IDs |
| `generated/diagnostics.py` | Diagnostics, source locations, error envelopes |
| `generated/operations.py` | Immutable request/result transports |
| `generated/qualification.py` | Requirements, obligations, EvaluationSpecs, qualification package |
| `generated/rollout.py` | Attempts, rollout events, observations, and evidence transports |
| `generated/model.py` | Model A/B coordinates, controls, operations, and effect types |
| `generated/runtime.py` | Repository/VCS/blob/module coordinates and graph snapshots |
| `generated/mutation.py` | MutationPlan, PlanQualification, MutationSpec, and MutationOccurrence |
| `generated/delta.py` | GraphDelta and typed before/after relationships |
| `generated/evidence.py` | Proof-graph aggregates, bindings, strength, and coverage |
| `generated/cpython_evidence.py` | Capture integrity, coordinates, values, and runtime observations |
| `generated/control_policy.py` | Belief projections and bounded policy-evaluation summaries |
| `generated/ppf_v0_2_0.py` | Generated projection of the supplied PPF documents only |
| `generated/operation_registry.py` | Declarative operation identities |
| `generated/adapter_registry.py` | Legal adapter/operation relationships |
| `generated/profile_registry.py` | Supplied PPF profile identities |
| `generated/serializer_registry.py` | Media type to serializer identities |
| `generated/cli_registry.py` | Command ID to application operation identities |

Generated models use frozen Pydantic configuration and perform no filesystem,
CUE, serialization, or process effects.

CPython provider implementations live under
`evidence_adapters/cpython/{monitoring,traceback,frames,tracemalloc,faulthandler}.py`.
They may access runtime objects but emit only generated bounded transports. The
pure kernel imports neither these adapters nor python-control.

`control_eval` may import the `control` distribution behind an injected port.
It consumes pure-kernel-admitted legal actions and fixed-dimensional feature
projections, stores raw numerical traces as non-authoritative artifacts, and
returns generated float-free summaries. No semantic, profile, or promotion
module imports `control_eval`.

## Planning and semantic compiler

| Capability | Module | Responsibility |
| --- | --- | --- |
| CommonMark parsing | `planning/markdown.py` | Parse Markdown and retain source positions |
| Source occurrences | `planning/provenance.py` | Produce byte/line anchors and source digests |
| Authored record decoding | `planning/records.py` | Decode CUE-exported records into transports |
| Reference resolution | `semantic/references.py` | Resolve IDs and reject missing or mistyped references |
| Obligation derivation | `semantic/obligations.py` | Compile admitted normative records into obligations |
| Evaluation derivation | `semantic/evaluations.py` | Produce static EvaluationSpecs and coverage |
| Attempt selection | `semantic/attempts.py` | Select the newest eligible completed attempt |
| Rollout validation | `semantic/rollouts.py` | Validate causal event lineage and closure |
| Evidence derivation | `semantic/evidence.py` | Bind observations to admitted evidence |
| Verdict/promotion | `semantic/verdicts.py`, `semantic/promotion.py` | Apply deterministic qualification policy |

Pure entry point:

```python
def compile_semantic_package(
    document: PlanDocument, sidecars: SemanticSidecars
) -> QualificationPackage: ...
```

It accepts values, not paths. CUE validates authored structure and invariants;
the Python kernel owns derivation and qualification policy.

OSCAL is a projection and vocabulary source. It does not own local derivation,
transition decisions, or qualification authority.

## Model authority namespaces

```text
model/
├── model_a.py
├── model_b.py
├── controls.py
├── effects.py
├── operations.py
├── transitions.py
└── evidence_requirements.py
```

| Module | Responsibility |
| --- | --- |
| `model_a.py` | Governed objects, identities, relationships, and control vocabulary |
| `model_b.py` | Operations, requests, responses, and transition surfaces |
| `controls.py` | Control applicability and assessment objectives |
| `effects.py` | Closed effect taxonomy and graph-region semantics |
| `operations.py` | Closed operation definitions and contracts |
| `transitions.py` | Legal source, candidate, and delta relationships |
| `evidence_requirements.py` | Required proof roles and strength classes |

CUE validates authored representations of these values. Pure Python interprets
and derives from them.

## Runtime graph namespaces

```text
runtime/{coordinates,materialization,snapshots,delta,identities}.py
ports/{graph_runtime,repository_runtime,artifact_runtime}.py
adapters/runtime/{vcs,blob,module,workspace}.py
```

Repository, revision, operation, content root, module, and workspace realization
remain distinct typed coordinates.

```python
class GraphRuntime(Protocol):
    def materialize(self, request: MaterializeGraphRequest) -> GraphSnapshot: ...

    def derive_delta(
        self,
        before: GraphSnapshot,
        after: GraphSnapshot,
    ) -> GraphDelta: ...
```

Runtime adapters materialize external state. Pure transition comparison consumes
the resulting snapshots and independently derived `GraphDelta`.

## Mutation lifecycle namespaces

```text
mutation/
├── planning.py
├── qualification.py
├── authorization.py
├── occurrence.py
└── transition_evaluation.py
```

| Module | Canonical objects and responsibility |
| --- | --- |
| `planning.py` | `MutationPlan`, derivation inputs, admissions, and planner projections |
| `qualification.py` | `PlanQualification`, coverage evaluation, and admission results |
| `authorization.py` | Closed `MutationSpec`, `CapabilityEnvelope`, graph regions, and effect budgets |
| `occurrence.py` | `MutationOccurrence` and SDK-native operation events |
| `transition_evaluation.py` | Four-axis `TransitionEvaluation` and `TransitionDecision` |

The four transition axes are authorization, conformance, completion, and
resulting-state validity.

```text
MutationPlan
  → PlanQualification
  → MutationSpec
  → MutationOccurrence
  → GraphDelta
  → TransitionEvaluation
```

## Rollout and evidence architecture

Rollout producers emit canonical execution facts before observations:

```text
role-specific operation
  → MutationOccurrence
  → RolloutOccurrence
  → operation and rollout events
  → raw observations
  → normalized observations
  → evidence bindings
  → pure transition evaluation
```

The proof-graph aggregate binds authored records, obligations, EvaluationSpecs,
attempts, rollouts, events, artifact productions, observations, evidence,
results, verdicts, and exact serialization identities. Evidence adapters never
implement qualification policy.

## Evidence-tool adapters

```text
evidence_adapters/
├── pytest_plugin/
│   ├── plugin.py
│   ├── collector.py
│   ├── hooks.py
│   ├── rollout.py
│   └── observations.py
├── hypothesis/
├── schemathesis/
├── mutmut/
├── coverage/
├── crosshair/
├── atheris/
└── regression/
```

Concrete P1 producers and fixture adapters are:

```text
adapters/rollout/{planner,implementer,adversary,evaluator}.py
adapters/fixtures/{repository,pyfakefs,clock,environment}.py
adapters/process/bounded_subprocess.py
evidence_adapters/regression/pytest_regressions.py
```

The first-party pytest collector projects admitted `EvaluationSpec` records to
stable pytest items. Its hooks and rollout producer emit raw observation
envelopes bound to attempt, rollout, event, and evaluation identities.

Deterministic fixture adapters cover repository state, `pyfakefs`, clock, and
environment values with declared strength classes. The bounded-process adapter
produces typed `inconclusive` results for timeout and sandbox failures. A
first-party regression adapter records canonical projection comparisons.

## PPF profile boundary

Use the supplied version namespace, not a reconstructed Kattis profile:

```text
profiles/ppf/v0_2_0/
```

| Module | Responsibility |
| --- | --- |
| `profile.py` | Pin supplied document identities, provenance, licences, and digests |
| `bindings.py` | Bind local semantic IDs to inspected PPF entities |
| `decoder.py` | Pure `PackageTree → PPFPackage` decoding |
| `projection.py` | Project semantic records into admitted PPF structures |
| `closure.py` | Validate references and cross-record closure |
| `equivalence.py` | Compare semantic equality independent of bytes |

The profile layer never reads paths or invokes tools.

## Reader/decoder split

```text
filesystem path
  → PackageReader
  → PackageTree
  → decode_package_tree
  → typed PPF package
```

```python
class PackageReader(Protocol):
    def read(self, source: PackageSource) -> PackageTree: ...
```

Reader ports and adapters own filesystem/archive access, path normalization,
file modes, byte loading, symlink policy, and tree digests:

```text
ports/package_reader.py
adapters/package/directory_reader.py
adapters/package/archive_reader.py
```

The pure decoder owns recognized paths, structured-file decoding, defaults,
cross-file references, profile closure, and semantic diagnostics.

## Application and composition

Application services are stable callable SDK functions:

```text
application/compile.py       compile_package
application/import_package.py import_package
application/project.py       project_package
application/validate.py      validate_package
application/plan_mutation.py plan_mutation
application/authorize_mutation.py authorize_mutation
application/execute_mutation.py execute_mutation
application/qualify_transition.py qualify_transition
application/verify_promotion.py verify_promotion
```

Composition root:

```python
def build_application() -> Application: ...
```

It wires application services, CUE adapters, runtime and package ports,
role-specific rollout producers, generated registries, and artifact stores.

Promotion verification requalifies the exact release artifact through its own
attempt, rollout, observations, and evidence before producing authoritative
`PromotionAuthorization`. Publication remains outside v0.

## Cyclopts boundary

```text
argv
  → generated request
  → application service
  → generated result
  → one JSON document
```

```text
src/tdd_agent_skills/
├── __main__.py
├── bootstrap/
│   ├── __init__.py
│   └── application.py
└── cli/
    ├── __init__.py
    ├── app.py
    ├── errors.py
    ├── io.py
    ├── package.py
    └── rendering.py
```

`__main__.py` delegates to `tdd_agent_skills.cli.main`; the project script
remains `tdd_agent_skills.cli:main`.

## Canonical provisional tree

```text
src/tdd_agent_skills/
├── __init__.py
├── __main__.py
├── py.typed
├── generated/
│   ├── common.py
│   ├── diagnostics.py
│   ├── delta.py
│   ├── evidence.py
│   ├── model.py
│   ├── mutation.py
│   ├── operations.py
│   ├── qualification.py
│   ├── rollout.py
│   ├── runtime.py
│   ├── ppf_v0_2_0.py
│   ├── operation_registry.py
│   ├── adapter_registry.py
│   ├── profile_registry.py
│   ├── serializer_registry.py
│   └── cli_registry.py
├── planning/{markdown,provenance,records}.py
├── model/{model_a,model_b,controls,effects,operations,transitions,evidence_requirements}.py
├── runtime/{coordinates,materialization,snapshots,delta,identities}.py
├── mutation/{planning,qualification,authorization,occurrence,transition_evaluation}.py
├── semantic/
│   ├── attempts.py
│   ├── evidence.py
│   ├── evaluations.py
│   ├── obligations.py
│   ├── promotion.py
│   ├── references.py
│   ├── rollouts.py
│   └── verdicts.py
├── profiles/ppf/v0_2_0/{bindings,closure,decoder,equivalence,profile,projection}.py
├── ports/
│   ├── artifact_runtime.py
│   ├── graph_runtime.py
│   ├── evidence.py
│   ├── package_reader.py
│   ├── package_writer.py
│   ├── process.py
│   ├── repository_runtime.py
│   ├── rollout.py
│   └── semantic_engine.py
├── adapters/
│   ├── cue/
│   ├── fixtures/{repository,pyfakefs,clock,environment}.py
│   ├── package/
│   ├── process/bounded_subprocess.py
│   ├── rollout/{planner,implementer,adversary,evaluator}.py
│   └── runtime/{vcs,blob,module,workspace}.py
├── evidence_adapters/
│   ├── pytest_plugin/{plugin,collector,hooks,rollout,observations}.py
│   ├── hypothesis/
│   ├── schemathesis/
│   ├── mutmut/
│   ├── coverage/
│   ├── crosshair/
│   ├── atheris/
│   └── regression/pytest_regressions.py
├── artifacts/{canonical_json,identity,manifest}.py
├── projections/{marimo,qualification_sbom}/
├── application/
│   ├── authorize_mutation.py
│   ├── compile.py
│   ├── execute_mutation.py
│   ├── import_package.py
│   ├── plan_mutation.py
│   ├── project.py
│   ├── qualify_transition.py
│   ├── validate.py
│   └── verify_promotion.py
├── bootstrap/{__init__,application}.py
└── cli/{__init__,app,errors,io,package,rendering}.py
```

This tree is provisional until exact PPF inspection establishes generated
namespaces and wire shapes.

## Capability integration status

Status legend:

- **F** — explicit in the authoritative matrix.
- **P** — represented but requiring additional contracts or adapters.
- **D** — intentionally deferred from the compiler/core-transition slice.
- **M** — materially missing and not yet assigned a module boundary.

| Capability | Status | Architectural placement |
| --- | ---: | --- |
| Unified semantic authority | **F** | `model`, CUE-authored validation, pure `semantic`/`mutation` policy |
| Repository-state model | **F** | `runtime`, runtime ports, and `adapters/runtime` |
| Mutation planning | **F** | `mutation/planning.py` |
| Plan qualification | **F** | `mutation/qualification.py` |
| Effect authorization | **F** | `model/effects.py`, `mutation/authorization.py` |
| SDK-native actuation | **F** | `mutation/occurrence.py` plus operation events |
| Graph-delta observation | **F** | `GraphRuntime.derive_delta`, generated delta, pure comparison |
| Transition qualification | **F** | `mutation/transition_evaluation.py` four-axis evaluator |
| Rollout production | **F** | Generated rollout schema and role-specific producer adapters |
| Evidence packaging | **F** | Generated proof graph and artifact serialization relationships |
| First-party pytest plugin | **F** | `evidence_adapters/pytest_plugin` |
| Custom pytest collector | **F** | `evidence_adapters/pytest_plugin/collector.py` |
| Deterministic fixture realization | **F** | Repository, pyfakefs, clock, and environment adapters with strength classes |
| Projection regression | **F** | First-party `pytest-regressions` adapter |
| Promotion verification | **F** | Exact release-artifact requalification service |
| Timeout and sandbox limits | **F** | Bounded subprocess adapter and typed inconclusive results |
| Reactive evidence surface | **D** | `projections/marimo` in P3 |
| Portable qualification projection | **D** | `projections/qualification_sbom` in P3 |
| Hypothesis probes/state machines | **D** | `evidence_adapters/hypothesis` in P2 |
| Metamorphic/differential probes | **D** | Probe-family derivation contracts in P2 |
| Schemathesis | **D** | Model B API/stateful transition adapter in P2 |
| mutmut | **D** | Mutation-candidate/survivor adapter in P2 |
| Coverage.py | **D** | Rollout/evaluation-bound context adapter in P2 |
| CrossHair | **D** | Pure-contract counterexample producer in P2 |
| Atheris | **D** | Fuzz-target registry and corpus adapters in P2 |
| pytest-xdist | **D** | Scheduler adapter after namespace isolation in P2 |

## Phased inclusion

### P0 — core transition kernel

```text
Model A/B contracts
runtime graph coordinates and snapshots
MutationPlan
PlanQualification
MutationSpec
MutationOccurrence
rollout/events
GraphDelta
EvidenceCoverage
pure transition evaluator
PromotionAuthorization
```

### P1 — canonical pytest/evidence path

```text
first-party pytest plugin and EvaluationSpec collector
fixture realization and strength classes
timeout/sandbox inconclusive-result classification
projection regression
release-artifact requalification
```

### P2 — generative and adversarial adapters

```text
Hypothesis and state machines
metamorphic and differential probes
Schemathesis
mutmut
coverage.py
CrossHair
Atheris
pytest-xdist
```

### P3 — derived interaction and exchange surfaces

```text
Marimo canvas
qualification SBOM
OSCAL assessment projection
SPDX/in-toto/SLSA-compatible publication
```
