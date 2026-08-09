# Test plan and deferred scope

Tests must cover:

- CUE rejection of malformed identities, unknown fields, invalid status combinations, provider-authored derived state, and cross-subject references.
- Deterministic schema/model generation, frozen transports, forbidden extras, and generation drift.
- Truncated event streams, missing terminal events, sequence gaps, provider failure, inconsistent snapshots, and incomplete-manifest sealing.
- Pytest and CPython provider success, retained-object detection, released-object detection, capture integrity, and normalized provenance.
- Admission tables for identity, freshness, applicability, rejected observations, and `UNKNOWN` propagation.
- Rationale-grounding admission for the all-true, empty-unsupported-reference
  satisfied case; every false predicate and non-empty unsupported-reference
  violation case; and missing, unavailable, provider-failed, or malformed
  candidate `UNKNOWN` cases.
- Terminal mapping from missing evidence to `UNKNOWN`/inconclusive and from invalid identity or malformed evidence to rejection.
- Distinction between a rejected malformed grounding candidate and malformed
  identity, envelope, or sealed-manifest evidence that rejects qualification.
- Canonicalization after NFC key normalization, post-NFC collision rejection,
  Unicode-codepoint key ordering, and rejection of finite non-integral,
  fraction-notation, and exponent-notation numbers.
- Controller rules, one-repair budget exhaustion, and proof that controller features cannot enter qualification inputs.
- Fork isolation across workspace, repository snapshot, environment/cache, process, and evidence namespace.
- Rejection of parent evidence for a repaired fork until the relevant probes are re-run.
- Kernel rejection when Codex reports success but hard claims remain unsatisfied.
- Kernel rejection when any non-kernel component attempts to create `AUTHORIZED`.
- One deterministic scripted end-to-end episode and one credential-gated live Codex episode with an advisory live `pytest-eval` observation.
- Proof that advisory semantic observations and advisory evaluator failures cannot alter hard claims or promotion.

Run repository gates in this order:

```text
just rollout-generate-check
just check
just test-clean-locked
just rollout-p0-scripted
just rollout-p0-live
just qualify
```

P0 is complete only when generated outputs are reproducible, the scripted and
live drivers use the same contracts, the forked subject is independently
re-observed, incomplete proof produces `QualifiedInconclusiveResult`, and no
component other than the kernel can issue authorization.

Deferred from P0 are mutation testing, repeated-rollout statistics, adaptive
`python-control`, broad CPython provider coverage, live steer, interrupt,
Stop-hook continuation, rollback, containers, waivers, and real merge/release/
deployment adapters.
