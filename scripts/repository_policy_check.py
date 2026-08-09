from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]
PACKAGES = {
    "packages/ppf": ("ppf", "0.4.0"),
    "packages/runtime": ("runtime-promptgen", "0.1.1"),
    "agents/tdd": ("tdd-agent-skills", "0.2.0"),
}
EXPECTED_SCRIPTS = {
    "ppf-validate": "ppf.cli:main",
    "ppf-assess": "ppf.assess_cli:main",
    "ppf-qualify": "ppf.qualify_cli:main",
    "python-ppf": "ppf.workflow_cli:main",
    "promptgen": "runtime_promptgen.cli:main",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    root = tomllib.loads((ROOT / "pyproject.toml").read_text())
    if root.get("tool", {}).get("uv", {}).get("package") is not False:
        fail("the workspace root must be a non-package uv project")
    members = set(root["tool"]["uv"]["workspace"]["members"])
    if members != set(PACKAGES):
        fail(f"unexpected uv workspace members: {sorted(members)}")

    scripts: dict[str, str] = {}
    for path, (name, version) in PACKAGES.items():
        project = tomllib.loads((ROOT / path / "pyproject.toml").read_text())["project"]
        if project["name"] != name or project["version"] != version:
            fail(f"unexpected identity for {path}")
        if project["requires-python"] != ">=3.14,<3.15":
            fail(f"unexpected Python range for {path}")
        for command, target in project.get("scripts", {}).items():
            if command in scripts:
                fail(f"duplicate console script: {command}")
            scripts[command] = target
    if scripts != EXPECTED_SCRIPTS:
        fail(f"unexpected console scripts: {scripts}")

    cue_module = (ROOT / "cue.mod/module.cue").read_text()
    if 'module: "github.com/fatb4f/ctrl"' not in cue_module:
        fail("unexpected root CUE module")
    if 'language: version: "v0.18.0"' not in cue_module:
        fail("unexpected CUE language version")

    if ".federation/" not in (ROOT / ".gitignore").read_text().splitlines():
        fail("managed federation checkouts must be ignored")

    migration = json.loads((ROOT / "ops/migration/manifest.json").read_text())
    if migration.get("cutoverReady") is not False:
        fail("S0 requires migration cutoverReady to remain false")

    old_imports = []
    for path in [
        *ROOT.glob("spec/**/*.cue"),
        *ROOT.glob("agents/tdd/**/*.cue"),
        *ROOT.glob("fixtures/**/*.cue"),
    ]:
        if (
            "github.com/fatb4f/kernel-spec" in path.read_text()
            or "github.com/fatb4f/tdd-agent-skills" in path.read_text()
        ):
            old_imports.append(path.relative_to(ROOT).as_posix())
    if old_imports:
        fail(f"legacy CUE imports remain: {old_imports}")
    if (ROOT / ".jj").exists():
        fail("machine-local .jj directory must not be committed or packaged")

    required = [
        "docs/s0-semantic-consolidation-plan.md",
        "federation/manifest.example.cue",
        "tools/federation.py",
        "ops/gerrit/project.config",
        "ops/gerrit/replication.config",
        "ops/zuul/tenant.yaml",
        "tools/vcs/repo.toml",
        "zuul.d/jobs.yaml",
        "zuul.d/projects.yaml",
        "ops/migration/manifest.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        fail(f"required repository controls are missing: {missing}")

    contaminated = []
    legacy_namespace = "fatba" + "4f"
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv", "dist"} for part in path.parts):
            continue
        try:
            if legacy_namespace in path.read_text():
                contaminated.append(path.relative_to(ROOT).as_posix())
        except UnicodeDecodeError:
            continue
    if contaminated:
        fail(f"legacy namespace remains: {contaminated}")

    print("repository policy: pass")


if __name__ == "__main__":
    main()
