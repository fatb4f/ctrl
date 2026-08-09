package positive

import qualification "github.com/fatb4f/ctrl/spec/qualification"

zero: "sha256:0000000000000000000000000000000000000000000000000000000000000000"

qualified: qualification.#QualificationResult & {
	repository: {revision: zero, components: {}}
	claims: {
		"semantic-authority": {
			claimID: "semantic-authority"
			observationID: "cue-vet"
			status: "SATISFIED"
			reason: "canonical CUE constraints passed"
		}
	}
	complete: true
	verdict: "QUALIFIED"
	violations: []
}
