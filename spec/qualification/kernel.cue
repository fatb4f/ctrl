// Package qualification is the sole executable qualification authority.
package qualification

import (
	core "github.com/fatb4f/ctrl/spec/core"
	repo "github.com/fatb4f/ctrl/spec/repository"
)

#ClaimStatus: "SATISFIED" | "VIOLATED" | "UNKNOWN"
#ResultVerdict: "QUALIFIED" | "INCONCLUSIVE" | "REJECTED"

#Observation: {
	id:        core.#ObservationID
	component: core.#ComponentID
	subject:   core.#ArtifactCoordinate
	value:     _
}

#ClaimAdmission: {
	claimID:       core.#ClaimID
	observationID: core.#ObservationID
	status:        #ClaimStatus
	reason:        core.#NonEmptyString
}

#QualificationResult: {
	repository: repo.#RepositoryRevision
	claims: [core.#ClaimID]: #ClaimAdmission
	complete: bool
	verdict:  #ResultVerdict
	violations: [...core.#ClaimID]

	if complete == false {
		verdict: "INCONCLUSIVE"
	}
	if verdict == "QUALIFIED" {
		complete: true
		claims: [core.#ClaimID]: {status: "SATISFIED"}
		violations: []
	}
	if verdict == "REJECTED" {
		complete: true
		violations: [core.#ClaimID, ...core.#ClaimID]
	}
}

#PromotionAuthorization: {
	result: #QualificationResult & {
		complete: true
		verdict:  "QUALIFIED"
	}
	authorized: true
}

// OSCAL, Gemara, and in-toto may supply obligations or projections. They do
// not replace the canonical CUE qualification evaluator.
#ObligationSource: "canonical-cue" | "oscal" | "gemara" | "in-toto"

#TransportProjection: {
	source: repo.#GeneratedArtifact
	authority: "canonical-cue"
	mechanism: #ObligationSource
}
