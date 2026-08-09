# Reference lineage for the qualification runtime

- **Status:** Supporting research; non-normative
- **Last reviewed:** 2026-08-08
- **Scope:** Obligation-governed autonomous qualification runtime
- **Normative baseline:** [Qualification P0](https://github.com/fatb4f/kernel-spec/blob/main/docs/qualification-p0-plan/00-summary-and-authority.md)
- **Accepted architecture:** [ADR-0001](https://github.com/fatb4f/kernel-spec/blob/main/docs/adr/0001-app-server-qualification-and-runtime-boundaries.md)
- **Accepted supporting analysis:** [Architecture landscape](https://github.com/fatb4f/kernel-spec/blob/main/docs/coding-agent-assurance-framework-landscape.md)

This document records research, standards, assurance-framework, benchmark, and
open-source lineage. It does not define obligations, schemas, evidence
admission, verdicts, promotion authority, or implementation staging. If this
document conflicts with an accepted document, the authority order in
[`docs/README.md`](README.md) wins:

```text
Qualification P0
    ↓
ADR-0001 boundaries
    ↓
Assurance Runtime v0 contracts
    ↓
accepted architecture landscape
    ↓
this supporting lineage
```

Inclusion is architectural and inspirational. It does not imply compliance,
certification, endorsement, interoperability, dependency adoption, or formal
derivation. Ecosystem conclusions are limited to the artifacts listed here and
reviewed on 2026-08-08.

## Ecosystem position

Within this reviewed corpus, the ecosystem supplies useful components but no
single artifact supplies the complete project-owned authority model end to end.
The project-specific integration boundary is the exact repository transition,
admitted evidence, deterministic qualification, and externally executed
promotion authorization.

```text
external control and research sources
        ↓
standards-facing projections and adapters
        ↓
CUE-authored project contracts
        ↓
producer-boundary evidence journal
        ↓
independent qualification kernel
        ↓
PromotionAuthorization
        ↓
external relying party or promotion adapter
```

No scorer, agent, telemetry system, attestation format, controller, or
analytical projection may issue the terminal qualification result.

## Review method

The register uses primary publisher pages, official repositories, package
registries, standards catalogs, and arXiv metadata. Each artifact records its
owner, exact title, version or status, review date, primary URL, contribution,
and boundary; the contribution and boundary are stated in the role sections
below. Repeated URLs are listed once as primary or supporting sources.
For living or unversioned pages, that status is explicit. An official page that
blocks automated retrieval remains a valid source but is marked as access-blocked
until its metadata is verified through another official source.

## Audited artifact register

| ID | Owner | Exact artifact | Version/status reviewed | Review date | Primary source |
|---|---|---|---|---|---|
| NIST-AIRM | NIST | Artificial Intelligence Risk Management Framework | Final 1.0 | 2026-08-08 | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) |
| NIST-GENAI | NIST | Generative Artificial Intelligence Profile | Final | 2026-08-08 | [NIST profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) |
| NIST-800-2 | NIST CAISI | Practices for Automated Benchmark Evaluations of Language Models | Initial Public Draft | 2026-08-08 | [NIST AI 800-2](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-2.ipd.pdf) |
| NIST-800-3 | NIST CAISI | Expanding the AI Evaluation Toolbox with Statistical Models | Report | 2026-08-08 | [NIST AI 800-3](https://www.nist.gov/publications/expanding-ai-evaluation-toolbox-statistical-models) |
| NIST-800-4 | NIST CAISI | Challenges to the Monitoring of Deployed AI Systems | Report | 2026-08-08 | [NIST AI 800-4](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation) |
| NIST-AGENT | NIST | AI Agent Standards Initiative / CAISI agent-security work | Living program | 2026-08-08 | [NIST initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) |
| NIST-SSDF | NIST | SSDF and SP 800-218A | Final guidance | 2026-08-08 | [SSDF](https://csrc.nist.gov/projects/ssdf) |
| NIST-AML | NIST | Adversarial Machine Learning taxonomy, AI 100-2e2025 | Final | 2026-08-08 | [AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) |
| OSCAL | NIST | Open Security Controls Assessment Language | Living open standard | 2026-08-08 | [OSCAL](https://pages.nist.gov/OSCAL/) |
| ISO-AI | ISO/IEC JTC 1/SC 42 | ISO/IEC 42001, 23894, 42005, and 42006 | Published standards; catalog access may require browser verification | 2026-08-08 | [ISO AI standards](https://www.iso.org/sectors/it-technologies/ai) |
| IEEE-7000 | IEEE | IEEE 7000 | 2021 standard | 2026-08-08 | [IEEE 7000](https://standards.ieee.org/standard/7000-2021.html) |
| ETSI-304223 | ETSI | EN 304 223, Baseline Cyber Security Requirements for AI Models and Systems | Published standard; catalog access may require browser verification | 2026-08-08 | [ETSI article](https://www.etsi.org/enjoy-magazine/articles/ai-cybersecurity-standard-etsi-en-304-223/) |
| CSA-AICM | Cloud Security Alliance | AI Controls Matrix | v1.1 | 2026-08-08 | [AICM](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1) |
| CSA-MAESTRO | Cloud Security Alliance | Agentic AI Threat Modeling Framework: MAESTRO | Published framework | 2026-08-08 | [MAESTRO](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) |
| CSA-REDTEAM | Cloud Security Alliance | Agentic AI Red Teaming Guide | Published guide | 2026-08-08 | [Red teaming guide](https://cloudsecurityalliance.org/artifacts/agentic-ai-red-teaming-guide) |
| CSA-TRUST | Cloud Security Alliance | Agentic Trust Framework | Open specification | 2026-08-08 | [Trust Framework](https://cloudsecurityalliance.org/blog/2026/02/02/the-agentic-trust-framework-zero-trust-governance-for-ai-agents) |
| OWASP-AGENT | OWASP | Top 10 for Agentic Applications | 2026 framework | 2026-08-08 | [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| MITRE-ATLAS | MITRE | ATLAS | Living knowledge base | 2026-08-08 | [MITRE ATLAS](https://atlas.mitre.org/) |
| CISA-AGENT | CISA | Careful Adoption of Agentic AI Services | Guidance | 2026-08-08 | [CISA guidance](https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-ai-services) |
| GOOGLE-SAIF | Google | Secure AI Framework | Living framework | 2026-08-08 | [SAIF](https://saif.google/) |
| OPENSSF-GEMARA | OpenSSF | Gemara GRC Engineering Model | Living project with CUE schemas | 2026-08-08 | [Gemara](https://openssf.org/projects/gemara/) |
| OPENSSF-OSPS | OpenSSF | Open Source Project Security Baseline | Living baseline | 2026-08-08 | [OSPS Baseline](https://baseline.openssf.org/) |
| COSAI-CODEGUARD | CoSAI / OASIS Open | Project CodeGuard | Open-source rules and skills | 2026-08-08 | [CodeGuard](https://github.com/cosai-oasis/project-codeguard) |
| OPENSSF-OSSCRS | OpenSSF | OSS-CRS | Open-source framework | 2026-08-08 | [OSS-CRS](https://oss-crs.openssf.org/) |
| IN-TOTO | in-toto | Attestation Framework | Test Result v0.1 and Runtime Trace v0.1 predicates | 2026-08-08 | [in-toto](https://in-toto.io/) |
| SLSA | OpenSSF / SLSA community | SLSA | Living specification | 2026-08-08 | [SLSA](https://slsa.dev/) |
| SIGSTORE | Sigstore | Sigstore and Cosign | Living project | 2026-08-08 | [Sigstore](https://www.sigstore.dev/) |
| GUAC | GUAC community | GUAC ontology and graph | Open-source analytical graph | 2026-08-08 | [GUAC](https://guac.sh/) |
| W3C-PROV | W3C | PROV-O | Recommendation | 2026-08-08 | [PROV-O](https://www.w3.org/TR/prov-o/) |
| IETF-RATS | IETF | RFC 9334 RATS Architecture | RFC | 2026-08-08 | [RFC 9334](https://datatracker.ietf.org/doc/rfc9334/) |
| SPDX | SPDX community | SPDX specifications | Living specification | 2026-08-08 | [SPDX](https://spdx.dev/use/specifications/) |
| OTEL | OpenTelemetry community | OpenTelemetry specification | Living specification | 2026-08-08 | [OTel specification](https://github.com/open-telemetry/opentelemetry-specification) |
| INSPECT-AI | UK AI Security Institute | Inspect AI | `inspect-ai` 0.3.253; beta software | 2026-08-08 | [Inspect package](https://pypi.org/project/inspect-ai/0.3.253/) |
| INSPECT-SWE | Meridian Labs | Inspect SWE | `inspect-swe` 0.2.69 | 2026-08-08 | [Inspect SWE package](https://pypi.org/project/inspect-swe/0.2.69/) |
| METR | METR | HCAST and RE-Bench | Capability benchmark lineage; distinct artifacts | 2026-08-08 | [METR research](https://metr.org/research/) |
| SWE-BENCH | SWE-bench community | SWE-bench | Living benchmark | 2026-08-08 | [SWE-bench](https://github.com/SWE-bench/SWE-bench) |
| SWE-AGENT | SWE-agent community | SWE-agent and mini-swe-agent | Open-source agent runtimes | 2026-08-08 | [SWE-agent](https://github.com/SWE-agent/SWE-agent) |
| PYTEST | pytest community | pytest | Stable open-source framework | 2026-08-08 | [pytest](https://github.com/pytest-dev/pytest) |
| HYPOTHESIS | HypothesisWorks | Hypothesis | Stable open-source framework | 2026-08-08 | [Hypothesis](https://github.com/HypothesisWorks/hypothesis) |
| PYDANTIC | Pydantic | PydanticAI and Pydantic Evals | Living open-source tooling | 2026-08-08 | [PydanticAI](https://github.com/pydantic/pydantic-ai) |
| MCP | Model Context Protocol community | Model Context Protocol | Living protocol | 2026-08-08 | [MCP](https://github.com/modelcontextprotocol/modelcontextprotocol) |

Research papers are recorded by their arXiv identifiers and exact metadata:

| ID | Reference | Project relevance |
|---|---|---|
| REACT | [2210.03629](https://arxiv.org/abs/2210.03629) | Observe/reason/act loop |
| REFLEXION | [2303.11366](https://arxiv.org/abs/2303.11366) | Governed repair and replanning |
| SWE-AGENT-PAPER | [2405.15793](https://arxiv.org/abs/2405.15793) | Explicit agent-computer interface |
| SWE-BENCH-PAPER | [2310.06770](https://arxiv.org/abs/2310.06770) | Repository-level executable criteria |
| FORMAL-LLM | [2402.00798](https://arxiv.org/abs/2402.00798) | Machine-checkable constraints |
| AGENT-SPEC | [2503.18666](https://arxiv.org/abs/2503.18666) | Runtime enforcement DSL |
| PROBGUARD | [2508.00500](https://arxiv.org/abs/2508.00500) | Probabilistic monitoring; derived, not canonical, evidence |
| AGENTGUARD | [2509.23864](https://arxiv.org/abs/2509.23864) | Runtime event verification |
| POLICIES-PATHS | [2603.16586](https://arxiv.org/abs/2603.16586) | Path-sensitive governance |
| POLICY-CONSTRAINED | [2604.07833](https://arxiv.org/abs/2604.07833) | External policy and enforcement boundary |
| BEHAVIORAL-CONTRACTS | [2602.22302](https://arxiv.org/abs/2602.22302) | Formal agent behavior contracts |
| OPERATIONAL-DATA | [2608.03609](https://arxiv.org/abs/2608.03609) | Verification over evolving external state |
| AI-CONTROL | [2312.06942](https://arxiv.org/abs/2312.06942) | External observation under untrusted agents |
| SAFETY-CASES | [2410.21572](https://arxiv.org/abs/2410.21572) | Structured claims and evidence |
| SAFETY-CASES-ADVANCED | [2403.10462](https://arxiv.org/abs/2403.10462) | Inspectable assurance arguments |
| BIG-ARGUMENT | [2503.11705](https://arxiv.org/abs/2503.11705) | Whole-system safety cases |
| OSS-CRS-PAPER | [2603.08566](https://arxiv.org/abs/2603.08566) | Autonomous security remediation |

The following supporting sources belong to the register rows above. They are
kept here so the reviewed source set remains auditable without duplicating
artifact rows:

- NIST: [AI 800-2 announcement](https://www.nist.gov/news-events/news/2026/01/towards-best-practices-automated-benchmark-evaluations), [AI 800-3 announcement](https://www.nist.gov/news-events/news/2026/02/new-report-expanding-ai-evaluation-toolbox-statistical-models), [AI 800-4 announcement](https://www.nist.gov/news-events/news/2026/03/new-report-challenges-monitoring-deployed-ai-systems), [AI agent standards](https://www.nist.gov/agentic-ai), [CAISI](https://www.nist.gov/caisi), [SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final), and [OSCAL repository](https://github.com/usnistgov/OSCAL).
- OSCAL assessment sources: [assessment layer](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/), [assessment plan](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-plan/), and [assessment results](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/assessment-results/).
- Gemara and OpenSSF: [Gemara site](https://gemara.openssf.org/), [Gemara schemas](https://gemara.openssf.org/schema/), [Gemara repository](https://github.com/gemaraproj/gemara), [OSPS project](https://openssf.org/projects/osps-baseline/), [OSPS repository](https://github.com/ossf/security-baseline), [OSS-CRS project](https://openssf.org/projects/oss-crs/), and [OSS-CRS repository](https://github.com/ossf/oss-crs).
- CSA and OWASP: [MAESTRO lab page](https://labs.cloudsecurityalliance.org/maestro/), [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/), and [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/).
- Security and provenance: [in-toto repository](https://github.com/in-toto/attestation), [Test Result predicate](https://in-toto.io/attestation/test-result/), [Runtime Trace predicate](https://github.com/in-toto/attestation/blob/main/spec/predicates/runtime-trace.md), [SLSA repository](https://github.com/slsa-framework/slsa), [Sigstore organization](https://github.com/sigstore), [Cosign repository](https://github.com/sigstore/cosign), [Cosign attestation verification](https://docs.sigstore.dev/cosign/verifying/attestation/), [GUAC ontology](https://docs.guac.sh/guac/guac-ontology/), [SPDX](https://spdx.dev/), and [GUAC](https://guac.sh/).
- Policy and workflow adapters: [CUE](https://github.com/cue-lang/cue), [OPA](https://github.com/open-policy-agent/opa), [Cedar](https://github.com/cedar-policy/cedar), [LangGraph](https://github.com/langchain-ai/langgraph), [MCP](https://github.com/modelcontextprotocol/modelcontextprotocol), and [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent).
- Inspect and METR: [Inspect](https://inspect.aisi.org.uk/), [Inspect agents](https://inspect.aisi.org.uk/agents.html), [Inspect agent bridge](https://inspect.aisi.org.uk/agent-bridge.html), [Inspect eval logs](https://inspect.aisi.org.uk/eval-logs.html), [METR](https://metr.org/), [autonomous capabilities](https://metr.org/measuring-autonomous-ai-capabilities/), and [time horizons](https://metr.org/time-horizons/).
- Benchmarks and challenges: [CyberSecEval](https://ai.meta.com/research/publications/purple-llama-cyberseceval-a-benchmark-for-evaluating-the-cybersecurity-risks-of-large-language-models/), [DARPA AI Cyber](https://www.darpa.mil/research/programs/ai-cyber), and [AIxCC results](https://www.darpa.mil/news/2025/aixcc-results).
- Frontier governance: [Anthropic RSP](https://www.anthropic.com/responsible-scaling-policy), [OpenAI Preparedness update](https://openai.com/index/updating-our-preparedness-framework/), and [OpenAI Frontier Governance Framework](https://openai.com/index/openai-frontier-governance-framework/).
- Google, ETSI, and ISO: [SAIF agents](https://saif.google/focus-on-agents), [SAIF risks](https://saif.google/secure-ai-framework/risks), [SAIF controls](https://saif.google/secure-ai-framework/controls), [ETSI announcement](https://www.etsi.org/newsroom/press-releases/2627-etsi-releases-world-leading-standard-for-securing-ai/), [ISO 42001](https://www.iso.org/standard/42001), [ISO 42005](https://www.iso.org/standard/42005), and [ISO 23894](https://www.iso.org/standard/77304.html).
- Research: [Constitutional AI](https://arxiv.org/abs/2212.08073).

## Standards and research roles

Standards and research sources contribute vocabulary, controls, threats,
evaluation methodology, provenance, or assurance-case patterns. They do not
become the project’s semantic authority. Gemara and OSCAL are standards-facing
projections or obligation-source candidates; CUE remains the authored project
authority. W3C PROV, RATS, SPDX, in-toto, SLSA, Sigstore, GUAC, and
OpenTelemetry are projections or evidence/provenance mechanisms, not verdict
engines.

Threat taxonomies compile into candidate obligations and probes. A threat entry
does not itself establish a violation, and a benchmark score does not itself
establish promotion eligibility.

## Accepted App Server qualification lineage

The accepted App Server architecture is documented in ADR-0001 and the
landscape’s App Server harness section. Its non-normative external lineage is:

| Component | Permitted role | Boundary |
|---|---|---|
| Generated App Server schema | Protocol contract input | Schema/runtime drift fails explicitly |
| `pytest-lsp` | Subprocess and asynchronous stdio fixture pattern | Do not import LSP semantics |
| `agentverify` | Step, dependency, budget, and replay assertion patterns | Adapter only; approvals and lifecycle remain distinct |
| Hypothesis stateful testing | Generate and shrink hostile protocol sequences | Does not define legality |
| AgentEvals/OpenEvals | Strict/unordered/subset/superset trajectory vocabulary | Reproduce the small algebra in CUE |
| Pydantic Evals | Typed dataset and parametrization transport | CUE remains authoritative |
| AgentProbe | Redaction, review, diff, and snapshot patterns | Similarity is not a promotion gate |
| Inspect AI | Outer release-qualification campaigns | Consumes admitted traces |
| Inspect SWE | Optional Meridian Labs software-agent adapter | Separate from the Inspect harness |

The project-specific realization remains:

```text
generated schema
    → typed protocol client
    → sealed raw JSONL source journal
    → redacted canonical projection
    → deterministic lifecycle and trajectory assertions
    → Hypothesis protocol exploration
    → admitted evidence
    → independent qualification kernel
    → PromotionAuthorization
```

Raw records, canonical facts, admitted observations, derived claims, and
terminal results remain separate. The raw source journal is sealed and retained
under the accepted capture policy; canonicalization does not rewrite raw
evidence.

## Conceptual crosswalk to canonical contracts

The following terms are explanatory crosswalks, not new contract types:

| Lineage term | Project-owned representation | Disposition |
|---|---|---|
| `Plan`, `MutationPlan`, `MutationSpec` | `RolloutSpec`, `ControlAction`, `RepairDirective` | Use the canonical type appropriate to the record |
| `RepositoryState` | Repository snapshot identities in `RolloutIdentity` | Canonical subject binding |
| `MutationOccurrence` | `RolloutEpisode`, `LifecycleEvent`, and observations | Preserve occurrence provenance |
| `GraphDelta` | Before/after snapshots and `ExternalEffectManifest` | Derived state/effect evidence |
| `EvidenceCoverage` | `ClaimAdmission` and `EvidenceManifest` | Admission-owned |
| `EvaluationResult` | Typed observations and `ClaimAdmission` | Provider does not author claim status |
| `TransitionVerdict` | `QualificationVerdict` or terminal result | Kernel-owned |
| `RepairDecision` | Controller-owned `ControlAction` or `RepairDirective` | Cannot authorize promotion |
| `PromotionDecision` | `PromotionAuthorization` | Authorization artifact only; no side effect |
| `RolloutJournal` | Producer-boundary source journal and sealed evidence manifest | Raw and canonical layers stay distinct |
| `QualificationAttestation` | Deferred export projection | Not canonical authority |
| `QualificationGraph` | Deferred analytical projection | Not canonical authority |
| `ObligationProfile` | Pinned CUE policy or semantic bundle input | Do not add a second obligation authority |

## Project ownership map

The canonical qualification architecture is currently realized across several
project repositories. Repository location does not alter semantic authority.
Canonical types should have one physical authority location rather than
independent definitions in multiple repositories.

| Surface | Current repository | Intended ownership |
|---|---|---|
| Normative semantic contracts | `kernel-spec` / `sdk-feedback` | Qualification specification |
| PPF and evidence machinery | `ppf` | Qualification package |
| Runtime and state projection | `runtime` | Runtime package |
| TDD specialization | `tdd-seed` | Agent specialization |
| App Server qualification | `sdk-feedback` | Integration and evaluation package |
| Idiomatic CUE patterns | `cuestrap` | External reusable pattern library |

CUEstrap is a design and implementation dependency. It is not a normative
authority source and does not own qualification semantics.

## Implementation boundaries and deferred reuse

Accepted implementation mechanisms are limited to CUE-authored contracts,
generated frozen transports, pytest evidence, Hypothesis exploration, generated
App Server protocol handling, trace sealing/canonicalization, and the
project-owned admission and qualification kernel.

The following remain deferred interoperability or outer-loop candidates and
require a separate implementation decision before becoming dependencies:

- Gemara and OSCAL projections;
- Inspect AI and Inspect SWE campaigns;
- in-toto, SLSA, and Sigstore export;
- GUAC and OpenTelemetry projections;
- OPA, Cedar, LangGraph, and MCP adapters;
- external capability, security, or red-team benchmarks.

The qualification kernel emits one of `PromotionAuthorization`,
`QualifiedInconclusiveResult`, or `QualificationRejected`. A relying party or
promotion adapter may consume authorization later; P0 itself does not execute
merge, release, or deployment.

## Design observations

The lineage supports these non-normative observations:

1. Semantic authority must remain external to the agent.
2. Obligations require identity, applicability, required evidence roles,
   evaluation method, and satisfaction state.
3. Repository-transition semantics remain project-specific.
4. Observation and inference must remain distinct.
5. Retries and repairs are new governed occurrences.
6. Cryptographic integrity does not establish semantic sufficiency.
7. Telemetry, graph stores, snapshots, and semantic judges are projections or
   advisory evidence unless reduced to an accepted deterministic predicate.

These observations do not add obligations or change promotion policy.

## Reference-selection and update policy

Add or retain a reference only when it contributes formal semantics, an
obligation/control source, runtime verification, mature coding-agent execution,
software-assurance methodology, adversarial probes, provenance semantics, or an
adaptable implementation. Re-review volatile projects before using them as
release-policy evidence. Record a new version and review date instead of
silently changing the meaning of a prior citation.
