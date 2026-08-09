@experiment(explicitopen)

// Package generate contains tooling-only roots for transport generation.
package generate

import qualification "github.com/fatb4f/ctrl/spec/qualification"

#QualificationTransportBundle: close({
	result!: qualification.#QualificationResultTransport
	policy!: qualification.#QualificationPolicyTransport
})
