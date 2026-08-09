package workflowfixtures

import planning "github.com/fatb4f/tdd-agent-skills/contracts/planning"

probeSpecs: [planning.#ProbeSpec & {
	id:        "probe.workflow-example"
	fixtureID: "fixture.workflow-example"
	obligationIDs: [
		"obligation.hc7910fd07c9ba22bb309f5225aa71145722aa14910cadc534d750e8a0a84983d",
		"obligation.h2cb8ee3051c97c25295337e6d1dcb9a2b64fddef70c829197419824f146d4f03",
	]
	stimulus: argv: ["python-ppf", "workflow", "plan"]
	oracle: exitCode: 0
	timeoutSeconds: 30
	captureClaims: []
}]
