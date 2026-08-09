# Summary and authority

- **Status:** Authoritative qualification baseline
- **Accepted extension boundary:**
  [ADR-0001](https://github.com/fatb4f/kernel-spec/blob/main/docs/adr/0001-app-server-qualification-and-runtime-boundaries.md)
- **Documentation map:** [Authority and staging](https://github.com/fatb4f/kernel-spec/blob/main/docs/README.md)

P0 proves one complete, isolated rollout-feedback episode:

```text
CUE constraints
    ↓
generated Pydantic transports
    ↓
Codex lifecycle events
    ↓
immutable append-only raw event log
    ↓
typed pytest and CPython observations
    ↓
deterministic rationale-grounding facts
    ↓
optional advisory semantic observations
    ↓
claim-specific admission
    ↓
estimated control state
    ↓
bounded intervention
    ↓
reconciled and sealed evidence manifest
    ↓
independent qualification kernel
    ↓
PromotionAuthorization
```

Authority is partitioned as follows:

```text
CUE
    defines authored admissibility constraints

Generated Pydantic models
    transport structurally projected data

Admission service
    evaluates claims against CUE constraints

Controller
    selects bounded interventions

Codex
    proposes and executes repository changes

Qualification kernel
    exclusively authorizes merge, release, or deployment
```

`codex_reported_success` is an observation only. It cannot satisfy a promotion
claim or issue authorization.

P0 uses one scoped-cache state-lifetime fixture, one CPython provider, one
deterministic rationale-grounding provider, one advisory `pytest-eval`
behavioral case, one planner/implementer trajectory, one repair turn, and one
isolated fork. It includes a deterministic SDK-compatible driver for mandatory
CI and a credential-gated live Codex episode using the same contracts. Fresh
LLM judgments never satisfy a hard claim or directly authorize promotion.

P0 does not include mutation testing, repeated-rollout statistics, adaptive
`python-control`, broad provider registries, live steering, interruption,
Stop-hook continuation, rollback, containers, waivers, or real promotion-effect
adapters.
