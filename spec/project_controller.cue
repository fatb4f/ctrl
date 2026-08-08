package kernelspec

#ProjectSpec: close({
	id:      #ProjectID
	kind:    #ID
	title:   #NonEmptyString
	purpose: #NonEmptyString

	namespace: #NamespaceID

	resources: [#ResourceID]:     #ResourceSemantics
	operations: [#OperationID]:   #OperationSemantics
	states: [#StateID]:           #StateSemantics
	transitions: [#TransitionID]: #TransitionSemantics
	protocols: [#ProtocolID]:     #ProtocolSemantics

	requirements: [...#RequirementID]
	conformance:  [...#ConformanceID]
	projections:  [...#ProjectionID]
})

#ControllerSpec: close({
	id:      #ControllerID
	kind:    #ID
	title:   #NonEmptyString
	purpose: #NonEmptyString

	namespace: #NamespaceID

	observes:  [...#SemanticReference]
	decisions: [...#SemanticReference]
	operations: [#OperationID]: #OperationSemantics
	procedures: [#ProcedureID]: #ProcedureSpec

	declaredEffects: [...#ID]
	requirements:    [...#RequirementID]
	conformance:     [...#ConformanceID]
})

#AuthorityDisposition: "unchanged" | "narrowed" | "expanded"

#ControllerProjectBinding: close({
	id: #BindingID

	project:    #ProjectID
	controller: #ControllerID

	projectRevision:    #Revision
	controllerRevision: #Revision
	policyRevision:     #Revision

	observations: [...#SemanticReference]
	decisions:    [...#SemanticReference]
	operations:   [...#OperationID]
	effects:      [...#ID]
	projections:  [...#ProjectionID]

	authority: #AuthorityDisposition
	if authority == "expanded" {
		authorization: #SemanticReference
	}

	requiredProcedures: [...#ProcedureID]
	requiredEvidence:   [...#ArtifactKindID]
})
