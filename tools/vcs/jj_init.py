from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[2]
VERSION = re.compile(r"^jj 0\.43\.([0-9]+)")


def run(*argv: str) -> str:
    result = subprocess.run(argv, cwd=ROOT, check=False, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr.strip() or f"command failed: {' '.join(argv)}")
    return result.stdout.strip()


def require_supported_jj() -> None:
    executable = shutil.which("jj")
    if executable is None:
        raise SystemExit("jj is required (supported: >=0.43.0,<0.44.0)")
    version = run(executable, "--version")
    if VERSION.match(version) is None:
        raise SystemExit(f"unsupported jj version: {version} (supported: >=0.43.0,<0.44.0)")


def main() -> None:
    require_supported_jj()
    if not (ROOT / ".jj").exists():
        run("jj", "git", "init", "--colocate")
    name = run("jj", "config", "get", "user.name")
    email = run("jj", "config", "get", "user.email")
    if not name or not email:
        raise SystemExit("configure non-empty jj user.name and user.email before bootstrap")

    for remote in ("gerrit", "github"):
        url = run("git", "remote", "get-url", remote)
        if not url:
            raise SystemExit(f"Git remote {remote!r} has an empty URL")
    if run("git", "remote", "get-url", "gerrit") == run("git", "remote", "get-url", "github"):
        raise SystemExit("gerrit and github remotes must be distinct")

    config_path = Path(run("jj", "config", "path", "--repo"))
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text((ROOT / "tools/vcs/repo.toml").read_text(), encoding="utf-8")
    if run("jj", "log", "-r", "trunk()", "--no-graph", "-T", "commit_id") == "":
        raise SystemExit("trunk() did not resolve to main@gerrit")
    print(f"jj repository configuration installed: {config_path}")


if __name__ == "__main__":
    main()
