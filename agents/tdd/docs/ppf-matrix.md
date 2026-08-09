# PPF 0.2.0 authority and coverage matrix

This matrix does not reconstruct a PPF wire format. Its external authority is the
exact bytes of these four supplied documents:

```text
urn:python-policy-ppf:generation-policy:0.2.0
urn:python-policy-ppf:implementation-policy-extension:0.2.0
urn:python-policy-ppf:extension:evaluation-workflow:0.2.0
urn:python-policy-ppf:composed:extensions:0.2.0
```

Until their exact bytes, provenance URLs, licences, and digests are recorded,
the following remain unresolved:

```text
PPF field coverage       = unresolved
native mapping           = unsupported
format adoptability      = undecidable
filesystem projection    = unspecified
extension requirement    = provisional
```

The general Kattis repository may be used only as a non-authoritative
architectural comparison.

## Authority boundary

| Concern | Authority | Implementation role |
| --- | --- | --- |
| Authored PPF records | Exact supplied PPF documents | Normative source |
| Local authored contracts | CUE | Closed structure, types, invariants, and reference shape |
| Generated transports | Pydantic | Immutable transport projection |
| Markdown parsing | Python input adapter | Source occurrences and anchors |
| Model A/B and controls | Local contracts plus generated transports | Canonical semantic vocabulary |
| OSCAL vocabularies | External projection/vocabulary source | No local decision authority |
| Repository graph state | Runtime ports and immutable snapshots | Distinct repository/VCS/blob/module coordinates |
| Mutation planning and authorization | Pure Python kernel | Qualify plans and enforce effects/graph regions |
| Graph delta | Runtime materialization plus pure comparison | Independent transition evidence |
| Obligation and evaluation derivation | Pure Python kernel | Compile admitted normative records and static evaluation closure |
| Attempt selection | Pure Python kernel | Select the newest eligible completed attempt |
| Rollout validation | Pure Python kernel | Validate causal event lineage and closure |
| Observation classification | Pure Python kernel | Interpret raw adapter facts |
| Evidence, qualification, and verdict | Pure Python kernel | Derive proof relationships and apply deterministic policy |
| Promotion authorization | Pure Python kernel | Derive authority from qualified evidence |
| Graph orchestration | `pydantic-graph` | Bounded sequencing only |
| CUE subprocess | Adapter | Validate/export declared authored contracts |
| Cyclopts | Inbound adapter | Decode commands into generated requests |
| Runtime, pytest, and Jujutsu | Evidence adapters | Emit raw facts and rollout events |

The exact PPF documents own their admitted authored wire structures. Local CUE
contracts bind and validate those structures. The pure Python kernel derives
obligations, evaluation occurrences, evidence coverage, verdicts, transitions,
and promotion authorization.

## Coverage status

| Capability | Supplied PPF 0.2.0 status | Local authority |
| --- | --- | --- |
| Package vocabulary | Pending exact source inspection | Must not reconstruct |
| Evaluation workflow | Pending exact source inspection | Bound from supplied extension |
| Generator policy | Pending exact source inspection | Bound from supplied generation policy |
| Implementation policy | Pending exact source inspection | Bound from supplied implementation extension |
| Composed package shape | Pending exact source inspection | Bound from supplied composed document |
| Markdown provenance | Not expected to be native | Local authored contract |
| Obligation derivation | Not authored by PPF | Pure Python kernel |
| Attempt selection | Not authored by PPF | Pure Python kernel |
| Rollout lineage | Local mandatory semantic law | CUE structure plus Python validation |
| Evidence coverage | Local mandatory semantic law | Pure Python derivation |
| Verdict and promotion | Local mandatory semantic law | Pure Python kernel |

## Transformation chain

```text
Markdown bytes
  → source occurrences
  → CUE-validated authored records
  → generated Pydantic transports
  → pure Python semantic compilation
  → static obligations and EvaluationSpecs
```

The complete local capability chain is:

```text
Model A/B authority
  → runtime graph state
  → MutationPlan
  → PlanQualification
  → MutationSpec and effect authorization
  → MutationOccurrence
  → rollout occurrence and events
  → before/after GraphDelta
  → observations
  → proof-graph evidence
  → four-axis TransitionEvaluation
  → promotion-artifact verification
  → PromotionAuthorization
  → derived projections
```

PPF is an admitted package/profile projection within this chain. It does not
replace Model A/B authority, repository-state identity, mutation authorization,
transition policy, or promotion verification.

## Lifecycle and causal records

The canonical causal order is:

```text
plan
  → obligations
  → candidate
  → attempt
  → rollout occurrence
  → rollout events
  → artifact productions
  → observations
  → evaluation occurrences
  → evidence bindings
  → evaluation results
  → qualification
  → verdict
  → promotion authorization
```

The controlling relationship is:

```text
candidate × campaign × probe × attempt × rollout → observation
```

Every observation binds an attempt ID, rollout ID, reachable terminal event ID,
input-closure digest, and raw artifact/report identity. `RolloutOccurrence` is
the causal execution journal, never a post-decision publication record.

Every transition evaluation independently assesses authorization, conformance,
completion, and resulting-state validity. A missing axis is indeterminate and
cannot produce promotion authority.

Publication is outside v0 implementation authority. A future post-authorization
effect would use a distinct term such as `PublicationOccurrence`.

## Minimum extension set

```text
SourceOccurrence
PlanRevision
MutationPlan
PlanQualification
MutationSpec
MutationOccurrence
GraphSnapshot
GraphDelta
Obligation
EvaluationSpec
EvidenceRequirement
EvaluationAttempt
RolloutOccurrence
Observation
EvidenceItem
ObligationResult
TransitionDecision
PromotionAuthorization
ArtifactManifest
ProofGraph
```

The central seam is the binding between these local semantic records and the
exact supplied PPF records. It must remain provisional until source inspection
establishes the generated field names and wire shapes.
