package planning

#PlanRevision: close({
	id:          #Identifier
	sequence:    uint
	title:       #NonEmptyString
	supersedes?: #Identifier
})

#PlanPhase: close({
	id:             #Identifier
	planRevisionID: #Identifier
	sequence:       uint
	title:          #NonEmptyString
	summary:        #NonEmptyString
})

#DeliverableFamily: close({
	id:             #Identifier
	planRevisionID: #Identifier
	phaseID:        #Identifier
	sequence:       uint
	title:          #NonEmptyString
	summary:        #NonEmptyString
	rationale?:     #NonEmptyString
	dependsOn:      [...#Identifier]
})
