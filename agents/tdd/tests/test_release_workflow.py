from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_publish_workflow_is_conditional() -> None:
    workflow = ROOT / ".github" / "workflows" / "publish.yml"

    assert not workflow.exists()
