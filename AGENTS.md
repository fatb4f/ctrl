# Monorepo working rules

Use `just` as the repository command contract. Run `just check` for fast
quality gates and `just qualify` before release work. Keep edits scoped and
reversible. Do not edit generated, cache, vendor, runtime, secret, credential,
or machine-local files unless explicitly requested.

Commit the root `uv.lock`. Run `just test-clean-locked` before artifact checks.
The root is not a distribution; package metadata and versions belong to the
owning workspace component.
The project-local `.lazy.lua` exposes commands but does not define policy.
