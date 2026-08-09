# Documentation authority

Machine-readable qualification meaning originates in [`spec/`](../spec/).
These documents explain that authority and record accepted design boundaries;
prose cannot override canonical CUE.

The documentation authority order is:

```text
canonical CUE in spec/
    ↓
Qualification P0 baseline
    ↓
accepted ADR-0001 boundaries
    ↓
Assurance Runtime v0 evidence-core contracts
    ↓
supporting research and integration notes
```

- `qualification-p0-plan/` is the canonical P0 plan.
- `adr/0001-…` is the accepted application/runtime boundary decision.
- `assurance-runtime-v0.md` is the accepted successor runtime specification.
- `research/` and `reference-lineage.md` retain provenance but are
  non-normative.
- Integration-specific exploration remains under `integrations/openai/`.
