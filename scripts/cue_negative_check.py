from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "fixtures/cue-negative/manifest.json"


def main() -> None:
    cases = json.loads(MANIFEST.read_text())
    for case in cases:
        result = subprocess.run(
            case["argv"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            raise SystemExit(f"negative CUE fixture unexpectedly passed: {case['id']}")
        if case["errorContains"] not in result.stderr:
            raise SystemExit(
                f"negative CUE fixture failed for the wrong reason: {case['id']}\n{result.stderr}"
            )
        print(f"negative CUE fixture: pass: {case['id']}")


if __name__ == "__main__":
    main()
