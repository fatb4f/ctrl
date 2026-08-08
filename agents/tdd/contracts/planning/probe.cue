package planning

#JsonPointer: #NonEmptyString & =~"^/([^/~]|~[01])+(\\/([^/~]|~[01])*)*$"

#WorkflowCaptureClaim: close({
	obligationID:       #Identifier
	oraclePaths:        [...#JsonPointer]
	failureConditionIDs: [...#Identifier]
})

#ProbeSpec: close({
	id:            #Identifier
	fixtureID:     #Identifier
	obligationIDs: [#Identifier, ...#Identifier]
	stimulus: close({
		argv: [#NonEmptyString, ...#NonEmptyString]
	})
	oracle: close({
		exitCode: #SafeInteger
	})
	timeoutSeconds: uint & >0
	captureClaims: [...#WorkflowCaptureClaim]
})
