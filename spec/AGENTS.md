# kernel-spec agent contract

## Purpose

This repository defines and qualifies the CUE semantic lattice and compiler contracts required to execute a bundled, pinned OSCAL API data model. It is not the CUEstrap pattern laboratory and it is not yet the production controller runtime.

## Authority

1. Pinned upstream CUE semantics are the external lattice and evaluator authority.
2. Pinned official OSCAL semantics define the authoritative governed API data model; the OSCAL Component Definition defines the canonical governed capability/API contract.
3. `spec/` is the canonical machine-readable CUE encoding of the OSCAL model together with kernel, compiler, admission, projection, and conformance contracts.
4. `profiles/` may refine or instantiate the bundled OSCAL model and kernel contracts; profiles may not redefine their base semantics.
5. `docs/` explains and projects the machine-readable authority. Normative meaning must not originate only in prose.
6. Generated artifacts and runtime observations are non-authoritative descendants.

## Editing constraints

- Preserve the CUE-lattice / OSCAL-model / derived-IR boundary.
- Preserve the Model A / derived-IR boundary: Model A is the executable CUE closure of the OSCAL-defined API data model; Model B is a generated transport IR.
- Keep project, controller, and controller/project binding as separate first-class concepts.
- Declare every authority expansion explicitly.
- Represent requirements, transitions, protocols, conformance classes, compiler stages, and projection loss as addressable data.
- Treat OSCAL as bundled domain authority, not as a downstream schema profile.
- Keep other external schema languages as import or projection profiles; CUE remains the evaluator.
- Do not hand-edit generated descendants once generation exists.
- Add positive and negative fixtures for each semantic change.

## Bootstrap discipline

The initial implementation may be hand-written, but its accepted inputs, outputs, preconditions, postconditions, preservation properties, losses, and receipts must be modeled here first.

## Required checks

```sh
cue vet ./...
cue eval ./examples/bootstrap
cue eval ./tests/positive
```
