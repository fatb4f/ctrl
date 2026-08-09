package bootstrap

import qualification "github.com/fatb4f/ctrl/spec/qualification"

zero: "sha256:0000000000000000000000000000000000000000000000000000000000000000"

result: qualification.#QualificationResult & {
	repository: {
		revision: zero
		components: {
			ppf: {id: "ppf", root: "packages/ppf"}
		}
	}
	claims: {
		"workspace-coherent": {
			claimID:       "workspace-coherent"
			observationID: "root-check"
			status:        "SATISFIED"
			reason:        "root qualification passed"
		}
	}
	complete:   true
	verdict:    "QUALIFIED"
	violations: []
}

let Result = result

promotion: qualification.#PromotionAuthorization & {
	schema: "promotion-authorization/s0"
	scope:  "RESULT_LOCAL"
	result: Result
}
