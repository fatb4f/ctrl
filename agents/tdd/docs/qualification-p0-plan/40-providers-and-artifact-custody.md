# Providers and artifact custody

Implement a project-owned pytest provider using public pytest hooks. It emits normalized collection,
call, setup/teardown, exit, timeout, signal, output, and capture-integrity facts. It does not
classify qualification.

Repository snapshots include normalized file paths, bytes, modes, and execution-environment
identity. VCS metadata, caches, build output, and runtime files are excluded from the subject
digest.

The typed repair executor supports only exact file replacements in P0. It verifies the R0 subject,
preimage digests, allowed paths, and non-symlink/path-safe targets before materializing R1.

Build R1 into a wheel, then verify A1 metadata, `RECORD`, paths, contents, permissions, and
provenance. Install A1 into an isolated environment, derive the installed environment and file
identity, and create distinct subject I1. Installed probes execute from a neutral directory without
source-path leakage.
