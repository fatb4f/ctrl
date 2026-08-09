package jsonstructure

import repository "github.com/fatb4f/ctrl/spec/repository"

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

#Projection: repository.#GeneratedArtifact & {
	artifact: {
		path: "generated/json-structure.schema.json"
		digest: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
		mediaType: "application/schema+json"
	}
	authoritativeInputs: [{
		path: "spec/profiles/import/json-structure/profile.cue"
		revision: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
	}]
	role: "projection"
}
