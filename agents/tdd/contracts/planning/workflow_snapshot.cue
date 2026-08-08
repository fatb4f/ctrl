package planning

#WorkflowSnapshotIdentity: close({
	fullDigest:     #SHA256
	semanticDigest: #SHA256
})

#WorkflowSnapshot: close({
	identity: #WorkflowSnapshotIdentity
	payload: close({
		schema:                 "workflow-snapshot/v0"
		algorithmVersions:      [string]: #NonEmptyString
		planArtifactOccurrence: #PlanArtifactOccurrence
		sourceBlocks:           [...#SourceBlock]
		planRevision:           #PlanRevision
		phases:                 [...#PlanPhase]
		families:               [...#DeliverableFamily]
		interimSpecRevision:    #InterimSpecRevision
		specSections:           [...#SpecSection]
		obligations:            [...]
		fixtureManifests:       [...#FixtureManifest]
		probes:                 [...#ProbeSpec]
		realizationSpecs:       [...#RealizationSpec]
		revisionLedger:         [#Identifier]: #SHA256
	})
})
