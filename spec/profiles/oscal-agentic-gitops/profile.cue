package oscalagenticgitops

import (
	controller "github.com/fatb4f/ctrl/spec/controller"
	repository "github.com/fatb4f/ctrl/spec/repository"
)

#GovernedRepository: repository.#Component & {
	id:   "qualification-spec"
	root: "spec"
}

#AgenticGitOpsController: controller.#Controller & {
	id:        "oscal-agentic-gitops-controller"
	component: #GovernedRepository
}
