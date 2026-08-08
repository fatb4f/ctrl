# TDD Agent Skills

The reusable library for obligation-governed, domain-specialized TDD agent skills.

## Authority model

- `contracts/obligations.cue` defines the closed package contract.
- `package.cue` expresses this package against that contract.
- Skills describe how work is performed.
- Obligation sets define admissible outcomes and required evidence.
- Promotion requires all applicable obligations, fresh evidence, and no unresolved failures.
- Evaluation directories are placeholders for paired baseline, mutation, and grader assets.

## Current proof boundary

The seed contract validates document shape, identifiers, paths, lifecycle values, maturity states, evidence forms, and promotion policy. Cross-reference resolution and filesystem existence checks are intentionally deferred to the future evaluator.

The package exposes services and models. It does not own a control-plane
executable; `packages/ppf` composes the library and owns `python-ppf workflow
compile`.

## Validate

```sh
just test-tdd
cue vet ./agents/tdd/...
cue export ./agents/tdd -e packageManifest --out json
```

Shared evaluation assets live under `evals/tdd` and shared fixtures under
`fixtures/tdd`. Specialization-private skills and contracts remain here.
