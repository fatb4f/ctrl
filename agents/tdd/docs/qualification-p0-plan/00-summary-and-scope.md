# Summary and scope

P0 proves the complete qualification authority chain for one obligation, without mutation
testing, agent SDK execution, graph orchestration, runtime tracing, waivers, or `python-control`:

```text
CUE contracts
    ↓
JSON Schema projection
    ↓
generated frozen Pydantic transports
    ↓
repository subject identity
    ↓
pytest probe execution
    ↓
ProviderObservation
    ↓
EvidenceApplicability and EvidenceAdmission
    ↓
Claim and Residual derivation
    ↓
deterministic legal transition
    ↓
typed candidate repair
    ↓
source-candidate qualification
    ↓
release-artifact construction and verification
    ↓
installed-artifact identity
    ↓
installed-artifact requalification
    ↓
PromotionAuthorization
```

The proof subject is a dedicated fixture distribution with an unknown-configuration-key defect.
The shipped distribution remains `tdd-agent-skills`, the public command remains `python-ppf`, and
the Python import root is migrated from `tdd_agent_skills` to `tdd_seed` as a clean break without a
compatibility shim.

P1 adds mutation qualification, hostile-world generation, repeated-observation stability,
waivers, runtime providers, historical policy ranking, and control-policy integration. None of
those capabilities may be required for a P0 promotion decision.
