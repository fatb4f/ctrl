package planning

#InterfaceElement: close({
	id:          #Identifier
	name:        #NonEmptyString
	type:        #NonEmptyString
	statement?:  #NonEmptyString
})

#Invariant: close({
	#SourcePolicy
	id:        #Identifier
	statement: #NonEmptyString
})

#FailureMode: close({
	#SourcePolicy
	id:        #Identifier
	statement: #NonEmptyString
})

#Exclusion: close({
	id:        #Identifier
	statement: #NonEmptyString
})

#AcceptanceCriterion: close({
	#SourcePolicy
	id:        #Identifier
	kind:      "positive" | "negative"
	statement: #NonEmptyString
})

#InterimSpecRevision: close({
	id:             #Identifier
	planRevisionID: #Identifier
	sequence:       uint
	supersedes?:    #Identifier
})

#SpecSection: close({
	id:             #Identifier
	specRevisionID: #Identifier
	familyID:       #Identifier
	sequence:       uint
	title:          #NonEmptyString
	subject:        #NonEmptyString
	contract: close({
		inputs?:       [...#InterfaceElement]
		outputs?:      [...#InterfaceElement]
		invariants:    [#Invariant, ...#Invariant]
		failureModes?: [...#FailureMode]
		exclusions?:   [...#Exclusion]
	})
	acceptance: [#AcceptanceCriterion, ...#AcceptanceCriterion]
})
