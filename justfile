default:
    @just --list

sync:
    uv sync --locked --all-packages --all-groups

lock:
    uv lock --upgrade
    uv sync --all-packages --all-groups

tools-check:
    ./scripts/tools-check

lint:
    uv run --frozen --no-sync ruff check scripts tests packages/ppf/src packages/ppf/tests packages/runtime/src packages/runtime/tests packages/qualification-workflow/src packages/qualification-workflow/tests agents/tdd/src agents/tdd/tests

format-check:
    uv run --frozen --no-sync ruff format --check scripts tests packages/ppf/src packages/ppf/tests packages/runtime/src packages/runtime/tests packages/qualification-workflow/src packages/qualification-workflow/tests agents/tdd/src agents/tdd/tests

typecheck:
    uv run --frozen --no-sync ty check scripts tests packages/ppf/src packages/runtime/src packages/qualification-workflow/src agents/tdd/src

fix:
    uv run --frozen --no-sync ruff check --fix scripts tests packages/ppf/src packages/ppf/tests packages/runtime/src packages/runtime/tests packages/qualification-workflow/src packages/qualification-workflow/tests agents/tdd/src agents/tdd/tests
    uv run --frozen --no-sync ruff format scripts tests packages/ppf/src packages/ppf/tests packages/runtime/src packages/runtime/tests packages/qualification-workflow/src packages/qualification-workflow/tests agents/tdd/src agents/tdd/tests

test *args:
    uv run --frozen --no-sync pytest tests {{args}}
    uv run --frozen --no-sync python scripts/component_check.py qualification-workflow ppf runtime-promptgen tdd-agent-skills openai-sdk-feedback

cue-check:
    cue vet -c=false ./spec/core ./spec/repository ./spec/qualification ./spec/controller ./spec/examples/... ./spec/profiles/... ./spec/tests/positive ./agents/tdd/contracts ./agents/tdd/fixtures/...
    cue export ./spec/qualification/workflow/examples/normalized_sequence.cue -e normalizedPlan >/dev/null
    @if cue vet -c=false ./spec/tests/negative/incomplete-promotion.cue >/dev/null 2>&1; then echo "negative CUE fixture unexpectedly passed" >&2; exit 1; else echo "negative CUE fixture rejected as expected"; fi

generated-check:
    uv run --frozen --no-sync python scripts/generate_qualification_transports.py --check

architecture-check:
    uv run --frozen --no-sync python scripts/architecture_check.py

links-check:
    uv run --frozen --no-sync python scripts/markdown_links.py

standards-check:
    uv run --isolated --no-project python scripts/standards_check.py

check: lint format-check typecheck test cue-check generated-check architecture-check links-check standards-check

test-clean-locked *args:
    uv run --isolated --locked --all-packages --all-groups pytest tests {{args}}
    uv run --isolated --locked --all-packages --all-groups pytest packages/qualification-workflow/tests {{args}}
    uv run --isolated --locked --all-packages --all-groups pytest packages/ppf/tests packages/ppf/.codex/skills/python-policy-ppf/tests {{args}}
    uv run --isolated --locked --all-packages --all-groups pytest packages/runtime/tests {{args}}
    uv run --isolated --locked --all-packages --all-groups pytest agents/tdd/tests {{args}}

test-clean *args:
    just test-clean-locked {{args}}

build:
    uv build --all-packages --out-dir dist --clear

wheel-smoke: build
    uv run --frozen --no-sync python scripts/wheel_smoke.py

evaluations:
    uv run --frozen --no-sync python-ppf workflow compile agents/tdd/docs/workflow-plan-example.md --fixtures agents/tdd/fixtures/manifest.cue --probes agents/tdd/fixtures/probes.cue --realizations agents/tdd/fixtures/realization-specs.cue --check agents/tdd/generated/workflow/example.json

qualify: check test-clean-locked build wheel-smoke evaluations

component-check component:
    uv run --frozen --no-sync python scripts/component_check.py {{component}}

[private]
ui:
    @command -v lazyjust >/dev/null 2>&1 || { echo "optional tool missing: lazyjust" >&2; exit 127; }
    @lazyjust {{ quote(justfile_directory()) }}
