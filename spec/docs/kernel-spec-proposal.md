# Kernel Spec

## CUE lattice and OSCAL API compiler proposal

| Field | Value |
|---|---|
| Status | Bootstrap seed for architecture review |
| Kernel | CUE semantic lattice |
| Authoritative API data model | OSCAL |
| Canonical governed API | OSCAL Component Definition |
| Canonical executable model | Model A |
| Derived transport IR | Model B |
| Initial controller profile | OSCAL agentic GitOps controller |

## 1. Purpose

Kernel Spec defines the CUE semantic lattice and compiler contracts required to execute a bundled, pinned OSCAL API data model.

The kernel is not a domain metamodel above OSCAL. OSCAL defines the authoritative governed objects, identities, relationships, lifecycle artifacts, and Component Definition API model. CUE supplies the executable lattice through which those semantics are constrained, composed, admitted, evaluated, compiled, and projected.

CUEstrap remains upstream and retains its original role: discovering and qualifying idiomatic CUE patterns against pinned `cue-lang/cue` authority. Kernel Spec consumes those patterns, bundles pinned OSCAL authority, and defines the deterministic compilation boundary.

## 2. Core thesis

```text
Kernel          = CUE semantic lattice
API data model  = OSCAL
Governed API    = OSCAL Component Definition
Model A         = executable CUE closure of the OSCAL API data model
Model B         = generated transport-neutral API IR
State log       = Git
```

The authority split is deliberate:

| Concern | Authority |
|---|---|
| Governed objects and vocabulary | OSCAL |
| Stable lifecycle identities and relationships | OSCAL |
| Governed capability/API representation | OSCAL Component Definition |
| Structural and semantic composition | CUE |
| Unification, bottom, subsumption, defaults, and closure | CUE |
| Admission, transition legality, and effect bounds | CUE kernel contracts |
| Transport-neutral API lowering | Model B compiler |
| Generated transports and adapters | Derived projections |

Model A does not replace OSCAL. Model A is OSCAL made executable in the CUE lattice.

## 3. Compiler architecture

```text
cue-lang/cue
    ↓
CUEstrap-qualified lattice patterns and kernel primitives
    ↓
Kernel Spec distribution
    ├── CUE lattice and compiler contracts
    └── bundled pinned OSCAL API data model
          ↓ resolve, normalize, and unify
Model A — canonical executable OSCAL semantic closure
    ├── OSCAL definitions and constraints
    ├── Component Definition capabilities and operations
    ├── requirements and enforcement mechanisms
    ├── resources and semantic relations
    ├── lifecycle states, transitions, and protocols
    ├── procedures and qualification
    ├── projects and controllers
    ├── controller/project bindings
    ├── projection manifests
    ├── conformance classes
    └── compiler definitions
          ↓ deterministic typed compilation
Derived IR family
    ├── Model B transport-neutral API IR
    ├── OSCAL serialization/lifecycle IR
    ├── evaluation IR
    ├── runtime/controller IR
    └── documentation IR
          ↓ deterministic projection
OpenAPI / OSCAL / MCP / CLI / SDK / docs / tests
```

Only Model A is semantically authored inside the kernel repository. Model A includes the pinned OSCAL authority; derived IRs may not add normative meaning.

## 4. Normative completeness

The central invariant is:

> No normative semantic may exist exclusively in prose or originate in a generated descendant.

Every normative statement must resolve through a machine-addressable chain:

```text
OSCAL identity or kernel requirement ID
    → semantic subject
    → modality
    → declarative, procedural, or observational enforcement
    → evidence obligation
    → conformance class
    → conformance result
```

Documentation explains or projects these objects. It may not silently create new requirements, operations, transitions, protocol phases, projection obligations, or conformance rules.

## 5. Model A

Model A is the canonical CUE-native execution form of the OSCAL-defined API data model.

```text
Model A
    = pinned OSCAL semantics
    ∧ CUE structural constraints
    ∧ CUE semantic and relational constraints
    ∧ lifecycle invariants
    ∧ operation-admission rules
    ∧ project/controller/binding constraints
    ∧ compiler and projection contracts
```

Model A contains addressable objects for OSCAL definitions, requirements, resources, relations, capabilities, operations, states, transitions, protocols, procedures, conformance classes, projects, controllers, bindings, projections, and compiler definitions.

CUE owns evaluation mechanics: unification, bottom, subsumption, defaults, conditional constraints, comprehensions, closure, and concrete-value admission. OSCAL owns the governed API data semantics represented within that lattice.

## 6. OSCAL Component Definition as API

The OSCAL Component Definition is the canonical governed API contract. “API” is not restricted to HTTP. A governed operation may project to:

- a Go interface;
- a CLI command;
- an MCP tool;
- a Git mutation;
- a policy evaluation;
- a workflow action;
- an evidence collector;
- a remediation procedure;
- a human-governed transition.

Model A constrains the Component Definition and its operations through CUE. It does not create a separately authored API schema.

```text
OSCAL Component Definition authority
        +
CUE admission and semantic constraints
        =
Model A governed API closure
```

## 7. Model B

Model B is a generated transport-neutral API IR containing data types, resources, operations, messages, events, errors, security references, and exact Model A/compiler source coordinates.

```text
Model A OSCAL API closure
    ↓ deterministic lowering
Model B transport IR
    ↓
OpenAPI / MCP / CLI / Go / Python / SDK adapters
```

Model B owns no independently authored meaning and is not a second API authority. Editing generated Model B is prohibited once generation exists.

Model B is one member of a derived IR family. Complete OSCAL lifecycle serializations may use an OSCAL-specific IR rather than being forced through an API-shaped transport IR.

## 8. Project and controller separation

A project and a controller are sibling first-class specifications within the executable OSCAL closure.

```text
ProjectSpec
    defines the governed OSCAL domain, resources, lifecycle state,
    policy, and acceptance criteria.

ControllerSpec
    defines reusable observation, decision, procedure, operation,
    and bounded-effect capabilities.

ControllerProjectBinding
    narrows one controller to one project under exact revisions
    and delegated authority.
```

Effective authority is the intersection of:

```text
controller-declared capability
∩ project-permitted capability
∩ binding-delegated capability
∩ current OSCAL lifecycle state
∩ current policy and authorization posture
∩ requested effect bounds
```

A controller never acquires project authority merely because both are declared in the same module.

## 9. External schema imports

OSCAL is bundled domain authority, not an ordinary external-schema profile.

Other external schema languages are import front ends. For example:

```text
JSON Structure source
    → parse and resolve pinned language profile
    → validate source vocabulary
    → lower supported constructs to idiomatic CUE
    → preserve provenance
    → reject undeclared loss
    → unify into an admitted Model A namespace
```

An imported schema does not introduce a second evaluator or displace OSCAL as the governed API data model. CUE remains the evaluator.

## 10. Compiler stages

The initial stage algebra is:

1. **ingest** — receive the bundled OSCAL package, CUE modules, and supported external schema inputs;
2. **resolve** — resolve modules, namespaces, revisions, imports, and extensions;
3. **normalize** — canonicalize OSCAL identities, references, defaults, and ordering;
4. **unify** — compose OSCAL authority, kernel contracts, project, controllers, bindings, and extensions;
5. **evaluate** — detect bottom, incomplete values, and violated relations;
6. **qualify** — execute declared properties and qualified procedures;
7. **freeze** — close intended authority apertures and content-address the Model A closure;
8. **lower** — produce typed projection-specific IRs;
9. **project** — materialize external artifacts;
10. **verify** — validate targets and preservation obligations.

## 11. Compiler properties

The kernel specification must support executable properties for:

- deterministic output;
- OSCAL semantic preservation;
- semantic closure;
- source and identity traceability;
- explicit projection loss;
- qualified extension admission;
- acyclic materialization;
- reproducible revision binding;
- controller capability confinement;
- rejection of downstream drift.

## 12. Extension semantics

A qualified extension contributes to Model A through an explicit namespace aperture.

```text
A(n+1) = resolve(O ∧ K ∧ P ∧ C* ∧ B* ∧ E*)
```

Where:

```text
O = pinned OSCAL API data model
K = CUE lattice and kernel/compiler contracts
P = governed project
C = controllers
B = controller/project bindings
E = admitted extensions
```

Subject to:

```text
A(n+1) != bottom
OSCAL base semantics remain preserved
extension dependency graph is acyclic
external profiles are revision-pinned
authority expansion is explicitly authorized
projection loss is declared and verified
```

Compatibility distinguishes semantic refinement, additive vocabulary, additive API surface, restrictive change, semantic reinterpretation, removal, and authority narrowing or expansion.

## 13. Bootstrap model

The apparent compiler cycle is resolved by separating specification from implementation.

```text
Stage 0: pinned CUE parser and evaluator
Stage 1: K0, minimal CUE lattice contracts plus pinned OSCAL authority binding
Stage 2: C0, hand-written compiler implementing K0 contracts
Stage 3: K1, richer self-describing executable OSCAL model
Stage 4: C1, increasingly model-driven compiler
Stage N: self-hosting fixed point
```

Self-hosting is reached when the bootstrap and self-hosted compilers produce semantically equivalent canonical Model A closures and derived projections for the same pinned OSCAL and project inputs.

## 14. Initial completion gate

The initial Kernel Spec seed is sufficient when it can express and validate:

- the CUE-lattice and OSCAL-authority contract;
- Model A and Model B identities;
- bundled OSCAL Component Definition API semantics;
- normative requirements and enforcement;
- projects, controllers, and bindings;
- states, transitions, operations, and protocols;
- procedures and conformance classes;
- compiler, importer, and projection contracts;
- the JSON Structure import profile;
- the OSCAL governed-project instance;
- the OSCAL agentic GitOps controller profile;
- the binding between that controller and project.

The first implementation can then target this executable contract instead of reconstructing the architecture from prose.
