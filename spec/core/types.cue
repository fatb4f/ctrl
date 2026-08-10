@experiment(explicitopen)

// Package core owns qualification-neutral identities and coordinates.
package core

#NonEmptyString: string & =~"^[\\s\\S]+$"
#ID:             #NonEmptyString & =~"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$"
#ComponentID:    #ID
#ClaimID:        #ID
#ObservationID:  #ID
#Digest:         string & =~"^sha256:[a-f0-9]{64}$"

#SourceCoordinate: {
	path:     #NonEmptyString
	revision: #Digest
}

#ArtifactCoordinate: {
	path:       #NonEmptyString
	digest:     #Digest
	mediaType?: #NonEmptyString
}
