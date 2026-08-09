@experiment(explicitopen)

package qualification

#Applicability:       #ApplicabilityTransport
#EvidenceRequirement: #EvidenceRequirementTransport
#Obligation:          #ObligationTransport

#QualificationPolicy: Policy=(#QualificationPolicyTransport & {
	for requirementID, requirement in Policy.evidenceRequirements {
		evidenceRequirements: (requirementID): id: requirementID
	}

	for obligationID, obligation in Policy.obligations {
		obligations: (obligationID): id: obligationID
		for requirementRef in obligation.evidenceRequirementRefs {
			evidenceRequirements: (requirementRef): _
		}
	}

	for obligationRef in Policy.applicability.obligationRefs {
		obligations: (obligationRef): _
	}
})
