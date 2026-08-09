# ctrl

`ctrl` is an optional assembly workspace for independently qualifying
components. Canonical qualification semantics live in `fatb4f/kernel-spec`;
each component repository owns its descriptor, outgoing dependency
declarations, lock, build, and release.

The current checkout retains a CUE/Python integration projection of three
independently versioned distributions:

| Path | Distribution | Import | Version |
|---|---|---|---|
| `packages/ppf` | `ppf` | `ppf` | `0.4.0` |
| `packages/runtime` | `runtime-promptgen` | `runtime_promptgen` | `0.1.1` |
| `agents/tdd` | `tdd-agent-skills` | `tdd_agent_skills` | `0.2.0` |

This projection is not package or semantic authority. Physical co-location and
the root `uv.lock` prove only that selected versions coexist.

## Development

Python `>=3.14,<3.15`, uv, just, and a CUE binary reporting language version
`v0.18.0` are required. The root remains a non-package integration workspace.

```sh
just tools-check
just sync
just check
just qualify
```

Package-focused commands are `just test-ppf`, `just test-runtime`,
`just test-tdd`, and `just build-package PACKAGE`. `lazyjust`, Neovim, and
Mason are optional workstation integrations and are not Python dependencies.

Federation accepts explicit checkout roots or managed ignored checkouts:

```sh
just federation-verify federation/manifest.example.cue \
  --contract-root ../kernel-spec \
  --root qualification-spec=../kernel-spec \
  --root ppf=../ppf
```

The committed example remains intentionally non-runnable until descriptor-owning
changes have revisions that can be pinned without relying on dirty worktrees.

## Review and release

Review infrastructure is separate from semantic qualification. See
[`docs/contributing.md`](docs/contributing.md) for the existing prototype
workflow; Gerrit, Zuul, and Jujutsu are not S0 prerequisites.

Versions remain independent. Update one through
`just version DISTRIBUTION NEW_VERSION`, qualify it, and create a submitted,
path-scoped tag:

- `kernel-spec/v0.2.0`
- `ppf/v0.4.0`
- `runtime-promptgen/v0.1.1`
- `tdd-agent-skills/v0.2.0`

The migration ledger is intentionally not marked cutover-ready until an
operator completes source freezes, history rewrite maps, issue migration, and
staging service tests. See [`ops/migration/README.md`](ops/migration/README.md)
and [`ops/runbook.md`](ops/runbook.md).

## Authority boundary

`fatb4f/kernel-spec` owns the qualification contracts. CUEstrap remains an
external, non-normative laboratory. Component repositories specialize the
contract through imports and adapters; `ctrl` owns only source pins, assembly
identity, and federation-only evaluations. The frozen S0 contract is
[`docs/s0-semantic-consolidation-plan.md`](docs/s0-semantic-consolidation-plan.md).
