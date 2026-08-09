// Package controller consumes qualification results; qualification never
// imports this package.
package controller

import (
	core "github.com/fatb4f/ctrl/spec/core"
	qualification "github.com/fatb4f/ctrl/spec/qualification"
	repository "github.com/fatb4f/ctrl/spec/repository"
)

#Controller: {
	id:        core.#ID
	component: repository.#Component
}

#PromotionDecision: {
	controller:    #Controller
	result:        qualification.#QualificationResult
	let Result = result
	authorization: qualification.#PromotionAuthorization & {result: Result}
}
