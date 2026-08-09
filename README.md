# ctrl

Canonical federated monorepo for the qualification prototypes.

The repository root is a non-package uv workspace. Components retain their own
package metadata and public interfaces; root tooling supplies one lock and one
qualification command contract.

Stable component identities and roots are declared in `control/components.cue`.
Source snapshot revisions and tree IDs are recorded in
`control/source-imports.cue`. Qualification semantics are authoritative only in
`spec/`; co-located packages remain independent release and interface
boundaries.

```text
spec/                           qualification semantic authority
packages/ppf/                   PPF distribution and python-ppf owner
packages/runtime/               runtime-promptgen distribution
packages/qualification-workflow shared generic workflow distribution
agents/tdd/                     TDD agent skills and compatibility imports
integrations/openai/            OpenAI SDK feedback component
```

## Development

The package is OS-independent. The P0 development workflow supports Linux and
macOS and requires `uv` and `just` on `PATH`.

```sh
just tools-check
just sync
just check
just test-clean-locked
just build
just wheel-smoke
just qualify
```

`lazyjust` is optional workstation software. Run `lazyjust` directly or
`just ui` for its persistent terminal sessions, logs, reruns, and process
termination. Automation must use the documented `just` recipes directly.

Neovim users may trust the project-local `.lazy.lua` through lazy.nvim's
secure-read prompt and open lazyjust with `<leader>pj` in LazyVim.

The adapter was authored and last verified against LazyVim
`c10948c50b18fae7f256433afdef09e432410480`, lazy.nvim
`85c7ff3711b730b4030d03144f6db6375044ae82`, and Snacks.nvim
`882c996cf28183f4d63640de0b4c02ec886d01f2`.

The root never publishes a Python distribution. Package versions and release
metadata remain owned by each workspace component.

S0 uses normal GitHub development only. Gerrit, Zuul, Jujutsu review policy,
repository replication, history rewriting, source archival, and migration
infrastructure are explicitly deferred and are not referenced by any gate.
