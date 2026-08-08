package kernelspec

#APIDataType: close({
	id:     #ID
	source: #SemanticReference
})

#APIResource: close({
	id:       #ID
	source:   #SemanticReference
	dataType: #ID
})

#APIOperation: close({
	id:     #OperationID
	source: #SemanticReference

	input?:   #ID
	output?:  #ID
	errors:   [...#ID]
	security: [...#ID]
})

#APIMessage: close({
	id:       #ID
	dataType: #ID
})

#APIEvent: close({
	id:      #ID
	message: #ID
	source:  #SemanticReference
})

#APIError: close({
	id:        #ID
	dataType?: #ID
})

// Model B is generated from the authoritative Model A OSCAL API closure. It
// owns no independently authored semantics and is not a parallel API model.
#APIModel: close({
	authority: #ModelBAuthority

	identity: close({
		id:       #ID
		revision: #Revision
	})

	source: close({
		modelARevision:   #Revision
		compiler:         #CompilerID
		compilerRevision: #Revision
		profile:          #ProjectionID
	})

	dataTypes: [#ID]:           #APIDataType
	resources: [#ID]:           #APIResource
	operations: [#OperationID]: #APIOperation
	messages: [#ID]:            #APIMessage
	events: [#ID]:              #APIEvent
	errors: [#ID]:              #APIError
})
