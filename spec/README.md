# Qualification semantic authority

`spec/` is the sole physical authority for qualification semantics in `ctrl`.
Canonical CUE owns structural admissibility, applicability, reference closure,
claim/result consistency, verdicts, and the S0 promotion boundary. Generated
JSON Schema and Pydantic transports preserve structure only.

The package dependency direction is:

```text
core          -> []
repository    -> core
qualification -> core, repository
controller    -> core, repository, qualification
```

The transport projection is one-way:

```text
structural CUE transports
    -> generation-only bundle
    -> JSON Schema
    -> Pydantic transports
```

Semantic policy and result definitions refine the same structural transports.
An included `UNKNOWN` claim is unresolved local state. A `QUALIFIED` result is
complete and contains only satisfied claims; an `INCONCLUSIVE` result is
incomplete and contains unresolved claims; a `REJECTED` result contains a
violation and may be locally complete or incomplete. No S0 result proves that
all obligations from a separate policy are covered.

`#PromotionAuthorization` is mechanically labeled
`promotion-authorization/s0` and `RESULT_LOCAL`. It only marks an internally
qualified result as eligible to enter a future promotion boundary. It does not
authorize an external effect.

OSCAL, Gemara, and in-toto remain obligation-source or projection mechanisms,
not alternative qualification authorities. Imported proposals under
`spec/docs/` are historical and non-normative.

Run root `just cue-check`, `just generated-check`, and `just architecture-check`
to validate the authority boundary.
