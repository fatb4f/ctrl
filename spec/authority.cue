package kernelspec

// #KernelAuthority fixes the architecture-level division of responsibility.
// CUE is the executable lattice; OSCAL defines the governed API data model.
#KernelAuthority: close({
	lattice:      "cue"
	evaluator:    "cue"
	apiDataModel: "oscal"
	apiContract:  "oscal-component-definition"
	stateLog:     "git"
})

// #ModelAAuthority identifies Model A as the executable CUE closure of the
// OSCAL-defined API data model, not as an independent domain metamodel.
#ModelAAuthority: close({
	dataModel:      "oscal"
	apiContract:    "oscal-component-definition"
	representation: "cue"
	semantics:      "authoritative"
})

// #ModelBAuthority prevents the transport IR from becoming a parallel API
// authority or introducing independently authored normative meaning.
#ModelBAuthority: close({
	source:    "model-a"
	role:      "derived-transport-ir"
	semantics: "non-authoritative"
})
