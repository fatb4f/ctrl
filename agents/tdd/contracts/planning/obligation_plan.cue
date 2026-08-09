package planning

#ObligationPlan: close({
	schemaVersion!: "obligation-plan/v0"
	taskIntent:     #TaskIntent
	obligations:    [#Obligation, ...#Obligation]
	realizations:   [#Realization, ...#Realization]
})
