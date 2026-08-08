package kernelspec

#NonEmptyString: string & !=""
#ID:             #NonEmptyString & =~"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$"
#NamespaceID:    #ID
#DefinitionID:   #ID
#RequirementID:  #ID
#ResourceID:     #ID
#RelationID:     #ID
#OperationID:    #ID
#StateID:        #ID
#TransitionID:   #ID
#ProtocolID:     #ID
#ProcedureID:    #ID
#ProjectionID:   #ID
#CompilerID:     #ID
#ProjectID:      #ID
#ControllerID:   #ID
#BindingID:      #ID
#ConformanceID:  #ID
#ModelKindID:    #ID
#ArtifactKindID: #ID

#Digest:   string & =~"^sha256:[a-f0-9]{64}$"
#Revision: #Digest

#SemanticKind:
	"definition" |
		"requirement" |
		"resource" |
		"relation" |
		"operation" |
		"state" |
		"transition" |
		"protocol" |
		"procedure" |
		"projection" |
		"project" |
		"controller" |
		"binding" |
		"conformance" |
		"compiler"

#SemanticReference: close({
	namespace: #NamespaceID
	kind:      #SemanticKind
	id:        #ID
	revision?: #Revision
})

#ArtifactCoordinate: close({
	kind:       #ArtifactKindID
	digest:     #Digest
	mediaType?: #NonEmptyString
	path?:      #NonEmptyString
})

#SourceCoordinate: close({
	module:   #NonEmptyString
	package:  #NonEmptyString
	path?:    #NonEmptyString
	revision: #Revision
})
