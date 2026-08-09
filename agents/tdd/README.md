# TDD Agent Skills Seed

A minimal package skeleton for obligation-governed, domain-specialized TDD agent skills.

## Authority model

- `contracts/obligations.cue` defines the closed package contract.
- `package.cue` expresses this package against that contract.
- Skills describe how work is performed.
- Obligation sets define admissible outcomes and required evidence.
- Promotion requires all applicable obligations, fresh evidence, and no unresolved failures.
- Evaluation directories are placeholders for paired baseline, mutation, and grader assets.

## Current proof boundary

The seed contract validates document shape, identifiers, paths, lifecycle values, maturity states, evidence forms, and promotion policy. Cross-reference resolution and filesystem existence checks are intentionally deferred to the future evaluator.

## Validate

```sh
export PATH=/tmp/cuestrap/current/bin:$PATH
cue vet .
cue export . -e packageManifest --out json
```

All skill bodies and evaluation assets are intentionally placeholder-only at this stage.
