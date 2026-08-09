# Qualification semantic authority

`spec/` is the sole physical authority for qualification semantics in `ctrl`.
Canonical CUE decides applicability, reference resolution, cross-record
relations, verdicts, and promotion predicates. Generated JSON Schema and
Pydantic transports carry representable structure only.

The package dependency direction is:

```text
core          → []
repository    → core
qualification → core, repository
controller    → core, repository, qualification
```

Qualification therefore cannot import controller. The canonical episode is:

```text
Observation
    → ClaimAdmission
    → ClaimStatus
    → QualificationResult
    → PromotionAuthorization
```

Claim status is closed to `SATISFIED`, `VIOLATED`, or `UNKNOWN`; result verdict
is closed to `QUALIFIED`, `INCONCLUSIVE`, or `REJECTED`. Promotion requires a
complete `QUALIFIED` result. OSCAL, Gemara, and in-toto are obligation-source or
projection mechanisms, not alternative qualification authorities.

Run root `just cue-check` to vet the positive packages and prove that the
incomplete-promotion mutation is rejected.
