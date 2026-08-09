"""Verify independently qualified components and derive a federation identity."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, Final

DESCRIPTOR_DOMAIN: Final = b"fatb4f.component-descriptor.v0\0"
ASSEMBLY_DOMAIN: Final = b"fatb4f.federation-assembly.v0\0"
ARTIFACT_DOMAIN: Final = b"fatb4f.component-artifact.v0\0"


class FederationError(ValueError):
    """A pinned component cannot participate in the requested assembly."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def domain_digest(domain: bytes, payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(domain + payload).hexdigest()


def _run(
    arguments: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(arguments, cwd=cwd, check=False, capture_output=True)
    if check and completed.returncode:
        message = completed.stderr.decode("utf-8", "replace").strip()
        raise FederationError(message or f"command failed: {arguments!r}")
    return completed


def _git(root: Path, *arguments: str) -> bytes:
    return _run(["git", "-C", str(root), *arguments]).stdout


def load_cue(path: Path) -> dict[str, Any]:
    payload = json.loads(_run(["cue", "export", str(path.resolve()), "--out", "json"]).stdout)
    if not isinstance(payload, dict):
        raise FederationError(f"{path} did not export a JSON object")
    return payload


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = load_cue(path)
    if manifest.get("schema") != "federation-manifest/v0":
        raise FederationError("unsupported federation manifest schema")
    return manifest


def _managed_checkout(pin: dict[str, Any], managed_root: Path) -> Path:
    root = managed_root / pin["componentID"]
    if not root.exists():
        managed_root.mkdir(parents=True, exist_ok=True)
        _run(["git", "clone", "--filter=blob:none", "--no-checkout", pin["url"], str(root)])
    _run(["git", "-C", str(root), "fetch", "--depth=1", "origin", pin["revision"]])
    _run(["git", "-C", str(root), "checkout", "--detach", pin["revision"]])
    return root


def resolve_root(pin: dict[str, Any], roots: dict[str, Path], managed_root: Path) -> Path:
    override = roots.get(pin["componentID"])
    return override.resolve() if override is not None else _managed_checkout(pin, managed_root)


def verify_component_source(pin: dict[str, Any], root: Path) -> tuple[dict[str, Any], str]:
    actual_revision = _git(root, "rev-parse", "HEAD").decode().strip()
    if actual_revision != pin["revision"]:
        raise FederationError(
            f"{pin['componentID']}: expected revision {pin['revision']}, got {actual_revision}"
        )
    descriptor_path = root / "architecture/component.cue"
    if not descriptor_path.is_file():
        raise FederationError(f"{pin['componentID']}: missing architecture/component.cue")
    committed = _git(root, "show", f"{pin['revision']}:architecture/component.cue")
    if committed != descriptor_path.read_bytes():
        raise FederationError(f"{pin['componentID']}: component descriptor is dirty")
    exported = load_cue(descriptor_path)
    descriptor = exported.get("descriptor", exported)
    if descriptor.get("schema") != "component-descriptor/v0":
        raise FederationError(f"{pin['componentID']}: unsupported descriptor schema")
    if descriptor.get("componentID") != pin["componentID"]:
        raise FederationError(f"{pin['componentID']}: descriptor identity does not match its pin")
    descriptor_digest = domain_digest(DESCRIPTOR_DOMAIN, canonical_json(descriptor))
    return descriptor, descriptor_digest


def kernel_component_check(
    root: Path,
    descriptor_path: Path,
    observations_path: Path,
    contract_root: Path,
) -> dict[str, Any]:
    del root
    completed = _run(
        [
            "uv",
            "run",
            "--project",
            str(contract_root),
            "--frozen",
            "--no-sync",
            "python",
            "-m",
            "kernel_spec.component",
            "--descriptor",
            str(descriptor_path),
            "--observations",
            str(observations_path),
        ]
    )
    result = json.loads(completed.stdout)
    if result.get("qualified") is not True:
        raise FederationError("component architecture did not qualify")
    return result


ComponentChecker = Callable[[Path, Path, Path, Path], dict[str, Any]]


def _run_command(command: list[str], root: Path) -> None:
    _run(command, cwd=root)


def _artifact_digests(root: Path) -> dict[str, str]:
    artifacts: dict[str, str] = {}
    for path in sorted((root / "dist").glob("**/*.whl")) if (root / "dist").is_dir() else []:
        relative = path.relative_to(root).as_posix()
        artifacts[relative] = domain_digest(ARTIFACT_DOMAIN, path.read_bytes())
    return artifacts


def component_instance(
    pin: dict[str, Any],
    root: Path,
    contract_root: Path,
    *,
    checker: ComponentChecker = kernel_component_check,
    run_commands: bool = True,
) -> dict[str, Any]:
    descriptor, descriptor_digest = verify_component_source(pin, root)
    observations = root / "architecture/observed-dependencies.json"
    if not observations.is_file():
        raise FederationError(f"{pin['componentID']}: missing dependency observations")
    local_result = checker(
        root,
        root / "architecture/component.cue",
        observations,
        contract_root,
    )
    if local_result.get("descriptorDigest") != descriptor_digest:
        raise FederationError(f"{pin['componentID']}: local qualifier used another descriptor")
    if run_commands:
        _run_command(descriptor["commands"]["qualify"], root)
    return {
        "componentID": pin["componentID"],
        "sourcePin": pin,
        "descriptorDigest": descriptor_digest,
        "contractRefs": sorted(
            descriptor.get("contracts", []),
            key=lambda item: (item["contractID"], item["version"], item["contentDigest"]),
        ),
        "artifactDigests": _artifact_digests(root),
        "localQualificationDigest": local_result["localQualificationDigest"],
    }


def assemble(
    manifest: dict[str, Any],
    *,
    roots: dict[str, Path],
    managed_root: Path,
    contract_root: Path,
    checker: ComponentChecker = kernel_component_check,
    run_commands: bool = True,
) -> dict[str, Any]:
    pins = sorted(manifest["components"], key=lambda item: item["componentID"])
    instances = [
        component_instance(
            pin,
            resolve_root(pin, roots, managed_root),
            contract_root,
            checker=checker,
            run_commands=run_commands,
        )
        for pin in pins
    ]
    evaluations = sorted(manifest.get("evaluations", []), key=lambda item: item["id"])
    if run_commands:
        for evaluation in evaluations:
            _run_command(evaluation["command"], Path.cwd())
    payload = {
        "schema": "federation-assembly/v0",
        "components": instances,
        "evaluations": evaluations,
        "qualified": True,
    }
    return {**payload, "assemblyID": domain_digest(ASSEMBLY_DOMAIN, canonical_json(payload))}


def _root_overrides(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        component_id, separator, raw_path = value.partition("=")
        if not separator or not component_id or not raw_path:
            raise FederationError(f"invalid root override: {value!r}")
        result[component_id] = Path(raw_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", action="append", default=[])
    parser.add_argument("--managed-root", type=Path, default=Path(".federation"))
    parser.add_argument("--contract-root", required=True, type=Path)
    parser.add_argument("--skip-commands", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        result = assemble(
            load_manifest(arguments.manifest),
            roots=_root_overrides(arguments.root),
            managed_root=arguments.managed_root,
            contract_root=arguments.contract_root.resolve(),
            run_commands=not arguments.skip_commands,
        )
    except (FederationError, KeyError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical_json(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
