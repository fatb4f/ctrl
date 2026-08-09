from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_project_metadata() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert project["name"] == "ctrl"
    assert project["requires-python"] == ">=3.14,<3.15"
    assert project["license"] == "MIT"


def test_root_is_a_non_package_workspace() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert "build-system" not in data
    assert data["tool"]["uv"]["package"] is False
    assert isinstance(data["tool"]["uv"]["workspace"]["members"], list)


def test_dependency_groups() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert {"test", "quality", "dev"} <= set(data["dependency-groups"])
