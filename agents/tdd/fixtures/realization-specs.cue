package workflowfixtures

import planning "github.com/fatb4f/tdd-agent-skills/contracts/planning"

realizationSpecs: [planning.#RealizationSpec & {
	id:      "realization.workflow-example"
	subject: "workflow-plan compiler"
	obligationIDs: [
		"obligation.hc7910fd07c9ba22bb309f5225aa71145722aa14910cadc534d750e8a0a84983d",
		"obligation.h2cb8ee3051c97c25295337e6d1dcb9a2b64fddef70c829197419824f146d4f03",
	]
	probeIDs: ["probe.workflow-example"]
}]
