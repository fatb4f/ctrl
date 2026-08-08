from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parents[2]
CHANGE_ID = re.compile(r"^Change-Id: (I[0-9a-f]{40})$", re.MULTILINE)


def run(cwd: Path, *argv: str) -> str:
    result = subprocess.run(argv, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout.strip()


def trailer(cwd: Path, revision: str = "HEAD") -> str:
    message = run(cwd, "git", "show", "-s", "--format=%B", revision)
    match = CHANGE_ID.search(message)
    if match is None:
        raise SystemExit(f"exported commit has no Gerrit Change-Id trailer:\n{message}")
    return match.group(1)


def main() -> None:
    if shutil.which("jj") is None:
        raise SystemExit("jj is required for the Gerrit trailer smoke test")
    config = (ROOT / "tools/vcs/repo.toml").read_text()
    if "format_gerrit_change_id_trailer(self)" not in config:
        raise SystemExit("repository config does not enable Gerrit trailers")

    with tempfile.TemporaryDirectory(prefix="ctrl-jj-smoke-") as directory:
        base = Path(directory)
        repository = base / "work"
        repository.mkdir()
        run(repository, "git", "init", "-q", "-b", "main")
        run(repository, "git", "config", "user.name", "Smoke Test")
        run(repository, "git", "config", "user.email", "smoke@example.invalid")
        (repository / "base.txt").write_text("base\n")
        run(repository, "git", "add", "base.txt")
        run(repository, "git", "commit", "-qm", "base")
        run(base, "git", "clone", "-q", "--bare", str(repository), str(base / "gerrit.git"))
        run(repository, "git", "remote", "add", "gerrit", str(base / "gerrit.git"))
        run(repository, "jj", "git", "init", "--colocate")
        config_path = Path(run(repository, "jj", "config", "path", "--repo"))
        config_path.write_text(config)
        run(repository, "jj", "config", "set", "--repo", "user.name", "Smoke Test")
        run(repository, "jj", "config", "set", "--repo", "user.email", "smoke@example.invalid")
        run(repository, "jj", "git", "fetch", "--remote", "gerrit")
        run(repository, "jj", "new", "trunk()")
        (repository / "change.txt").write_text("one\n")
        run(repository, "jj", "describe", "-m", "first change")
        stable_change = run(repository, "jj", "log", "-r", "@", "--no-graph", "-T", "change_id")
        run(repository, "jj", "git", "export")
        first_commit = run(
            repository, "jj", "log", "-r", stable_change, "--no-graph", "-T", "commit_id"
        )
        first = trailer(repository, first_commit)
        (repository / "change.txt").write_text("two\n")
        run(repository, "jj", "describe", "-m", "amended change")
        run(repository, "jj", "git", "export")
        amended_commit = run(
            repository, "jj", "log", "-r", stable_change, "--no-graph", "-T", "commit_id"
        )
        amended = trailer(repository, amended_commit)
        if first != amended:
            raise SystemExit("Gerrit Change-Id changed across amend")
        run(repository, "jj", "new", "trunk()")
        (repository / "base-2.txt").write_text("new base\n")
        run(repository, "jj", "describe", "-m", "new base")
        run(repository, "jj", "rebase", "-s", stable_change, "-d", "@")
        run(repository, "jj", "git", "export")
        rebased_commit = run(
            repository, "jj", "log", "-r", stable_change, "--no-graph", "-T", "commit_id"
        )
        rebased_message = run(
            repository, "jj", "log", "-r", stable_change, "--no-graph", "-T", "description"
        )
        if "amended change" not in rebased_message:
            raise SystemExit("rebased jj change could not be resolved by stable change ID")
        if trailer(repository, rebased_commit) != amended:
            raise SystemExit("Gerrit Change-Id changed across rebase")
    print("jj Gerrit Change-Id smoke: pass")


if __name__ == "__main__":
    main()
