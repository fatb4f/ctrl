package seed

import "github.com/fatb4f/ctrl/agents/tdd/contracts"

packageManifest: contracts.#ObligationsGovernedPackage & {
	identity: {
		name:        "tdd-agent-skills"
		version:     "0.1.0"
		description: "Seed package for obligation-governed, domain-specialized TDD agent skills."
	}

	governance: {
		controlSkill:   "tdd-control"
		diagnosisSkill: "active-diagnosis"
	}

	skills: close({
		"tdd-control": {
			kind:     "control"
			path:     "skills/tdd-control/SKILL.md"
			maturity: "placeholder"
			governs:  ["tdd-cycle"]
		}

		"active-diagnosis": {
			kind:      "diagnosis"
			path:      "skills/active-diagnosis/SKILL.md"
			maturity:  "placeholder"
			dependsOn: ["tdd-control"]
		}

		"python-library-obligations": {
			kind:      "obligation"
			path:      "skills/obligations/python-library/SKILL.md"
			maturity:  "placeholder"
			dependsOn: ["tdd-control"]
			governs:   ["python-library"]
		}

		"python-cli-obligations": {
			kind:      "obligation"
			path:      "skills/obligations/python-cli/SKILL.md"
			maturity:  "placeholder"
			dependsOn: ["tdd-control", "active-diagnosis"]
			governs:   ["python-cli"]
		}

		"python-data-pipeline-obligations": {
			kind:      "obligation"
			path:      "skills/obligations/python-data-pipeline/SKILL.md"
			maturity:  "placeholder"
			dependsOn: ["tdd-control", "active-diagnosis"]
			governs:   ["python-data-pipeline"]
		}

		"temporal-workflow-obligations": {
			kind:      "obligation"
			path:      "skills/obligations/temporal-workflow/SKILL.md"
			maturity:  "placeholder"
			dependsOn: ["tdd-control", "active-diagnosis"]
			governs:   ["temporal-workflow"]
		}
	})

	obligationSets: close({
		"tdd-cycle": {
			domain:     "cross-cutting"
			ownerSkill: "tdd-control"
			maturity:   "placeholder"
			obligations: close({
				"fresh-promotion-evidence": {
					statement: "TODO: define the evidence required before promotion."
					phase:     "promote"
					level:     "must"
					maturity:  "placeholder"
					evidence: [{
						kind:        "command"
						description: "TODO: execute the authoritative qualification command."
					}]
				}
			})
		}

		"python-library": {
			domain:     "python-library"
			ownerSkill: "python-library-obligations"
			maturity:   "placeholder"
			obligations: close({
				"public-api-contract": {
					statement: "TODO: define the public API behavior obligation."
					phase:     "red"
					level:     "must"
					maturity:  "placeholder"
					evidence: [{
						kind:        "test"
						description: "TODO: add a failing public-interface test."
					}]
				}
			})
		}

		"python-cli": {
			domain:     "python-cli"
			ownerSkill: "python-cli-obligations"
			maturity:   "placeholder"
			obligations: close({
				"process-contract": {
					statement: "TODO: define exit-status, stdout, stderr, and side-effect obligations."
					phase:     "red"
					level:     "must"
					maturity:  "placeholder"
					evidence: [{
						kind:        "test"
						description: "TODO: exercise the CLI as an external process."
					}]
				}
			})
		}

		"python-data-pipeline": {
			domain:     "python-data-pipeline"
			ownerSkill: "python-data-pipeline-obligations"
			maturity:   "placeholder"
			obligations: close({
				"deterministic-transformation": {
					statement: "TODO: define schema, row-invariant, idempotence, and replay obligations."
					phase:     "red"
					level:     "must"
					maturity:  "placeholder"
					evidence: [{
						kind:        "test"
						description: "TODO: compare fixture input with deterministic expected output."
					}]
				}
			})
		}

		"temporal-workflow": {
			domain:     "temporal-workflow"
			ownerSkill: "temporal-workflow-obligations"
			maturity:   "placeholder"
			obligations: close({
				"replay-safety": {
					statement: "TODO: define replay, retry, timeout, and compensation obligations."
					phase:     "red"
					level:     "must"
					maturity:  "placeholder"
					evidence: [{
						kind:        "test"
						description: "TODO: execute workflow history under deterministic replay."
					}]
				}
			})
		}
	})

	evaluations: {
		root:                  "evals"
		pairedBaseline:        true
		mutationCoverage:      true
		freshEvidenceRequired: true
		scenarios:             "evals/scenarios"
		mutations:             "evals/mutations"
		graders:               "evals/graders"
		runner:                "evals/runner"
	}
}
