# Tiered implementation matrix

The progression should preserve one invariant:

> Analyzer output is a versioned observation. Qualified semantic facts are derived claims. One admitted provider supplies each authoritative semantic dimension.

That matches the uploaded architecture’s separation between analyzer observations, derived claims, persistent LSP state, analytical projections, and the React Flow surface.

```text
Python orchestration prototype
        ↓
typed observation kernel
        ↓
persistent interactive LSP plane
        ↓
reactive graph workbench
        ↓
runtime/native correlation
        ↓
PyO3 acceleration boundary
        ↓
Rust-backed local and remote qualification plane
```

## Overview

|  Tier | Realization                   | Primary result                                    |
| ----: | ----------------------------- | ------------------------------------------------- |
| **0** | Python batch scripts          | Reproducible analyzer artifacts                   |
| **1** | Typed observation kernel      | Canonical observations and claims                 |
| **2** | Persistent LSP controller     | Interactive semantic queries                      |
| **3** | Reactive graph workbench      | Marimo + React Flow projections                   |
| **4** | Dynamic process probes        | Static/runtime correlation                        |
| **5** | Cross-language binding graph  | Python symbol → Rust implementation               |
| **6** | PyO3 native kernels           | Accelerated transforms behind stable Python APIs  |
| **7** | Rust-backed execution plane   | Remote agents, CI workers, continuous observation |
| **8** | Incremental semantic platform | Unified local/remote qualification graph          |

---

# Tier 0 — Python batch baseline

## Objective

Prove that useful repository evidence can be collected without building an interactive platform.

```text
repository revision
    → invoke tools
    → retain raw output
    → normalize minimally
    → render tables
```

## Stack

| Concern           | Component                        |
| ----------------- | -------------------------------- |
| Controller        | Python                           |
| Process execution | `asyncio.create_subprocess_exec` |
| Configuration     | TOML                             |
| Serialization     | stdlib `json` or `orjson`        |
| Models            | Pydantic                         |
| Raw storage       | Content-addressed JSON files     |
| UI                | Marimo tables                    |
| Static tools      | Ruff, Tach, one type provider    |
| Testing           | pytest fixtures and golden files |

## Initial providers

```text
tach map
tach check
ruff check --output-format=json
pyrefly coverage
```

A type-checker batch diagnostic command may also be included, but exactly one engine should be configured as:

```python
primary_type_provider = "pyrefly"  # or ty / zuban
```

## Minimal contract

```python
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel


Provider = Literal["tach", "ruff", "ty", "pyrefly", "zuban"]


class RepositoryCoordinate(BaseModel):
    repository_id: str
    revision: str
    content_root: str


class AnalyzerInvocation(BaseModel):
    invocation_id: str
    provider: Provider
    provider_version: str
    adapter_version: str
    repository: RepositoryCoordinate
    configuration_digest: str
    raw_artifact_digest: str
    started_at: datetime
    completed_at: datetime


class Observation(BaseModel):
    observation_id: str
    invocation_id: str
    subject_id: str
    kind: str
    payload: dict[str, Any]
```

## Output layout

```text
.analysis/
├── invocations/
│   └── <invocation-id>.json
├── raw/
│   └── <sha256>
├── observations/
│   └── <revision>.jsonl
└── reports/
    └── repository-summary.json
```

## Exit gate

Tier 0 is complete when:

- identical repository state and tool versions produce identical normalized observations;
- raw analyzer output is retained;
- every normalized observation links to its invocation;
- one Marimo view can show modules, diagnostics, imports, and type coverage;
- tool failures become typed invocation results rather than Python exceptions escaping the controller.

## Explicit exclusions

Do not add:

- custom LSP infrastructure;
- React Flow;
- DuckDB;
- PyO3;
- a graph database;
- remote workers.

---

# Tier 1 — Typed observation and transform kernel

## Objective

Separate provider-specific formats from the canonical semantic model.

```text
provider output
    → provider adapter
    → normalized observation
    → validation
    → derived claim
```

## Added stack

| Concern                    | Component           |
| -------------------------- | ------------------- |
| Semantic authority         | CUE                 |
| Runtime models             | Pydantic            |
| Fast JSON decode           | `orjson`            |
| Transform engine           | Polars              |
| Persistent columnar format | Parquet             |
| Interchange                | Arrow               |
| Analytical query           | DuckDB              |
| Schema tests               | pytest + Hypothesis |

## Data plane

```text
JSON / JSONL / text analyzer artifacts
              ↓
       provider adapters
              ↓
      Polars LazyFrames
              ↓
physical schema validation
              ↓
Pydantic/CUE semantic admission
              ↓
 partitioned Parquet
              ↓
        DuckDB views
```

## Polars responsibility

Polars performs deterministic transforms:

- flatten provider payloads;
- normalize file and module coordinates;
- join observations with repository subjects;
- calculate coverage aggregates;
- classify diagnostics;
- compute provider differences;
- produce node and edge tables;
- calculate revision deltas.

It does **not** decide whether an observation is true.

## ConnectorX responsibility

ConnectorX is optional at this tier.

Use it only when observations or supporting metadata originate in relational systems:

```text
PostgreSQL / SQLite / MySQL
        ↓
ConnectorX
        ↓
Arrow / Polars
        ↓
normalization
```

Do not use ConnectorX merely to read the platform’s own Parquet files.

## Canonical distinction

```python
class DerivedClaim(BaseModel):
    claim_id: str
    subject_id: str
    predicate: str
    value: object
    supported_by: list[str]
    evaluator: str
    evaluator_version: str
```

```text
Observation:
    Pyrefly reported return type list[str].

Claim:
    Under the admitted Pyrefly authority policy,
    the projected return type is list[str].
```

## Generated contract surfaces

```text
CUE semantic model
    ├── JSON Schema
    ├── Pydantic transport models
    ├── TypeScript projection types
    ├── Rust serde transport structs
    └── Arrow schema adapter
```

The Arrow schema should be a generated or checked **physical projection**, not the semantic authority itself.

## Exit gate

- provider adapters are fixture-tested independently;
- observations survive Parquet round trips;
- DuckDB can reconstruct repository summaries;
- changing the primary type provider changes derived claims without rewriting observations;
- disagreement between providers is represented explicitly;
- before/after revision comparison is deterministic.

---

# Tier 2 — Persistent interactive LSP plane

## Objective

Move from batch diagnostics to live semantic exploration.

```text
document edit
    → didChange
    → incremental analyzer update
    → diagnostics / hover / definition / references
    → observation delta
```

## Stack

| Concern            | Initial implementation       |
| ------------------ | ---------------------------- |
| LSP client         | Python `asyncio` JSON-RPC    |
| Process lifecycle  | Long-lived subprocesses      |
| Python primary LSP | One of ty, Pyrefly, or Zuban |
| Rust LSP           | rust-analyzer                |
| Lint LSP           | Ruff server                  |
| Workspace state    | In-memory Python objects     |
| Batch persistence  | Existing Parquet lane        |
| UI                 | Marimo controls and tables   |

## Required LSP methods

```text
initialize
initialized
textDocument/didOpen
textDocument/didChange
textDocument/didClose
textDocument/hover
textDocument/definition
textDocument/references
textDocument/documentSymbol
workspace/symbol
textDocument/publishDiagnostics
```

Call hierarchy can be added only after the base operations are stable.

## Workspace model

```python
class WorkspaceSession(BaseModel):
    workspace_id: str
    repository: RepositoryCoordinate
    primary_type_provider: Literal["ty", "pyrefly", "zuban"]
    open_documents: list[str]
    document_versions: dict[str, int]
    analyzer_sessions: dict[str, str]
```

## Virtual documents

Marimo and generated PyO3 stubs may not correspond directly to ordinary source files. Introduce a source-map contract:

```python
class SourceMapSegment(BaseModel):
    projected_uri: str
    projected_start: int
    projected_end: int

    original_subject_id: str
    original_start: int
    original_end: int
```

```text
Marimo cells
    → projected Python module
    → Python LSP
    → mapped observations
    → original cells
```

## Control boundary

Marimo cells must not own analyzer processes.

```text
Marimo
    → AnalysisService
        → WorkspaceManager
            → LSP sessions
```

## Exit gate

- analyzer processes survive multiple Marimo cell executions;
- hover and definition responses resolve to canonical subject coordinates;
- document changes produce observation deltas rather than full database rebuilds;
- stale responses are rejected using document versions;
- primary and challenger providers remain distinguishable;
- subprocess failure can be recovered without restarting the notebook.

## Suggested performance budget

| Operation               | Prototype target |
| ----------------------- | ---------------: |
| Cached node selection   |      under 50 ms |
| Hover request           |     under 250 ms |
| Definition request      |     under 300 ms |
| Incremental diagnostics |   under 1 second |
| Workspace restart       |  under 5 seconds |

These are evaluation targets, not architectural guarantees.

---

# Tier 3 — Reactive semantic graph workbench

## Objective

Expose bounded semantic projections through Marimo and React Flow.

```text
canonical observation store
        +
active LSP workspace
        ↓
projection query
        ↓
bounded graph
        ↓
React Flow
```

## Added stack

| Concern               | Component                        |
| --------------------- | -------------------------------- |
| Python reactive shell | Marimo                           |
| Browser graph         | React Flow                       |
| Widget boundary       | `anywidget`                      |
| Transform             | Polars                           |
| Query                 | DuckDB                           |
| Type generation       | TypeScript projection types      |
| Messaging             | Narrow typed commands and deltas |

## Graph contract

```python
class GraphNode(BaseModel):
    node_id: str
    subject_id: str
    node_kind: str
    label: str
    attributes: dict[str, object]
    provenance_ids: list[str]


class GraphEdge(BaseModel):
    edge_id: str
    source_id: str
    target_id: str
    relation: str
    provenance_ids: list[str]


class GraphProjection(BaseModel):
    projection_id: str
    root_subject_ids: list[str]
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    truncated: bool
```

## UI command model

```ts
type GraphCommand =
  | {
      type: "select";
      subjectId: string;
    }
  | {
      type: "expand";
      subjectId: string;
      relation: string;
      depth: number;
    }
  | {
      type: "request-hover";
      subjectId: string;
    }
  | {
      type: "capture-runtime-snapshot";
      executionId: string;
    };

type GraphUpdate =
  | {
      type: "replace";
      projection: GraphProjection;
    }
  | {
      type: "delta";
      addedNodes: GraphNode[];
      changedNodes: GraphNode[];
      removedNodeIds: string[];
      addedEdges: GraphEdge[];
      removedEdgeIds: string[];
    };
```

## Projection pivots

Initial pivots should be narrow:

1. **Architecture**

   - modules;
   - import edges;
   - declared permissions;
   - violations.

2. **Type coverage**

   - typed, `Any`, and untyped counts;
   - primary-provider observations;
   - provider disagreements.

3. **Diagnostics**

   - errors;
   - warnings;
   - security diagnostics;
   - fix proposals.

4. **Impact**

   - module-level reverse dependency closure;
   - changed files;
   - dependent modules.

## Polars versus DuckDB

```text
Polars:
    raw observations → deterministic derived tables

DuckDB:
    derived tables → interactive bounded projections
```

ConnectorX becomes relevant when the graph must join data from external CI, issue, rollout, or observability databases.

## Exit gate

- selecting a node never triggers full tool reruns;
- graph projections are bounded by node count, depth, and relation type;
- UI updates can use deltas;
- every visible node and edge links to provenance;
- provider disagreement is visually distinct from diagnostic severity;
- UI state is not part of semantic authority.

---

# Tier 4 — Dynamic snapshot and profiling probes

## Objective

Join static semantic observations with externally captured runtime state.

```text
static subject graph
        +
runtime frame observations
        ↓
correlation evaluator
        ↓
runtime-semantic claims
```

## Tools

| Probe           | Initial role                          |
| --------------- | ------------------------------------- |
| PyStack         | Timeout, deadlock, core-dump snapshot |
| `py-spy dump`   | Lightweight stack snapshot            |
| `py-spy record` | Statistical profiling                 |
| Austin          | High-rate sample stream               |
| Scalene         | Controlled Python/native attribution  |
| Parca           | Deferred to the remote tier           |

## Python-first implementation

The controller invokes external tools through subprocess adapters. No native extension is required yet.

```python
class DynamicProbeInvocation(BaseModel):
    probe_id: str
    provider: Literal["pystack", "py-spy", "austin", "scalene"]
    execution_id: str
    pid: int
    mode: Literal["snapshot", "sample", "instrumented-profile"]
    configuration_digest: str
    raw_artifact_digest: str
```

## Runtime tables

```text
probe_invocations
processes
threads
samples
frames
thread_states
profile_aggregates
runtime_correlations
```

## Polars transform path

```text
Austin / py-spy / PyStack output
        ↓
Python parser adapter
        ↓
Polars frame table
        ↓
symbol normalization
        ↓
stack aggregation
        ↓
Parquet
```

## Initial correlation claims

Permit only claims supported by available evidence:

```text
executing-symbol
samples-attributed-to-symbol
crossed-binding-boundary
blocked-near-symbol
likely-native-bottleneck
```

Do not initially claim exact native lock ownership.

## Reactive trigger example

```text
Marimo cell starts
    → execution timer begins
    → timeout threshold reached
    → capture PyStack snapshot
    → normalize frames
    → correlate Python frames with workspace subjects
    → annotate cell and graph path
```

## Exit gate

- a timed-out Python execution can produce a retained runtime artifact;
- frames correlate to repository files and symbols;
- runtime evidence is attached to an exact execution and revision;
- local-variable capture is disabled by default;
- raw profiler artifacts can be replayed without rerunning the process.

---

# Tier 5 — Cross-language Python/Rust binding graph

## Objective

Resolve the opaque boundary between Python-visible APIs and Rust implementations.

```text
Python import/call
    → stub symbol
    → PyO3 export
    → Rust implementation
    → native symbol/build ID
```

## Added sources

| Source                 | Information                             |
| ---------------------- | --------------------------------------- |
| Generated `.pyi`       | Python-visible API                      |
| PyO3 introspection     | Exported module/function/class metadata |
| Rust source attributes | Binding declarations                    |
| Cargo metadata         | Crate/package topology                  |
| rust-analyzer          | Rust definitions and references         |
| Native build metadata  | Build IDs and symbol files              |
| Maturin                | Extension build and install lifecycle   |

## Binding manifest

```python
class BindingEdge(BaseModel):
    binding_id: str

    python_module: str
    python_qualified_name: str
    python_stub_subject_id: str | None

    rust_crate: str
    rust_qualified_name: str
    rust_subject_id: str

    binding_kind: Literal[
        "pyfunction",
        "pymethod",
        "pyclass",
        "pymodule",
    ]

    native_artifact_digest: str
    native_build_id: str | None
    exported_symbol: str | None
```

## Binding extraction progression

### P0

Require explicit metadata beside the PyO3 declaration:

```rust
#[pyfunction]
#[binding_id = "engine.analyze"]
fn analyze(source: &str) -> PyResult<AnalysisResult> {
    // ...
}
```

### P1

Generate the manifest from:

- PyO3 attributes;
- module registration;
- generated stubs;
- Cargo metadata.

### P2

Check the generated manifest against the Python stub surface.

## Runtime resolution

```text
native instruction address
    → native build ID
    → native symbol
    → rust-analyzer subject
    → BindingEdge
    → Python-visible symbol
    → calling Python subject or Marimo cell
```

## Exit gate

- clicking a Python extension function navigates to its Rust implementation;
- a native stack frame resolves to the correct built artifact;
- generated stubs and binding manifests are qualification artifacts;
- stale native artifacts are rejected when their build IDs do not match the execution;
- Rust and Python symbol identities remain namespaced rather than collapsed.

---

# Tier 6 — PyO3-backed native transform kernels

## Objective

Accelerate measured bottlenecks without moving semantic authority out of Python/CUE.

```text
stable Python API
    → private PyO3 extension
    → Rust implementation
```

## Candidate native kernels

Good early candidates:

| Kernel                         | Why it is suitable                  |
| ------------------------------ | ----------------------------------- |
| Source-range translation       | Pure, deterministic, high-volume    |
| Graph-delta calculation        | CPU-heavy set and index operations  |
| Stack-sample decoding          | Large repetitive input              |
| Native-symbol resolution       | Existing Rust ecosystem advantage   |
| Content hashing                | Pure and parallelizable             |
| Interval indexing              | Clear contract and measurable speed |
| Large edge-table normalization | Columnar, batch-oriented workload   |

Poor early candidates:

- workspace orchestration;
- analyzer-provider policy;
- CUE admission;
- user-facing API models;
- REST routing;
- Marimo lifecycle;
- projection semantics.

## Package shape

```text
src/semantic_workbench/
├── __init__.py
├── contracts/
├── adapters/
├── services/
├── _native.pyi
└── py.typed

crates/
├── workbench-native/
│   ├── Cargo.toml
│   └── src/
└── workbench-core/
```

Python exposes stable public APIs:

```python
from semantic_workbench.transforms import graph_delta
```

The private extension remains replaceable:

```python
from semantic_workbench import _native
```

## Boundary contract

Prefer batch APIs:

```python
def translate_source_ranges(
    ranges: list[ProjectedRange],
    source_map: SourceMap,
) -> list[OriginalRange]:
    ...
```

Avoid fine-grained object chatter:

```python
# Avoid one PyO3 crossing per frame or graph edge.
for edge in edges:
    native_process_edge(edge)
```

## Arrow boundary

For large columnar data:

```text
Polars DataFrame / Arrow table
        ↓
Arrow C Data Interface
        ↓
Rust kernel
        ↓
Arrow output
        ↓
Polars LazyFrame continuation
```

Do not serialize large frame tables through JSON merely to cross the PyO3 boundary.

## Promotion gate

Move a kernel to Rust only when all are true:

1. profiling identifies it as material;
2. the operation has a narrow deterministic contract;
3. golden fixtures exist;
4. Python and Rust implementations can be differentially tested;
5. the Rust version produces a meaningful latency, memory, or throughput gain;
6. the build and packaging cost is acceptable.

Suggested admission threshold:

```text
≥3× throughput improvement
or
≥50% peak-memory reduction
or
required latency unattainable in Python
```

This is a project policy, not a universal performance law.

## Exit gate

- native implementation is behaviorally equivalent to its Python reference;
- extension failure can fall back to Python where feasible;
- generated `.pyi` matches the runtime API;
- free-threading and GIL behavior are explicit;
- native artifact identity is included in every relevant observation.

---

# Tier 7 — Rust-backed execution and observation plane

## Objective

Move privileged, concurrent, and host-local operations into a small Rust service while preserving Python as the control and modeling plane.

```text
Python controller / Marimo
        ↓ OpenAPI commands
host-local Rust agent
        ├── manages probes
        ├── watches executions
        ├── resolves native symbols
        └── emits artifacts
```

## Rust service responsibilities

| Responsibility                   | Rationale                     |
| -------------------------------- | ----------------------------- |
| Process supervision              | OS-level and concurrent       |
| Probe capability enforcement     | Security-sensitive            |
| Native build-ID resolution       | Native ecosystem              |
| High-rate sample ingestion       | Throughput-sensitive          |
| Artifact hashing and compression | Deterministic native workload |
| Streaming Arrow batches          | Efficient data plane          |
| Remote heartbeat and health      | Long-running service concern  |

## Python responsibilities retained

| Responsibility               |
| ---------------------------- |
| Canonical semantic contracts |
| CUE qualification            |
| Provider policy              |
| Projection definitions       |
| Marimo workflow              |
| React Flow interaction       |
| Evaluation orchestration     |
| Evidence packaging           |
| User-facing API              |

## Control and data planes

```text
Control plane
    OpenAPI / JSON
    - start probe
    - stop probe
    - capture snapshot
    - retrieve metadata
    - check status

Data plane
    Arrow IPC / Parquet / pprof
    - samples
    - frames
    - profile artifacts
    - normalized observation batches
```

## Remote capability model

```cue
#ProbeCapability: {
    targetExecutionIDs: [...string]
    providers: [...string]
    modes: [...string]

    nativeFrames: bool
    localVariables: bool

    maximumDurationMilliseconds: int & <=30000
    maximumSamplingRateHz:       int & <=1000

    rawMemoryExport: false
    reason:          string
}
```

## ConnectorX at this tier

ConnectorX becomes useful for importing external operational state:

- CI job databases;
- evaluation registries;
- rollout metadata;
- execution inventories;
- historical incident databases.

```text
operational database
    → ConnectorX
    → Polars
    → canonical operational observations
```

## Exit gate

- remote probe operations require explicit capabilities;
- all probe invocations are auditable;
- raw memory is never transferred;
- artifacts are content-addressed and retention-bounded;
- the local workbench can replay remote evidence;
- the same contracts are used locally, in CI, and remotely.

---

# Tier 8 — Unified incremental qualification platform

## Objective

Introduce a Rust incremental-query core only after the lower tiers prove the required query model.

```text
repository inputs
runtime observations
binding metadata
policy declarations
        ↓
incremental query database
        ↓
qualified projections
```

## Possible Rust core

```text
Salsa-style query layer
    ├── repository subjects
    ├── observation indexes
    ├── source maps
    ├── graph closures
    ├── provider comparisons
    ├── runtime correlations
    └── projection deltas
```

This core should consume normalized observations. It should not reimplement ty, Pyrefly, Ruff, Tach, or rust-analyzer.

## Query model

```rust
#[salsa::input]
struct RepositoryRevision {
    repository_id: String,
    revision: String,
}

#[salsa::tracked]
fn subject_observations(
    db: &dyn Db,
    subject: SubjectId,
) -> Arc<Vec<ObservationId>> {
    // ...
}

#[salsa::tracked]
fn reverse_dependencies(
    db: &dyn Db,
    module: ModuleId,
) -> Arc<Vec<ModuleId>> {
    // ...
}

#[salsa::tracked]
fn runtime_correlations(
    db: &dyn Db,
    execution: ExecutionId,
) -> Arc<Vec<CorrelationClaim>> {
    // ...
}
```

## Final shape

```text
┌─────────────────────────────────────────────┐
│ Marimo + React Flow                         │
│ investigation · control · qualification     │
└───────────────────┬─────────────────────────┘
                    │ generated Python SDK
┌───────────────────▼─────────────────────────┐
│ Python semantic/control plane               │
│ Pydantic · CUE · evaluations · projections  │
└───────────────────┬─────────────────────────┘
                    │ OpenAPI / Arrow
┌───────────────────▼─────────────────────────┐
│ Rust execution/query plane                  │
│ incremental indexes · probes · symbolization│
└────────────┬───────────────────┬────────────┘
             │                   │
┌────────────▼────────┐  ┌───────▼────────────┐
│ Static providers   │  │ Runtime providers   │
│ LSP + batch tools  │  │ PyStack/Austin/eBPF │
└────────────────────┘  └─────────────────────┘
```

---

# Cross-tier implementation matrix

| Dimension            | T0                      | T1                  | T2                 | T3                   | T4                      | T5                        | T6                         | T7–8                              |
| -------------------- | ----------------------- | ------------------- | ------------------ | -------------------- | ----------------------- | ------------------------- | -------------------------- | --------------------------------- |
| Controller           | Python script           | Python service      | Async Python       | Python service       | Python service          | Python service            | Python + private extension | Python control + Rust agent       |
| Semantic contract    | Pydantic                | CUE + Pydantic      | Same               | Same                 | Extended runtime schema | Binding schema            | Generated Rust structs     | Shared cross-plane contract       |
| Static acquisition   | Batch CLI               | Batch adapters      | Persistent LSP     | Persistent LSP       | Same                    | Python + Rust LSP         | Same                       | Distributed workers               |
| Transform            | Python lists            | Polars              | Polars             | Polars               | Polars                  | Polars                    | Polars + Rust kernels      | Rust/Polars hybrid                |
| Relational ingestion | None                    | Optional ConnectorX | Optional           | Optional             | Optional                | Optional                  | Optional                   | ConnectorX for operational stores |
| Storage              | JSONL                   | Parquet             | Parquet + memory   | Parquet + DuckDB     | Runtime Parquet         | Binding artifacts         | Arrow/Parquet              | Remote artifact store             |
| UI                   | Marimo tables           | Marimo tables       | Interactive Marimo | React Flow anywidget | Runtime overlays        | Cross-language navigation | Same                       | Local/remote workbench            |
| Runtime probes       | None                    | None                | None               | None                 | External subprocesses   | Native correlation        | Native parsers             | Host-local Rust agent/eBPF        |
| PyO3                 | None                    | None                | None               | None                 | None                    | Metadata target           | Hot-path kernels           | SDK/native bridge                 |
| Rust-owned state     | Analyzer internals only | Same                | Analyzer processes | Same                 | Same                    | Binding metadata          | Native indexes             | Execution/query plane             |
| Deployment           | Local                   | Local               | Local              | Local                | Local/CI                | Local/CI                  | Local/CI                   | Local + CI + remote               |

---

# Recommended delivery slices

## Slice A — Evidence kernel

```text
Tier 0 + minimum Tier 1
```

Deliver:

- batch Ruff/Tach/type-provider adapters;
- invocation and observation contracts;
- Polars normalization;
- Parquet storage;
- Marimo summary;
- DuckDB queries.

This proves the semantic model.

## Slice B — Interactive semantic workspace

```text
Tier 2 + minimum Tier 3
```

Deliver:

- one primary Python LSP;
- rust-analyzer;
- persistent sessions;
- virtual documents;
- source maps;
- one React Flow module projection.

This proves interactive exploration.

## Slice C — Runtime correlation

```text
Tier 4 + minimum Tier 5
```

Deliver one end-to-end path:

```text
Marimo timeout
    → PyStack snapshot
    → frame normalization
    → Python/Rust symbol correlation
    → graph annotation
```

This proves the unified static/dynamic model.

## Slice D — Native acceleration

```text
Tier 6
```

Select exactly one measured bottleneck, preferably:

- stack-sample decoding;
- source-map translation; or
- graph-delta calculation.

This proves the PyO3 boundary without prematurely rewriting the platform.

## Slice E — Remote qualification

```text
Tier 7
```

Deliver:

- constrained host-local agent;
- signed probe request;
- artifact return;
- local replay;
- CI integration.

---

# Recommended stopping point for the prototype

The highest-value prototype ends around **Tier 4–5**:

```text
Python control plane
+ CUE/Pydantic contracts
+ Polars/Arrow/Parquet
+ DuckDB
+ persistent Python and Rust LSPs
+ Marimo/React Flow
+ PyStack runtime snapshots
+ explicit PyO3 binding manifest
```

At that stage, the system can already answer:

- Which module violates architecture policy?
- What does the primary type provider infer?
- Where do providers disagree?
- What depends on this changed module?
- Which Python cell invoked this Rust function?
- Where was the process blocked when the execution timed out?
- Which observations support the projected claim?

Only measured bottlenecks or remote deployment requirements justify advancing the implementation into PyO3-native kernels and a Rust execution plane.
