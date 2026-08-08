package planning

#FailureCondition: close({
	id:        #Identifier
	statement: #NonEmptyString
})

#BehaviorObligation: close({
	id:    #Identifier
	kind!: "behavior"
	contract: close({
		given: #NonEmptyString
		when:  #NonEmptyString
		then:  #NonEmptyString
	})
	statement:         #NonEmptyString
	sourceRefs:        [#Identifier, ...#Identifier]
	blocking:          bool
	failureConditions: [#FailureCondition, ...#FailureCondition]
})

#InvariantObligation: close({
	id:    #Identifier
	kind!: "invariant"
	contract: close({
		scope:     #NonEmptyString
		invariant: #NonEmptyString
	})
	statement:         #NonEmptyString
	sourceRefs:        [#Identifier, ...#Identifier]
	blocking:          bool
	failureConditions: [#FailureCondition, ...#FailureCondition]
})

#FailureHandlingObligation: close({
	id:    #Identifier
	kind!: "failure_handling"
	contract: close({
		givenFailure: #NonEmptyString
		response:     #NonEmptyString
	})
	statement:         #NonEmptyString
	sourceRefs:        [#Identifier, ...#Identifier]
	blocking:          bool
	failureConditions: [#FailureCondition, ...#FailureCondition]
})

#Obligation: #BehaviorObligation | #InvariantObligation | #FailureHandlingObligation
