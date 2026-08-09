package workflowfixtures

import planning "github.com/fatb4f/ctrl/spec/qualification/workflow:planning"

fixtureSpecs: [planning.#FixtureSpec & {
	id:          "fixture.workflow-example"
	description: "Minimal fixture for static workflow compilation."
}]
