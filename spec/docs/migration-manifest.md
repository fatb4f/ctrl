# Proposal migration manifest

## Source

- Repository: `fatb4f/cuestrap`
- Path: `docs/cuestrap-governed-repository-controller-proposal.md`
- Branch at migration: `main`
- Blob: `9fe2cb6708d0c2a8a98f2d03cdaae2754c139f36`

## Destination

The source document is normalized into:

- `docs/kernel-spec-proposal.md` — Model A, Model B, compiler, import, extension, and bootstrap contracts;
- `docs/oscal-agentic-gitops-controller-proposal.md` — governed repository, OSCAL, GitOps, agent, runtime, and settlement profile;
- `spec/` — machine-readable base seeds;
- `profiles/oscal-agentic-gitops/` — project/controller/binding seed;
- `profiles/import/json-structure/` — JSON Structure import seed.

## Semantic disposition

| Source concern | Destination |
|---|---|
| CUE executable semantic authority | `spec/model_a.cue`, `spec/kernel.cue` |
| Generated API and adapter architecture | `spec/model_b.cue`, `spec/compiler.cue` |
| Requirements and conformance | `spec/normative.cue` |
| State, transitions, protocols, procedures | `spec/behavior.cue` |
| Project/controller separation | `spec/project_controller.cue` |
| OSCAL governed repository | `profiles/oscal-agentic-gitops/profile.cue` |
| Agentic GitOps controller | `profiles/oscal-agentic-gitops/profile.cue` |
| JSON Structure ingestion | `profiles/import/json-structure/profile.cue` |
| Original CUEstrap identity | Removed; CUEstrap retains its laboratory role |

## Preservation

The original source is not destroyed: Git preserves it at the recorded blob and prior commits. The destination documents preserve its architecture while correcting the repository and authority boundaries.
