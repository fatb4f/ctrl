from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from tools.federation import FederationError, assemble, canonical_json, domain_digest


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _repository(root: Path, component_id: str) -> dict[str, Any]:
    (root / "architecture").mkdir(parents=True)
    (root / "cue.mod").mkdir()
    (root / "cue.mod/module.cue").write_text(
        f'module: "example.invalid/{component_id}"\nlanguage: version: "v0.18.0"\n'
    )
    (root / "architecture/component.cue").write_text(
        "package architecture\n\n"
        "descriptor: {\n"
        '\tschema: "component-descriptor/v0"\n'
        f'\tcomponentID: "{component_id}"\n'
        "\tpackages: []\n"
        '\tcommands: {check: ["true"], qualify: ["true"], build: ["true"]}\n'
        "\tcontracts: []\n"
        "\tdependencies: []\n"
        "}\n"
    )
    (root / "architecture/observed-dependencies.json").write_text('{"observations":[]}\n')
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    _git(root, "add", ".")
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Federation Test",
            "-c",
            "user.email=federation-test@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "fixture",
        ],
        check=True,
    )
    return {
        "componentID": component_id,
        "repositoryID": component_id,
        "url": f"https://example.invalid/{component_id}.git",
        "revision": _git(root, "rev-parse", "HEAD"),
    }


def _checker(
    root: Path, descriptor_path: Path, observations_path: Path, contract_root: Path
) -> dict[str, Any]:
    del root, observations_path, contract_root
    exported = json.loads(
        subprocess.run(
            ["cue", "export", str(descriptor_path), "--out", "json"],
            check=True,
            capture_output=True,
        ).stdout
    )["descriptor"]
    descriptor_digest = domain_digest(b"fatb4f.component-descriptor.v0\0", canonical_json(exported))
    return {
        "qualified": True,
        "descriptorDigest": descriptor_digest,
        "localQualificationDigest": "sha256:" + "1" * 64,
    }


def _assemble(root: Path, pin: dict[str, Any]) -> dict[str, Any]:
    return assemble(
        {"schema": "federation-manifest/v0", "components": [pin], "evaluations": []},
        roots={pin["componentID"]: root},
        managed_root=root.parent / "managed",
        contract_root=root,
        checker=_checker,
        run_commands=False,
    )


def test_dirty_descriptor_rejects_but_unrelated_dirty_file_is_allowed(tmp_path: Path) -> None:
    root = tmp_path / "component"
    pin = _repository(root, "component-a")
    first = _assemble(root, pin)
    (root / "notes.txt").write_text("unrelated dirty work\n")
    assert _assemble(root, pin)["assemblyID"] == first["assemblyID"]
    descriptor = root / "architecture/component.cue"
    descriptor.write_text(descriptor.read_text() + "\n// dirty\n")
    with pytest.raises(FederationError, match="descriptor is dirty"):
        _assemble(root, pin)


def test_descriptor_digest_and_revision_bind_component_instance(tmp_path: Path) -> None:
    root = tmp_path / "component"
    pin = _repository(root, "component-a")
    first = _assemble(root, pin)
    descriptor = root / "architecture/component.cue"
    descriptor.write_text(
        descriptor.read_text().replace(
            "packages: []", 'packages: [{kind: "command", name: "example"}]'
        )
    )
    _git(root, "add", "architecture/component.cue")
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Federation Test",
            "-c",
            "user.email=federation-test@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "descriptor change",
        ],
        check=True,
    )
    pin = {**pin, "revision": _git(root, "rev-parse", "HEAD")}
    second = _assemble(root, pin)
    assert first["components"][0]["descriptorDigest"] != second["components"][0]["descriptorDigest"]
    assert first["assemblyID"] != second["assemblyID"]
