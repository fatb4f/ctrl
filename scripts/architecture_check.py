from __future__ import annotations

import json
import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]
LAYERS = ("core", "repository", "qualification", "controller")
ALLOWED_IMPORTS = {
    "core": set(),
    "repository": {"core"},
    "qualification": {"core", "repository", "qualification"},
    "controller": {"core", "repository", "qualification", "controller"},
}
IMPORT_LAYER = re.compile(
    r"github\.com/fatb4f/ctrl/spec/(core|repository|qualification|controller)"
)


def fail(message: str) -> None:
    raise SystemExit(message)


def components() -> dict[str, dict[str, str]]:
    completed = subprocess.run(
        ["cue", "export", "./control", "-e", "components"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        fail(f"cannot load component manifest:\n{completed.stderr}")
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        fail("component manifest must export an object")
    return value


def project(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))["project"]


def dependency_name(requirement: object) -> str:
    if not isinstance(requirement, str):
        return ""
    return re.split(r"[ @<>=!~\[]", requirement, maxsplit=1)[0].lower().replace("_", "-")


def forbidden_cue_imports(layer: str, content: str) -> set[str]:
    return set(IMPORT_LAYER.findall(content)) - ALLOWED_IMPORTS[layer]


def main() -> None:
    manifest = components()
    roots: dict[str, Path] = {}
    for component_id, item in manifest.items():
        root = ROOT / item["root"]
        if not root.is_dir():
            fail(f"component root does not exist: {component_id}: {item['root']}")
        roots[component_id] = root

    document = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    members = document["tool"]["uv"]["workspace"]["members"]
    for member in members:
        if not (ROOT / member / "pyproject.toml").is_file():
            fail(f"workspace member does not exist: {member}")

    owners: dict[str, str] = {}
    script_owners: dict[str, list[str]] = {}
    for component_id, root in roots.items():
        pyproject = root / "pyproject.toml"
        if not pyproject.is_file() or root == ROOT / "spec":
            continue
        metadata = project(pyproject)
        distribution = metadata["name"].lower().replace("_", "-")
        if distribution in owners:
            fail(f"distribution {distribution!r} has multiple owners")
        owners[distribution] = component_id
        for script in metadata.get("scripts", {}):
            script_owners.setdefault(script, []).append(component_id)

    if script_owners.get("python-ppf") != ["ppf"]:
        fail(f"python-ppf must belong only to PPF: {script_owners.get('python-ppf')}")

    ppf = project(ROOT / "packages/ppf/pyproject.toml")
    ppf_runtime = {dependency_name(item) for item in ppf.get("dependencies", [])}
    if "tdd-agent-skills" in ppf_runtime:
        fail("PPF has a forbidden runtime dependency on TDD")
    if "qualification-workflow" not in ppf_runtime:
        fail("PPF must consume qualification-workflow")
    tdd = project(ROOT / "agents/tdd/pyproject.toml")
    if "qualification-workflow" not in {
        dependency_name(item) for item in tdd.get("dependencies", [])
    }:
        fail("TDD must consume qualification-workflow")

    for layer in LAYERS:
        for path in (ROOT / "spec" / layer).rglob("*.cue"):
            for imported in forbidden_cue_imports(layer, path.read_text(encoding="utf-8")):
                fail(f"forbidden CUE edge: {layer} -> {imported}: {path.relative_to(ROOT)}")

    nested_git = [path for path in ROOT.rglob(".git") if path != ROOT / ".git"]
    if nested_git:
        fail(f"nested .git directories are forbidden: {nested_git}")
    locks = [path for path in ROOT.rglob("uv.lock") if ".venv" not in path.parts]
    if locks != [ROOT / "uv.lock"]:
        fail(f"exactly one root uv.lock is required: {locks}")

    provenance = ROOT / "spec/generated/qualification.provenance.json"
    try:
        generated = json.loads(provenance.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read generated transport provenance: {error}")
    if not generated.get("authoritativeInputs") or generated.get("role") != "transport-only":
        fail("generated qualification transports must identify authoritative inputs")

    print(
        json.dumps(
            {
                "components": sorted(manifest),
                "distributions": owners,
                "status": "pass",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
