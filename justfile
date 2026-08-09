default:
    @just --list

sync:
    uv sync --locked --all-packages --all-groups

lock:
    uv lock
    uv sync --locked --all-packages --all-groups

version package new:
    uv version --package {{package}} {{new}} --no-sync

tools-check:
    ./scripts/tools-check

test *args:
    uv run --frozen --no-sync pytest {{args}}

test-ppf *args:
    uv run --frozen --no-sync pytest packages/ppf/tests {{args}}

test-runtime *args:
    uv run --frozen --no-sync pytest packages/runtime/tests {{args}}

test-tdd *args:
    uv run --frozen --no-sync pytest agents/tdd/tests {{args}}

lint:
    uv run --frozen --no-sync ruff check .

format-check:
    uv run --frozen --no-sync ruff format --check .

typecheck:
    uv run --frozen --no-sync ty check packages/ppf/src packages/runtime/src agents/tdd/src scripts tools

cue-check:
    cue mod tidy --check
    cue vet ./...
    uv run --frozen --no-sync python scripts/cue_negative_check.py

policy-check:
    uv run --frozen --no-sync python scripts/repository_policy_check.py

federation-test:
    uv run --frozen --no-sync pytest tests/test_federation.py

federation-verify manifest="federation/manifest.example.cue" *args:
    uv run --frozen --no-sync python tools/federation.py {{manifest}} {{args}}

fix:
    uv run --frozen --no-sync ruff check --fix .
    uv run --frozen --no-sync ruff format .

build:
    uv build --package ppf --out-dir dist/packages/ppf
    uv build --package runtime-promptgen --out-dir dist/packages/runtime
    uv build --package tdd-agent-skills --out-dir dist/packages/tdd

build-package package:
    uv build --package {{package}} --out-dir dist/packages/{{package}}

check: lint format-check typecheck cue-check policy-check test

test-clean-locked *args:
    uv run --isolated --locked --all-packages --all-groups pytest {{args}}

test-clean *args:
    just test-clean-locked {{args}}

wheel-smoke:
    uv run --frozen --no-sync python scripts/wheel_smoke.py

migration-verify:
    uv run --isolated --no-project python tools/migration.py verify ops/migration/manifest.json

jj-init:
    uv run --isolated --no-project python tools/vcs/jj_init.py

review topic revset="@":
    uv run --isolated --no-project python tools/vcs/review.py {{quote(topic)}} {{quote(revset)}}

jj-smoke:
    uv run --isolated --no-project python tools/vcs/jj_smoke.py

qualify: check test-clean-locked build wheel-smoke

ops-qualify: migration-verify jj-smoke

[private]
ui:
    @command -v lazyjust >/dev/null 2>&1 || { echo "optional tool missing: lazyjust" >&2; exit 127; }
    @lazyjust {{ quote(justfile_directory()) }}
