# Controller, Codex execution, and isolation

Define a small driver protocol for thread start, streamed turn execution,
thread fork, and shutdown. Provide:

```text
openai-codex AsyncCodex driver
    uses public SDK notifications, turn streaming, and thread_fork

scripted driver
    emits the same typed lifecycle records and deterministic candidate changes
```

The planner turn uses a read-only sandbox with denied escalation. The initial
implementer and repair turns use workspace-write sandboxing, disabled network,
an allowlisted environment, and no promotion or evaluator credentials.

P0 sets `continuationOwner = deterministic-controller` and
`delegationState = inactive`. These are project terms whose values must be
proven by the pinned protocol capability and continuation-ownership observation,
not presumed App Server fields. The controller alone observes, reconciles,
evaluates guards, authorizes transitions, and issues explicit continuation
commands. A later integration must be a bounded delegation with an authorized
objective, operation and resource bounds, mandatory observation surfaces,
start and terminal records, reclaim conditions, and a reconciled terminal
checkpoint before controller ownership resumes.

P0 implements only these actions:

```text
continue collection/evaluation
isolated fork
subsequent-turn repair
terminate inconclusive
```

The controller uses deterministic rules:

```text
missing required observation, incomplete capture, or incomplete closure
    → QualifiedInconclusiveResult

invalid identity, cross-subject evidence, or malformed envelope or sealed manifest
    → QualificationRejected

hidden liveness violation with applicable CPython evidence
    → isolated fork + RepairDirective

hard violation remaining after the one repair budget
    → QualifiedInconclusiveResult

all applicable hard claims satisfied
    → request qualification
```

A valid branch is the composite operation:

```text
CodexContextFork
  + RepositorySnapshotMaterialization
  + WorkspaceIsolation
  + EnvironmentMaterialization
  + NewEvidenceNamespace
```

Materialize the candidate snapshot into a new temporary directory with a new
virtual environment, uv cache, process boundary, workspace identity, and
rollout identity. Parent observations are not reused for the fork; qualifying
probes run again against the forked subject.

Record effectful tool calls in `ExternalEffectManifest`. P0 permits only
workspace-local file and process effects. Network access, credentials, and
external service mutations are denied. Codex messages, including success
statements, remain lifecycle observations only.
