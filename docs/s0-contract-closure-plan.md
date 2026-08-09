# Simplified S0 contract closure plan

## Summary

Implement the approved S0 closure with generated result and policy transports,
uniformly scoped CUE closedness semantics, mechanically result-local promotion,
truthful provenance, SDK de-packaging, and authority-document cleanup. Do not
add policy/result binding or runtime qualification.

## Contract changes

- Define closed structural types:
  - `#ComponentIdentityTransport`
  - `#RepositoryRevisionTransport`
  - `#ClaimAdmissionTransport`
  - `#QualificationResultTransport`
  - `#ApplicabilityTransport`
  - `#EvidenceRequirementTransport`
  - `#ObligationTransport`
  - `#QualificationPolicyTransport`
- Mark all wire fields explicitly required, including empty-capable maps and
  lists.
- Add the generation-only, non-semantic root:

  ```cue
  #QualificationTransportBundle: close({
      result!: #QualificationResultTransport
      policy!: #QualificationPolicyTransport
  })
  ```

- Define `#QualifiedResult`, `#QualifiedInconclusiveResult`,
  `#QualificationRejected`, and `#QualificationResult` exclusively as
  refinements of `#QualificationResultTransport`.
- Define canonical policy types as refinements of their structural transports,
  enforcing map-key identity, obligation reference resolution, applicability,
  and evidence-requirement closure.
- Define `complete` operationally over included claims: `UNKNOWN` is unresolved
  local state; `complete: true` forbids it, while `complete: false` marks an
  unresolved local evaluation. `QUALIFIED` is complete with only satisfied
  claims, `INCONCLUSIVE` is incomplete with unresolved claims, and `REJECTED`
  may be complete or incomplete but must resolve every listed violation to a
  violated claim. None of these states establishes policy coverage.
- Replace promotion with a mechanically scoped boundary record:

  ```cue
  #PromotionAuthorization: close({
      schema!: "promotion-authorization/s0"
      scope!:  "RESULT_LOCAL"
      result!: #QualifiedResult
  })
  ```

  It contains no effects, operations, capabilities, target,
  policy-completeness assertion, or external-mutation authority.

## Generation and provenance

- Keep the generation root in the separate, tooling-only
  `spec/qualification/generate/` package.
- Enable `@experiment(explicitopen)` consistently in every file loaded by the
  generation closure: `spec/core/*.cue`, `spec/repository/*.cue`, top-level
  `spec/qualification/*.cue`, and `spec/qualification/generate/*.cue`.
- Generate one schema with the exact pinned CUE v0.18 development build:

  ```sh
  cue def ./spec/qualification/generate \
    --out jsonschema \
    -e '#QualificationTransportBundle'
  ```

- Preserve the emitted schema structure and only canonicalize JSON
  serialization with sorted keys, stable indentation, and a trailing newline.
- Use the CUE definition names for generated symbols. The only explicit Python
  naming override is the non-exported root bundle class.
- Run pinned `datamodel-code-generator==0.71.0` once to produce Pydantic v2
  result, policy, and nested transport models. Export the transport types, but
  not the generation-only bundle.
- Record in generated provenance:
  - `cue.mod/module.cue` and every sorted CUE file in the generation closure,
    with SHA-256 digests.
  - Exact CUE and datamodel-code-generator versions and argument arrays.
  - JSON Schema and Python transport paths and SHA-256 digests.
- Make generation refuse unpinned tool versions, render into a temporary tree,
  atomically replace tracked outputs only in write mode, and make `--check`
  byte-compare without rewriting.
- Add explicit root code-generation and JSON Schema test dependencies and
  update `uv.lock`.

## Repository cleanup

- Record runtime as `sourceKind: "unpublished-local"`, retain revision
  `e5373...` and tree `4e09...`, and remove its GitHub repository assertion.
- Retire the empty `sdk-feedback` package, import stub, package tests, nested
  CI, and duplicated project tooling. Retain its license, attribution, and
  integration documentation.
- Rename the logical component to `openai-integration` and remove its
  import/build qualification path.
- Mark imported `spec/docs/` proposals historical and non-normative.
- Align active contributor and authority documentation with CUE ownership,
  result-local completeness, and S0-scoped promotion.

## Acceptance tests

| Fixture | JSON Schema | Pydantic strict | CUE structural | CUE semantic |
|---|---:|---:|---:|---:|
| Valid qualified result | pass | pass | pass | pass |
| Missing `repository` | fail | fail | fail | fail |
| `"complete": "true"` | fail | fail | fail | fail |
| Unknown field | fail | fail | fail | fail |
| `UNKNOWN` claim with `QUALIFIED` verdict | pass | pass | pass | fail |
| Rejected violation referencing satisfied claim | pass | pass | pass | fail |

- Validate result fixtures against the generated
  `QualificationResultTransport` definition.
- Validate an unknown `obligationRef` against all policy boundaries:
  - `#QualificationPolicyTransport`: pass
  - Generated JSON Schema: pass
  - Generated Pydantic transport: pass
  - Canonical `#QualificationPolicy`: fail
- Explicitly test nested model typing, required collections, strict boolean
  rejection, and extra-field rejection.
- Prove that a complete rejected result passes, an incomplete rejected result
  with unresolved claims passes, and an inconclusive result without unresolved
  claims fails canonical CUE.
- Update promotion fixtures for the required `schema` and `scope`
  discriminators.
- Extend the thin architecture checker to execute the shared fixtures and
  verify the complete provenance manifest.

## Validation and assumptions

- Run `just check`, `just test-clean-locked`, and `just qualify`; require no
  tracked residue.
- Baseline `just check` and `just qualify` currently pass.
- Policy/result binding, policy coverage, stronger promotion authority,
  runtime episodes, resolver witnesses, federation machinery, and operational
  review infrastructure remain deferred.
