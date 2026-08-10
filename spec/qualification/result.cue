@experiment(explicitopen)

package qualification

import (
	"list"

	repo "github.com/fatb4f/ctrl/spec/repository"
)

#QualificationResult: Result=(#QualificationResultTransport & {
	repository: repo.#RepositoryRevision

	for claimID, claim in Result.claims {
		claims: (claimID): claimID: claimID

		if Result.verdict == "QUALIFIED" {
			claims: (claimID): status: "SATISFIED"
		}

		if Result.verdict == "INCONCLUSIVE" {
			claims: (claimID): status: "SATISFIED" | "UNKNOWN"
		}
	}

	_claimStatuses:         [for _, claim in Result.claims {claim.status}]
	_completeMatchesClaims: Result.complete == !list.Contains(_claimStatuses, "UNKNOWN")
	_completeMatchesClaims: true

	if Result.verdict == "QUALIFIED" {
		_qualifiedComplete: Result.complete == true
		_qualifiedComplete: true
		_noViolations:      len(Result.violations) == 0
		_noViolations:      true
	}

	if Result.verdict == "INCONCLUSIVE" {
		_inconclusiveIncomplete: Result.complete == false
		_inconclusiveIncomplete: true
		_noViolations:           len(Result.violations) == 0
		_noViolations:           true
	}

	if Result.verdict == "REJECTED" {
		_hasViolations: len(Result.violations) >= 1
		_hasViolations: true

		for violation in Result.violations {
			claims: (violation): status: "VIOLATED"
		}
	}
})

#QualifiedResult: Result=(#QualificationResult & {
	_qualifiedVerdict: Result.verdict == "QUALIFIED"
	_qualifiedVerdict: true
})

#QualificationRejected: Result=(#QualificationResult & {
	_rejectedVerdict: Result.verdict == "REJECTED"
	_rejectedVerdict: true
})

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
