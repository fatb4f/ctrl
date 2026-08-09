package oscalagenticgitops

import ks "github.com/fatb4f/kernel-spec/spec:kernelspec"

#Namespace:    "oscal-agentic-gitops"
#ZeroRevision: "sha256:0000000000000000000000000000000000000000000000000000000000000000"

#GovernedRepositoryProject: ks.#ProjectSpec & {
	id:        "oscal-governed-repository"
	kind:      "governed-repository"
	title:     "OSCAL governed repository"
	purpose:   "Maintain a continuously evaluated, event-sourced governance graph and its validated OSCAL lifecycle projections."
	namespace: #Namespace

	resources:   {}
	operations:  {}
	states:      {}
	transitions: {}
	protocols:   {}

	requirements: []
	conformance:  []
	projections:  ["oscal-lifecycle"]
}

#AgenticGitOpsController: ks.#ControllerSpec & {
	id:        "oscal-agentic-gitops-controller"
	kind:      "semantic-gitops-controller"
	title:     "OSCAL agentic GitOps controller"
	purpose:   "Observe governed project state, derive bounded conclusions, propose admissible transitions, and execute explicitly delegated one-use effects."
	namespace: #Namespace

	observes:   []
	decisions:  []
	operations: {}
	procedures: {}

	declaredEffects: [
		"construct-object",
		"mutate-worktree",
		"construct-commit",
		"move-authorized-reference",
		"publish-authorized-reference",
	]
	requirements: []
	conformance:  []
}

#ControllerBinding: ks.#ControllerProjectBinding & {
	id: "oscal-agentic-gitops-binding"

	project:    #GovernedRepositoryProject.id
	controller: #AgenticGitOpsController.id

	projectRevision:    #ZeroRevision
	controllerRevision: #ZeroRevision
	policyRevision:     #ZeroRevision

	observations: []
	decisions:    []
	operations:   []
	effects:      []
	projections:  ["oscal-lifecycle"]

	authority: "narrowed"

	requiredProcedures: []
	requiredEvidence:   []
}
