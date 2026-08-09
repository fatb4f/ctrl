package kernelspec

#CompilerStageKind:
	"ingest" |
		"resolve" |
		"normalize" |
		"unify" |
		"evaluate" |
		"qualify" |
		"freeze" |
		"lower" |
		"project" |
		"verify"

#ModelKind: close({
	id:            #ModelKindID
	description:   #NonEmptyString
	authoritative: bool
})

#SemanticFeature: close({
	id:           #ID
	description?: #NonEmptyString
})

#ProjectionFidelity: close({
	preserved:    [...#ID]
	approximated: [...#ID]
	omitted:      [...#ID]
})

#ProjectionMapping: close({
	id: #ID

	source: #SemanticReference
	target: #NonEmptyString

	cardinality: #RelationCardinality
	transform:   #ProcedureID
	preserves:   [...#ID]
	loses:       [...#ID]
})

#ProjectionSpec: close({
	id: #ProjectionID

	sourceModel: #ModelKindID
	target: close({
		family:  #ID
		version: #NonEmptyString
	})

	mappings: [#ID]: #ProjectionMapping
	fidelity: #ProjectionFidelity

	validators: [...#ProcedureID]
	properties: [...#SemanticReference]
})

#CompilerDefinition: close({
	id:       #CompilerID
	revision: #Revision

	stage:   #CompilerStageKind
	accepts: #ModelKindID
	emits:   #ModelKindID

	preconditions:   [...#SemanticReference]
	transformations: [...#ProcedureID]
	preservation:    [...#SemanticReference]
	losses:          [...#ID]

	implementation?: #ArtifactCoordinate
})

#ImporterDefinition: close({
	id:       #CompilerID
	revision: #Revision

	sourceFormat:  #NonEmptyString
	sourceVersion: #NonEmptyString
	targetModel:   #ModelKindID

	lossPolicy: "reject" | "declare" | "permit"
	resolver:   #ProcedureID
	lowerer:    #ProcedureID
	validator:  #ProcedureID
})

#MaterializationNode: close({
	id: #ID

	inputs:   [#ArtifactCoordinate, ...#ArtifactCoordinate]
	output:   #ArtifactCoordinate
	compiler: #CompilerID

	dependencies:  [...#ID]
	deterministic: true
	effectful:     bool | *false
})

#CompilerKernel: close({
	identity: close({
		id:       #ID
		revision: #Revision
	})

	modelKinds: [#ModelKindID]:   #ModelKind
	features: [#ID]:              #SemanticFeature
	compilers: [#CompilerID]:     #CompilerDefinition
	importers: [#CompilerID]:     #ImporterDefinition
	projections: [#ProjectionID]: #ProjectionSpec
})
