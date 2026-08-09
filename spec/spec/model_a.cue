package kernelspec

// Model A is the authoritative OSCAL API data model expressed and admitted
// through the CUE semantic lattice.
#SemanticSpec: close({
	authority: #ModelAAuthority

	identity: close({
		id:       #ID
		revision: #Revision
	})

	namespaces: [#NamespaceID]: close({
		id:           #NamespaceID
		description?: #NonEmptyString
	})

	definitions: [#DefinitionID]:   #Definition
	requirements: [#RequirementID]: #Requirement
	resources: [#ResourceID]:       #ResourceSemantics
	relations: [#RelationID]:       #RelationSemantics
	operations: [#OperationID]:     #OperationSemantics
	states: [#StateID]:             #StateSemantics
	transitions: [#TransitionID]:   #TransitionSemantics
	protocols: [#ProtocolID]:       #ProtocolSemantics
	procedures: [#ProcedureID]:     #ProcedureSpec
	projections: [#ProjectionID]:   #ProjectionSpec
	conformance: [#ConformanceID]:  #ConformanceClass
	compilers: [#CompilerID]:       #CompilerDefinition

	projects: [#ProjectID]:       #ProjectSpec
	controllers: [#ControllerID]: #ControllerSpec
	bindings: [#BindingID]:       #ControllerProjectBinding
})
