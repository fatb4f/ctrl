package workflowfixtures

import planning "github.com/fatb4f/tdd-agent-skills/contracts/planning"

fixtureSpecs: [planning.#FixtureSpec & {
	id:          "fixture.workflow-example"
	description: "Minimal fixture for static workflow compilation."
}]
