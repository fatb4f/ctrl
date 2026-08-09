package examples

import "github.com/fatb4f/tdd-agent-skills/contracts/planning"

validPlan: planning.#ObligationPlan & {
	schemaVersion: "obligation-plan/v0"
	taskIntent: {
		id:      "task.cli-json-output"
		summary: "Add structured JSON output to the inspect command."
		requirements: [{
			id:        "task.requirement.json-output"
			statement: "JSON mode emits one JSON object on stdout."
		}]
	}
	obligations: [{
		id:        "cli.inspect.json-success"
		kind:      "behavior"
		statement: "JSON mode emits exactly one JSON object on stdout and exits successfully."
		sourceRefs: ["task.requirement.json-output"]
		blocking: true
		contract: {
			given: "a valid project"
			when:  "app inspect --json is invoked"
			then:  "stdout contains exactly one JSON object and the process exits successfully"
		}
		failureConditions: [
			{
				id:        "cli.failure.stdout-not-json"
				statement: "stdout is not valid JSON"
			},
			{
				id:        "cli.failure.multiple-documents"
				statement: "stdout contains more than one JSON document"
			},
			{
				id:        "cli.failure.unsuccessful-exit"
				statement: "the process exits unsuccessfully"
			},
		]
	}]
	realizations: [{
		id:            "realization.cli-inspect-json-success"
		kind:          "process"
		obligationIds: ["cli.inspect.json-success"]
		setup: repositoryFixture: "valid-project"
		stimulus: argv: ["app", "inspect", "--json"]
		oracle: {
			exitCode: 0
			stdout: {
				parsesAs:      "json"
				rootType:      "object"
				documentCount: 1
			}
		}
		counterexamples: [{
			id:                   "counterexample.cli-diagnostic-prefix"
			description:          "A diagnostic line precedes the JSON document on stdout."
			expectedOracleResult: "fail"
		}]
		baselineExpectation: {
			outcome: "fail"
			reason:  "JSON mode does not exist yet."
		}
		captureClaims: [{
			obligationId: "cli.inspect.json-success"
			oraclePaths: [
				"/oracle/exitCode",
				"/oracle/stdout/parsesAs",
				"/oracle/stdout/rootType",
				"/oracle/stdout/documentCount",
			]
			failureConditionIds: [
				"cli.failure.stdout-not-json",
				"cli.failure.multiple-documents",
				"cli.failure.unsuccessful-exit",
			]
		}]
	}]
}
