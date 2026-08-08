## Generalized foundational decision matrix

The matrix should operate on **independent validation planes**, not on a particular diagnostic category.

```text
Static model
    ↓
Interpreter acceptance
    ↓
Program loading
    ↓
Path execution
    ↓
Behavioral contract
    ↓
Liveness
```

### Observation axes

| Plane    | Question                                                       |
| -------- | -------------------------------------------------------------- |
| Static   | Does the checker reject the program or infer an inconsistency? |
| Compile  | Can the selected CPython interpreter parse and compile it?     |
| Load     | Can CPython initialize the relevant modules and dependencies?  |
| Reach    | Does execution reach the implicated location or operation?     |
| Execute  | Does that operation complete without an exception?             |
| Contract | Does the resulting value or state satisfy expectations?        |
| Liveness | Does the operation complete within the expected bound?         |

## Decision matrix

| Static checker | Compile/load               | Runtime observation                     | Candidate concentration                                                                            |
| -------------- | -------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Fail           | Fail at compile            | Not executable                          | Syntax, encoding, unsupported language feature, interpreter-version mismatch                       |
| Fail           | Compile passes; load fails | Relevant path not entered               | Dependency, package initialization, configuration, native loading, environment                     |
| Fail           | Load passes                | Same operation raises                   | Checker and runtime agree on the failure region; concentrate on the reported contract or operation |
| Fail           | Load passes                | Same operation succeeds                 | Static model, annotation, stub, configuration, narrowing, or checker limitation                    |
| Fail           | Load passes                | Reported location is unreachable        | Dead code, disabled branch, platform guard, stale diagnostic, incorrect causal attribution         |
| Pass           | Fail at compile            | Not executable                          | Static coverage gap or checker/interpreter grammar divergence                                      |
| Pass           | Compile passes; load fails | Relevant path not entered               | Runtime-only initialization, dependency, side effect, native extension, or environment failure     |
| Pass           | Load passes                | Name or attribute lookup raises         | Dynamic namespace, initialization order, reflection, mutation, or static coverage gap              |
| Pass           | Load passes                | Call raises                             | Runtime value, input, state, external resource, or unchecked behavioral precondition               |
| Pass           | Load passes                | Call returns invalid result             | Behavioral contract, state transition, postcondition, or data-integrity failure                    |
| Pass           | Load passes                | Assertion fails                         | Specification and implementation disagree despite structural validity                              |
| Pass           | Load passes                | Execution hangs                         | Blocking, scheduling, lock, nontermination, resource starvation, or external dependency            |
| Pass           | Load passes                | Process exits or crashes                | Native fault, explicit termination, resource exhaustion, signal, or interpreter/runtime defect     |
| Pass           | Load passes                | Relevant path succeeds                  | No observed defect under this probe; broaden inputs, environment, path, or timing                  |
| Fail near X    | Load passes                | Runtime reaches X and succeeds          | Static false positive or modeled/runtime context divergence                                        |
| Fail near X    | Load passes                | Runtime reaches X and fails differently | Diagnostic is correlated but not causally precise                                                  |
| Fail near X    | Load passes                | Runtime never reaches X                 | Dead path, wrong reproduction, guard divergence, or incorrect causal attribution                   |

## Generalized by failure family

The same matrix applies to several diagnostic families.

| Diagnostic family          | Static signal                           | CPython/runtime discriminator             |
| -------------------------- | --------------------------------------- | ----------------------------------------- |
| Syntax or language version | Parser/checker diagnostic               | `py_compile`                              |
| Import or dependency       | Unresolved module/export                | Module load                               |
| Name resolution            | Undefined name                          | Reach the lookup                          |
| Attribute access           | Missing member                          | Evaluate `object.attribute`               |
| Type compatibility         | Assignment, return, argument mismatch   | Execute with representative values        |
| Call compatibility         | Invalid arguments or signature          | Perform the call                          |
| Control flow               | Unreachable, unbound, incomplete return | Exercise the branch                       |
| Resource handling          | Potential misuse or leak                | Execute acquisition/release lifecycle     |
| State mutation             | Static warning may be absent            | Assert state before and after             |
| Concurrency                | Static warning usually absent           | Bounded execution and scheduling probes   |
| Performance/liveness       | Usually no static signal                | Timeout, sampling, or process observation |
| Native interoperability    | Stub or checker mismatch                | Load and invoke extension boundary        |

## Phase-oriented interpretation

### 1. Static failure and runtime failure agree

```text
checker rejects operation X
runtime reaches X
runtime fails at X in a compatible way
```

This is the strongest foundational correlation. The candidate set becomes:

- the operation itself;
- its input values;
- the declared versus actual contract;
- the local environment required by that operation.

It still does not prove that the checker identified the root cause, only that it identified the correct failure region.

### 2. Static failure but runtime succeeds

```text
checker rejects X
runtime executes X successfully
```

Concentrate on:

- incomplete or incorrect annotations;
- inaccurate stubs;
- checker configuration;
- unsupported dynamic behavior;
- narrowing or inference limitations;
- environment differences between checker and interpreter;
- a runtime case that is narrower than the checker must conservatively model.

### 3. Static success but runtime fails

```text
checker accepts X
runtime fails at or after X
```

Concentrate on:

- unchecked runtime values;
- mutation after validation;
- dynamic lookup;
- environment and external resources;
- module initialization;
- native code;
- concurrency;
- behavioral properties not represented by the type system.

### 4. Both pass but the contract fails

```text
static structure is acceptable
execution completes
observed result violates expectation
```

This is primarily a behavioral failure:

- incorrect return value;
- invalid state transition;
- missing side effect;
- excessive side effect;
- data corruption;
- ordering error;
- invariant or postcondition violation.

### 5. Both pass but execution does not complete

```text
static structure is acceptable
program loads
operation starts
operation exceeds its bound
```

This shifts the candidate set away from language validity and toward:

- infinite or excessively large iteration;
- deadlock or lock contention;
- blocking I/O;
- unavailable external service;
- scheduler starvation;
- subprocess waiting;
- resource exhaustion.

## Minimal normalized matrix

For implementation, the full table can be reduced to three independent result dimensions:

```python
StaticOutcome = Literal["pass", "fail", "not_run"]

RuntimePhase = Literal[
    "compile",
    "load",
    "reach",
    "execute",
    "contract",
    "liveness",
]

RuntimeOutcome = Literal[
    "pass",
    "exception",
    "assertion_failure",
    "timeout",
    "crash",
    "not_reached",
    "not_run",
]
```

The foundational classification function is then conceptually:

```text
classify(
    static_outcome,
    first_failed_runtime_phase,
    runtime_outcome,
    diagnostic_location_reached,
    runtime_failure_location,
)
    → candidate concentration
```

## Core invariant

> A static diagnostic is one observation about a possible invalid program state. CPython phase probes determine whether that state prevents acceptance, loading, reachability, execution, correctness, or termination.

This generalization makes unresolved imports only one specialization:

```text
unresolved import
    = static failure
    + runtime load-phase probe
```

Other diagnostics bind to different runtime phases:

```text
type mismatch        → execution or contract phase
undefined name       → reach or execution phase
invalid attribute    → execution phase
incorrect return     → contract phase
blocking call        → liveness phase
native extension     → load, execution, or crash phase
```
