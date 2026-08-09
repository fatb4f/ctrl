package planning

#NonEmptyString: string & =~"\\S"
#Identifier:     #NonEmptyString & =~"^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$"

#TaskRequirement: close({
	id:        #Identifier
	statement: #NonEmptyString
})

#TaskIntent: close({
	id:           #Identifier
	summary:      #NonEmptyString
	requirements: [#TaskRequirement, ...#TaskRequirement]
})
