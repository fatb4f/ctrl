package contracts

#NonEmptyString:  string & =~"[^[:space:]]"
#PackageName:     #NonEmptyString & =~"^[a-z][a-z0-9-]*$"
#SemanticVersion: string & =~"^0\\.[0-9]+\\.[0-9]+$"
#Identifier:      #NonEmptyString & =~"^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)*$"
#SkillID:         #Identifier
#ObligationSetID: #Identifier
#ObligationID:    #Identifier
#RelativePath:    #NonEmptyString & !~"^/" & !~"(^|/)\\.\\.(/|$)"

#Maturity: "placeholder" | "prototype" | "qualified"
#Phase:    "plan" | "red" | "green" | "refactor" | "promote"
#Domain:   "cross-cutting" | "python-library" | "python-cli" | "python-data-pipeline" | "temporal-workflow"

#EvidenceRequirement: close({
	kind:        "test" | "command" | "artifact" | "inspection"
	description: #NonEmptyString
	fresh:       bool | *true
})

#Obligation: close({
	statement: #NonEmptyString
	phase:     #Phase
	level:     "must" | "should"
	maturity:  #Maturity
	evidence:  [#EvidenceRequirement, ...#EvidenceRequirement]
})

#ObligationSet: close({
	domain:     #Domain
	ownerSkill: #SkillID
	maturity:   #Maturity

	obligations: [#ObligationID]: #Obligation
})

#Skill: close({
	kind:     "control" | "diagnosis" | "obligation"
	path:     #RelativePath
	maturity: #Maturity

	dependsOn: [...#SkillID] | *[]
	governs:   [...#ObligationSetID] | *[]
})

#EvaluationPolicy: close({
	root: #RelativePath

	pairedBaseline:        bool
	mutationCoverage:      bool
	freshEvidenceRequired: bool

	scenarios: #RelativePath
	mutations: #RelativePath
	graders:   #RelativePath
	runner:    #RelativePath
})

// #ObligationsGovernedPackage is the authoritative package contract.
// Skills describe how work is performed; obligation sets define what must be true.
// Promotion is admissible only when all applicable obligations have fresh evidence.
#ObligationsGovernedPackage: close({
	schema: "agent-skills.obligations-governed-package/v0"

	identity: close({
		name:        #PackageName
		version:     #SemanticVersion
		description: #NonEmptyString
	})

	governance: close({
		authority:      "obligations"
		controlSkill:   #SkillID
		diagnosisSkill: #SkillID
		lifecycle:      ["plan", "red", "green", "refactor", "promote"]

		promotion: close({
			requiresAllApplicableObligations: true
			requiresFreshEvidence:            true
			allowsUnresolvedFailures:         false
		})
	})

	skills: [#SkillID]:                 #Skill
	obligationSets: [#ObligationSetID]: #ObligationSet
	evaluations: #EvaluationPolicy

	// Cross-reference closure is intentionally evaluated outside this seed schema.
	// The contract governs document shape and authority; the future evaluator will
	// prove that skill, dependency, ownership, and governed-set references resolve.
})
