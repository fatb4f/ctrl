default:
    @just --list

sync:
    uv sync --locked --group dev

lock:
    uv lock --upgrade
    uv sync --group dev

version new:
    uv version {{new}} --no-sync

tools-check:
    ./scripts/tools-check

test *args:
    uv run --frozen --no-sync pytest {{args}}

lint:
    uv run --frozen --no-sync ruff check .

format-check:
    uv run --frozen --no-sync ruff format --check .

typecheck:
    uv run --frozen --no-sync ty check src tests scripts

fix:
    uv run --frozen --no-sync ruff check --fix .
    uv run --frozen --no-sync ruff format .

build:
    rm -rf dist
    uv build

check: lint format-check typecheck test

test-clean-locked *args:
    uv run --isolated --locked --no-default-groups --group test pytest {{args}}

test-clean *args:
    just test-clean-locked {{args}}

package-check:
    uv run --isolated --locked --no-default-groups --group test python scripts/package_check.py dist sdk_feedback

package-check-online:
    uv run --isolated --locked --no-default-groups --group test python scripts/package_check.py --online dist sdk_feedback

standards-check:
    uv run --isolated --no-project python scripts/standards_check.py

qualify: check test-clean-locked build standards-check

[private]
ui:
    @command -v lazyjust >/dev/null 2>&1 || { echo "optional tool missing: lazyjust" >&2; exit 127; }
    @lazyjust {{ quote(justfile_directory()) }}
