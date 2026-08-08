from __future__ import annotations

import configparser
import os
import subprocess
import sysconfig
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).parents[1]
IMPORTS = ("ppf", "runtime_promptgen", "tdd_agent_skills")
COMMANDS = ("ppf-validate", "ppf-assess", "ppf-qualify", "python-ppf", "promptgen")


def run(argv: list[str], *, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(argv, cwd=ROOT, env=env, check=False, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(f"command failed: {' '.join(argv)}\n{result.stdout}{result.stderr}")


def wheel_entry_points(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as archive:
        names = [
            name for name in archive.namelist() if name.endswith(".dist-info/entry_points.txt")
        ]
        if not names:
            return {}
        if len(names) != 1:
            raise SystemExit(f"multiple entry-point files in {path}")
        parser = configparser.ConfigParser()
        parser.read_string(archive.read(names[0]).decode())
        return dict(parser["console_scripts"]) if parser.has_section("console_scripts") else {}


def main() -> None:
    wheels = sorted((ROOT / "dist/packages").glob("*/*.whl"))
    if len(wheels) != 3:
        raise SystemExit(f"expected three workspace wheels, found {len(wheels)}")
    scripts: dict[str, str] = {}
    for wheel in wheels:
        for name, target in wheel_entry_points(wheel).items():
            if name in scripts:
                raise SystemExit(f"duplicate installed console script: {name}")
            scripts[name] = target
    if set(scripts) != set(COMMANDS):
        raise SystemExit(f"unexpected installed console scripts: {sorted(scripts)}")
    if sum(name == "python-ppf" for name in scripts) != 1:
        raise SystemExit("python-ppf must have exactly one owner")

    with tempfile.TemporaryDirectory(prefix="ctrl-wheel-smoke-") as directory:
        environment = {**os.environ, "UV_PROJECT_ENVIRONMENT": str(Path(directory) / "venv")}
        run(
            ["uv", "venv", "--python", "3.14", environment["UV_PROJECT_ENVIRONMENT"]],
            env=environment,
        )
        python = str(Path(environment["UV_PROJECT_ENVIRONMENT"]) / "bin/python")
        run(
            [
                "uv",
                "pip",
                "install",
                "--offline",
                "--no-deps",
                "--python",
                python,
                *map(str, wheels),
            ],
            env=environment,
        )
        # Dependencies come from the already verified locked workspace. The
        # candidate projects themselves come only from the installed wheels.
        environment["PYTHONPATH"] = sysconfig.get_paths()["purelib"]
        run([python, "-c", "; ".join(f"import {name}" for name in IMPORTS)], env=environment)
        binary = Path(environment["UV_PROJECT_ENVIRONMENT"]) / "bin"
        for command in COMMANDS:
            if not (binary / command).is_file():
                raise SystemExit(f"installed command is missing: {command}")
        run([str(binary / "python-ppf"), "workflow", "--help"], env=environment)
    print("installed wheel smoke: pass")


if __name__ == "__main__":
    main()
