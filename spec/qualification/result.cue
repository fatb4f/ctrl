@experiment(explicitopen)

package qualification

import (
	"struct"

	repo "github.com/fatb4f/ctrl/spec/repository"
)

#QualifiedResult: Result=(#QualificationResultTransport & {
	repository: repo.#RepositoryRevision

	for claimID, claim in Result.claims {
		claims: (claimID): claimID: claimID
	}

	complete: true
	verdict:  "QUALIFIED"
	claims: [string]: {
		status: "SATISFIED"
	}
	violations: []
})

#QualifiedInconclusiveResult: Result=(#QualificationResultTransport & {
	repository: repo.#RepositoryRevision

	for claimID, claim in Result.claims {
		claims: (claimID): claimID: claimID
	}

	complete: false
	verdict:  "INCONCLUSIVE"
	claims: struct.MinFields(1) & {
		[string]: status: "UNKNOWN"
	}
	violations: []
})

#QualificationRejected: Result=(#QualificationResultTransport & {
	repository: repo.#RepositoryRevision

	for claimID, claim in Result.claims {
		claims: (claimID): claimID: claimID
	}

	for violation in Result.violations {
		claims: (violation): status: "VIOLATED"
	}

	if Result.complete == true {
		claims: [string]: status: "SATISFIED" | "VIOLATED"
	}

	verdict:    "REJECTED"
	violations: [string, ...string]
})

#QualificationResult: #QualifiedResult | #QualifiedInconclusiveResult | #QualificationRejected

// S0 authorizes entry into a future promotion boundary only. It does not prove
// policy coverage or authorize any external effect.
#PromotionAuthorization: close({
	schema!: "promotion-authorization/s0"
	scope!:  "RESULT_LOCAL"
	result!: #QualifiedResult
})

// OSCAL, Gemara, and in-toto may supply obligations or projections. They do
// not replace the canonical CUE qualification evaluator.
#ObligationSource: "canonical-cue" | "oscal" | "gemara" | "in-toto"

#TransportProjection: close({
	source!:    repo.#GeneratedArtifact
	authority!: "canonical-cue"
	mechanism!: #ObligationSource
})
