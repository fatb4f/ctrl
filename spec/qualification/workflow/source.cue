package planning

#ChangeIntent:   "introduce" | "preserve" | "modify"
#BaselinePolicy: "must-fail" | "must-pass" | "unconstrained"

#SourcePolicy: close({
	blocking:           bool | *true
	changeIntent:       #ChangeIntent
	baselinePolicy?:    #BaselinePolicy
	baselineRationale?: #NonEmptyString
})

#SourceBlock: close({
	kind:         "plan.revision" | "plan.phase" | "plan.family" | "spec.revision" | "spec.section"
	lineStart:    uint & >=1
	lineEnd:      uint & >=lineStart
	byteStart:    uint
	byteEnd:      uint & >=byteStart
	sourceDigest: #SHA256
	recordDigest: #SHA256
	recordID:     #Identifier
})

#PlanArtifactOccurrence: close({
	path:            #RepositoryPath
	bytesDigest:     #SHA256
	normativeDigest: #SHA256
})
