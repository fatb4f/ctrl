package kernelspec

#KernelSpec: close({
	authority: #KernelAuthority

	// Model A is the executable CUE closure of the bundled OSCAL API data model.
	modelA:   #SemanticSpec
	compiler: #CompilerKernel

	// Model B is a derived transport compilation product, not a second API
	// authority or an authored child model.
	modelB?: #APIModel
})

#ExtensionSemanticDelta: "refinement" | "addition" | "reinterpretation"
#ExtensionAPIDelta:      "none" | "additive" | "restrictive" | "breaking"

#ExtensionDelta: close({
	semantic:  #ExtensionSemanticDelta
	api:       #ExtensionAPIDelta
	authority: #AuthorityDisposition

	if semantic == "reinterpretation" {
		migration: #ProcedureID
	}
	if authority == "expanded" {
		authorization: #SemanticReference
	}
})

#ProjectExtension: close({
	id:        #ID
	namespace: #NamespaceID
	revision:  #Revision

	requires: close({
		kernelRevision: #Revision
		extensions:     [...#Revision]
	})

	contributes: close({
		definitions?: [#DefinitionID]:   #Definition
		requirements?: [#RequirementID]: #Requirement
		resources?: [#ResourceID]:       #ResourceSemantics
		relations?: [#RelationID]:       #RelationSemantics
		operations?: [#OperationID]:     #OperationSemantics
		states?: [#StateID]:             #StateSemantics
		transitions?: [#TransitionID]:   #TransitionSemantics
		protocols?: [#ProtocolID]:       #ProtocolSemantics
		procedures?: [#ProcedureID]:     #ProcedureSpec
		projections?: [#ProjectionID]:   #ProjectionSpec
	})

	delta: #ExtensionDelta
})
