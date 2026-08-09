// Package repository describes source-tree and generated-artifact structure.
package repository

import core "github.com/fatb4f/ctrl/spec/core"

#Component: {
	id:   core.#ComponentID
	root: core.#NonEmptyString
}

#RepositoryRevision: {
	revision: core.#Digest
	components: [core.#ComponentID]: #Component
}

#GeneratedArtifact: {
	artifact: core.#ArtifactCoordinate
	authoritativeInputs: [core.#SourceCoordinate, ...core.#SourceCoordinate]
	role: "transport" | "projection"
}
