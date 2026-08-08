package kernelspec

#StateSemantics: close({
	id:           #StateID
	description?: #NonEmptyString
	terminal:     bool | *false
})

#EffectSemantics: close({
	id:           #ID
	kind:         #ID
	description?: #NonEmptyString
	input?:       #SemanticReference
	output?:      #SemanticReference
})

#TransitionSemantics: close({
	id:      #TransitionID
	subject: #SemanticReference
	from:    #StateID
	to:      #StateID

	trigger?:       #SemanticReference
	preconditions:  [...#SemanticReference]
	authority:      [#SemanticReference, ...#SemanticReference]
	procedure:      #ProcedureID
	effects:        [...#EffectSemantics]
	postconditions: [...#SemanticReference]
	evidence:       [...#ArtifactKindID]
})

#ProtocolRole: close({
	id: #ID
})

#ProtocolPhase: close({
	id:       #ID
	terminal: bool | *false
})

#ProtocolTransition: close({
	id:    #ID
	from:  #ID
	to:    #ID
	actor: #ID

	input?:    #SemanticReference
	guards:    [...#SemanticReference]
	procedure: #ProcedureID
	output?:   #SemanticReference
})

#ProtocolSemantics: close({
	id: #ProtocolID

	roles: [#ID]:  #ProtocolRole
	phases: [#ID]: #ProtocolPhase

	initial:  #ID
	terminal: [#ID, ...#ID]

	transitions: [#ID]: #ProtocolTransition
	invariants: [...#SemanticReference]
})

#ProcedureSpec: close({
	id:       #ProcedureID
	revision: #Revision

	accepts: [...#SemanticReference]
	emits:   [...#SemanticReference]

	preconditions:  [...#SemanticReference]
	postconditions: [...#SemanticReference]
	properties:     [...#SemanticReference]

	implementation?: #ArtifactCoordinate
})
