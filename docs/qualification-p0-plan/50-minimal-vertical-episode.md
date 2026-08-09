# Minimal vertical episode

The fixture obligation concerns lifecycle ownership of a scoped cache. R0
contains a defect that permits reads after closure and retains a scope-owned
object after the lifecycle ends.

The deterministic episode is:

1. Materialize defective fixture snapshot R0.
2. Run the visible baseline test and record its failure.
3. Run a read-only planner turn.
4. Run the initial implementer with the declared repair scope limited to closed-read behavior.
5. Snapshot candidate R1 and verify the visible test passes.
6. Run the hidden weak-reference/GC probe; admit the retained-object violation and CPython facts.
7. Derive a bounded `RepairDirective`.
8. Fork the completed Codex context and materialize R1 into isolated workspace W1.
9. Run the repair as a subsequent turn on the fork, targeting lifecycle cleanup.
10. Snapshot R2 and re-run visible, hidden, and CPython probes in W1.
11. Evaluate the deterministic rationale-grounding predicates against admitted facts.
12. Optionally run the advisory `pytest-eval` behavioral case against the repair rationale.
13. Reconcile observations, validate consistency, and seal the evidence manifest.
14. Invoke the independent kernel and authorize only the exact R2 subject.

The scripted driver must produce the hard evidence for this episode
deterministically. The live Codex episode uses the same RolloutSpec, providers,
admission service, controller, isolation, and qualification kernel; its fresh
semantic judgment remains advisory.

Evidence from R0 or R1 cannot qualify R2 or its fork. A Codex success statement
cannot qualify any subject. Only the qualification kernel can emit
`PromotionAuthorization`.
