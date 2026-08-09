# Typed workflow compiler example

This small plan is the compiler's committed dogfood fixture. The fenced records below are
normative; this prose is explanatory only.

```cue plan.revision
id: "plan.workflow.r1"
sequence: 1
title: "Workflow compiler example"
```

```cue plan.phase
id: "phase.workflow"
planRevisionID: "plan.workflow.r1"
sequence: 0
title: "Compile workflow"
summary: "Compile typed Markdown into an admitted static snapshot."
```

```cue plan.family
id: "family.workflow"
planRevisionID: "plan.workflow.r1"
phaseID: "phase.workflow"
sequence: 0
title: "Workflow compilation"
summary: "Extract, validate, and derive one static workflow."
dependsOn: []
```

```cue spec.revision
id: "spec.workflow.r1"
planRevisionID: "plan.workflow.r1"
sequence: 1
```

```cue spec.section
id: "spec.section.example"
specRevisionID: "spec.workflow.r1"
familyID: "family.workflow"
sequence: 0
title: "Static workflow snapshot"
subject: "workflow-plan compiler"
contract: {
    invariants: [{
        id: "invariant.example.nonempty"
        statement: "A compiled workflow contains at least one admitted fixture manifest."
        changeIntent: "preserve"
    }]
}
acceptance: [{
    id: "criterion.example.compile"
    kind: "positive"
    statement: "A valid typed Markdown plan compiles to a canonical static workflow snapshot."
    changeIntent: "introduce"
}]
```
