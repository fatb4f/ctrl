@experiment(explicitopen)

// Package repository describes source-tree and generated-artifact structure.
package repository

import core "github.com/fatb4f/ctrl/spec/core"

#ComponentIdentityTransport: close({
	id!:   core.#ComponentID
	root!: core.#NonEmptyString
})

#Component: #ComponentIdentityTransport

#RepositoryRevisionTransport: close({
	revision!:   core.#Digest
	components!: {[string]: #ComponentIdentityTransport}
})

#RepositoryRevision: Revision=(#RepositoryRevisionTransport & {
	for componentID, component in Revision.components {
		components: (componentID): id: componentID
	}
})

#GeneratedArtifact: {
	artifact:            core.#ArtifactCoordinate
	authoritativeInputs: [core.#SourceCoordinate, ...core.#SourceCoordinate]
	role:                "transport" | "projection"
}
