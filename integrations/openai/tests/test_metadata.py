from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_project_metadata() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert project["name"] == "sdk-feedback"
    assert project["requires-python"] == ">=3.14"
    assert project["license"] == "MIT"


def test_dependency_groups() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert {"test", "quality", "dev"} <= set(data["dependency-groups"])
