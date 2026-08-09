from __future__ import annotations

import tomllib
from importlib.metadata import version
from pathlib import Path

import sdk_feedback


def test_package_imports() -> None:
    pyproject = (Path(__file__).parents[1] / "pyproject.toml").read_text()
    project = tomllib.loads(pyproject)["project"]
    assert sdk_feedback.__doc__
    assert version("sdk-feedback") == project["version"]
