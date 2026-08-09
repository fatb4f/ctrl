# kernel-spec

`kernel-spec` defines the CUE semantic lattice and compiler contracts used to execute a bundled, pinned OSCAL API data model.

It is downstream of [CUEstrap](https://github.com/fatb4f/cuestrap): CUEstrap remains the narrow upstream-alignment and pattern-qualification laboratory; this repository composes qualified CUE patterns into the executable kernel that constrains, admits, compiles, and projects OSCAL-defined APIs.

## Core contract

```text
Kernel          = CUE semantic lattice
API data model  = OSCAL
Governed API    = OSCAL Component Definition
Model A         = executable CUE closure of the OSCAL API data model
Model B         = derived transport-neutral API IR
State log       = Git
```

CUE and OSCAL have distinct authority roles:

- **OSCAL** defines the governed objects, identities, relationships, lifecycle artifacts, and Component Definition API model.
- **CUE** defines executable structural and semantic constraints, composition, admission, transition legality, authorization narrowing, and deterministic compilation.

The kernel does not replace OSCAL with a generic metamodel. It bundles OSCAL and makes that model executable through the CUE lattice.

## Scope

The repository owns:

- the **CUE lattice kernel** and its compiler contracts;
- the bundled, pinned **OSCAL API data model**;
- **Model A** — the canonical CUE-executable OSCAL semantic closure;
- **Model B** — the derived transport-neutral API IR;
- importer, lowering, projection, and verification contracts;
- project, controller, and controller/project binding semantics;
- conformance, qualification, provenance, and compatibility semantics;
- the OSCAL agentic GitOps controller as a downstream controller/profile binding.

OSCAL itself is not a downstream profile. The agentic GitOps controller is.

The repository does not yet implement the compiler kernel. Its initial deliverable is the machine-readable authority and compiler contract from which the first implementation can be built.

## Authority chain

```text
cue-lang/cue
    ↓
CUEstrap qualified lattice patterns and kernel primitives
    ↓
kernel-spec
    ├── CUE semantic lattice and compiler contracts
    └── bundled pinned OSCAL API data model
            ↓ resolution and unification
Model A — executable OSCAL semantic closure
            ↓ deterministic compilation
projection-specific IRs, including Model B
            ↓
OpenAPI / OSCAL serializations / MCP / CLI / SDK / documentation / tests
```

No normative information may originate in a derived IR or generated target. Official OSCAL semantics enter the authority closure through the bundled OSCAL model; they are not invented by a projection.

## Repository map

```text
spec/                           CUE lattice, OSCAL authority, and compiler contracts
profiles/import/json-structure/ non-OSCAL schema import profile
profiles/oscal-agentic-gitops/  governed project, controller, and binding profile
examples/bootstrap/             minimal resolved bootstrap instance
tests/positive/                 admitted fixture instances
docs/                           architecture and migrated proposals
```

## Validation

Use the pinned CUE toolchain inherited from the CUEstrap release bundle, then run:

```sh
cue vet ./...
cue eval ./examples/bootstrap
cue eval ./tests/positive
```

## Bootstrap sequence

```text
K0  hand-authored CUE lattice contracts plus pinned OSCAL authority binding
C0  hand-written compiler implementation
K1  richer self-describing executable OSCAL specification model
C1  model-driven compiler implementation
…
Kn  self-hosting kernel fixed point
```
