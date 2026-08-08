package planning

import "list"

#ChangeID:    string & =~"^[a-z][a-z0-9-]*$"
#PathPattern: #NonEmptyString

#AuthorityID:  "semantic-product" | "qualification-procedure" | "skill-product"
#AuthorityRef: #AuthorityID
#ArtifactRef:  #NonEmptyString
#EvidenceType: #NonEmptyString

#Authority: close({
	id:         #AuthorityID
	path:       #RepositoryPath
	owns:       #NonEmptyString
	precedence: int & >=0
})

#Prohibition: close({
	id:        #ChangeID
	statement: #NonEmptyString
})

#PlanAcceptanceCriterion: close({
	id:           #ChangeID
	statement:    #NonEmptyString
	initialState: "failing" | "passing" | "not-applicable"
})

#Gate: close({
	command: #NonEmptyString
	purpose: #NonEmptyString
})

#GeneratedArtifact: close({
	artifact:      #ArtifactRef
	generator:     #NonEmptyString
	checkCommand:  #NonEmptyString
	manualEditing: false
})

#Proof: close({
	kind:        #NonEmptyString
	entryPoint?: #NonEmptyString
	statement?:  #NonEmptyString
	identities?: [#NonEmptyString, ...#NonEmptyString]
})

#PlanChange: {
	id:          #ChangeID
	title:       #NonEmptyString
	phase:       int & >=0
	dependsOn:   [...#ChangeID]
	authorities: [#AuthorityRef, ...#AuthorityRef]

	scope: close({
		include: [#PathPattern, ...#PathPattern]
		exclude: [...#PathPattern]
	})

	inputs:     [...#ArtifactRef]
	outputs:    [#ArtifactRef, ...#ArtifactRef]
	generated:  [...#GeneratedArtifact]
	prohibits:  [#Prohibition, ...#Prohibition]
	acceptance: [#PlanAcceptanceCriterion, ...#PlanAcceptanceCriterion]
	gates:      [#Gate, ...#Gate]

	implementation: close({
		runtimeCode:        bool
		subprocesses:       bool
		repositoryMutation: bool
		persistentState:    bool
		newEntryPoints:     [...#NonEmptyString]
	})

	proof: close({
		required: [...#Proof]
		evidence: [...#EvidenceType]
	})

	_acceptanceInitialStates: [for criterion in acceptance {criterion.initialState}]
	if implementation.runtimeCode {
		_runtimeStartsFailing: true & list.Contains(_acceptanceInitialStates, "failing")
	}
}

#CLITopology: close({
	applications: close({
		"python-ppf": close({
			framework: "cyclopts"
			role:      "product-control-plane"
			commands:  ["qualify run"]
		})

		"jj-agent": close({
			framework: "cyclopts"
			role:      "external-qualified-adapter"
			commands: [
				"observe",
				"atomic",
				"split",
				"resolve-conflict",
				"workspace",
			]
		})
	})

	shared: close({
		conventions:       "shared-cyclopts"
		requestDecoding:   "generated-transport"
		transportTypes:    "generated-transport"
		operationRegistry: "generated-registry"
		errorEnvelope:     "shared"
		exitMapping:       "shared"
	})

	forbidden: [
		"argparse",
		"entry-point-local request models",
		"entry-point-local operation registries",
		"implicit JSON coercion",
	]
})

#PlanContract: {
	schemaVersion: "plan-change-sequence/v0"

	authorityModel: close({
		authorities: [#Authority, #Authority, #Authority]
		conflictRules: [
			"Semantic invariants cannot be weakened by procedural documents.",
			"Procedural sequencing cannot silently alter product interfaces.",
			"Skill packaging cannot introduce runtime behavior absent from the semantic or procedural plans.",
			"An irreconcilable conflict requires an explicit decision record; implementation cannot choose implicitly.",
		]
	})

	cliTopology: #CLITopology
	changes:     [#PlanChange, ...#PlanChange]
	changeIndex: {
		for index, change in changes {
			(change.id): index
		}
	}

	_dependencyChecks: {
		for index, change in changes {
			for dependency in change.dependsOn {
				("\(index)-\(dependency)"): true & (changeIndex[dependency] < index)
			}
		}
	}

	_authorityReconciliationIsRuntimeFree: false & changes[changeIndex["authority-reconciliation"]].implementation.runtimeCode
	_observePrecedesAtomic:                true & (changeIndex["observe-production"] < changeIndex["atomic-production"])
	_releaseUsesInstalledAdapter: true & list.Contains(
		changes[changeIndex["vertical-release-proof"]].proof.required,
		{kind: "installed-entry-point", entryPoint: "jj-agent"},
	)
}
