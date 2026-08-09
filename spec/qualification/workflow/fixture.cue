package planning

#FixtureSpec: close({
	id:          #Identifier
	description: #NonEmptyString
})

#FixtureEntry: close({
	path:       #RepositoryPath
	mode:       "100644" | "100755"
	byteLength: uint
	fileDigest: #SHA256
})

#FixtureManifest: close({
	fixtureID:  #Identifier
	entries:    [...#FixtureEntry]
	treeDigest: #SHA256
})
