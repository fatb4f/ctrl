# Pure qualification kernel

Implement pure functions over generated transports:

```python
derive_evidence_applicability(...)
admit_observation(...)
derive_claims(...)
derive_residuals(...)
derive_legal_actions(...)
rank_actions(...)
decide_transition(...)
derive_terminal_result(...)
```

Legal actions are kernel-derived. P0 ranking is deterministic:

```python
tuple(
    sorted(
        legal_actions,
        key=lambda action: (
            action.estimated_cost,
            -action.targeted_residual_count,
            action.action_id,
        ),
    )
)
```

The kernel emits:

- `RepairDirective` only for a supported residual with a declared `CandidateChange`;
- `QualifiedInconclusiveResult` for incomplete identity or capture, conflicting facts,
  normalization failure, incomplete artifact provenance, unsupported residuals, unsupported waiver
  references, or model-version mismatch; and
- `PromotionAuthorization` only when source-candidate and installed-artifact qualification are
  independently complete, linked through verified artifact provenance, and residual-free.

Every transition returns a new immutable state and validates the complete result. Identical
canonical inputs must produce byte-identical decisions and terminal results.
