"""Generated structural transports; canonical CUE owns semantic validity."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

AUTHORITATIVE_INPUT = "spec/qualification/kernel.cue"
AUTHORITATIVE_INPUT_DIGEST = (
    "sha256:37d2d6baed6f736118410f7d24ea378f84965d3732ec2b084651a4662cffdfb0"
)


class ClaimAdmissionTransport(BaseModel):
    """Representable claim-admission structure without semantic evaluation."""

    model_config = ConfigDict(extra="forbid")

    claimID: str
    observationID: str
    status: Literal["SATISFIED", "VIOLATED", "UNKNOWN"]
    reason: str


class QualificationResultTransport(BaseModel):
    """Representable result structure without CUE cross-record predicates."""

    model_config = ConfigDict(extra="forbid")

    claims: dict[str, ClaimAdmissionTransport]
    complete: bool
    verdict: Literal["QUALIFIED", "INCONCLUSIVE", "REJECTED"]
    violations: list[str]
