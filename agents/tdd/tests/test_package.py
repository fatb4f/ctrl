from __future__ import annotations

import tomllib
from importlib.metadata import version
from pathlib import Path

import tdd_agent_skills


def test_package_imports() -> None:
    pyproject = (Path(__file__).parents[1] / "pyproject.toml").read_text()
    project = tomllib.loads(pyproject)["project"]
    assert tdd_agent_skills.__doc__
    assert version("tdd-agent-skills") == project["version"]
