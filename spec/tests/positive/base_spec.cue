package positive

import ks "github.com/fatb4f/kernel-spec/spec:kernelspec"

zero: "sha256:0000000000000000000000000000000000000000000000000000000000000000"

requirement: ks.#Requirement & {
	id: "no-prose-only-norms"
	subject: {
		namespace: "kernel"
		kind:      "requirement"
		id:        "normative-completeness"
	}
	modality: "must"
	enforcement: [{
		kind: "procedural"
		procedure: {
			namespace: "kernel"
			kind:      "procedure"
			id:        "lint-normative-completeness"
		}
	}]
	statement: "Every normative requirement resolves to at least one enforcement mechanism."
}

compiler: ks.#CompilerDefinition & {
	id:       "compile-model-a-to-model-b"
	revision: zero
	stage:    "lower"
	accepts:  "model-a"
	emits:    "model-b"

	preconditions:   []
	transformations: []
	preservation:    []
	losses:          []
}
