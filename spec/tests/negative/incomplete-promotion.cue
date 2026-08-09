package negative

import qualification "github.com/fatb4f/ctrl/spec/qualification"

zero: "sha256:0000000000000000000000000000000000000000000000000000000000000000"

invalid: qualification.#PromotionAuthorization & {
	schema: "promotion-authorization/s0"
	scope:  "RESULT_LOCAL"
	result: {
		repository: {revision: zero, components: {}}
		claims:     {}
		complete:   false
		verdict:    "INCONCLUSIVE"
		violations: []
	}
}
