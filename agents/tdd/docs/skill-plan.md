# Jujutsu Skills Consolidation Plan

## Summary

Consolidate the Jujutsu skills around this generated workflow:

```text
CUE contracts
  → committed JSON Schema
  → datamodel-code-generator
  → committed frozen Pydantic models
  → one pydantic-graph workflow per workflow skill
  → jj-agent JSON CLI
  → pytest contract, graph, and repository tests
```

Keep CUE authoritative, `.codex/skills` concise, and graph execution in-process. Support
`jj >=0.43.0,<0.44.0`.

The six Jujutsu skill directories represent exactly five workflows plus one deprecated
compatibility alias:

```text
jj-observe
jj-atomic-change
jj-split-change
jj-resolve-conflict
jj-workspace-worker
jj-conflict-check       deprecated alias only
```

`docs/plan.md` owns qualification and release-promotion semantics.
`docs/qualification-v0-plan.md` owns the executable v0 proof procedure. This document owns the
shipped `jj-agent` product behavior; the proof fixture may exercise this product but may not replace
or impersonate its production entry point.

Those roles are not interchangeable: this document cannot weaken semantic invariants, silently
change procedural sequencing, or introduce runtime behavior absent from the semantic and procedural
plans. An irreconcilable conflict requires an explicit decision record before implementation.

### Current reconciliation slice

The supplied revision archive has SHA-256
`31317b466a4d9a9f573c8dbb6488834eec0d5da02d4606f4aa99f2e2dad17ccb`. Its manifest contains 22
total entries, of which 18 are the skill/reference files adopted here.

Apply this documentation-and-skill slice in order:

1. import the six explicit skill directories and references;
2. correct the split fixture and tree-versus-patch terminology;
3. fold semantic amendments into the three canonical plans;
4. add deterministic manifest generation and checking;
5. add repository-native pytest artifact tests; and
6. run `just jj-skills-manifest-check`, `just check`, `just test-clean-locked`, and `just qualify`.

This slice does not implement `jj-agent`, the qualification kernel, graph runtime, or proof fixtures.

## Implementation Changes

### Contracts and generation

- Add closed CUE definitions for shared evidence and each workflow: observe, atomic change, split,
  conflict resolution, and workspace management.
- Define versioned request/result envelopes with operation literals, repository-independent inputs,
  normalized failures, command evidence, operation snapshots, change IDs, diff digests, and probe
  results.
- Export a committed `jj-agent/v0` JSON Schema with `cue def --out jsonschema`.
- Generate committed Pydantic v2 models using `datamodel-code-generator` targeting Python 3.14.
- Generate models from a shared frozen base using `ConfigDict(frozen=True, extra="forbid")`; never
  hand-edit generated files.
- Add deterministic generation and drift-check recipes. Generate into a temporary directory during
  `--check` and compare byte-for-byte.
- Maintain `.codex/skills/jj-manifest.json` with schema `jj-skills-manifest.v0`. Generate it from the
  explicit six-directory set above; require exactly the current 18 skill/reference files; exclude
  the manifest itself, artifact README and amendments, tests, and caches; reject missing or
  unexpected `jj-*` directories, symlinks, and non-regular files; sort repository-relative POSIX
  paths; and hash exact file bytes. `--check` compares exact coverage and hashes.
- Add `pydantic` and `pydantic-graph` as runtime dependencies; place
  `datamodel-code-generator` in a locked codegen dependency group and commit `uv.lock`.
- Record generator versions in generated headers. Permit a different CUE binary only when it
  reproduces the committed schema exactly.
- Generate the closed declarative operation registry at
  `tdd_agent_skills/jj_agent/operations-v0.json`. Each operation maps to its module and callable, and
  the runtime dispatcher must consume this resource directly rather than maintain a second
  hard-coded operation map.
- Each registry entry is authoritative for the operation name, request type, result type, mutability
  classification, required repository capabilities, allowed exit outcomes, and deprecated aliases.
- Generate `tdd_agent_skills/jj_agent/adapter-artifacts-v0.json` as a projection of that registry,
  not a separately maintained document. It identifies the packaged entry-point, request-decoding,
  registry, dispatch, exception-normalization, serialization, stream, and exit-code implementation.
- Fix the v0 adapter scope in schema rather than trusting manifest-selected paths: the unique
  entry-point metadata, registry and manifest resources, exact generated transport path
  `tdd_agent_skills/generated/jj_agent.py`, and every regular file beneath
  `tdd_agent_skills/jj_agent/`. Require exactly the eight roles defined by the
  qualification procedure, recompute complete wheel coverage independently, reject dynamic
  project-owned imports outside that scope and the separately bound core, and hash sorted
  wheel-path/exact-byte-digest pairs.

### Runtime and public interfaces

Expose:

```text
jj-agent --repo REPO observe REQUEST.json
jj-agent --repo REPO atomic REQUEST.json
jj-agent --repo REPO split REQUEST.json
jj-agent --repo REPO resolve-conflict prepare REQUEST.json
jj-agent --repo REPO resolve-conflict finalize REQUEST.json
jj-agent --repo REPO workspace prepare REQUEST.json
jj-agent --repo REPO workspace collect REQUEST.json
jj-agent --repo REPO workspace dispose REQUEST.json
```

Both `jj-agent` and the `python-ppf` control plane use Cyclopts through shared CLI conventions,
generated transports, the generated operation registry, one error envelope, and one exit mapping.
The executables are separate to preserve the qualified external-process boundary, not to permit a
second CLI architecture. Argparse, entry-point-local request models or registries, and implicit JSON
coercion are forbidden. The pure kernels remain independent of Cyclopts.

- Accept `-` for JSON stdin. Emit exactly one typed JSON result on stdout; send human diagnostics
  to stderr.
- Strictly decode JSON as UTF-8, preserve object pairs, reject duplicate keys, route floats through a
  rejecting `parse_float`, and route `NaN` and infinities through a rejecting `parse_constant`.
  Recursively admit only objects, arrays, strings, integers in ±(2^53−1), booleans, and null; reject
  lone Unicode surrogates and unsupported values before Pydantic validation. Apply the same loader
  to request references and the skill manifest. NFC normalization is repository-path-specific and
  does not apply to arbitrary JSON strings.
- Use exit `0` for success, `2` for rejected postconditions or failed probes, `3` for invalid input
  or unsupported Jujutsu versions, `4` for tool/infrastructure failures, and `70` for unexpected
  internal failures.
- Execute argv arrays without a shell, with bounded output and timeouts. Force noninteractive
  editor, pager, and color behavior.
- Keep generated request/result models immutable. Use small hand-written mutable graph-state
  dataclasses for transient execution state.
- Persist typed results and evidence, not `pydantic-graph` internals. Restart interrupted
  invocations after inspecting Jujutsu's operation log.
- Include typed runtime-dispatch evidence in results: entry-point identity, operation key, registry
  digest, resolved module/callable, shared-core artifact digest, and production-adapter artifact
  digest.
- Runtime operation selection must load the packaged declarative registry, confirm that the selected
  target is callable, and fail closed on missing, ambiguous, malformed, or mismatched targets.

### Skill graphs

- `jj-observe`: preflight version → fingerprint repository identity plus filesystem/Jujutsu state →
  execute typed observation with `--ignore-working-copy` → normalize facts → capture both identities
  again → prove both unchanged. Include conflict-root observations and Git-format diff digests. A
  successful result alone is not non-mutation evidence.
- The production `observe` path always enters through the installed console script, request decoder,
  packaged operation registry, dispatcher, shared safe core, serializer, and exit mapper. The
  controlled unsafe candidate_tree₁ observer exists only in the proof-fixture repository or test
  fixtures. It is not located in or importable from the production package, exposed through
  `jj-agent`, or referenced by production skills.
- `jj-atomic-change`: snapshot `@` → reject conflicts, immutable targets, or unexpected paths →
  run declared probes → describe the logical change → create an empty successor → verify IDs,
  paths, and clean successor state. Never advance on failed evidence.
- `jj-split-change`: inspect source → checkpoint operation → duplicate source → form ordered
  path partitions → validate each partition → prove combined patch and final-tree equivalence →
  rebase descendants → run per-change probes → abandon the source last. Any failure must retain
  the original source and report created change IDs and recovery evidence.
- The split reference's test-only partition uses an explicitly successful static probe:

  ```json
  {
    "id": "tests-static",
    "argv": ["uv", "run", "python", "-m", "compileall", "-q", "tests/test_feature.py"],
    "timeout_ms": 120000
  }
  ```

  A failing pytest run is not a valid partition probe when every partition probe must pass.
- `jj-resolve-conflict`: prepare the earliest `roots(conflicts())` revision and return a resolution
  token; allow the agent to edit directly; finalize by validating the token, checking conflict and
  marker residue, running parser/formatter/test probes, squashing the resolution, and recomputing
  descendant conflicts.
- `jj-workspace-worker` is three independently reversible production changes: `workspace.prepare`
  creates a controller-owned workspace and capability manifest; `workspace.collect` snapshots and
  validates worker results while rejecting path, bookmark, remote, operation-authority, and stale
  workspace violations; and `workspace.dispose` removes only successfully collected workspaces
  through controller authority. Preserve failed workspaces for inspection.
- Merge `jj-conflict-check` into `jj-observe`. Keep its current command as a deprecated alias through
  schema v0, returning the same conflict observation model; remove it with schema v1. Compatibility
  is `conflicts → observe`: project the alias to the canonical operation before registry dispatch and
  never add a separate conflicts handler.
- Keep each `SKILL.md` limited to triggers, authority, invocation, preconditions, and
  postconditions. Generate detailed request examples and field references beneath that skill's
  `references/` directory.
- Update the existing project plan's "no graph runtime" statement with a narrow exception for these
  bounded Jujutsu transaction graphs; do not introduce a general workflow engine.

## Test Plan

- Use pytest markers for `jj_contract`, `jj_graph`, and `jj_integration`.
- Contract tests validate CUE examples, JSON Schema generation, Pydantic round-trips, closed-field
  rejection, operation literals, and schema/model drift.
- Artifact tests assert the explicit five-workflow/one-alias classification, exact 18-file manifest
  coverage and hashes, regular-file-only inputs, and absence of missing or unexpected `jj-*`
  directories.
- Artifact JSON tests apply the production loader to references and the manifest and reject duplicate
  keys, floats, `NaN`, infinities, integers outside ±(2^53−1), invalid UTF-8, lone surrogates, and
  unsupported values. Safe-observer assertions inspect production files only so deliberate proof
  fixtures remain possible.
- Terminology tests reject the legacy unapproved test-delta token and its numbered variants in the
  three canonical plans and Jujutsu references while permitting `approved_test_patch` forms.
- Graph tests use a fake Jujutsu adapter to assert node order, branch selection, failure
  normalization, skipped destructive nodes, and complete evidence.
- CLI tests run `jj-agent` as an external process and verify JSON-only stdout, stderr separation,
  exit codes, stdin support, timeouts, and malformed requests.
- Production-path tests install the exact content-addressed wheel into a fresh environment, invoke
  the absolute generated console script, and prove that request decoding, operation selection,
  argument translation, exception normalization, result serialization, stream separation, and exit
  mapping all occur on the qualified path.
- Static wheel tests parse entry-point metadata, the operation registry, shared-core bytes, and the
  adapter-artifact manifest without importing application modules. Runtime tests independently
  confirm that the declared target is callable and that dispatch evidence matches static inspection.
- Adapter-coverage tests reject missing or duplicate roles, omitted in-scope files, paths outside the
  fixed scope, dynamic project-owned imports, non-regular entries, and any exhaustive digest drift.
- Real integration tests create temporary Jujutsu repositories and cover:
  - observation without operation or working-copy mutation;
  - atomic success, failed probes, conflicts, and unexpected paths;
  - duplicate-first splitting, same-file rejection, descendant rebasing, equivalence failure, and
    source retention;
  - root-first conflict preparation, marker residue, failed validation, successful squash, and
    descendant recomputation;
  - workspace path capabilities, unique names, stale workspace collection, authority violations,
    success disposal, and failure preservation;
  - acceptance of 0.43.x and rejection of unsupported version families.
- Add controlled mutations that remove `--ignore-working-copy`, permit `--ignore-immutable`,
  advance after failed probes, abandon split sources early, skip marker checks, or allow
  worker-owned refs. The corresponding pytest scenarios must fail.
- Add identity mutations for a direct core call, broken entry-point wiring, a different safe core,
  registry/dispatcher disagreement, result/exit mapping defects, and a correct core in a different
  wheel. Each must fail its intended candidate or release gate.
- Add fast schema, model, fake-adapter, and graph tests to `just check`; run real temporary-repository
  scenarios through `just qualify`.

## Assumptions

- `.codex/skills` remains the skill source of truth.
- CUE owns public structure and invariants; generated Pydantic classes are transport models; graph
  code owns execution only.
- Graphs are independent per skill and share adapters, policy checks, evidence types, and reusable
  nodes.
- The wheel's declarative registry is the single operation-routing source for both static inspection
  and production runtime dispatch.
- Jujutsu 0.43.x is the only v0 compatibility family.
- Remote-truth reset, pushing, bookmark integration, and global `op restore` remain outside
  agent-facing skills.
- The correct generator dependency is `datamodel-code-generator`; its executable is
  `datamodel-codegen`.

## Validation

- `just jj-generate-check`: generated JSON Schema, Pydantic models, and skill references have no
  drift.
- `just jj-skills-manifest-check`: the repository skill manifest has exact deterministic coverage
  and hashes.
- `cue vet ./contracts/jj/...`: all Jujutsu contracts and examples pass.
- `just check`: formatting, typing, contract, CLI, and graph tests pass.
- `just test-clean-locked`: locked clean-environment tests pass before artifact inspection.
- `just qualify`: remains the repository's existing qualification gate during the skill and
  documentation reconciliation slice. Passing it does not claim that the deferred `jj-agent`
  runtime or production-entry-point proof exists; those scenarios extend this gate only when their
  implementation lands.
