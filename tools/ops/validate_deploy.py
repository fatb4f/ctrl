from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DIGEST = re.compile(r"^[^\s@]+@sha256:[0-9a-f]{64}$")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("lock", type=Path)
    parser.add_argument("--require-ready", action="store_true")
    arguments = parser.parse_args()
    data = json.loads(arguments.lock.read_text())
    invalid = [
        name
        for name, image in data.get("images", {}).items()
        if not isinstance(image.get("reference"), str)
        or DIGEST.fullmatch(image["reference"]) is None
    ]
    plugins = data.get("gerritPlugins")
    if not isinstance(plugins, dict):
        raise SystemExit("gerritPlugins must be an object")
    invalid_plugins = [
        name for name, reference in plugins.items() if DIGEST.fullmatch(reference) is None
    ]
    if arguments.require_ready and (
        invalid or invalid_plugins or data.get("cutoverReady") is not True
    ):
        raise SystemExit(
            "deployment lock is not cutover-ready; unresolved images/plugins: "
            + ", ".join([*invalid, *invalid_plugins])
        )
    state = "ready" if not invalid and not invalid_plugins else "prepared"
    print(f"deployment lock: pass ({state})")


if __name__ == "__main__":
    main()
