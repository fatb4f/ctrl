package planning

#JsonPointer: #NonEmptyString & =~"^/([^/~]|~[01])+(\/([^/~]|~[01])*)*$"

#BaselineExpectation: close({
	outcome: "fail" | "pass" | "unknown"
	reason:  #NonEmptyString
})

#Counterexample: close({
	id:                    #Identifier
	description:           #NonEmptyString
	expectedOracleResult!: "fail"
})

#CaptureClaim: close({
	obligationId:        #Identifier
	oraclePaths:         [#JsonPointer, ...#JsonPointer]
	failureConditionIds: [#Identifier, ...#Identifier]
})

#ProcessSetup: close({
	repositoryFixture: #NonEmptyString
})

#ProcessStimulus: close({
	argv: [#NonEmptyString, ...#NonEmptyString]
})

#JsonStdoutOracle: close({
	parsesAs!:     "json"
	rootType:      "object" | "array"
	documentCount: int & >=1
})

#ProcessOracle: close({
	exitCode: int
	stdout:   #JsonStdoutOracle
})

#ProcessRealization: close({
	id:                  #Identifier
	kind!:               "process"
	obligationIds:       [#Identifier, ...#Identifier]
	setup:               #ProcessSetup
	stimulus:            #ProcessStimulus
	oracle:              #ProcessOracle
	counterexamples:     [#Counterexample, ...#Counterexample]
	baselineExpectation: #BaselineExpectation
	captureClaims:       [#CaptureClaim, ...#CaptureClaim]
})

#Realization: #ProcessRealization
