package workflowfixtures

import planning "github.com/fatba4f/ctrl/agents/tdd/contracts/planning"

fixtureSpecs: [planning.#FixtureSpec & {
	id:          "fixture.workflow-example"
	description: "Minimal fixture for static workflow compilation."
}]
