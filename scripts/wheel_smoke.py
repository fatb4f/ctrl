from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parents[1]
EXPECTED_IMPORTS = ("ppf", "runtime_promptgen", "tdd_agent_skills", "qualification_workflow")
EXPECTED_COMMANDS = ("ppf-validate", "ppf-assess", "ppf-qualify", "python-ppf", "promptgen")


def run(*argv: str) -> None:
    completed = subprocess.run(argv, cwd=ROOT, check=False, text=True, capture_output=True)
    if completed.returncode:
        raise SystemExit(f"command failed: {' '.join(argv)}\n{completed.stdout}{completed.stderr}")


def main() -> None:
    wheels = sorted((ROOT / "dist").glob("*.whl"))
    if len(wheels) != 4:
        raise SystemExit(f"expected four workspace wheels, found {len(wheels)}")
    with tempfile.TemporaryDirectory(prefix="ctrl-wheel-smoke-") as temporary:
        temporary_root = Path(temporary)
        environment = temporary_root / "venv"
        requirements = temporary_root / "requirements.txt"
        run(
            "uv",
            "export",
            "--frozen",
            "--all-packages",
            "--all-groups",
            "--no-emit-workspace",
            "--no-hashes",
            "--output-file",
            str(requirements),
        )
        run("uv", "venv", "--python", "3.14", str(environment))
        python = environment / "bin" / "python"
        run(
            "uv",
            "pip",
            "install",
            "--python",
            str(python),
            "--requirements",
            str(requirements),
        )
        run(
            "uv",
            "pip",
            "install",
            "--offline",
            "--no-deps",
            "--python",
            str(python),
            *(str(wheel) for wheel in wheels),
        )
        probe = (
            "imports = "
            + repr(EXPECTED_IMPORTS)
            + "\ncommands = "
            + repr(EXPECTED_COMMANDS)
            + "\n"
            + """
import importlib
import importlib.metadata
import subprocess
import sysconfig
from pathlib import Path

for name in imports:
    importlib.import_module(name)
entries = importlib.metadata.entry_points(group="console_scripts")
for command in commands:
    matches = [entry for entry in entries if entry.name == command]
    if len(matches) != 1:
        raise SystemExit(f"expected one {command} owner, found {matches}")
    completed = subprocess.run(
        [str(Path(sysconfig.get_path("scripts")) / command), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise SystemExit(f"{command} --help failed: {completed.stdout}{completed.stderr}")
"""
        )
        run(str(python), "-c", probe)
    print("wheel smoke passed")


if __name__ == "__main__":
    main()
