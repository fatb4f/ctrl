# ctrl

`ctrl` is the obligation-governed qualification monorepo. Gerrit is the
canonical source and review repository; GitHub is the submitted-code mirror
and canonical issue tracker.

The repository contains one CUE v0.18 module and three independently versioned
Python distributions:

| Path | Distribution | Import | Version |
|---|---|---|---|
| `packages/ppf` | `ppf` | `ppf` | `0.4.0` |
| `packages/runtime` | `runtime-promptgen` | `runtime_promptgen` | `0.1.1` |
| `agents/tdd` | `tdd-agent-skills` | `tdd_agent_skills` | `0.2.0` |

`python-ppf` belongs only to PPF. Its existing `workflow plan` behavior is
preserved, and PPF composes the TDD library for `workflow compile`.

## Development

Python `>=3.14,<3.15`, uv, just, and a CUE binary reporting language version
`v0.18.0` are required. The root is a non-package uv workspace with one lock.

```sh
just tools-check
just sync
just check
just qualify
```

Package-focused commands are `just test-ppf`, `just test-runtime`,
`just test-tdd`, and `just build-package PACKAGE`. `lazyjust`, Neovim, and
Mason are optional workstation integrations and are not Python dependencies.

## Review and release

Contributors use colocated Git/jj and upload changes to Gerrit; see
[`docs/contributing.md`](docs/contributing.md). GitHub pull requests are not a
review path.

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

The project owns its qualification contracts. CUEstrap remains an external
laboratory and may be a non-normative implementation dependency; its code,
history, issues, and contracts are not part of this product boundary. The
supporting lineage register is [`docs/REFERENCES.md`](docs/REFERENCES.md).
