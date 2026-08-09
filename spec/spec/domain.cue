package kernelspec

#Definition: close({
	id:           #DefinitionID
	kind:         #ID
	description?: #NonEmptyString
	shape?:       _
})

#ResourceSemantics: close({
	id:         #ResourceID
	definition: #DefinitionID

	identity?: #SemanticReference
	states:    [...#StateID]
	relations: [...#RelationID]

	authority?: #SemanticReference
	evidence:   [...#ArtifactKindID]
})

#RelationCardinality: "oneToOne" | "oneToMany" | "manyToOne" | "manyToMany"

#RelationSemantics: close({
	id: #RelationID

	from: #SemanticReference
	to:   #SemanticReference

	cardinality: #RelationCardinality
	constraints: [...#SemanticReference]
})

#OperationSemantics: close({
	id: #OperationID

	input?:  #SemanticReference
	output?: #SemanticReference
	errors:  [...#SemanticReference]
	effects: [...#ID]

	preconditions:  [...#SemanticReference]
	postconditions: [...#SemanticReference]
	authority:      [...#SemanticReference]
	procedure?:     #ProcedureID
})
