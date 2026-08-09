package control

// sourceImports records the exact committed trees materialized for S0.
sourceImports: [
	{
		componentID: "qualification-spec"
		source:      "fatb4f/kernel-spec"
		repository:  "https://github.com/fatb4f/kernel-spec.git"
		revision:    "c6f4dea0e962a0a7459c0e86df8ddd8aafce5c83"
		tree:        "7deda7eb8e1a34cf80884dc2fb881bc92701f941"
		destination: "spec"
	},
	{
		componentID: "ppf"
		source:      "fatb4f/ppf"
		repository:  "https://github.com/fatb4f/ppf"
		revision:    "53af6aa42aec6fc104bbf2abe7410d125c7540cb"
		tree:        "7cf9ce516078e958fde58be3a030b26d589f3c20"
		destination: "packages/ppf"
	},
	{
		componentID: "runtime-promptgen"
		source:      "fatb4f/runtime"
		repository:  "https://github.com/fatb4f/runtime"
		revision:    "e5373bf8361ed88bd0bb3226f0ce827a41b90ec7"
		tree:        "4e09e6cf34f258ec08078aae208922f913b80d79"
		destination: "packages/runtime"
	},
	{
		componentID: "tdd-agent-skills"
		source:      "fatb4f/tdd-seed"
		repository:  "https://github.com/fatb4f/tdd-seed"
		revision:    "8126842b911a5a2c43699016c9c040ecf77d63de"
		tree:        "6c94abfada2f2485b3705b7484b4279798f4c8da"
		destination: "agents/tdd"
	},
	{
		componentID: "openai-sdk-feedback"
		source:      "fatb4f/sdk-feedback"
		repository:  "https://github.com/fatb4f/sdk-feedback"
		revision:    "8711b89e3c40f6652101ecba7b1e8cc192907a91"
		tree:        "167fec95ff520568d8a5796c9042cf17f7b18fc4"
		destination: "integrations/openai"
	},
]
