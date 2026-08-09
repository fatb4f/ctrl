package kernelspec

#Modality: "must" | "mustNot" | "should" | "shouldNot" | "may"

#DeclarativeEnforcement: close({
	kind:       "declarative"
	constraint: #SemanticReference
})

#ProceduralEnforcement: close({
	kind:      "procedural"
	procedure: #SemanticReference & {kind: "procedure"}
})

#ObservationalEnforcement: close({
	kind:         "observational"
	evidenceKind: #ArtifactKindID
	assessor?:    #SemanticReference
})

#EnforcementMechanism:
	#DeclarativeEnforcement |
		#ProceduralEnforcement |
		#ObservationalEnforcement

#Requirement: close({
	id:       #RequirementID
	subject:  #SemanticReference
	modality: #Modality

	establishes?: [#SemanticReference, ...#SemanticReference]
	enforcement:  [#EnforcementMechanism, ...#EnforcementMechanism]
	evidence?:    [#ArtifactKindID, ...#ArtifactKindID]

	statement?:   #NonEmptyString
	rationale?:   #NonEmptyString
	explanation?: #NonEmptyString
})

#ConformanceClass: close({
	id: #ConformanceID

	subjectKinds: [#SemanticKind, ...#SemanticKind]
	requirements: [#RequirementID, ...#RequirementID]

	evaluator: #ProcedureID
	evidence?: [#ArtifactKindID, ...#ArtifactKindID]
})

#ConformanceOutcome: "conforming" | "nonconforming" | "indeterminate"

#RequirementOutcome: "satisfied" | "notSatisfied" | "notApplicable" | "indeterminate"

#ConformanceResult: close({
	subject: #SemanticReference
	class:   #ConformanceID

	requirements: [#RequirementID]: close({
		outcome:  #RequirementOutcome
		evidence: [...#ArtifactCoordinate]
		receipt?: #ArtifactCoordinate
	})

	conclusion: #ConformanceOutcome
})
