# ADR-0001: App Server qualification and assurance-runtime boundaries

- **Status:** Accepted
- **Decision date:** 2026-08-06
- **Scope:** Architecture and staged implementation; no promotion authorization
- **Supersedes:** Nothing
- **Normative baseline:** [Qualification P0](../qualification-p0-plan/00-summary-and-authority.md)
- **Supporting specification:** [Diagnostics-Aligned Assurance Runtime v0](../assurance-runtime-v0.md)
- **Supporting analysis:** [Coding-Agent Assurance Framework and Qualification Architecture](../coding-agent-assurance-framework-landscape.md)

## Context

Codex App Server qualification requires a long-lived subprocess client,
bidirectional JSONL handling, generated protocol types, lifecycle and approval
invariants, deterministic replay, and hostile sequence exploration. The OSS
ecosystem supplies useful components but no end-to-end project authority model.

The accepted design must preserve the existing Qualification P0 authority chain,
attribute failures to the correct capture or normalization subsystem, prevent
fresh stochastic inference from becoming a deterministic promotion gate, and
keep operational projections outside verdict authority.

## Decision

Adopt a thin `pytest-codex-appserver` architecture as repository P1, with AR0 as
the evidence-core runtime slice:

```text
generated App Server schema
→ typed protocol client
→ producer-boundary source journal and raw artifact store
→ pinned canonicalization profile
→ canonical facts with many-to-one provenance
→ policy-relative closure witness
→ deterministic admission and qualification kernel
→ replay equality tests
→ Hypothesis state-machine exploration
```

Qualification P0 remains the normative baseline and is not superseded.

### Authority rules

- CUE is the authored structural authority.
- Generated frozen Pydantic models are transports, not independent authority.
- Providers emit observations; they do not author admissions or verdicts.
- The qualification kernel alone derives terminal qualification results.
- Inspect, semantic judges, DuckDB, OpenTelemetry, marimo, and
  `python-control` are outer-loop or advisory consumers.
- Xonsh and marimo must use the same generated `WorkbookApplicationService`
  before AR1 admission.

### Capture, normalization, and closure

Producer-boundary capture fidelity and normalization coverage are separate
predicates. A normalization failure cannot retroactively make capture lossy.
Qualification requires lossless permitted capture, total normalization or an
explicit unhandled reason, a policy-derived `CLOSED_COMPLETE` closure witness,
and reconciled required evidence.

The runtime release pins one immutable `canonicalization-profile/v0` artifact
and the implementation that realizes it. Canonical fact deduplication retains
all contributing source-record identities.

### Deterministic and advisory evaluation

Hard claims are limited to deterministic executable evidence, including hidden
probe outcomes, CPython retention observations, regression tests, and closed
rationale-grounding predicates.

Fresh `pytest-eval` `ai.judge` inference is `ADVISORY_SEMANTIC`. Pinning its
experiment specification does not make inference byte-deterministic. A recorded
judgment is replayable as an immutable advisory observation; re-running the
judge creates a new evaluation episode. Advisory results and failures cannot
directly change hard claims or promotion.

### Continuation ownership

AR0 has one continuation owner: the deterministic controller. Project terms
such as `delegationState` are not presumed App Server fields. Ownership must be
proven by a pinned protocol capability profile plus configuration/request,
controller-command, active-delegation, delegation-terminal, and reclaim
records. A delegated future interval transfers ownership until reconciled
terminal or suspension evidence permits reclaim.

## Alternatives considered

- Depend directly on `pytest-lsp`: rejected because LSP abstractions do not
  model App Server approvals, threads, turns, items, or generated protocol
  authority.
- Make `agentverify`, Pydantic Evals, or LangChain trajectory types canonical:
  rejected to avoid a second contract authority.
- Use transcript or semantic similarity snapshots as promotion gates: rejected
  because output similarity does not prove legal control flow or repository
  mutation.
- Treat fresh LLM judging as `HARD_SEMANTIC`: rejected because a pinned
  experiment specification is not a byte-deterministic inference result.
- Combine capture, normalization, and reconciliation into one losslessness
  predicate: rejected because it obscures subsystem attribution.

## Consequences

- P1 requires generated protocol models, a pytest-owned subprocess, separated
  raw and canonical traces, lifecycle invariants, replay, and Hypothesis state
  machines.
- AR0 requires closed canonicalization and closure contracts before evidence is
  qualifiable.
- Live model and judge episodes remain credential-gated and non-gating unless
  their outputs are reduced to separate deterministic predicates.
- AR1 cannot expose independent Xonsh or marimo application behavior; both are
  generated adapters over one service.
- The design adds explicit profile, provenance, closure, and continuation
  records, increasing implementation work in exchange for auditable replay.

## Generated-artifact and interoperability rules

- Generated artifacts bind their CUE source digest, generator version,
  canonicalization profile digest, and normalization implementation digest.
- Schema or runtime drift fails explicitly.
- The SDK and App Server are equivalent only under a pinned projection profile
  covering every policy-required field.
- Provider-specific omissions and conflicts remain discrepancy facts.

## Reversal conditions

Revisit this decision if the shipped App Server contract cannot expose the
required lifecycle or continuation evidence, CUE generation cannot produce
deterministic closed transports, or another maintained component supplies the
same authority model with lower integration and migration cost. A reversal
requires a superseding ADR and must not reinterpret sealed prior results.
