from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def main() -> None:
    document = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = document["project"]
    groups = document["dependency-groups"]
    uv = document["tool"]["uv"]
    assertions = {
        "project.valid": project["name"] == "ctrl" and project["requires-python"] == ">=3.14,<3.15",
        "dependency-groups.valid": {"test", "quality", "dev"} <= set(groups),
        "license.valid": project["license"] in {"MIT", "Apache-2.0"}
        and (ROOT / "LICENSE").is_file(),
        "workspace-root.valid": uv["package"] is False
        and "build-system" not in document
        and isinstance(uv["workspace"]["members"], list),
    }
    print(json.dumps({"probe": "metadata", "assertions": assertions}, sort_keys=True))


if __name__ == "__main__":
    main()
