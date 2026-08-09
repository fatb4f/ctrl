from __future__ import annotations

from pathlib import Path

import pytest
import runtime_promptgen.cli as cli_module
from runtime_promptgen.cli import main


def test_cli_preserves_option_surface(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    handoff = tmp_path / "handoff.json"
    output = tmp_path / "prompt.json"

    def fake_compose(**values):
        assert values == {
            "slice_repository": "fatb4f/runtime",
            "slice_issue": 7,
            "handoff_path": handoff,
            "output_path": output,
        }
        return output.resolve()

    monkeypatch.setattr(cli_module, "compose_prompt", fake_compose)
    assert (
        main(
            [
                "--slice-repo",
                "fatb4f/runtime",
                "--slice-issue",
                "7",
                "--handoff-file",
                str(handoff),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out.strip() == str(output.resolve())


def test_cli_parse_failures_return_two(capsys) -> None:
    assert main([]) == 2
    captured = capsys.readouterr()
    assert "promptgen failed:" in captured.err


def test_cli_requires_exactly_one_handoff_selector(capsys) -> None:
    assert (
        main(
            [
                "--slice-repo",
                "fatb4f/runtime",
                "--slice-issue",
                "7",
            ]
        )
        == 2
    )
    assert "exactly one" in capsys.readouterr().err
