from __future__ import annotations

from scripts.architecture_check import dependency_name, forbidden_cue_imports


def test_qualification_to_controller_mutation_is_rejected() -> None:
    mutation = 'import "github.com/fatb4f/ctrl/spec/controller"'
    assert forbidden_cue_imports("qualification", mutation) == {"controller"}


def test_declared_downstream_controller_edge_is_allowed() -> None:
    content = 'import "github.com/fatb4f/ctrl/spec/qualification"'
    assert forbidden_cue_imports("controller", content) == set()


def test_runtime_dependency_names_are_normalized() -> None:
    assert dependency_name("tdd_agent_skills>=1") == "tdd-agent-skills"
