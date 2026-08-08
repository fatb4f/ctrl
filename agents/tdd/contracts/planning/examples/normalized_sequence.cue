package examples

import (
	"list"

	"github.com/fatba4f/ctrl/agents/tdd/contracts/planning"
)

commonExclude: [
	".git/**",
	".jj/**",
	".venv/**",
	"**/__pycache__/**",
]

repositoryGate: [{
	command: "just check"
	purpose: "Run the repository-wide fast quality gate."
}]

#PlanSchema: planning.#PlanContract

normalizedPlan: planning.#PlanContract & {
	schemaVersion: "plan-change-sequence/v0"

	authorityModel: {
		authorities: [
			{
				id:         "semantic-product"
				path:       "docs/plan.md"
				owns:       "Semantic product intent and invariants."
				precedence: 0
			},
			{
				id:         "qualification-procedure"
				path:       "docs/qualification-v0-plan.md"
				owns:       "Qualification lifecycle and implementation sequencing."
				precedence: 1
			},
			{
				id:         "skill-product"
				path:       "docs/skill-plan.md"
				owns:       "Skill packaging, references, manifests, and skill-facing interfaces."
				precedence: 2
			},
		]
	}

	cliTopology: {}

	changes: [
		{
			id:          "baseline"
			title:       "Record the generated project baseline"
			phase:       0
			dependsOn:   []
			authorities: ["semantic-product"]
			scope: {
				include: ["**"]
				exclude: commonExclude
			}
			inputs:    ["generated-project-tree"]
			outputs:   ["initial-vcs-revision"]
			generated: []
			prohibits: [{
				id:        "baseline-content-change"
				statement: "Do not alter project content while recording the baseline."
			}]
			acceptance: [{
				id:           "baseline-checks-pass"
				statement:    "The unmodified generated project passes its fast gate."
				initialState: "passing"
			}]
			gates: repositoryGate
			implementation: {
				runtimeCode:        false
				subprocesses:       false
				repositoryMutation: false
				persistentState:    false
				newEntryPoints:     []
			}
			proof: {
				required: [{kind: "baseline-tree", statement: "Bind the exact initial source tree."}]
				evidence: ["source-tree-digest", "fast-gate-report"]
			}
		},
		{
			id:          "authority-reconciliation"
			title:       "Reconcile authority and skill artifacts"
			phase:       0
			dependsOn:   ["baseline"]
			authorities: ["semantic-product", "qualification-procedure", "skill-product"]
			scope: {
				include: ["docs/**", ".codex/skills/jj-*/**", "contracts/planning/**", "tests/**", "scripts/**", "justfile"]
				exclude: list.Concat([commonExclude, ["src/**"]])
			}
			inputs: [
				"docs/plan.md",
				"docs/qualification-v0-plan.md",
				"docs/skill-plan.md",
				"supplied-jj-skill-revision-archive",
			]
			outputs: [
				"authority-reconciliation-record",
				"completed-skill-directory-inventory",
				"command-interface-compatibility-matrix",
				".codex/skills/jj-manifest.json",
				"zero-missing-reference-report",
			]
			generated: [{
				artifact:      ".codex/skills/jj-manifest.json"
				generator:     "just jj-skills-manifest-generate"
				checkCommand:  "just jj-skills-manifest-check"
				manualEditing: false
			}]
			prohibits: [{
				id:        "reconciliation-runtime-code"
				statement: "Do not add or modify Python runtime behavior."
			}]
			acceptance: [{
				id:           "skill-inventory-exact"
				statement:    "The six skill directories and all required references have exact manifest coverage."
				initialState: "failing"
			}]
			gates: list.Concat([[{
				command: "just jj-skills-manifest-check"
				purpose: "Prove exact skill and reference coverage."
			}], repositoryGate])
			implementation: {
				runtimeCode:        false
				subprocesses:       false
				repositoryMutation: false
				persistentState:    false
				newEntryPoints:     []
			}
			proof: {
				required: [{kind: "authority-reconciliation", statement: "Record every resolved conflict and explicit decision."}]
				evidence: ["authority-record", "skill-manifest", "compatibility-matrix", "missing-reference-report"]
			}
		},
		{
			id:          "executable-specification"
			title:       "Generate the executable Jujutsu specification"
			phase:       1
			dependsOn:   ["authority-reconciliation"]
			authorities: ["semantic-product", "qualification-procedure", "skill-product"]
			scope: {
				include: ["contracts/**", "generated/schema/**", "src/tdd_agent_skills/generated/**", "src/tdd_agent_skills/jj_agent/*.json", ".codex/skills/jj-*/references/**", "scripts/**", "tests/**", "justfile", "uv.lock"]
				exclude: list.Concat([commonExclude, ["src/tdd_agent_skills/jj_agent/**/*.py"]])
			}
			inputs:  ["authority-reconciliation-record", "command-interface-compatibility-matrix"]
			outputs: ["closed-jj-cue-contracts", "jj-agent-v0-schema", "frozen-transport-models", "operation-registry", "adapter-manifest-projection", "generated-skill-references"]
			generated: [
				{
					artifact:      "generated/schema/jj-agent-v0.schema.json"
					generator:     "just jj-generate"
					checkCommand:  "just jj-generate-check"
					manualEditing: false
				},
				{
					artifact:      "src/tdd_agent_skills/generated/jj_agent.py"
					generator:     "just jj-generate"
					checkCommand:  "just jj-generate-check"
					manualEditing: false
				},
				{
					artifact:      "src/tdd_agent_skills/jj_agent/operations-v0.json"
					generator:     "just jj-generate"
					checkCommand:  "just jj-generate-check"
					manualEditing: false
				},
				{
					artifact:      "src/tdd_agent_skills/jj_agent/adapter-artifacts-v0.json"
					generator:     "just jj-generate"
					checkCommand:  "just jj-generate-check"
					manualEditing: false
				},
			]
			prohibits: [{
				id:        "separate-adapter-manifest-authority"
				statement: "The adapter manifest must be generated as a projection of the operation registry."
			}]
			acceptance: [{
				id:           "schema-drift-detected"
				statement:    "The drift check rejects any manually altered generated artifact, and every registry entry fixes its operation name, request and result types, mutability, repository capabilities, exit outcomes, and deprecated aliases."
				initialState: "failing"
			}]
			gates: list.Concat([[{command: "just jj-generate-check", purpose: "Reproduce all generated Jujutsu artifacts byte-for-byte."}], repositoryGate])
			implementation: {
				runtimeCode:        false
				subprocesses:       false
				repositoryMutation: false
				persistentState:    false
				newEntryPoints:     []
			}
			proof: {
				required: [{kind: "generation-drift", statement: "Regeneration produces no diff."}]
				evidence: ["cue-validation-report", "generation-drift-report"]
			}
		},
		{
			id:          "pure-qualification-kernel"
			title:       "Derive qualification decisions in a pure kernel"
			phase:       2
			dependsOn:   ["executable-specification"]
			authorities: ["semantic-product", "qualification-procedure"]
			scope: {
				include: ["src/tdd_agent_skills/qualification/kernel/**", "tests/qualification/kernel/**"]
				exclude: list.Concat([commonExclude, ["src/tdd_agent_skills/cli.py", "src/tdd_agent_skills/jj_agent/**"]])
			}
			inputs:     ["frozen-transport-models", "semantic-product-invariants"]
			outputs:    ["pure-qualification-kernel", "kernel-law-tests"]
			generated:  []
			prohibits:  [{id: "kernel-side-effects", statement: "Do not import Cyclopts or execute subprocesses, repository operations, or persistent writes."}]
			acceptance: [{id: "kernel-law-counterexample", statement: "A semantic counterexample fails before the minimum pure implementation exists.", initialState: "failing"}]
			gates:      list.Concat([[{command: "just test tests/qualification/kernel", purpose: "Run pure qualification law tests."}], repositoryGate])
			implementation: {
				runtimeCode:        true
				subprocesses:       false
				repositoryMutation: false
				persistentState:    false
				newEntryPoints:     []
			}
			proof: {
				required: [{kind: "pure-law-suite", statement: "All semantic laws are derived without effects."}]
				evidence: ["kernel-test-report"]
			}
		},
		{
			id:          "observe-production"
			title:       "Observe a Jujutsu repository through the installed adapter contract"
			phase:       3
			dependsOn:   ["pure-qualification-kernel"]
			authorities: ["semantic-product", "qualification-procedure", "skill-product"]
			scope: {
				include: ["src/tdd_agent_skills/cli_shared/**", "src/tdd_agent_skills/jj_agent/**", "tests/jj/observe/**", "pyproject.toml", "uv.lock", ".codex/skills/jj-observe/**", ".codex/skills/jj-conflict-check/**"]
				exclude: commonExclude
			}
			inputs:    ["operation-registry", "adapter-manifest-projection", "frozen-transport-models"]
			outputs:   ["jj-agent-entry-point", "observe-handler", "conflicts-to-observe-alias-projection", "observe-contract-tests"]
			generated: []
			prohibits: [
				{id: "observe-repository-mutation", statement: "Do not mutate Jujutsu operations, working-copy state, or filesystem state."},
				{id: "alias-handler", statement: "Do not implement a separate conflicts handler; project conflicts to observe before dispatch."},
				{id: "second-cli-architecture", statement: "Do not introduce a parser, transport, registry, error envelope, or exit taxonomy at the entry-point boundary."},
			]
			acceptance: [{id: "observe-immutable-operation", statement: "The external observe invocation initially fails the two-level repository and filesystem identity proof.", initialState: "failing"}]
			gates:      list.Concat([[{command: "just test tests/jj/observe", purpose: "Run observe contract, CLI, graph, and repository tests."}], repositoryGate])
			implementation: {
				runtimeCode:        true
				subprocesses:       true
				repositoryMutation: false
				persistentState:    false
				newEntryPoints:     ["jj-agent"]
			}
			proof: {
				required: [
					{kind: "repository-identity", statement: "Repository identity is equal before and after invocation."},
					{kind: "state-digest", statement: "Filesystem and Jujutsu state digests are equal before and after invocation."},
				]
				evidence: ["pre-observe-repository-identity", "post-observe-repository-identity", "pre-observe-state-digest", "post-observe-state-digest", "external-process-report"]
			}
		},
		{
			id:          "qualification-orchestration"
			title:       "Reconstruct qualification projections from immutable evidence"
			phase:       4
			dependsOn:   ["observe-production"]
			authorities: ["semantic-product", "qualification-procedure"]
			scope: {
				include: ["src/tdd_agent_skills/qualification/**", "src/tdd_agent_skills/cli.py", "tests/qualification/**"]
				exclude: list.Concat([commonExclude, ["src/tdd_agent_skills/jj_agent/**"]])
			}
			inputs:     ["pure-qualification-kernel", "jj-agent-entry-point"]
			outputs:    ["content-addressed-evidence-store", "restartable-qualification-graph", "python-ppf-qualify-run", "orchestration-equivalence-tests"]
			generated:  []
			prohibits:  [{id: "transition-state-authority", statement: "Attempt state, evidence artifacts, graph projections, and promotion decisions must remain distinct; decisions reconstruct from immutable evidence."}]
			acceptance: [{id: "restart-from-evidence", statement: "A restart test initially fails when partial transition state is treated as authoritative.", initialState: "failing"}]
			gates:      list.Concat([[{command: "just test tests/qualification", purpose: "Run store, graph, CLI, restart, and equivalence tests."}], repositoryGate])
			implementation: {
				runtimeCode:        true
				subprocesses:       true
				repositoryMutation: false
				persistentState:    true
				newEntryPoints:     []
			}
			proof: {
				required: [{kind: "restart-equivalence", statement: "Restarted and uninterrupted projections are byte-identical."}]
				evidence: ["attempt-state", "evidence-artifact", "graph-projection", "promotion-decision", "restart-equivalence-report"]
			}
		},
		{
			id:          "vertical-release-proof"
			title:       "Qualify the exact installed wheel through jj-agent"
			phase:       5
			dependsOn:   ["qualification-orchestration"]
			authorities: ["semantic-product", "qualification-procedure"]
			scope: {
				include: ["fixtures/qualification/**", "tests/qualification/proof/**", "scripts/**", "justfile"]
				exclude: list.Concat([commonExclude, ["src/**"]])
			}
			inputs:     ["source-revision", "built-wheel", "installed-distribution-metadata", "resolved-jj-agent-path"]
			outputs:    ["installed-wheel-release-proof", "negative-boundary-proofs"]
			generated:  []
			prohibits:  [{id: "source-tree-shim", statement: "Do not accept an executable resolved from the source tree or another environment."}]
			acceptance: [{id: "wrong-executable-rejected", statement: "The proof initially fails when jj-agent resolves outside the bound installation.", initialState: "failing"}]
			gates: [
				{command: "just test-clean-locked", purpose: "Test from the exact locked environment."},
				{command: "just qualify", purpose: "Run the complete installed-wheel qualification proof."},
			]
			implementation: {
				runtimeCode:        true
				subprocesses:       true
				repositoryMutation: true
				persistentState:    true
				newEntryPoints:     []
			}
			proof: {
				required: [
					{kind: "installed-entry-point", entryPoint: "jj-agent"},
					{kind: "identity-pins", identities: ["source-revision", "wheel-digest", "installed-distribution-metadata", "invoked-executable-path"]},
				]
				evidence: ["source-revision", "wheel-digest", "installed-distribution-metadata", "invoked-executable-path", "release-proof-report"]
			}
		},
		{
			id:             "atomic-production"
			title:          "Advance one atomic Jujutsu change only after green probes"
			phase:          6
			dependsOn:      ["vertical-release-proof"]
			authorities:    ["semantic-product", "skill-product"]
			scope:          {include: ["src/tdd_agent_skills/jj_agent/atomic/**", "tests/jj/atomic/**", ".codex/skills/jj-atomic-change/**"], exclude: commonExclude}
			inputs:         ["operation-registry", "frozen-transport-models"]
			outputs:        ["atomic-handler", "atomic-graph", "atomic-skill-references"]
			generated:      []
			prohibits:      [{id: "advance-after-failed-probe", statement: "Do not advance after failed evidence."}]
			acceptance:     [{id: "atomic-failed-probe", statement: "A failing probe initially permits an invalid advance.", initialState: "failing"}]
			gates:          list.Concat([[{command: "just test tests/jj/atomic", purpose: "Run atomic graph and repository scenarios."}], repositoryGate])
			implementation: {runtimeCode: true, subprocesses: true, repositoryMutation: true, persistentState: false, newEntryPoints: []}
			proof:          {required: [{kind: "atomic-postconditions", statement: "IDs, paths, probe evidence, and successor state satisfy the contract."}], evidence: ["operation-snapshot", "probe-results", "successor-state"]}
		},
		{
			id:             "split-production"
			title:          "Split a Jujutsu change while preserving patch and tree equivalence"
			phase:          7
			dependsOn:      ["atomic-production"]
			authorities:    ["semantic-product", "skill-product"]
			scope:          {include: ["src/tdd_agent_skills/jj_agent/split/**", "tests/jj/split/**", ".codex/skills/jj-split-change/**"], exclude: commonExclude}
			inputs:         ["operation-registry", "frozen-transport-models"]
			outputs:        ["split-handler", "split-graph", "split-skill-references"]
			generated:      []
			prohibits:      [{id: "early-source-abandon", statement: "Do not abandon the source before all equivalence and probe checks pass."}]
			acceptance:     [{id: "split-equivalence-failure", statement: "A non-equivalent partition initially escapes rejection.", initialState: "failing"}]
			gates:          list.Concat([[{command: "just test tests/jj/split", purpose: "Run split graph and repository scenarios."}], repositoryGate])
			implementation: {runtimeCode: true, subprocesses: true, repositoryMutation: true, persistentState: false, newEntryPoints: []}
			proof:          {required: [{kind: "split-equivalence", statement: "Combined patch and final tree equal the source."}], evidence: ["partition-change-ids", "patch-digest", "tree-digest", "probe-results"]}
		},
		{
			id:             "resolve-conflict-production"
			title:          "Resolve the earliest Jujutsu conflict through a validated token"
			phase:          8
			dependsOn:      ["split-production"]
			authorities:    ["semantic-product", "skill-product"]
			scope:          {include: ["src/tdd_agent_skills/jj_agent/resolve_conflict/**", "tests/jj/resolve_conflict/**", ".codex/skills/jj-resolve-conflict/**"], exclude: commonExclude}
			inputs:         ["operation-registry", "frozen-transport-models"]
			outputs:        ["resolve-conflict-handler", "resolve-conflict-graph", "resolve-conflict-skill-references"]
			generated:      []
			prohibits:      [{id: "unchecked-conflict-squash", statement: "Do not squash while conflicts, marker residue, or failed probes remain."}]
			acceptance:     [{id: "marker-residue-rejected", statement: "Marker residue initially reaches the squash step.", initialState: "failing"}]
			gates:          list.Concat([[{command: "just test tests/jj/resolve_conflict", purpose: "Run conflict preparation and finalization scenarios."}], repositoryGate])
			implementation: {runtimeCode: true, subprocesses: true, repositoryMutation: true, persistentState: false, newEntryPoints: []}
			proof:          {required: [{kind: "conflict-resolution", statement: "The token, parser, formatter, probes, squash, and descendant conflict state are valid."}], evidence: ["resolution-token", "marker-scan", "probe-results", "descendant-conflicts"]}
		},
		{
			id:             "workspace-prepare-production"
			title:          "Prepare a capability-bounded Jujutsu worker workspace"
			phase:          9
			dependsOn:      ["resolve-conflict-production"]
			authorities:    ["semantic-product", "skill-product"]
			scope:          {include: ["src/tdd_agent_skills/jj_agent/workspace/prepare.py", "tests/jj/workspace/test_prepare.py", ".codex/skills/jj-workspace-worker/**"], exclude: commonExclude}
			inputs:         ["operation-registry", "frozen-transport-models"]
			outputs:        ["workspace-prepare-handler", "workspace-capability-manifest"]
			generated:      []
			prohibits:      [{id: "worker-ref-authority", statement: "Do not grant bookmark, remote, or operation authority to the worker."}]
			acceptance:     [{id: "workspace-capability-boundary", statement: "An over-broad capability manifest initially permits undeclared paths.", initialState: "failing"}]
			gates:          list.Concat([[{command: "just test tests/jj/workspace/test_prepare.py", purpose: "Run workspace preparation scenarios."}], repositoryGate])
			implementation: {runtimeCode: true, subprocesses: true, repositoryMutation: true, persistentState: true, newEntryPoints: []}
			proof:          {required: [{kind: "workspace-capability", statement: "The workspace and manifest are controller-owned and path bounded."}], evidence: ["workspace-identity", "capability-manifest", "operation-snapshot"]}
		},
		{
			id:             "workspace-collect-production"
			title:          "Collect bounded worker results without trusting worker authority"
			phase:          10
			dependsOn:      ["workspace-prepare-production"]
			authorities:    ["semantic-product", "skill-product"]
			scope:          {include: ["src/tdd_agent_skills/jj_agent/workspace/collect.py", "tests/jj/workspace/test_collect.py", ".codex/skills/jj-workspace-worker/**"], exclude: commonExclude}
			inputs:         ["workspace-capability-manifest", "worker-workspace-state"]
			outputs:        ["workspace-collect-handler", "workspace-collection-evidence"]
			generated:      []
			prohibits:      [{id: "unvalidated-worker-result", statement: "Do not accept path, bookmark, remote, operation, or stale-workspace violations."}]
			acceptance:     [{id: "workspace-stale-collection", statement: "A stale worker workspace initially passes collection.", initialState: "failing"}]
			gates:          list.Concat([[{command: "just test tests/jj/workspace/test_collect.py", purpose: "Run workspace collection scenarios."}], repositoryGate])
			implementation: {runtimeCode: true, subprocesses: true, repositoryMutation: true, persistentState: true, newEntryPoints: []}
			proof:          {required: [{kind: "workspace-collection", statement: "Collected snapshots and validation evidence satisfy every capability."}], evidence: ["collection-snapshot", "capability-validation", "probe-results"]}
		},
		{
			id:             "workspace-dispose-production"
			title:          "Dispose successful workspaces while preserving failed workspaces"
			phase:          11
			dependsOn:      ["workspace-collect-production"]
			authorities:    ["semantic-product", "skill-product"]
			scope:          {include: ["src/tdd_agent_skills/jj_agent/workspace/dispose.py", "tests/jj/workspace/test_dispose.py", ".codex/skills/jj-workspace-worker/**"], exclude: commonExclude}
			inputs:         ["workspace-collection-evidence", "workspace-identity"]
			outputs:        ["workspace-dispose-handler", "workspace-disposal-evidence"]
			generated:      []
			prohibits:      [{id: "failed-workspace-deletion", statement: "Do not dispose a failed or uncollected workspace."}]
			acceptance:     [{id: "workspace-failure-preserved", statement: "A failed workspace is initially removed instead of preserved.", initialState: "failing"}]
			gates:          list.Concat([[{command: "just test tests/jj/workspace/test_dispose.py", purpose: "Run workspace disposal and preservation scenarios."}], repositoryGate])
			implementation: {runtimeCode: true, subprocesses: true, repositoryMutation: true, persistentState: true, newEntryPoints: []}
			proof:          {required: [{kind: "workspace-disposal", statement: "Only the controller disposes a successfully collected workspace."}], evidence: ["disposal-preconditions", "disposal-result", "failed-workspace-preservation"]}
		},
	]
}
