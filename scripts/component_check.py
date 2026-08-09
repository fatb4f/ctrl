from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
PYTEST = [sys.executable, "-m", "pytest", "-q"]
COMMANDS = {
    "qualification-spec": [
        [
            "cue",
            "vet",
            "-c=false",
            "./spec/core",
            "./spec/repository",
            "./spec/qualification",
            "./spec/controller",
            "./spec/examples/...",
            "./spec/profiles/...",
            "./spec/tests/positive",
        ]
    ],
    "qualification-workflow": [PYTEST + ["packages/qualification-workflow/tests"]],
    "ppf": [
        PYTEST
        + [
            "packages/ppf/tests",
            "packages/ppf/.codex/skills/python-policy-ppf/tests",
        ]
    ],
    "runtime-promptgen": [PYTEST + ["packages/runtime/tests"]],
    "tdd-agent-skills": [PYTEST + ["agents/tdd/tests"]],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("components", nargs="*", choices=sorted(COMMANDS))
    arguments = parser.parse_args()
    selected = arguments.components or list(COMMANDS)
    results: list[dict[str, object]] = []
    for component in selected:
        for command in COMMANDS[component]:
            completed = subprocess.run(command, cwd=ROOT, check=False)
            results.append(
                {"component": component, "argv": command, "returncode": completed.returncode}
            )
            if completed.returncode:
                print(json.dumps({"results": results, "status": "fail"}, sort_keys=True))
                raise SystemExit(completed.returncode)
    print(json.dumps({"results": results, "status": "pass"}, sort_keys=True))


if __name__ == "__main__":
    main()
