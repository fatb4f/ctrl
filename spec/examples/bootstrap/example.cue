package bootstrap

import ks "github.com/fatb4f/kernel-spec/spec:kernelspec"

zero: "sha256:0000000000000000000000000000000000000000000000000000000000000000"

kernel: ks.#CompilerKernel & {
	identity: {
		id:       "kernel-spec-bootstrap"
		revision: zero
	}

	modelKinds: {
		"model-a": {
			id:            "model-a"
			description:   "Canonical executable CUE closure of the OSCAL-defined API data model"
			authoritative: true
		}
		"model-a-fragment": {
			id:            "model-a-fragment"
			description:   "Imported contribution awaiting admission into the OSCAL Model A closure"
			authoritative: false
		}
		"model-b": {
			id:            "model-b"
			description:   "Derived transport-neutral API IR"
			authoritative: false
		}
	}

	features:    {}
	compilers:   {}
	importers:   {}
	projections: {}
}
