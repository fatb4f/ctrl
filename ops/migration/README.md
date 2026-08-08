# Historical migration runbook

`manifest.json` is the checked-in cutover ledger. It deliberately reports
`cutoverReady: false`: the source freezes, history rewrite, issue export, and
live service checks require source-repository and operator authority that is
not available in this worktree.

Before cutover, the operator must make every source validation and freeze entry
successful, populate one original-to-rewritten map per source beneath `maps/`,
record every frozen branch and tag, and set the historical rewrite status to
`complete`. Then run:

```sh
just migration-verify
uv run --isolated --no-project python tools/migration.py verify \
  --require-cutover-ready ops/migration/manifest.json
```

Do not archive a source repository until the second command passes and the
staging restore drill in `ops/runbook.md` is complete. The root MIT license
covers post-cutover first-party monorepo content. Source license declarations
and `NOASSERTION` findings remain explicit in the ledger instead of being
silently inferred.
