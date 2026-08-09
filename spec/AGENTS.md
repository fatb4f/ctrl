# Qualification specification agent contract

## Purpose

`spec/` defines the canonical CUE structural and semantic contracts for the S0
qualification boundary. It is not a production controller runtime.

## Authority

1. Pinned CUE supplies the external language and evaluator semantics.
2. `spec/` is the sole machine-readable qualification authority in `ctrl`.
3. Structural transport definitions own exact wire admissibility.
4. Semantic refinements own applicability, reference closure, claim/result
   consistency, verdicts, and the result-local promotion marker.
5. OSCAL, Gemara, and in-toto are obligation sources or projections, not
   alternative qualification authorities.
6. Generated JSON Schema and Pydantic models are non-authoritative descendants.

## Editing constraints

- Keep the dependency direction `core -> repository -> qualification -> controller`.
- Keep generation-only CUE roots outside the semantic qualification package.
- Enable `@experiment(explicitopen)` consistently across the transport generation closure.
- Do not hand-edit generated descendants.
- Add shared structural and semantic fixtures for each contract change.
- Treat `complete` as result-local only; policy coverage requires a future
  explicit result/policy binding.
- Treat `PromotionAuthorization` as an S0 `RESULT_LOCAL` marker with no effect authority.

## Required checks

```sh
just cue-check
just generated-check
just architecture-check
```
