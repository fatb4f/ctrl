# Qualification kernel and evidence sealing

The qualification kernel is an independent, deterministic component. It
accepts only the reconciled evidence manifest, admitted claims, exact subject
identity, and qualification policy. It does not import the Codex SDK, pytest,
providers, or controller implementation.

The external collector performs sealing:

```text
terminal-event reconciliation
    → incomplete-stream detection
    → provider finalization
    → manifest consistency validation
    → append-only manifest seal
```

The kernel derives residuals only for unsatisfied obligations:

```text
unobserved | contradicted | incomplete | untrusted | unstable | unsupported
```

It emits `PromotionAuthorization` only when every applicable hard claim is
`SATISFIED`, no hard claim is `UNKNOWN` or `VIOLATED`, subject and branch
identities match, the event manifest is reconciled, and external effects comply
with policy.

It emits `QualifiedInconclusiveResult` when missing required evidence produces
`ClaimAdmission.UNKNOWN`, including when a grounding observation is absent,
unavailable, or rejected as structurally invalid with no valid replacement; it
also does so for incomplete streams, unsupported observations, required
deterministic provider failure, or exhausted repair budget. A valid grounding
observation that fails its satisfied predicate is instead an admitted
`VIOLATED` claim.

It emits `QualificationRejected` for invalid or mismatched identity,
cross-subject or cross-fork evidence, malformed evidence, or manifest
inconsistency. Here malformed evidence means an invalid identity, envelope, or
sealed manifest, not a rejected candidate observation that admission records
without admitting. Advisory evaluator failure is retained as an unavailable
advisory observation and does not change a hard claim or terminal result.

`PromotionAuthorization` is bound to the exact rollout, target repository
snapshot, environment, evidence manifest, evaluation specification, and policy.
P0 produces the authorization artifact but does not execute merge, release, or
deployment.

Identical canonical inputs produce byte-identical admissions, residuals,
decisions, and terminal results. Controller-derived state cannot substitute for
admitted claim evidence.
