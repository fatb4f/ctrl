# Test plan and validation gates

- CUE tests reject invalid subject-kind combinations, extra fields, unresolved references,
  provider-authored derived fields, malformed patches, unsafe paths, and unsupported schema
  versions.
- Generation tests prove deterministic schema/model output, frozen models, forbidden extras,
  CUE-example validation, runtime round trips, pinned tools, and drift detection.
- Kernel tables cover every applicability dimension, residual class, legal-action ordering,
  terminal result, and deterministic replay.
- Freshness tests prove R0 evidence cannot qualify R1, A1, or I1; changed probes, oracles,
  policies, environments, and provider trust invalidate applicability.
- Provider tests cover truncated capture, missing nodes, collection/internal errors, timeout,
  conflicting facts, and normalization failure.
- Repair tests cover subject mismatch, preimage drift, path escape, symlink targets, and successful
  R0 → R1 materialization.
- Artifact tests cover wheel tampering, inconsistent `RECORD`, provenance mismatch, omitted data,
  installation failure, and installed-file drift.
- The positive end-to-end episode must authorize promotion.
- A negative end-to-end episode must make the installed artifact fail, reopen an installed-subject
  residual, and block promotion despite R1 passing.
- Static dependency tests confirm the kernel has no SDK-agent, graph, mutation, or control-policy
  dependency.

Run the repository gates in this order:

```text
just qualification-generate-check
just check
just test-clean-locked
just qualify
```

The P0 implementation is complete only when all generated outputs are reproducible, the source and
installed fixture subjects qualify independently, unsupported proof conditions produce
`QualifiedInconclusiveResult`, and promotion is impossible with any open or unsupported residual.
