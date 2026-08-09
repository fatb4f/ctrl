package jsonstructure

import ks "github.com/fatb4f/kernel-spec/spec:kernelspec"

#Profile: close({
	id: "json-structure-import"

	// Pin the exact Internet-Draft family revision used by the importer.
	source: close({
		format:  "json-structure"
		core:    "draft-vasters-json-structure-core-04"
		imports: "draft-vasters-json-structure-import-00"
	})

	semantics: close({
		role:                          "import-language"
		canonicalEvaluator:            "cue"
		liveExternalReferences:        false
		circularExtensionDependencies: false
		lossPolicy:                    "reject"
	})
})

#Importer: ks.#ImporterDefinition & {
	id:       "import-json-structure"
	revision: "sha256:0000000000000000000000000000000000000000000000000000000000000000"

	sourceFormat:  #Profile.source.format
	sourceVersion: #Profile.source.core
	targetModel:   "model-a-fragment"

	lossPolicy: "reject"
	resolver:   "resolve-json-structure"
	lowerer:    "lower-json-structure-to-cue"
	validator:  "validate-json-structure"
}
