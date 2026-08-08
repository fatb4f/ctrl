# Minimal vertical episode

The fixture obligation is:

```text
Unknown configuration keys must be rejected with diagnostic code
configuration.unknown-key.
```

The deterministic episode is:

1. Snapshot defective fixture R0.
2. Run the probe against R0 and admit the failed observation.
3. Derive a contradicted residual and emit `RepairDirective`.
4. Apply the digest-bound change and snapshot R1.
5. Run the same evaluation against R1 and qualify the source candidate.
6. Build and verify release artifact A1 from R1.
7. Install A1, identify installed subject I1, and run the same evaluation against I1.
8. Derive independent installed-artifact evidence and claims.
9. Authorize promotion only for the complete R1 → A1 → I1 lineage.

Evidence from R0 cannot qualify R1, A1, or I1. A repository pass cannot imply artifact or
installed-artifact qualification.
