# Package and module boundaries

Move the current package tree from `src/tdd_agent_skills` to `src/tdd_seed` and update all imports,
tests, documentation, package checks, and the `python-ppf` entry-point target. Do not ship an old
namespace re-export package.

Keep the `tdd-agent-skills` distribution name, `python-ppf` command, and existing workflow planning
behavior. Existing workflow request/result dataclasses remain handwritten because they are planning
service types, not qualification transports; no artificial compatibility adapter is introduced.

The pure qualification kernel lives under `tdd_seed.qualification` and imports only generated
transports and pure standard-library helpers. It must not import pytest, an SDK agent,
`pydantic-graph`, mutation providers, or `python-control`.
