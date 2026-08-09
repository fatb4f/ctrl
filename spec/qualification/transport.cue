@experiment(explicitopen)

// Package qualification is the sole executable qualification authority.
package qualification

import (
	core "github.com/fatb4f/ctrl/spec/core"
	repo "github.com/fatb4f/ctrl/spec/repository"
)

#ClaimStatus:   "SATISFIED" | "VIOLATED" | "UNKNOWN"
#ResultVerdict: "QUALIFIED" | "INCONCLUSIVE" | "REJECTED"

#Observation: close({
	id!:        core.#ObservationID
	component!: core.#ComponentID
	subject!:   core.#ArtifactCoordinate
	value!:     _
})

#ClaimAdmissionTransport: close({
	claimID!:       core.#ClaimID
	observationID!: core.#ObservationID
	status!:        #ClaimStatus
	reason!:        core.#NonEmptyString
})

#ClaimAdmission: #ClaimAdmissionTransport

#ApplicabilityTransport: close({
	obligationRefs!: [...string]
})

#EvidenceRequirementTransport: close({
	id!:          core.#ID
	description!: core.#NonEmptyString
})

#ObligationTransport: close({
	id!:                      core.#ClaimID
	evidenceRequirementRefs!: [...string]
})

#QualificationPolicyTransport: close({
	id!:                   core.#ID
	applicability!:        #ApplicabilityTransport
	evidenceRequirements!: {[string]: #EvidenceRequirementTransport}
	obligations!:          {[string]: #ObligationTransport}
})

#QualificationResultTransport: close({
	repository!: repo.#RepositoryRevisionTransport
	claims!:     {[string]: #ClaimAdmissionTransport}
	complete!:   bool
	verdict!:    #ResultVerdict
	violations!: [...string]
})
