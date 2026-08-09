# Event collection, providers, and admission

Store rollout evidence outside every Codex-writable workspace. Append each
Codex SDK method result and streamed notification to a rollout-scoped JSONL
event log. Existing records are never rewritten.

AR0 separates producer-boundary capture fidelity from normalization coverage:

```text
capture_lossless_at_surface(run) :=
    every_received_payload_retained_exactly
    ∧ every_payload_has_stable_source_identity

normalization_total_under_release(run, release) :=
    every_source_record_normalized
    ∨ explicitly_unhandled_with_reason
```

A normalizer or reconciliation failure does not retroactively make capture
lossy. AR0 does not claim universal process observability: an expected but
unreceived event is not evidence that the underlying event or state was absent.

Raw app-server payload bytes are retained as private content-addressed
artifacts. The SDK producer retains its complete public notification
representation together with SDK and runtime versions; it does not claim
wire-level details unavailable through the SDK.

Terminal-event reconciliation checks turn and item pairing, sequence
continuity, SDK errors, provider completion, repository snapshots, and external
effect records. A stream may be sealed while incomplete; affected claims remain
`UNKNOWN`.

Sealing requires a policy-relative closure witness identifying the expected
terminal surfaces, observed terminal payloads, unresolved streams, timeout or
termination policy, and closure classification. Closure is bounded observation
closure, not a claim of global completeness.

The closed `ClosureWitness`, canonicalization profile, and terminal mapping are
defined by the accepted
[runtime specification](../assurance-runtime-v0.md#7-producer-boundary-event-journal).

Implement one project-owned pytest provider that emits normalized collection,
setup/teardown, call, exit, timeout, signal, output, and capture-integrity
facts. It does not classify qualification.

Implement one CPython state-lifetime provider using `weakref`,
`gc.collect()`, and normalized candidate-owned referrer facts. It reports
whether the scoped object remains alive after closure and what candidate
container retains it. It does not derive claim status.

Implement one deterministic rationale-grounding provider. It checks that the
repair references the admitted hidden-probe and CPython-retention facts,
identifies the lifecycle owner, targets the proposed fix at that owner, and
introduces no unsupported fact references. This provider emits a neutral
`RationaleGroundingObservation` containing the individual predicate values and
their fact and provider provenance. It does not emit claim status or an
already-satisfied witness.

Implement one advisory `pytest-eval` `ai.judge` case over the repair rationale.
It assesses rationale quality but cannot satisfy a hard claim or directly
affect promotion.

The advisory evaluator runs in a trusted process after Codex execution.
Provider, model, budget, and evaluator configuration are required by
`EvaluationSpec`; evaluator credentials never enter a Codex workspace or
process environment. A fresh inference is a new evaluation episode. Only an
already recorded immutable observation can be replayed byte-for-byte.

The admission service evaluates every proposed claim against:

```text
exact subject identity
probe and oracle identity
policy and evaluation digests
environment compatibility
provider identity and version
capture integrity
freshness and applicability
CUE constraints
```

For rationale grounding, admission unifies each structurally valid observation
with `SatisfiedRationaleGrounding`: a match is `SATISFIED`, a valid non-match is
`VIOLATED`, and no usable observation is `UNKNOWN`. A malformed grounding
candidate is rejected as an observation and leaves the claim `UNKNOWN` when no
valid replacement exists; it does not by itself make the sealed qualification
manifest malformed.

There is no universal confidence scalar. Controller features derived from
admissions are not evidence and cannot be reused as qualification claims.
