# S0 — Establish Federated Semantic Authority

## Summary

Establish one canonical CUE qualification contract while keeping every
consumer independently buildable, testable, versionable, and releasable.
`ctrl` is an optional federation workspace; it cannot redefine component
architecture or make a locally invalid component valid.

Five identities remain distinct:

- `ContractID`: semantic contract identity, version, and content digest.
- `ComponentID`: stable logical software identity.
- `SourceID`: repository, revision, and verified source closure.
- `ComponentInstance`: an exact pinned realization, including descriptor and
  artifact digests.
- `AssemblyID`: an exact compatible federation of component instances and
  federation-only evaluations.

The governing rules are:

```text
semantic centralization != physical centralization
local validity precedes federated compatibility
observations are evidence, never architectural authority
```

## Public contracts and interfaces

### Contract bundle and resolution

`fatb4f/kernel-spec` publishes contract `urn:fatb4f:qualification`, initially
at version `0.1.0`. It owns canonical CUE, deterministic bundle identities,
structural transport projections, and the resolver CLI:

```text
qualification-resolve \
  --lock <qualification-contract.lock> \
  --candidate <candidate.json> \
  --contract-root <checkout>
```

Contract verification requires both:

```text
checkout HEAD == locked revision
every file in the locked contract closure matches its digest
```

Dirty files outside that closure are permitted. Bundle identity hashes sorted
logical paths and per-file digests, so moving an unchanged checkout does not
change `ContractID`.

The resolver emits a canonical receipt containing the contract reference,
resolver identity, resolved policy, and two distinct digests:

- `candidateInputDigest` hashes the exact submitted bytes for replay identity.
- `resolvedPolicyDigest` hashes canonical JSON exported from the CUE-resolved
  policy for semantic identity.

Generated `*Transport` models provide only structural validation. A
transport-valid value must still pass canonical CUE resolution.

Python exposes a nominal `ResolvedQualificationPolicy` witness whose
constructor is private to the verified-receipt adapter.
`QualificationService.qualify()` accepts that witness, never an unvalidated
transport or mapping. PPF may select inputs, construct a candidate, and invoke
resolution; it cannot decide applicability, resolve obligations, establish
qualification, or authorize promotion.

### Qualification result lattice

Claim, result, and promotion identities remain mechanically separate:

```text
Observation
    -> ClaimAdmission
    -> ClaimStatus

all admitted claims + coverage + transitions + effective policy
    -> QualificationResult

QUALIFIED result + promotion predicate
    -> PromotionAuthorization
```

`ClaimStatus` is exactly `SATISFIED`, `VIOLATED`, or `UNKNOWN`.
`QualificationResult` is a closed discriminated union with outcomes
`QUALIFIED`, `INCONCLUSIVE`, and `REJECTED`. Only the qualified member can be
used to construct `PromotionAuthorization`; inconclusive and rejected members
have no promotion fields.

### Component-owned architecture

Each component repository owns `architecture/component.cue`:

```cue
#ComponentDescriptor: close({
    schema:      "component-descriptor/v0"
    componentID: #ComponentID
    packages:    [...#PackageIdentity]
    commands:    #LocalCommands
    contracts:   [...#ContractRequirement]
    dependencies: [...#DeclaredDependency]
})

#DeclaredDependency: close({
    provider: #ComponentID
    kind:     #DependencyKind
})
```

It contains no acquisition URL or self-referential Git revision. Dependency
kinds are `runtime`, `build`, `generated-from`, `test`, `fixture`, and
`evaluation`.

Discovery output has a separate evidence-bearing shape:

```cue
#ObservedDependency: close({
    consumer: #ComponentID
    provider: #ComponentID
    kind:     #DependencyKind
    evidence: [#DependencyEvidence, ...#DependencyEvidence]
})
```

Local qualification normalizes observations by `(consumer, kind, provider)`,
retains every import/provenance site as evidence, projects each observation to
`{provider, kind}`, and requires membership in the component-owned declaration.
Undeclared observations fail. Every `generated-from` declaration requires
provenance evidence. Other unused declarations are reported but do not fail,
allowing conditional prototype dependencies.

Neither observations nor federation configuration can create a locally
permitted dependency.

### Federation pins, instances, and assembly identity

`ctrl` owns acquisition coordinates:

```cue
#ComponentPin: close({
    componentID:  #ComponentID
    repositoryID: #RepositoryID
    url:          string
    revision:     #GitRevision
})
```

For each pin, federation verifies exact `HEAD`, compares the working descriptor
to the pinned Git blob, checks `ComponentID`, and requires local qualification.
It then derives:

```cue
#ComponentInstance: close({
    componentID:              #ComponentID
    sourcePin:                #ComponentPin
    descriptorDigest:         #Digest
    contractRefs:             [...#ContractBundleRef]
    artifactDigests:          [string]: #Digest
    localQualificationDigest: #Digest
})
```

Dirty unrelated notes are permitted; a dirty descriptor is rejected.
`AssemblyID` is a domain-separated digest over the canonical assembly payload,
excluding the digest field itself. It binds component IDs, repository IDs,
revisions, descriptor digests, contract references, artifact/local-result
digests, and federation-only evaluation definitions.

## Implementation sequence

1. Add the canonical core, repository, qualification, controller, and
   federation contracts to `kernel-spec`; reclassify OSCAL, Gemara, in-toto,
   JSON Schema, and language models as non-authoritative projections.
2. Add deterministic bundle/source digests, resolver receipts, CUE-only
   conformance fixtures, and local dependency qualification to `kernel-spec`.
3. Create independent `fatb4f/qualification-workflow` version `0.1.0` and move
   the generic TDD Markdown/CUE compiler, canonicalization, fixtures, and
   snapshot service there without changing snapshot bytes.
4. Publish the workflow package, then make TDD's old import path a silent
   one-release re-export and replace its duplicate implementation. Do not use a
   sibling path source while publication is pending.
5. Add PPF's resolver adapter and nominal witness without changing its existing
   evaluation-state-machine compatibility surface.
6. Give participating repositories their own descriptors, outgoing
   declarations, observations, locks, and local `just` qualification commands.
7. Add manifest-driven federation to `ctrl`, supporting explicit `--root`
   overrides and managed ignored `.federation/` checkouts. Delegate local
   architecture decisions to the kernel/component repositories.
8. Keep the root workspace and `uv.lock` as a coexistence projection only.
   Leave migration `cutoverReady: false` and keep Gerrit, Zuul, Jujutsu,
   history rewriting, and source archival outside S0.

## Acceptance tests

- The same contract bundle at different paths resolves identically.
- Dirty files outside the contract closure pass; dirty contract files fail.
- Exact candidate bytes may differ while the resolved semantic digest remains
  equal.
- A structurally valid candidate violating a CUE-only relation fails canonical
  resolution.
- An unresolved transport cannot be passed to `QualificationService`.
- `SATISFIED` alone cannot construct promotion authority.
- Inconclusive and rejected results cannot contain promotion fields.
- Observations deduplicate by logical edge and retain multiple evidence sites.
- An undeclared `ppf --runtime--> tdd-agent-skills` edge fails locally.
- Federation cannot legalize a locally forbidden edge.
- Pinned revision plus dirty descriptor fails; dirty unrelated documentation
  succeeds.
- Descriptor, artifact, contract, or local-result changes alter the component
  instance and assembly identity.
- Independent and colocated checkouts of the same pins produce the same logical
  assembly result.
- Each repository passes `just check`; release work additionally passes
  `just test-clean-locked`, build checks, and `just qualify`.

## Deferred work

Runtime renaming, stronger wheel isolation, full provider admission/evidence
sealing, richer standards projections, repository history migration,
Gerrit/Zuul/Jujutsu deployment, and physical consolidation remain outside S0.
A future monorepo may colocate components without changing their contract,
component, source, instance, or assembly identities.
