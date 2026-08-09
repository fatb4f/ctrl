# Documentation map

This index separates normative authority, accepted architecture, and staged
implementation work.

| Document | Status | Role |
| --- | --- | --- |
| [Qualification P0](https://github.com/fatb4f/kernel-spec/blob/main/docs/qualification-p0-plan/00-summary-and-authority.md) | Authoritative baseline | Defines the current qualification episode and promotion authority chain |
| [ADR-0001](https://github.com/fatb4f/kernel-spec/blob/main/docs/adr/0001-app-server-qualification-and-runtime-boundaries.md) | Accepted | Records the App Server and assurance-runtime architecture decision and staging |
| [Assurance Runtime v0](https://github.com/fatb4f/kernel-spec/blob/main/docs/assurance-runtime-v0.md) | Accepted successor specification | Defines AR0 evidence-core contracts without replacing Qualification P0 |
| [Architecture landscape](https://github.com/fatb4f/kernel-spec/blob/main/docs/coding-agent-assurance-framework-landscape.md) | Accepted supporting analysis | Records the ecosystem survey, rationale, and executable architecture |
| [Reference lineage](https://github.com/fatb4f/kernel-spec/blob/main/docs/reference-lineage.md) | Supporting research; non-normative | Records external standards, research, and implementation lineage without defining contracts or staging |

Authority order:

```text
Qualification P0 baseline
    ↓
accepted ADR-0001 boundaries
    ↓
AR0 evidence-core contracts
    ↓
P1 / AR1 staged implementation
```

A document being present on `main` is not, by itself, an approval signal. New
or superseding decisions require an ADR status change reviewed with the
corresponding repository change. The accepting commit supplies the durable
history for the decision.
