# Contracts and generated transports

Add a closed, versioned CUE contract family beneath `contracts/qualification/` for:

```text
SubjectIdentity
RepositorySnapshot
EvaluationSpec
ProbeRequest
ProviderObservation
CaptureIntegrity
EvidenceApplicability
EvidenceAdmission
Claim
Residual
QualificationState
LegalAction
TransitionDecision
ArtifactManifest
PromotionAuthorization
RepairDirective
QualifiedInconclusiveResult
```

Add `CandidateChange` and exact file-replacement records because the repair transition must be
typed and digest-bound. A change names its base subject, allowed paths, expected preimage digests,
and replacement artifact digests.

All records carry a `qualification-v0` schema identifier. `SubjectIdentity` is derived, never
provider-authored:

```text
repository-snapshot / candidate-worktree
    repositoryDigest + environmentDigest

release-artifact
    repositoryDigest + artifactDigest + environmentDigest

installed-artifact
    repositoryDigest + artifactDigest + installed-environmentDigest
```

The identity digest is a domain-separated digest of the canonical identity fields. Release and
installed artifacts are separate subjects even when they share an artifact digest.

Observations contain only normalized provider facts: exact subject, probe, evaluation/oracle,
policy, environment, provider identity, capture integrity, and pytest outcomes. Providers cannot
set applicability, admissions, claims, residuals, transitions, or verdicts.

The kernel derives applicability by checking exact subject, probe, policy, environment,
provider-trust, and capture identities. Freshness is identity compatibility, not wall-clock age:
changed repository, probe, oracle, policy, or incompatible environment makes evidence stale or
inapplicable.

Residuals represent only unsatisfied obligations:

```text
unobserved | contradicted | incomplete | untrusted | unstable | unsupported
```

A satisfied obligation is represented by an admitted positive claim and an empty residual for that
obligation. Residuals are derived outputs and are never rewritten as closed.

Export `generated/schema/qualification-v0.schema.json` and generate
`src/tdd_seed/generated/qualification_models.py`. The single generation script must:

1. verify CUE and `datamodel-code-generator` versions;
2. validate CUE definitions and concrete examples;
3. export deterministic JSON Schema;
4. generate Python 3.14/Pydantic v2 models with forbidden extras and frozen model configuration;
5. format generated Python with locked Ruff;
6. emit source, tool, command, and output digests; and
7. compare temporary output byte-for-byte in check mode.

Generated output is never hand-edited. Add `just qualification-generate` and
`just qualification-generate-check`; the latter is part of `just check`.
