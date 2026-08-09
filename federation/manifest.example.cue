package federation

schema: "federation-manifest/v0"

// Pins become active only after each descriptor is committed in its owning
// repository. Machine-local checkout paths are supplied with --root and never
// committed here.
components: [
	{
		componentID:  "qualification-spec"
		repositoryID: "kernel-spec"
		url:          "https://github.com/fatb4f/kernel-spec.git"
		revision:     "c6f4dea0e962a0a7459c0e86df8ddd8aafce5c83"
	},
	{
		componentID:  "ppf"
		repositoryID: "ppf"
		url:          "https://github.com/fatb4f/ppf.git"
		revision:     "53af6aa42aec6fc104bbf2abe7410d125c7540cb"
	},
]

evaluations: []
