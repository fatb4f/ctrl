# Coding-Agent Assurance Framework and Qualification Architecture

- **Status:** Accepted architecture; implementation staged
- **Decision record:**
  [ADR-0001: App Server qualification and assurance-runtime boundaries](https://github.com/fatb4f/kernel-spec/blob/main/docs/adr/0001-app-server-qualification-and-runtime-boundaries.md)
- **Normative baseline:** [Qualification P0](https://github.com/fatb4f/kernel-spec/blob/main/docs/qualification-p0-plan/00-summary-and-authority.md)
- **Runtime specification:** [Diagnostics-Aligned Assurance Runtime v0](https://github.com/fatb4f/kernel-spec/blob/main/docs/assurance-runtime-v0.md)
- **Approval condition resolved:** Fresh LLM judgments are advisory and cannot
  satisfy hard promotion claims.

## Executive conclusion

**Review date:** 2026-08-06  
**Survey scope:** the public primary-source artifacts listed in the artifact register below.

Within this reviewed corpus, no artifact satisfies all seven operational criteria defined here for promotion-complete coding-agent assurance. This is a bounded survey result, not proof that no qualifying artifact exists outside the stated organizations, repositories, publication set, or review date.

The reviewed ecosystem is nevertheless strong when treated as a layered control system:

1. Governance frameworks define organizational obligations and risk-management expectations.
2. Threat models and taxonomies identify agent-specific failure modes.
3. Evaluation methodologies define validity, reproducibility, and reporting practices.
4. Execution harnesses, adapter suites, certification prototypes, and benchmarks run tasks and collect traces, scores, or reports.
5. Project-owned qualification logic determines whether evidence applies to the exact candidate artifact and whether promotion is authorized.
6. Runtime sensing and supervisory analysis can improve diagnosis without acquiring release authority.

The practical requirement is therefore to compose an assurance profile from recognized external artifacts while retaining a deterministic, project-owned evidence-admission, qualification, and release kernel.

The proposed executable realization is a thin `pytest-codex-appserver` stack with two additional subsystems:

```text
App Server protocol adapter
    = control-plane execution and lifecycle evidence

CPython Lib adapters
    = runtime sensing and diagnostic evidence

python-control
    = controller modeling, replay simulation and policy evaluation
```

These implementation choices are **project constraints**, not conclusions established by the landscape survey. Their selection basis and ADR boundary are stated separately below.

---

## 1. Scope and review method

### Review question

The review asks:

> Which publicly available artifacts materially contribute to governance, threat modeling, secure-coding policy, evaluation methodology, behavioral certification, coding-agent execution, capability calibration, or patch-release assurance?

The unit of analysis is an individual named artifact or software release, not an organization.

### Review date and research window

- **Review completed:** 2026-08-06.
- **Publication cutoff:** artifacts publicly available by 2026-08-06.
- **Software versions:** the latest official release located on the review date, where a package or release registry exposed an unambiguous version.
- **Draft handling:** drafts and prototypes are included but explicitly labeled and are not treated as final normative authority.

### Source method

The survey used:

1. official publisher and standards-body pages;
2. official project repositories;
3. official package registries for software version and release-date verification;
4. the artifact itself when status or scope was not fully stated on the landing page.

Secondary commentary was not used to establish title, ownership, version, status, publication date, or core capability.

### Inclusion criteria

An artifact was included when it:

- was publicly accessible from a primary source;
- was published or maintained by NIST, CSA, OWASP, UK AISI, Meridian Labs, METR, CoSAI, or OpenSSF;
- materially addressed AI governance, agentic security, coding agents, software-agent evaluation, secure coding, or release assurance;
- supplied a framework, control catalog, taxonomy, methodology, executable system, adapter suite, benchmark, ruleset, or practitioner guide.

### Exclusion criteria

The review excludes:

- closed vendor services without an auditable public artifact;
- general AI-safety material with no material agentic or software-development relevance;
- unpublished proposals and conference statements without a stable artifact;
- secondary summaries where a primary source was available;
- general-purpose test tools except where they are used later as implementation analogues rather than landscape authorities.

### Limitations and update rule

The corpus is purposive rather than exhaustive. Rapidly changing repositories can invalidate version-specific observations. Any statement using “reviewed,” “current,” “latest,” or “strongest” is scoped to this artifact register and review date. The survey should be rerun before adopting it as release-policy evidence.

---

## 2. Artifact register and comparison

### Auditable artifact register

| ID | Publisher / maintainer | Exact artifact title | Version or status reviewed | Publication or release date | Primary URL |
|---|---|---|---|---|---|
| NIST-01 | NIST | *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1 | Final; voluntary framework | 2023-01-26 | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf |
| NIST-02 | NIST | *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*, NIST AI 600-1 | Final cross-sectoral profile | 2024-07-26 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |
| NIST-03 | NIST CAISI | *Practices for Automated Benchmark Evaluations of Language Models*, NIST AI 800-2 | **Initial Public Draft**; preliminary voluntary practices | Publicly released 2026-01-30; draft PDF dated 2026-01-09 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-2.ipd.pdf |
| NIST-04 | NIST CAISI | *Technical Blog: Strengthening AI Agent Hijacking Evaluations* | Research blog reporting initial experiments | 2025-01-17 | https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations |
| NIST-05 | NIST | *Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities*, SP 800-218 | Final NIST Special Publication | 2022-02-03 | https://csrc.nist.gov/pubs/sp/800/218/final |
| NIST-06 | NIST | *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile*, SP 800-218A | Final NIST Special Publication | 2024-07-26 | https://csrc.nist.gov/pubs/sp/800/218/a/final |
| CSA-01 | Cloud Security Alliance | *AI Controls Matrix v1.1* | Released control catalog; 247 controls in 18 domains | 2026-06-22 | https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1 |
| CSA-02 | Cloud Security Alliance | *NIST AI Risk Management Framework: Agentic Profile* | **Draft** white paper | 2026-03-27 | https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/ |
| CSA-03 | Cloud Security Alliance | *Agentic AI Threat Modeling Framework: MAESTRO* | Published practitioner framework | 2025-02-06 | https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro |
| CSA-04 | Cloud Security Alliance | *Agentic AI Red Teaming Guide* | Released practitioner guide | 2025-05-28 | https://cloudsecurityalliance.org/artifacts/agentic-ai-red-teaming-guide |
| CSA-05 | Cloud Security Alliance / MassiveScale.AI | *The Agentic Trust Framework: Zero Trust Governance for AI Agents* | Open specification; community-governed | 2026-02-02 | https://cloudsecurityalliance.org/blog/2026/02/02/the-agentic-trust-framework-zero-trust-governance-for-ai-agents |
| CSA-06 | Cloud Security Alliance AI Safety Initiative | *TAISE-Agent v0.1 — AI Agent Behavioral Certification System* | **Prototype** executable certification system | 2026-03 | https://github.com/CloudSecurityAlliance/taise-agent-v01 |
| OWASP-01 | OWASP GenAI Security Project | *OWASP Top 10 for Agentic Applications for 2026* | Published community framework | 2025-12-09 | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| AISI-01 | UK AI Security Institute | *Inspect AI: Framework for Large Language Model Evaluations* | `inspect-ai` 0.3.252; Beta software | 2026-08-04 | https://pypi.org/project/inspect-ai/0.3.252/ |
| MERIDIAN-01 | Meridian Labs | *Inspect SWE: Software Engineering Agents for Inspect AI* | `inspect-swe` 0.2.68 | 2026-08-05 | https://pypi.org/project/inspect-swe/0.2.68/ |
| METR-01 | METR | *HCAST: Human-Calibrated Autonomy Software Tasks* | arXiv v1; research benchmark | 2025-03-21 | https://arxiv.org/abs/2503.17354 |
| METR-02 | METR | *RE-Bench: Evaluating Frontier AI R&D Capabilities of Language Model Agents Against Human Experts* | Public benchmark release | 2024-11-22 | https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/ |
| COSAI-01 | CoSAI / OASIS Open | *Project CodeGuard: Security Skills and Rules for AI Coding Agents* | v1.4.0 open-source release | 2026-06-29 | https://github.com/cosai-oasis/project-codeguard/releases/tag/v1.4.0 |
| OPENSSF-01 | OpenSSF Best Practices and AI/ML Working Groups | *Security-Focused Guide for AI Code Assistant Instructions* | Published community guidance | 2025-08-01 | https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions |

### Contribution and limitation comparison

| ID | Primary contribution | Main limitation for coding-patch assurance |
|---|---|---|
| NIST-01 | Cross-sector risk vocabulary, governance functions, and lifecycle outcomes | No coding episode, repository identity, evidence contract, or patch-promotion semantics |
| NIST-02 | Generative-AI risk profile and recommended risk-management actions | General GAI profile; no coding-agent execution or release calculus |
| NIST-03 | Preliminary practices for objective definition, benchmark selection, implementation, analysis, and reporting | Initial Public Draft; methodology rather than an executable coding-agent qualification profile |
| NIST-04 | Adaptive hijacking evaluation, repeated-attack measurement, and task-specific security analysis | Research findings rather than a reusable software-development assurance standard |
| NIST-05 | Secure-development and release-process practices | Assures producer process rather than one agent-generated candidate |
| NIST-06 | AI-model-development extension to SSDF | Focuses on producing AI systems, not qualifying generated patches |
| CSA-01 | Auditable control objectives, assessment questions, mappings, and machine-readable bundles | Organization- and system-level controls rather than episode-level behavioral qualification |
| CSA-02 | Autonomy tiers, tool-risk modeling, runtime telemetry, delegation accountability, and incident handling | Draft governance profile; no repository fixtures, scorers, evidence admission, or patch promotion |
| CSA-03 | Seven-layer agentic threat modeling | Threat derivation only; no execution, scoring, or evidence verdict |
| CSA-04 | Operational red-team scenarios and procedures for agentic systems | Partially executable methodology; no standardized coding-patch subject or promotion contract |
| CSA-05 | Identity, behavior, data, segmentation, incident response, and progressive autonomy | Organizational governance and autonomy promotion, not repository-artifact promotion |
| CSA-06 | Executable scenarios, deterministic and LLM-judge scoring, decisions, and reports | General behavioral certification prototype; no coding-repository or installed-artifact semantics |
| OWASP-01 | Peer-reviewed taxonomy of critical agentic application risks and mitigations | Taxonomy and guidance rather than an evaluation or release harness |
| AISI-01 | General evaluation tasks, datasets, solvers, scorers, logs, tool use, agent support, sandboxing, and checkpointing | General harness; does not define project evidence admission or patch-release authority |
| MERIDIAN-01 | Software-engineering agent implementations and adapters for Inspect AI | Agent suite layered on Inspect; does not itself own Inspect’s general harness or promotion policy |
| METR-01 | Human-calibrated autonomy tasks across software and related domains | Capability and time-horizon measurement rather than release correctness or security |
| METR-02 | Realistic AI R&D task environments and human-expert calibration | Capability benchmark with score optimization; no patch-promotion semantics |
| COSAI-01 | Model-agnostic secure-coding skills, rules, translators, validators, and review tooling | Preventive and compliance-oriented; not a complete behavioral assurance or release system |
| OPENSSF-01 | Security-focused instructions for AI code assistants and retained human responsibility | Practitioner guidance rather than executable qualification |

---

## 3. Classification and promotion-completeness rubric

### Classification schema

```cue
#FrameworkClassification: {
    domainSpecificity: "general-ai"
        | "models-and-agents"
        | "agentic"
        | "software"
        | "coding-agent"

    artifactType: "governance-framework"
        | "governance-profile"
        | "control-catalog"
        | "threat-model"
        | "methodology"
        | "research"
        | "benchmark"
        | "execution-harness"
        | "adapter-suite"
        | "certification-prototype"
        | "ruleset"
        | "guidance"

    executable: "no" | "partial" | "yes"

    // "yes" means the artifact intentionally prescribes controls,
    // practices, rules, or conformance expectations. It does not
    // imply legal mandate.
    normative: "no" | "partial" | "yes"

    promotionCoverage: {
        subjectBinding:        "absent" | "partial" | "full"
        authorityProvenance:   "absent" | "partial" | "full"
        executableEvidence:    "absent" | "partial" | "full"
        evidenceAdmission:     "absent" | "partial" | "full"
        claimsAndResiduals:    "absent" | "partial" | "full"
        deterministicDecision: "absent" | "partial" | "full"
        rollbackReversibility: "absent" | "partial" | "full"
    }

    promotionComplete: bool
}
```

### Necessary and sufficient tests

An artifact is `promotionComplete: true` only if it fully supplies all seven criteria:

| Code | Criterion | Full-coverage test |
|---|---|---|
| **S** | Subject binding | Binds evidence and decision to an exact repository/worktree and, where applicable, installed artifact |
| **A** | Authority and provenance | Records delegated capabilities, tool/mutation authority, trajectory, patch provenance, and actor identity |
| **E** | Executable evidence | Executes relevant functional, security, regression, or adversarial checks and emits machine-readable observations |
| **D** | Evidence admission | Defines applicability, integrity, freshness, duplication, conflict, and rejection semantics |
| **C** | Claims and residuals | Derives typed claims, contradictions, unresolved residuals, and sufficiency outcomes |
| **P** | Deterministic decision | Produces reproducible promote/reject/inconclusive decisions from canonical inputs |
| **R** | Rollback and reversibility | Identifies the promoted artifact and defines auditable rollback or restoration semantics |

Legend:

- `✓` = full criterion;
- `△` = partial or adjacent coverage;
- `—` = absent;
- `promotionComplete` is true only for `✓✓✓✓✓✓✓`.

### Per-artifact classification

| ID | Domain | Artifact type | Executable | Normative | Promotion coverage `S A E D C P R` | Complete |
|---|---|---|---|---|---|---:|
| NIST-01 | general-ai | governance-framework | no | yes | `— △ — — △ △ —` | No |
| NIST-02 | general-ai | governance-profile | no | yes | `— △ — — △ △ —` | No |
| NIST-03 | models-and-agents | methodology | no | partial | `— — △ △ — — —` | No |
| NIST-04 | agentic | research | partial | no | `— — △ — — — —` | No |
| NIST-05 | software | governance-framework | no | yes | `— △ — — △ △ △` | No |
| NIST-06 | general-ai | governance-profile | no | yes | `— △ — — △ △ △` | No |
| CSA-01 | general-ai | control-catalog | no | yes | `— △ — △ △ △ —` | No |
| CSA-02 | agentic | governance-profile | no | partial | `— △ — △ △ △ △` | No |
| CSA-03 | agentic | threat-model | no | partial | `— — — — △ — —` | No |
| CSA-04 | agentic | methodology | partial | yes | `— △ △ — △ — —` | No |
| CSA-05 | agentic | governance-framework | no | partial | `— △ — — △ △ △` | No |
| CSA-06 | agentic | certification-prototype | yes | partial | `— △ ✓ △ △ △ —` | No |
| OWASP-01 | agentic | threat-model | no | yes | `— — — — △ — —` | No |
| AISI-01 | agentic | execution-harness | yes | no | `△ △ ✓ △ △ — —` | No |
| MERIDIAN-01 | coding-agent | adapter-suite | yes | no | `△ △ ✓ — — — —` | No |
| METR-01 | software | benchmark | yes | no | `△ — ✓ — — — —` | No |
| METR-02 | models-and-agents | benchmark | yes | no | `△ — ✓ — — — —` | No |
| COSAI-01 | coding-agent | ruleset | partial | yes | `— △ △ — △ — —` | No |
| OPENSSF-01 | coding-agent | guidance | no | yes | `— △ — — △ — —` | No |

### Scoped landscape conclusion

Within the reviewed corpus:

- **Inspect AI** supplies the broadest general execution harness and owns tasks, datasets, solvers, scorers, logs, sandboxing, agent support, and checkpointing.
- **Inspect SWE**, maintained by Meridian Labs, supplies software-engineering agents and adapters that run on Inspect AI; it is not the owner of the underlying Inspect harness.
- **TAISE-Agent v0.1** is an executable behavioral-certification prototype with scenarios, scoring, decisions, and reports.
- **HCAST and RE-Bench** provide human-calibrated capability benchmarks.
- **NIST AI 800-2** is an Initial Public Draft evaluation methodology, not a final standard.
- **NIST, CSA, OWASP, CoSAI, and OpenSSF** contribute governance, controls, threats, red-team methods, secure-coding rules, and practitioner guidance.

These surfaces are complementary and should not be ranked as though harnesses, certification prototypes, benchmarks, and governance artifacts solve the same problem.

No reviewed artifact fully combines exact candidate identity, authority provenance, executable behavioral evidence, evidence admission, typed claims and residuals, deterministic patch promotion, and rollback.

---

## 4. Capability evaluation versus assurance qualification

Coding-agent capability and coding-agent assurance are separate control problems.

### Capability evaluation

Capability evaluation asks:

- Can the agent complete the requested task?
- How long can it execute autonomously?
- How does its performance compare with human baselines?
- How reliably does it solve a benchmark?
- Can its trajectory be monitored or interpreted?

HCAST, RE-Bench, Inspect-based campaigns, and related coding-agent evaluations primarily operate at this layer.

### Assurance qualification

Assurance qualification asks:

- Did the agent modify the correct repository state?
- Was every tool action authorized?
- Is the resulting patch attributable and reproducible?
- Does the evidence apply to the exact promoted artifact?
- Are functional, security, and regression claims supported?
- Were adversarial repository-content and tool-use cases evaluated?
- Are residual risks explicitly represented?
- Is promotion deterministic, reviewable, and reversible?

No artifact in the reviewed corpus defines this complete calculus.

---

## 5. Recommended external composition

A coding-agent assurance profile can compose reviewed artifacts by responsibility without treating them as competing end-to-end systems.

```text
Governance and control obligations
    NIST AI RMF 1.0
    NIST AI 600-1
    NIST SP 800-218 and SP 800-218A
    CSA AI Controls Matrix v1.1
    CSA Agentic Profile (draft)
            │
            ▼
Threat and adversarial-case derivation
    CSA MAESTRO
    CSA Agentic AI Red Teaming Guide
    OWASP Top 10 for Agentic Applications 2026
            │
            ▼
Secure coding policy
    CoSAI Project CodeGuard
    OpenSSF Security-Focused Guide
            │
            ▼
Evaluation methodology
    NIST AI 800-2 Initial Public Draft
            │
            ▼
Behavioral certification reference
    CSA TAISE-Agent v0.1 prototype
            │
            ▼
General episode execution
    UK AISI Inspect AI
            │
            ▼
Coding-agent implementations and adapters
    Meridian Labs Inspect SWE
    Codex App Server adapter
            │
            ▼
Capability calibration
    METR HCAST
    METR RE-Bench
            │
            ▼
Project-owned evidence qualification and release control
```

External artifacts define obligations, threats, methods, policies, executable evaluation surfaces, and calibration references. They do not replace the project-owned evidence calculus.

---

## 6. Project implementation constraints and ADR boundary

The following technologies are accepted project constraints under
[ADR-0001](https://github.com/fatb4f/kernel-spec/blob/main/docs/adr/0001-app-server-qualification-and-runtime-boundaries.md). They do
**not** follow deductively from the landscape comparison.

| Project decision | Current project status | Selection requirements | Survey limitation |
|---|---|---|---|
| CUE as structural contract authority | Accepted by ADR-0001 | Closed structural constraints, unification, validation, projection, deterministic schema generation | This review did not compare CUE against Jsonnet, Nickel, Dhall, Rego, TypeSpec, Protobuf, or JSON-Schema-first designs |
| Generated frozen Pydantic models | Accepted by ADR-0001 | Typed Python adapters, validation, serialization, generated-model discipline | This review did not compare Pydantic with dataclasses, attrs, msgspec, or generated Protobuf classes |
| pytest and Hypothesis | Accepted by ADR-0001 | Deterministic tests, fixtures, state-machine generation, shrinking, plugin integration | The landscape review treats these as implementation tools, not external assurance authorities |
| CPython runtime adapters | Accepted by ADR-0001 | Low-overhead event capture, exception/call-path evidence, process isolation | Applicable only to Python execution; other runtimes require separate adapters |
| `python-control` | Accepted for shadow analysis by ADR-0001 | Replay simulation, policy comparison, stability, saturation, and hysteresis analysis | It is not evidence authority, transition authority, or release authority |

ADR-0001 records:

1. functional and nonfunctional requirements;
2. evaluated alternatives;
3. decision criteria and tradeoffs;
4. generated-artifact authority rules;
5. migration and interoperability constraints;
6. reversal conditions.

The architecture below assumes these constraints while keeping their authority separate from external standards and survey findings.

### P0 boundary and staged adoption

The repository’s existing P0 remains the baseline qualification slice: an
SDK-compatible driver, an append-only raw event log, the scoped CPython
state-lifetime provider, one isolated fork, one bounded repair, and independent
kernel authorization. ADR-0001 accepts the App Server adapter, broad runtime
sensing, and `python-control` shadow analysis as P1/AR1 work; it does not
supersede P0.

Use two interchangeable execution providers that emit the same typed lifecycle records:

```text
SDK driver
    = mandatory CI and qualification automation path

App Server driver
    = explicit App Server protocol-conformance path
```

Current Codex guidance positions the SDK for automation and CI and App Server for deep product integrations. The App Server path is therefore an additional conformance surface, not a replacement for the qualification driver.[^appserver]

---

## 7. Executable qualification architecture

### Three-loop model

The unified system contains three interacting but separately authorized loops.

#### Protocol loop

Owns whether the Codex App Server interaction is structurally legal:

```text
    initialize
    → initialize response
    → initialized notification
    → thread/start
→ turn/start
→ item and approval events
→ steer / interrupt
→ terminal reconciliation
```

Primary mechanisms:

- pytest-managed subprocess fixture;
- generated protocol schemas;
- sealed raw JSONL log plus redacted canonical trace;
- lifecycle invariants;
- replay transport;
- Hypothesis protocol state machine.

A protocol violation is a hard failure. Semantic scores and controller recommendations cannot override it.

#### Diagnostic loop

Owns whether the current evidence sufficiently distinguishes likely failure causes:

```text
pytest result
→ exception and call-path observation
→ observability estimate
→ targeted probe or repair recommendation
→ new admitted evidence
```

Primary mechanisms:

- `sys.monitoring`;
- canonical traceback and call-edge normalization;
- progressive instrumentation;
- redacted variable shapes;
- allocation, import, audit, and resource adapters;
- deterministic feature projection;
- shadow-mode supervisory policy.

The core policy is:

```text
low observability
    → increase observation

high observability + unchanged failure
    → request repair
```

This prevents repeated speculative mutations when the active causal path is still unknown.

#### Release loop

Owns whether the exact candidate artifact may be promoted:

```text
repository snapshot
+ installed artifact
+ admitted evidence
+ claims
+ residuals
+ deterministic decision
→ promote / reject / inconclusive
```

Neither the App Server harness, the runtime collector, nor `python-control` owns promotion.

### End-to-end architecture

```text
               Project contract authority: CUE
                              │
          generated JSON Schema + frozen Pydantic models
                              │
              ┌───────────────┴────────────────┐
              │                                │
              ▼                                ▼
    App Server protocol loop          CPython runtime loop
    ------------------------          --------------------
    process fixture                    instrumented worker
    JSONL frames                       sys.monitoring
    approvals                          traceback / inspect
    turns and items                    audit observations
    interrupts                         allocation/resources
    lifecycle state                    exception/call graph
              │                                │
              ▼                                ▼
       AppServerTrace                 RuntimeProbeObservation
              └───────────────┬────────────────┘
                              ▼
                     Evidence admission
              identity · applicability · freshness
                              │
                              ▼
                    EpisodeStateEstimate
                              │
                              ▼
                 ControlPolicyEvaluation
                    advisory, shadow mode
                              │
                              ▼
                    TransitionDecision
               selected through legal CUE rules
                              │
             ┌────────────────┼─────────────────┐
             ▼                ▼                 ▼
       focused probe      agent action      terminate
       / test run         steer/repair      inconclusive
                              │
                              ▼
                    Qualification kernel
                 claims · residuals · verdict
                              │
                              ▼
                     Promotion service
```

---

## 8. Authority partition

| Component or layer | Role | Authority |
|---|---|---|
| CUE | Defines admissible structures, identities, invariants, and policy constraints | Project-selected canonical contract authority; governed by ADR |
| Generated JSON Schema | Interchange projection of the project-selected CUE contracts | Generated projection |
| Frozen Pydantic models | Typed Python transport models | Project-selected generated transport |
| App Server protocol collector | Captures requests, responses, notifications, approvals, turns, items, and process state | Protocol evidence provider |
| CPython adapters | Observe execution and produce raw runtime evidence | Runtime evidence provider |
| Evidence admission | Validates identity, applicability, integrity, freshness, and duplication semantics | Admission authority |
| Feature extractor | Deterministically projects admitted evidence into state variables | Derived-artifact producer |
| `python-control` | Simulates the plant and evaluates controller behavior | Advisory analysis |
| Transition service | Selects among CUE-admissible actions | Decision authority |
| Qualification kernel | Derives claims, conflicts, residuals, and verdicts | Qualification authority |
| Promoter | Accepts an exact repository and installed-artifact state | Release authority |
| Rollback service | Restores an accepted prior artifact and records the transition | Recovery authority |

`ControlPolicyEvaluation` is **derived and advisory**. It is not evidence about program correctness and cannot override a failed test, illegal protocol transition, inadmissible observation, unresolved residual, or failed promotion rule.

### Canonical taxonomy authority and release contracts

The canonical taxonomy is a versioned typed semantic graph governed by CUE
constraints. Statistical methods propose changes; an admission service publishes
immutable ontology releases; qualification consumes pinned ontology and
evaluation-policy releases.

The authority chain is:

```text
sealed raw event log
    → redaction and canonicalization
    → canonical observations
    → deterministic providers
    → typed structural facts
    → advisory taxonomy candidates
    → reproducible admission
    → immutable ontology release
    → obligation binding
    → pinned qualification bundle
    → evidence admission
    → qualification result
```

The artifact authorities are deliberately distinct:

| Artifact | Authority |
|---|---|
| Raw observation | Historical record, subject to capture controls |
| Canonical observation | Redacted, normalized projection |
| Structural fact | Provider-derived assertion |
| Taxonomy candidate | Advisory proposal |
| Ontology release | Published semantic authority |
| Evidence admission | Applicability and integrity decision |
| Qualification result | Verdict authority |

Structural facts precede ontology induction and therefore must not require an
ontology-release digest. They reference a structural schema and provider
version; optional semantic interpretation is a separate, later binding:

```cue
#StructuralFact: close({
    factID:     #FactID
    kind:       #FactKind
    snapshotID: #SnapshotID

    structuralSchemaDigest: #Digest
    provider: {
        id:      #ProviderID
        version: #SemanticVersion
    }
    observation: {
        rawDigest:        #Digest
        canonicalDigest:  #Digest
        captureIntegrity: #CaptureIntegrity
    }
    payload: #FactPayloadByKind[kind]
})

#SemanticFactBinding: close({
    factID:             #FactID
    ontologyReleaseDigest: #Digest
    nodeIDs:             [...#NodeID]
    edgeIDs:             [...#EdgeID]
    predicateResults:    [...#PredicateResult]
})
```

Content digests are computed over canonical content with digest fields excluded
from the hashed material (or represented by a defined placeholder). An optional
record-envelope digest may cover the complete serialized record. This prevents
self-referential identities for workspace manifests, ontology releases, and
qualification bundles.

```cue
#WorkspaceManifest: close({
    entries: [...#WorkspaceEntry]
    dependencyLockDigest: #Digest
    configurationDigest:  #Digest
    environmentProjection: {
        digest:          #Digest
        redactionPolicy: #PolicyDigest
    }
    exclusions: [...#PathPattern]
})

#OntologyRelease: close({
    releaseID:     #OntologyReleaseID
    releaseDigest: #Digest // digest of canonical content, excluding this field
    schemaVersion: #SemanticVersion
    nodes: [...#AdmittedTaxonomyNode]
    edges: [...#AdmittedTaxonomyEdge]
    relationVocabularyDigest: #Digest
    predicateRegistryDigest:  #Digest
    admissionPolicyDigest:    #Digest
    supersedes?: #OntologyReleaseID
})

#OntologyAdmissionDecision: close({
    candidateDigest:       #Digest
    releaseDraftID:        #OntologyReleaseDraftID
    admissionPolicyDigest: #Digest
    decision: "admitted" | "rejected" | "merged"
    rationale: string
    mergeTarget?: #NodeID
    actor: #EvaluatorIdentity
    decidedAt: #Timestamp
    supersedes?: #AdmissionDecisionID
})

#QualificationSemanticBundle: close({
    ontologyReleaseDigest: #Digest
    evaluationPolicyDigest: #Digest
    schemaVersion: #SemanticVersion
    providers: [...{
        providerID: #ProviderID
        version:    #SemanticVersion
        digest:     #Digest
    }]
    predicateRegistryDigest: #Digest
})
```

Provider lists and all digest-bearing collections must have canonical ordering
and duplicate rejection before a bundle or result is sealed. Admission decisions
target a release draft; the immutable release digest is computed only after the
accepted nodes, edges, vocabularies, predicates, and policy are assembled.

Raw means pre-normalization, not pre-safety. Credentials, tokens, private paths,
environment secrets, command arguments, MCP parameters, output, and diffs are
scrubbed at capture time by default. Exceptional sensitive records require
encrypted restricted storage, explicit retention, and access audit; they are
never copied into the normal canonical projection.

Qualification consumes a pinned `#QualificationSemanticBundle`. A later ontology,
policy, predicate, schema, or provider release cannot reinterpret a sealed
result; re-evaluation creates a new result linked to the prior one.

```cue
#RequalificationResult: close({
    qualificationID: #QualificationID
    requalifies: #QualificationID
    previousBundleDigest: #Digest
    currentBundleDigest:  #Digest
    result: #QualificationResult
})
```

---

## 9. App Server qualification harness

### OSS ecosystem fit

The OSS ecosystem contains most of the components needed for Codex App Server qualification, but no project provides the required authority model end to end.

The strongest realization is a thin `pytest-codex-appserver` plugin composed around:

```text
generated App Server schema
        ↓
typed protocol client
        ↓
sealed raw JSONL event log
        ↓
redacted canonical event projection
        ↓
deterministic lifecycle + trajectory assertions
        ↓
Hypothesis state-machine exploration
        ↓
optional live semantic qualification
```

The App Server surface is a long-lived child process with bidirectional JSONL communication, multi-event request lifecycles, server-initiated approval requests, and protocol definitions generated from the shipped binary.[^appserver]

### Highest-signal projects

Inspect AI and Inspect SWE are separate projects: UK AISI maintains the general evaluation harness; Meridian Labs maintains the software-engineering agent suite built for that harness.

| Project | Signal | Recommended use |
|---|---:|---|
| **`pytest-lsp`** | Very high | Process and stdio fixture architecture |
| **`agentverify`** | Very high | Deterministic step, tool, dependency, budget, and replay assertions |
| **Hypothesis stateful testing** | Very high | Generate and shrink protocol interaction sequences |
| **AgentEvals / OpenEvals** | High | Trajectory matching vocabulary |
| **Pydantic Evals** | High | Typed case datasets and generated JSON Schema |
| **AgentProbe** | Medium-high | Snapshot review, redaction, tool assertions, and CI diffs |
| **Inspect AI** | High, outer loop | Sandboxed release qualification and benchmark campaigns |
| **DeepEval / LangSmith / Scenario** | Selective | Semantic judges, telemetry, and simulated-user tests |

### Architectural borrowing

#### `pytest-lsp`

Borrow:

- subprocess ownership by a fixture;
- asynchronous stdin/stdout pumps;
- startup and teardown failure handling;
- client/server message capture;
- implementation-independent end-to-end tests.

Do not depend on LSP abstractions. Implement the generated App Server contract directly.[^pytest-lsp]

#### `agentverify`

Adapt:

- recorded cassettes;
- step-level execution models;
- exact, partial, regex, and wildcard tool matching;
- dependency assertions between steps;
- tool-success and retry assertions;
- token, cost, latency, and forbidden-tool budgets;
- human-reviewable recordings.

Project its model from `AppServerTrace`, but do not flatten approvals, interrupts, thread operations, and item lifecycles into ordinary tool calls.

```text
AppServerTrace
    → AgentExecution
        → Step[]
        → ToolInvocation[]
        → DependencyEdge[]
        → BudgetObservation
        → TerminalOutcome
```

#### Hypothesis stateful testing

Generate and shrink interaction sequences such as:

```text
initialize
→ initialize response
→ initialized notification
→ thread/start
→ turn/start
→ notification*
→ approval request?
→ approval response?
→ turn/steer | turn/interrupt
→ turn terminal event
→ thread/fork | thread/resume | thread/unsubscribe
```

Hostile actions include:

- request before initialization;
- duplicate initialization;
- duplicate or stale request IDs;
- approval response after turn termination;
- interrupt during tool execution;
- process exit during a pending server request;
- malformed JSONL;
- notification reordering in replay;
- disconnect and reconnect;
- fork at arbitrary prior turn boundaries.

A reduced failing sequence becomes durable qualification evidence.[^hypothesis]

#### AgentEvals / OpenEvals

Adopt the trajectory algebra:

- strict;
- unordered;
- subset;
- superset;
- exact, ignored, subset, superset, or custom tool-argument matching.

Represent the small algebra in CUE and expose Python assertion adapters rather than importing an unrelated framework representation as contract authority.[^agentevals]

#### Pydantic Evals

Use as a dataset and parametrization transport:

```text
CUE authored authority
    ↓
generated JSON Schema
    ↓
generated/frozen Pydantic transports
    ↓
pytest parametrization
    ↓
evaluation report
```

Use it for repository-task inputs, environment profiles, expected structural constraints, trajectory alternatives, terminal outcomes, and semantic rubrics. CUE remains authoritative.[^pydantic-evals]

#### AgentProbe and semantic tools

Reuse redaction, diff, review, cost-limit, and trace-display patterns.

Do not treat output similarity as proof of:

```text
legal control trajectory
correct repository mutation
evidence applicability
promotion eligibility
```

Scenario, DeepEval, and LangSmith may produce advisory or aggregate live-run evidence. They cannot determine protocol legality.

#### Inspect AI

Use UK AISI Inspect AI as an outer release-qualification campaign layer:

```text
pytest contract suite
    → validates protocol and evidence adapters

Inspect campaign
    → validates coding-agent behavior across repositories and task classes
```

Inspect should consume admitted traces rather than replace the inner protocol suite.[^inspect]

### App Server trace contract

```python
class AppServerTrace(BaseModel):
    schema_version: str
    schema_digest: str
    raw_trace_digest: str
    canonical_trace_digest: str
    runtime_identity: RuntimeIdentity
    repository_identity: RepositoryIdentity
    frames: tuple["ProtocolFrame", ...]
    stderr: tuple[str, ...]
    exit_status: int | None
    started_at: datetime
    duration_ms: int


ProtocolFrame = Annotated[
    ClientRequest
    | ClientResponse
    | ServerResponse
    | ClientNotification
    | ServerNotification
    | ServerRequest,
    Field(discriminator="kind"),
]
```

`AppServerTrace` is the canonical projection: `stderr`, tool arguments, and
diffs are redacted according to the evidence policy. The immutable raw log is
stored separately and referenced by `raw_trace_digest`.

The projection preserves control-plane meaning without treating lifecycle
events as semantic success:

| App Server concept | Assurance projection |
|---|---|
| Thread | Session or conversation reference |
| Turn | Controller interval |
| Item | Control-plane trajectory event |
| Command execution | Candidate action plus primary execution observation |
| File change | Mutation proposal or lifecycle status |
| MCP call | External-tool action with effect context |
| Approval request/response | Proposed authority change plus resulting effective scope |
| Sandbox policy | Declared capability constraint |
| Reasoning item | Redacted controller self-report |
| `turn/completed` | Control-plane terminal event |

Approval request is not an authority transition; the effective scope must be
derived from the response and policy. A declared sandbox is not enforcement
proof. A command completion is not proof of its side effects, and a file-change
item is not proof that the workspace changed. Independent workspace snapshots,
diffs, and effect observations establish those facts. `turn/completed` is not
runtime success and never implies `VerifiedRepair`.

Command, file-change, and MCP records carry origin, requested capability,
approval decision, effective scope, declared sandbox policy, observed
enforcement context, external-effect classification, raw-record digest, and
redacted-projection digest.

### Preserve raw evidence; normalize only the canonical projection

The raw append-only event log is retained outside the Codex-writable workspace and is never rewritten. Canonicalization produces a separate redacted projection with an explicit alias map and source digest. Admission consumes the canonical projection while retaining lineage to the raw record.

Normalize:

- request, thread, turn, and item IDs into stable aliases;
- temporary-directory prefixes;
- timestamps;
- environment-specific absolute paths;
- explicitly designated nondeterministic text fields.

Preserve in the restricted raw record (subject to capture-time scrubbing):

- method names;
- causal order;
- tool arguments;
- approval scope;
- thread, turn, and item relationships;
- diffs and file identities;
- error classes;
- terminal outcomes;
- process exit state.

The canonical projection retains only the policy-approved normalized or
redacted forms of these fields and preserves lineage to every contributing raw
source record.

### Fixtures

```python
codex_binary
app_server_process
app_server_client
app_server_trace
approval_controller
replay_transport
repository_snapshot
codex_case
```

`repository_snapshot` remains separate from thread history. A thread fork can copy conversation state, but it does not clone the repository, worktree, processes, caches, environment, or credentials.

### Hard protocol invariants

The first prototype should enforce:

1. Initialization occurs exactly once.
2. No ordinary request is admitted before initialization.
3. Every client request ID has exactly one response.
4. Every started item has one legal terminal state.
5. Every turn reaches one terminal outcome.
6. Approval requests are scoped and resolved at most once.
7. No semantic item events occur after their terminal event.
8. Interrupts leave no unresolved control request.
9. Process termination leaves no orphan subprocess.
10. Recorded traces contain no configured secrets.
11. Every frame validates against the generated protocol schema.
12. Schema/runtime drift is explicit rather than silently tolerated.

The generated client must allow only methods required by the qualification
profile. Methods that execute outside the thread sandbox, such as
`thread/shellCommand`, and experimental process controls remain denied unless
an explicit capability and isolation rule admits them.

---

## 10. CPython Lib as the sensing layer

### Primary collector: `sys.monitoring`

For Python 3.12+, use `sys.monitoring` as the main low-overhead event collector. It exposes calls, returns, raises, unwinds, yields, branches, jumps, lines, and instruction events, while allowing local events to be disabled selectively.[^sys-monitoring]

Use progressive instrumentation rather than tracing everything:

```text
Level 0 — normal qualification
    exceptions
    Python starts/returns
    calls crossing repository boundaries

Level 1 — failing module
    calls
    returns
    raises/unwinds
    coroutine resume/yield

Level 2 — suspected function
    branch-left/right
    jump
    line

Level 3 — exceptional diagnostic probe
    instructions
    selected locals
    allocation traceback
```

This is gain scheduling for observability: increase instrumentation only where current evidence cannot distinguish competing failure hypotheses.

The project baseline is Python 3.14+. Use `BRANCH_LEFT` and `BRANCH_RIGHT`;
the legacy `BRANCH` event is retained only as a compatibility observation and
is not the preferred collector path.

### Initial event set

```python
BASE_EVENTS = (
    sys.monitoring.events.PY_START
    | sys.monitoring.events.PY_RETURN
    | sys.monitoring.events.CALL
    | sys.monitoring.events.RAISE
    | sys.monitoring.events.PY_UNWIND
)
```

Branch and line events should be enabled only for selected code objects associated with the failing traceback.

### Supporting standard-library adapters

| Adapter | Evidence produced |
|---|---|
| `traceback` | Canonical exception chain, stack locations, and causal relationships |
| `inspect` | Signature, frame, coroutine, and callable identity |
| `dis` | Bytecode-level callsite and branch interpretation |
| `ast` | Static source structure associated with runtime frames |
| `importlib` | Module origin, loader, package, and import-resolution facts |
| `trace` | Lightweight caller/callee and executed-function probes |
| `tracemalloc` | Allocation deltas and allocation traceback |
| `faulthandler` | Crash, deadlock, and timeout stack dumps |
| `cProfile` / `pstats` | Call counts and time distribution |
| `gc` | Leak-oriented object and reference probes |
| `resource` | Process resource envelope on supported platforms |

The `trace` module can report executed functions and caller/callee relationships. `tracemalloc` supports allocation traceback and before/after snapshot comparison. Deterministic profilers expose call counts and execution-time statistics, but profiling output should not be treated as precise benchmark measurement.[^trace]

### Audit hooks

Use CPython audit events to observe operations such as process creation, file access, imports, and network activity where events are available.

Do not treat audit hooks as a sandbox or hard policy boundary. Python-level audit hooks can be disabled or bypassed by malicious code.[^audit]

```text
audit observation
    → evidence

sandbox / isolated credentials / OS policy
    → enforcement
```

### Runtime evidence contract

```cue
#RuntimeProbeSpec: close({
    schema: "qualification.runtime-probe-spec.v0"

    subject: #SubjectIdentity
    scope: {
        modules: [...#ModuleSelector]
        functions?: [...#FunctionSelector]
    }

    events: [...(
        "py-start"
        | "py-resume"
        | "py-return"
        | "py-yield"
        | "call"
        | "raise"
        | "unwind"
        | "jump"
        | "instruction"
        | "branch-left"
        | "branch-right"
        | "line"
        | "allocation"
        | "audit"
    )]

    capture: {
        locals: "none" | "shape" | "redacted-values"
        maxStackDepth: int & >=1 & <=64
        maxEvents: int & >=1
    }
})

#RuntimeEvent: close({
    sequence: uint
    processID: #StableAlias
    threadID: #StableAlias
    taskID?: #StableAlias

    kind: "py-start"
        | "py-resume"
        | "py-return"
        | "py-yield"
        | "call"
        | "raise"
        | "unwind"
        | "jump"
        | "instruction"
        | "branch-left"
        | "branch-right"
        | "line"
        | "allocation"
        | "audit"
    code?: #CodeIdentity
    location?: #SourceLocation
    parentEvent?: uint

    value?: #RedactedValue
    exception?: #ExceptionObservation
})

#RuntimeProbeObservation: close({
    schema: "qualification.runtime-probe-observation.v0"

    subject: #SubjectIdentity
    runtime: #CPythonRuntimeIdentity
    probe: #RuntimeProbeSpec & {subject: subject}
    probeDigest: #Digest
    pytestNodeID: string
    processID: #StableAlias
    appServerThreadID: #StableAlias
    appServerTurnID?: #StableAlias

    events: [...#RuntimeEvent]
    allocations?: #AllocationDelta
    imports?: [...#ImportObservation]
    resources?: #ResourceObservation

    startedAt: #DecisionInputTimestamp
    finishedAt: #DecisionInputTimestamp
})
```

### Identity requirements

Every runtime observation should bind to:

```text
repository tree digest
worktree digest
Python implementation and version
Python executable digest
dependency-lock digest
probe-spec digest
pytest node ID
process identity
App Server thread and turn
```

Without these fields, a stack or runtime event cannot establish applicability to the candidate being promoted.

### Variable capture

Do not serialize arbitrary `frame.f_locals`.

Default representation:

```python
class RedactedValue(BaseModel):
    type_name: str
    shape: tuple[int, ...] | None
    length: int | None
    stable_digest: str | None
    preview: str | None = None
    redaction: Literal["none", "secret", "volatile", "unsupported"]
```

Only explicitly approved probes should capture values. Secrets, credentials, large payloads, and nondeterministic object representations should be redacted before entering the evidence store.

---

## 11. `python-control` as the supervisory analysis layer

Coding-agent episodes are not naturally continuous, linear systems. They are discrete, event-driven, nonlinear, partially observed, mode-switching, constrained by legal actions, and subject to stochastic disturbances.

Model the episode initially as a discrete nonlinear I/O system, not as a continuous PID loop or global LTI approximation. `python-control` supports nonlinear input/output systems with explicit update and output functions, discrete timebases, simulation, operating-point search, and local linearization.[^nlsys]

### State definition

A minimal normalized state vector:

```text
x[k] =
[
  normalized failing-test count,
  unchanged-failure streak,
  new-regression count,
  mutation-survivor ratio,
  unresolved-exception count,
  protocol-violation count,
  unresolved-approval count,
  repository churn ratio,
  probe information gain,
  observability,
  evidence freshness,
  runtime instability score,
  remaining budget ratio
]
```

State variables are deterministic projections from admitted evidence, not controller-owned mutable facts.

### Inputs

```text
u[k] =
[
  run focused test,
  run broader test set,
  enable call tracing,
  enable branch tracing,
  inspect variable shape,
  run allocation probe,
  request agent repair,
  steer current turn,
  interrupt current turn,
  roll back candidate,
  terminate inconclusive
]
```

Use an enum or one-hot action vector rather than arbitrary continuous control values.

### Disturbances

```text
d[k] =
[
  model-output variance,
  test flakiness,
  dependency nondeterminism,
  scheduler variance,
  environment drift,
  external-process failure
]
```

### Outputs

```text
y[k] =
[
  progress score,
  qualification confidence,
  observability score,
  safety margin,
  expected remaining attempts,
  oscillation risk
]
```

### Plant equation

```text
x[k+1] = f(x[k], u[k], d[k])
y[k]   = h(x[k])
```

The initial `f` should come from conservative manually specified bounds or replayed episode transitions. It should not claim to predict exact agent behavior.

### Control concepts mapped to qualification

#### Observability

Question:

> Can the currently admitted evidence distinguish the plausible root causes?

```text
pytest failure alone
    → low observability

pytest failure + exception chain
    → moderate observability

exception chain + call edges + branch outcome
    → high observability
```

When observability is low, select a probe rather than authorize another speculative repository mutation.

#### Controllability and reachability

Question:

> Is there an admissible sequence of allowed actions that can reach a qualified state?

Examples of unreachable conditions:

- required dependency unavailable;
- unsupported interpreter version;
- reproduction requires forbidden credentials;
- failing test depends on an external system outside the sandbox;
- mutation or execution budgets are exhausted.

The correct terminal state is `inconclusive` or `infrastructure-failure`, not repeated repair.

#### Stability

The main unstable mode is oscillation:

```text
repair A
→ test
→ repair B
→ test
→ revert toward A
→ repeat
```

Detect this using:

- repeated failure fingerprints;
- repeated diff fingerprints;
- alternating touched-symbol sets;
- zero information-gain probes;
- no monotonic reduction in residuals.

#### Saturation

Every actuator needs limits:

```text
max focused-test repeats
max full-suite executions
max instrumentation level
max repair turns
max changed files
max wall-clock budget
max token budget
```

A saturated action must not be selected again.

#### Hysteresis

Do not change controller modes on one weak observation.

```text
enter targeted-diagnosis mode
    after 2 unchanged failure transitions

leave targeted-diagnosis mode
    only after a changed failure fingerprint
    or measurable information gain
```

This prevents probe/repair mode chatter.

#### Residuals

Residuals are differences between predicted and observed transitions:

```text
predicted:
    focused test after repair should remove failure F

observed:
    F remains with identical traceback

residual:
    repair did not affect the active causal path
```

A residual informs the next diagnostic decision. It does not itself prove a root cause.

### Controller artifact contracts

```cue
#EpisodeStateEstimate: close({
    schema: "qualification.episode-state-estimate.v0"

    episode: #EpisodeIdentity
    basedOn: [...#EvidenceDigest]

    state: {
        failingTestRatio: number & >=0 & <=1
        unchangedFailureStreak: uint
        regressionRatio: number & >=0 & <=1
        mutationSurvivorRatio: number & >=0 & <=1
        unresolvedExceptionCount: uint
        protocolViolationCount: uint
        unresolvedApprovalCount: uint
        repositoryChurnRatio: number & >=0 & <=1
        informationGain: number & >=0 & <=1
        observability: number & >=0 & <=1
        evidenceFreshness: number & >=0 & <=1
        runtimeInstability: number & >=0 & <=1
        budgetRemaining: number & >=0 & <=1
    }

    estimatorVersion: #Digest
})

#ControlAction:
    "run-focused-test"
    | "run-suite"
    | "increase-runtime-observation"
    | "inspect-variable-shape"
    | "run-allocation-probe"
    | "request-repair"
    | "steer-turn"
    | "interrupt-turn"
    | "rollback"
    | "terminate-inconclusive"
    | "continue-qualification"
    | "resolve-control-request"
    | "reproduce-stability"

#ControlActionRequest: close({
    kind: #ControlAction
    target?: string
    parameters?: {...}
})

#ControlPolicyEvaluation: close({
    schema: "qualification.control-policy-evaluation.v0"

    stateEstimate: #Digest
    policy: #PolicyIdentity

    candidates: [...close({
        action: #ControlActionRequest
        predictedState?: #Digest
        predictionModel?: #Digest
        cost: number
        risk: number & >=0 & <=1
        rationaleCodes: [...#RationaleCode]
    })]

    recommended: #ControlActionRequest
})

#TransitionDecision: close({
    schema: "qualification.transition-decision.v0"

    admittedEvidence: [...#EvidenceDigest]
    stateEstimate: #Digest
    policyEvaluation?: #Digest

    selectedAction: #ControlActionRequest
    authorityRule: #RuleIdentity
})
```

Critical distinction:

```text
RuntimeProbeObservation
    = evidence

EpisodeStateEstimate
    = deterministic derived artifact

ControlPolicyEvaluation
    = advisory analysis

TransitionDecision
    = authorized decision
```

### Thin controller realization

For P1 shadow mode, do not start with LQR, MPC, or learned state estimation.

Use a deterministic hybrid supervisor:

```python
def choose_action(state: EpisodeState) -> Action:
    if state.protocol_violation_count:
        return Action.INTERRUPT_TURN

    if state.unresolved_approval_count:
        return Action.RESOLVE_CONTROL_REQUEST

    if state.budget_remaining <= 0:
        return Action.TERMINATE_INCONCLUSIVE

    if state.runtime_instability >= 0.8:
        return Action.REPRODUCE_STABILITY

    if state.unchanged_failure_streak >= 2:
        if state.observability < 0.6:
            return Action.INCREASE_RUNTIME_OBSERVATION
        return Action.REQUEST_REPAIR

    if state.regression_ratio > 0:
        return Action.RUN_FOCUSED_TEST

    return Action.CONTINUE_QUALIFICATION
```

The Python policy returns a generated action kind; the transition adapter must
wrap it as `#ControlActionRequest` with the exact target, parameters, authority
rule, and preconditions before execution.

Use `python-control` initially to:

1. encode the transition model;
2. simulate recorded action sequences;
3. compare candidate policies;
4. detect oscillation and poor settling behavior;
5. evaluate sensitivity to delayed or noisy observations;
6. test saturation and hysteresis settings.

A nonlinear discrete model skeleton (a five-state shadow projection of the full
state contract, not an alternate contract):

```python
from __future__ import annotations

import control as ct
import numpy as np
from numpy.typing import NDArray


def update(
    _t: float,
    x: NDArray[np.float64],
    u: NDArray[np.float64],
    params: dict[str, float],
) -> NDArray[np.float64]:
    decay = params["evidence_decay"]

    failing, repetition, observability, instability, budget = x
    probe, repair, interrupt = u

    next_state = np.array(
        [
            failing - repair * observability,
            repetition + failing * (1.0 - repair),
            observability + probe * (1.0 - observability),
            instability + repair * (1.0 - observability) - interrupt,
            budget - params["action_cost"],
        ],
        dtype=float,
    )

    next_state[2] *= decay
    return np.clip(next_state, 0.0, 1.0)


def output(
    _t: float,
    x: NDArray[np.float64],
    _u: NDArray[np.float64],
    _params: dict[str, float],
) -> NDArray[np.float64]:
    failing, repetition, observability, instability, budget = x

    progress = 1.0 - failing
    safety_margin = 1.0 - instability

    return np.array(
        [progress, observability, safety_margin, budget],
        dtype=float,
    )


episode_model = ct.nlsys(
    update,
    output,
    states=[
        "failing",
        "repetition",
        "observability",
        "instability",
        "budget",
    ],
    inputs=["probe", "repair", "interrupt"],
    outputs=["progress", "observability", "safety_margin", "budget"],
    dt=True,
    params={
        "evidence_decay": 0.98,
        "action_cost": 0.05,
    },
)
```

This is a policy-test model, not a claim that coding-agent behavior follows those exact equations.

Once replay evidence supports a locally stable operating regime, `python-control` may be used offline to find operating points, linearize the nonlinear model, and evaluate discrete LQR or estimator designs. These remain later policy-analysis tools, not P0 actuation mechanisms.[^operating-point]

---

## 12. Unified episode and evidence contracts

### Coding-agent qualification episode

```cue
#CodingAgentQualificationEpisode: close({
    schema: "qualification.coding-agent-episode.v0"

    subject: {
        repository: #RepositorySnapshotIdentity
        worktree: #WorktreeIdentity
        installedArtifact?: #InstalledArtifactIdentity
    }

    request: #ChangeSpecification

    agent: #AgentIdentity
    authority: #CapabilityEnvelope
    sandbox: #SandboxProfile

    protocol: #AppServerTrace
    runtime: [...#RuntimeProbeObservation]

    admittedEvidence: [...#EvidenceDigest]
    stateEstimates: [...#EpisodeStateEstimate]
    policyEvaluations: [...#ControlPolicyEvaluation]
    transitions: [...#TransitionDecision]

    adversarialCases: [...#ThreatCase]
    claims: [...#QualifiedClaim]
    residuals: [...#Residual]

    verdict: #QualificationVerdict
    promotion?: #PromotionDecision
})
```

### Required standardized identities and semantics

A complete coding-agent assurance profile must standardize at least:

- repository, worktree, and installed-artifact identity;
- requested-change identity;
- agent, model, and policy identity;
- delegated tool and mutation authority;
- patch and trajectory provenance;
- execution-environment identity;
- App Server schema and runtime identity;
- runtime probe identity;
- evidence applicability and freshness;
- repeated stochastic-trial semantics;
- adversarial repository-content attacks;
- functional, security, and regression claims;
- conflicting and duplicate evidence handling;
- residual-risk accounting;
- deterministic promotion, rejection, rollback, and inconclusive decisions.

### Trace separation

Protocol and runtime traces remain separate because they prove different facts:

```text
AppServerTrace
    proves control-plane behavior

RuntimeProbeObservation
    observes candidate-program execution
```

They are joined only through explicit identities:

- qualification episode;
- repository tree;
- worktree;
- pytest node;
- App Server thread;
- App Server turn;
- runtime worker process;
- probe specification.

### Admission before state estimation

```text
raw observation
→ integrity validation
→ identity and applicability checks
→ freshness and duplication handling
→ admitted evidence
→ deterministic feature projection
→ state estimate
→ policy evaluation
```

The controller must never consume unadmitted raw events directly.

Execution results are primary observations. They become applicable evidence only
after subject identity, capture integrity, provenance, freshness, redaction, and
policy admission have been established. The qualification kernel remains the
sole verdict authority.

---

## 13. App Server and runtime integration

```text
turn/start
    │
    ▼
agent edits repository
    │
    ▼
pytest command launched in instrumented CPython worker
    │
    ├── pytest result
    ├── sys.monitoring events
    ├── exception and stack graph
    ├── audit observations
    ├── allocation/resource deltas
    └── process terminal state
            │
            ▼
     RuntimeProbeObservation
            │
            ▼
       evidence admission
            │
            ▼
       state estimation
            │
            ▼
    policy evaluation
            │
            ▼
    authorized action
       ├── turn/steer
       ├── new turn/start
       ├── focused probe
       ├── turn/interrupt
       └── terminate inconclusive
```

The CPython worker should be a child of the qualification harness, not embedded inside the App Server process. This preserves:

- independent process identity;
- crash isolation;
- explicit environment capture;
- reliable teardown;
- separate protocol and program-runtime evidence.

CPython instrumentation covers Python execution only. Go, Rust, shell tools, and native subprocesses require separate evidence adapters.

---

## 14. Combined state-machine qualification

The protocol state machine should be paired with runtime, admission, controller, and promotion machines:

```text
ProtocolMachine
    generates App Server interactions

RuntimeMachine
    generates runtime observations

AdmissionMachine
    validates applicability, freshness and identity

ControllerMachine
    projects state and selects legal actions

PromotionMachine
    derives claims and release decisions

CombinedMachine
    checks cross-loop invariants
```

### Important generated sequences

```text
same failure → same repair → same failure

low observability → repeated repair without probe

probe saturation → another probe request

interrupt → unresolved runtime worker

runtime crash → controller recommends continue

fresh state estimate → stale evidence replacement

new regression → promotion recommendation

failure fingerprint alternates A/B/A/B

high-cost full suite → no information gain

protocol terminal event → semantic event accepted

thread fork → repository state assumed cloned
```

### Cross-loop invariants

1. No control decision references unadmitted evidence.
2. No state estimate omits its evidence digests.
3. Identical canonical evidence produces the same state estimate.
4. Identical state and policy produce the same candidate ordering.
5. Illegal App Server actions are never emitted.
6. Saturated actions are not selected again.
7. Hard protocol or safety failures dominate progress scores.
8. Low observability cannot increase qualification confidence.
9. Controller output cannot directly promote a candidate.
10. Replay produces the same transition decisions.
11. Runtime workers terminate or are reconciled before episode closure.
12. Thread-history operations never imply repository cloning.
13. Stale evidence cannot replace fresh evidence without an explicit rule.
14. New regressions prevent promotion regardless of controller progress.
15. Identical evidence digests are idempotent; conflicting logical duplicates are rejected.
16. No qualification result consumes an unpinned ontology, evaluation policy, predicate registry, schema, or provider implementation.
17. Later semantic releases cannot reinterpret a sealed result; requalification emits a new result with explicit lineage.
18. Published ontology releases are immutable; corrections create a superseding release.
19. No raw-sensitive record enters the normal canonical projection without capture-time redaction or restricted-storage admission.

---

## 15. CI and qualification partition

### Pull requests: deterministic

```text
generated-schema drift
protocol unit tests
subprocess lifecycle tests
Hypothesis state-machine tests
recorded replay episodes
runtime collector unit tests
state-projection determinism
repository mutation assertions
zero live model calls
```

### Nightly: stochastic

```text
pinned live model matrix
repeated repository tasks
adversarial scenarios
trajectory-family analysis
latency and cost distributions
semantic judges
controller shadow-policy comparison
```

A single stochastic failure should not necessarily block promotion. Use repeated episodes and a distributional criterion, such as a lower confidence bound on success rate, while deterministic contract violations remain immediate hard failures.

### Release qualification

```text
sandboxed Inspect campaigns
real repository snapshots
mutation testing
installed-artifact requalification
security and supply-chain providers
non-inferiority comparison against accepted baseline
deterministic evidence admission
project-owned promotion decision
```

---

## 16. Recommended package boundary

```text
pytest_codex_appserver/
├── protocol/
│   ├── client.py
│   ├── frames.py
│   ├── normalize.py
│   └── invariants.py
├── runtime/
│   ├── spec.py
│   ├── monitoring.py
│   ├── audit.py
│   ├── stack.py
│   ├── allocations.py
│   ├── normalize.py
│   └── worker.py
├── evidence/
│   ├── admission.py
│   ├── identity.py
│   └── manifest.py
├── state/
│   ├── features.py
│   └── estimator.py
├── control/
│   ├── model.py
│   ├── policy.py
│   ├── simulator.py
│   └── evaluation.py
├── hypothesis/
│   ├── protocol_machine.py
│   ├── runtime_machine.py
│   ├── admission_machine.py
│   └── closed_loop_machine.py
├── qualification/
│   ├── claims.py
│   ├── residuals.py
│   └── verdict.py
└── plugin.py
```

The package should expose adapters and typed projections while keeping admission, qualification, and promotion rules in the project-owned kernel.

---

## 17. P1 App Server/runtime vertical slice

The repository qualification lifecycle remains **P0**. The App Server/runtime
slice is **P1** in the repository-wide lifecycle plan and uses the
`appserver-p1` identifier prefix. It does not introduce a second P0 taxonomy.

Implement one closed-loop episode:

```text
generated App Server JSON Schema
→ typed Python frame models
→ pytest-owned App Server subprocess
→ deterministic repository fixture with one Python defect
→ one Codex candidate repair
→ focused pytest run in an instrumented CPython worker
→ sys.monitoring call/return/raise observation
→ canonical exception and call-path evidence
→ sealed raw plus redacted canonical protocol and runtime observations
→ evidence admission
→ deterministic state projection
→ rule-based shadow recommendation
→ python-control replay simulation (shadow mode only)
→ Hypothesis cross-loop invariants
→ existing deterministic promotion gate
```

### P1 includes

- generated App Server schema and typed frames;
- pytest-lsp-style stdio fixture;
- sealed raw JSONL log plus redacted canonical trace;
- 10–12 protocol lifecycle invariants;
- replay cassette;
- protocol Hypothesis state machine;
- `sys.monitoring` collector;
- exception-chain and call-edge normalization;
- no arbitrary locals;
- one `RuntimeProbeObservation` schema;
- subject identity and evidence applicability;
- one deterministic state projector;
- one shadow-mode controller;
- `python-control` replay simulation in shadow mode only;
- Hypothesis tests for saturation, oscillation, stale evidence, and cross-loop teardown;
- no autonomous controller actuation;
- promotion controlled only by the existing release gate.

### P1 explicitly excludes

- arbitrary local-variable serialization;
- autonomous controller actuation;
- learned state estimation;
- LQR or MPC production control;
- semantic judges as hard gates;
- full-suite stochastic qualification;
- cross-language runtime instrumentation;
- controller-directed promotion;
- organizational waiver workflows.

### Shadow-mode exit criteria

The first actuator may be enabled only after replay demonstrates:

```text
zero illegal actions
zero promotion bypasses
bounded probe escalation
bounded repair repetition
deterministic replay
correct saturation handling
correct stale-evidence rejection
better information gain than the baseline policy
```

---

## 18. Diagnostics-aligned execution harness

This subsystem complements the semantic-taxonomy architecture. It records Codex
lifecycle events as sealed observations, derives canonical facts through pinned
adapters, executes qualification workflows through a typed graph, and exposes
DuckDB, OpenTelemetry, marimo, and `python-control` as projections or consumers.
None of those projections acquires semantic or verdict authority.

```text
Codex SDK / App Server
        │
        ▼
capture-time safety filtering
        │
        ▼
sealed source journal
        │
        ├──► canonical lifecycle facts
        ├──► OpenTelemetry projection
        ├──► DuckDB analytical projection
        └──► replay input
                     │
                     ▼
              typed episode workflow
                     │
                     ▼
              controlled probe runner
                     │
                     ▼
             admitted observations
                     │
        ┌────────────┴─────────────┐
        ▼                          ▼
 deterministic evaluation     marimo workbench
                                      │
                                      ▼
                        python-control shadow analysis
```

### 18.1 Source-specific JSONL journal

The journal is the first durable boundary. Producer-boundary capture fidelity
is evaluated separately from normalization coverage: capture retains every
received payload and stable source identity; normalization converts every
source record or marks it explicitly unhandled with a reason. The journal is
append-only, sequence-numbered, and content-addressed.
Capture-time scrubbing removes credentials, tokens, private paths, environment
secrets, MCP parameters, and other prohibited values before ordinary storage.
Exceptional sensitive records require separate encrypted, restricted storage,
retention rules, and access auditing.

```json
{
  "journalSchema": "codex-event-envelope.v0",
  "sequence": 184,
  "collectorRunId": "run_...",
  "sourceConnectionId": "conn_...",
  "observedAt": "2026-08-06T14:31:22.184Z",
  "source": "app-server",
  "sourceSchemaDigest": "sha256:...",
  "threadId": "thr_...",
  "turnId": "turn_...",
  "itemId": "item_...",
  "method": "item/completed",
  "payloadSchema": "app-server.protocol.current",
  "payload": {},
  "previousRecordDigest": "sha256:...",
  "recordDigest": "sha256:..."
}
```

`recordDigest` excludes itself from the canonical hashed content and uses a
domain-separated digest algorithm. A journal head checkpoint, external seal,
or equivalent trusted storage is required to detect truncation or forked
journals; a hash chain alone is not an immutability guarantee.

Codex surfaces have distinct wire lifecycles and must retain source provenance:

```text
codex exec --json:
    thread.started, turn.started, turn.completed, turn.failed, item.*

App Server:
    JSON-RPC/JSONL methods and notifications such as
    thread/started, turn/started, item/started, item/completed,
    error, and turn/completed(status = completed|interrupted|failed)
```

The adapters should expose a shared canonical fact vocabulary only where the
source supplies sufficient information. Each fact records source coverage,
loss/omission metadata, adapter version, and source digest. “SDK and App Server
representations normalize identically” is therefore a testable claim for shared
facts, not a presumption that the transports are interchangeable.

### 18.2 Canonical projections and DuckDB

Do not write directly from the source stream into normalized relations. First
seal the source journal, then materialize a redacted canonical projection:

```text
raw_events
threads
turns
items
commands
file_changes
approvals
tool_calls
warnings
errors
lifecycle_anomalies
event_correlations
```

DuckDB may ingest newline-delimited JSON for prototyping,[^duckdb] but production tables
use explicit schemas, stable keys, canonical ordering, source digests, and a
versioned projection SQL digest. The ordinary analytical database contains only
policy-approved canonical payloads; restricted raw records remain outside it.
Rebuilding the projection is equivalent when canonical relations and digests
match, independent of row order or DuckDB insertion order.

Canonical facts retain a non-empty list of all contributing source-record IDs.
Semantic deduplication never discards many-to-one provenance.

Retain both lifecycle transitions and terminal objects:

```text
item/started → item/delta* → item/completed
```

`item/completed` is authoritative for the item’s final control-plane
representation. Intermediate events remain necessary for timing, attempted
actions, partial output, and anomaly analysis. A completed item or turn never
proves that an obligation was satisfied. Commands require independent effect
observations, and `fileChange` items require workspace snapshots or diffs to
establish actual mutation.

### 18.3 Typed episode workflow

`pydantic-graph` is an operational workflow engine, not the canonical ontology.[^pydantic-graph]
Its graph definition, implementation version, and policy bundle are pinned.
Node transitions must be generated or checked against the CUE-authorized action
surface; graph execution does not independently enforce CUE constraints.

```text
MaterializeSubject
    ↓
StartCodexTurn
    ↓
CollectLifecycleEvents
    ↓
NormalizeObservations
    ↓
AdmitEvidence
    ├── sufficient → ProduceVerdict
    ├── ambiguous  → SelectProbe
    └── invalid    → RejectEpisode
                       ↓
                 ExecuteProbe
                       ↓
                 CollectObservation
```

Workflow state carries immutable identifiers and digests, not mutable evidence
objects:

```python
@dataclass(frozen=True)
class EpisodeState:
    episode_id: str
    subject_snapshot_digest: str
    ontology_release_digest: str
    evaluation_policy_digest: str
    workflow_release_digest: str
    journal_head_digest: str
    hypothesis_set_digest: str
    budget_state_digest: str
```

The qualification kernel alone determines whether admitted evidence satisfies
an obligation and produces a verdict. Graph-node transitions cannot create
ontology edges or promote an artifact.

### 18.4 Diagnostics-aligned interpreter

The interpreter is an explicit subject component. The P0 diagnostic runner uses
the exact qualified executable and records its implementation, version, prefix,
base prefix, `sys.path`, flags, `sysconfig` paths, installed distributions,
platform, working directory, and selected environment-variable projection.
Environment values are allow-listed and redacted; distribution and path lists
are canonically sorted before hashing.

Run the exact uninstrumented failing command before applying any diagnostic
bootstrap. A probe overlay must be explicit, versioned, and digested. It must
not silently use `sitecustomize`, executable `.pth` lines, or shell-wide
`PYTHONPATH`, because those mechanisms can change import behavior and invalidate
the subject being diagnosed. The overlay’s package paths and bootstrap digest
are part of the probe identity.

```text
qualified interpreter: reproduce the failure without instrumentation
diagnostic interpreter: run the declared probe overlay
comparison: classify observations and account for perturbation
```

CPython audit hooks and `sys.monitoring` are diagnostic providers only. They do
not establish a sandbox or hard authority boundary; process launch policy and
the external sandbox remain authoritative.

### 18.5 OpenTelemetry and marimo boundaries

OpenTelemetry is the correlation plane,[^otel] not the evidence store or verdict
authority. Use project-owned attributes such as:

```text
assurance.episode.id
assurance.subject.digest
assurance.ontology.release_digest
assurance.policy.digest
codex.thread.id
codex.turn.id
codex.item.id
probe.id
hypothesis.id
observation.id
evidence.id
```

Every span links to a journal, probe, or observation digest. Removing OTel data
must not change qualification.

marimo is a reproducible review and replay surface.[^marimo] It may query DuckDB, invoke
replay APIs, render timelines, compare policy revisions, run eval cases, and
export review artifacts. It must not mutate canonical records, issue authoritative
verdicts, or become the persistent workflow engine. Exported workbooks include
their source, dependency, projection, and bundle digests.

Before AR1, both Xonsh and marimo must be generated adapters over one explicit
application-service contract:

```text
Xonsh aliases ─┐
               ├──► WorkbookApplicationService
marimo controls┘

WorkbookApplicationService
├── application.status
├── episode.open
├── events.query
├── obligation.inspect
├── episode.replay
├── replay.compare
├── evaluation.run
├── policy.compare
└── artifact.export
```

This service boundary is deferred from AR0 but required before either operator
surface is admitted in AR1.

### 18.6 `python-control` shadow analysis

The first controller remains a deterministic discrete policy over admitted
evidence. `python-control` runs in shadow mode over recorded episodes to compare
probe-selection policies, information gain, cost, delay, oscillation, and
stability. Optimized or learned parameters may propose a bounded policy revision;
they cannot bypass legal transitions, evidence sufficiency, or promotion rules.

### 18.7 Diagnostics vertical slice

The repository qualification lifecycle remains P0. This diagnostics slice is
P1 in the repository-wide lifecycle plan and uses the `diagnostics-p1`
identifier prefix.

```text
capture one Codex JSONL/App Server episode
→ seal and redact the journal
→ derive canonical lifecycle facts
→ project to DuckDB and OTel
→ run one typed diagnostic workflow
→ execute one declared probe in a pinned interpreter
→ admit observations and evaluate deterministic assertions
→ inspect and replay in marimo
→ compare python-control policies in shadow mode
```

The initial scenario is a pytest collection `ModuleNotFoundError`. Required
probes identify the interpreter, inspect `sys.path`, inspect installation state,
resolve the import specification, rerun an isolated import, and rerun pytest
collection. The first slice excludes autonomous controller actuation, learned
state estimation, semantic judges as hard gates, cross-language instrumentation,
and controller-directed promotion.

### 18.8 Core evaluation matrix

| Evaluation | Invariant |
|---|---|
| Journal replay | Same sealed canonical journal produces the same facts |
| Adapter coverage | Shared facts match only where source coverage permits |
| Lifecycle closure | Every started object completes, fails, or is explicitly unresolved |
| Interpreter identity | Probe evidence binds to the requested executable and environment |
| Bootstrap visibility | Every injected helper is declared and digested |
| Trace correlation | Every projection links to a source or probe digest |
| Graph determinism | Same pinned state and admitted observations produce the same transition |
| Projection reproducibility | Rebuilding DuckDB produces equivalent canonical relations |
| Verdict independence | Removing OTel or marimo does not change qualification |
| Controller shadowing | `python-control` recommendations never directly actuate an episode |

---

## 19. Architectural conclusion

The reviewed standards and guidance corpus can specify:

- what must be governed;
- which threats should be considered;
- how evaluations should be designed;
- how coding-agent episodes can be executed;
- which secure-coding rules should apply.

The OSS ecosystem can supply:

- subprocess and stdio fixture patterns;
- protocol state-machine testing;
- trajectory constraint vocabulary;
- typed evaluation datasets;
- redaction and snapshot review;
- outer-loop sandboxed campaigns.

CPython can supply:

- runtime call, return, exception, branch, import, allocation, and resource observations.

`python-control` can supply:

- replay simulation;
- controller comparison;
- oscillation analysis;
- saturation and hysteresis evaluation;
- delayed and noisy observation analysis.

None of these components specifies the complete evidence calculus required to promote an agent-generated patch.

Under ADR-0001, the CUE qualification profile remains the selected canonical authority for:

```text
repository identity
+ authorized mutation scope
+ trajectory provenance
+ installed-artifact identity
+ observation applicability
+ evidence freshness
+ adversarial qualification
+ deterministic admission
+ state-projection identity
+ claim derivation
+ residual accounting
+ promotion and rollback
```

The resulting system is best described as a **coding-agent assurance profile and closed-loop qualification architecture** composed from recognized governance, security, evaluation, execution, runtime-observation, and control-analysis components, with deterministic project-owned evidence admission and release control.

The diagnostics harness adds a practical analytical surface—journal replay,
DuckDB projection, typed episode execution, OTel correlation, and marimo review—
without changing that authority model.

Its principal realization is not merely “runtime tracing plus an optimizer.” It is:

```text
typed protocol observations
+ typed CPython observations
→ admitted evidence
→ deterministic state estimate
→ simulated supervisory policy
→ separately authorized action
→ independent qualification and promotion
```

---

## References

[^appserver]: OpenAI, “Codex App Server” (SDK for automation/CI; App Server for deep product integrations): https://developers.openai.com/codex/app-server
[^pytest-lsp]: `pytest-lsp` project: https://pypi.org/project/pytest-lsp/
[^hypothesis]: Hypothesis stateful testing documentation: https://hypothesis.readthedocs.io/en/latest/stateful.html
[^agentevals]: AgentEvals repository: https://github.com/langchain-ai/agentevals
[^pydantic-evals]: Pydantic Evals dataset documentation: https://pydantic.dev/docs/ai/api/pydantic_evals/dataset/
[^inspect]: UK AISI Inspect documentation: https://inspect.aisi.org.uk/
[^sys-monitoring]: Python `sys.monitoring` documentation: https://docs.python.org/3/library/sys.monitoring.html
[^trace]: Python `trace` documentation: https://docs.python.org/3/library/trace.html
[^audit]: Python `sys` audit-hook documentation: https://docs.python.org/3/library/sys.html
[^nlsys]: Python Control Systems Library nonlinear I/O systems: https://python-control.readthedocs.io/en/latest/generated/control.nlsys.html
[^operating-point]: Python Control Systems Library operating-point documentation: https://python-control.readthedocs.io/en/latest/generated/control.find_operating_point.html
[^duckdb]: DuckDB, “Loading JSON”: https://duckdb.org/docs/stable/data/json/loading_json.html
[^pydantic-graph]: Pydantic, “Pydantic Graph”: https://pydantic.dev/docs/ai/graph/graph/
[^marimo]: marimo, “Running cells”: https://docs.marimo.io/guides/reactivity/
[^otel]: OpenTelemetry, “Semantic conventions”: https://opentelemetry.io/docs/specs/semconv/
