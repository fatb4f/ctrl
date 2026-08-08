package planning

#SubjectRef: #NonEmptyString

#RealizationSpec: close({
	id:            #Identifier
	subject:       #SubjectRef
	obligationIDs: [#Identifier, ...#Identifier]
	probeIDs:      [#Identifier, ...#Identifier]
})
