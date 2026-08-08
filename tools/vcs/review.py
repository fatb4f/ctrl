from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
TOPIC = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def run(*argv: str) -> str:
    result = subprocess.run(argv, cwd=ROOT, check=False, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout.strip()


def lines(revset: str) -> list[str]:
    output = run("jj", "log", "-r", revset, "--no-graph", "-T", 'commit_id ++ "\\n"')
    return [line for line in output.splitlines() if line]


def validate_stack(revset: str) -> str:
    commits = lines(revset)
    if not commits:
        raise SystemExit("review revset is empty")
    if lines(f"({revset}) & (merges() | empty() | immutable())"):
        raise SystemExit("review stack contains a merge, empty, or immutable commit")
    heads = lines(f"heads({revset})")
    roots = lines(f"roots({revset})")
    if len(heads) != 1 or len(roots) != 1:
        raise SystemExit("review revset must form one linear stack")
    if len(lines(f"({revset}) & ~ancestors({heads[0]})")) != 0:
        raise SystemExit("review revset contains a commit outside the stack tip ancestry")
    return heads[0]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: review.py TOPIC REVSET")
    topic, revset = sys.argv[1:]
    if TOPIC.fullmatch(topic) is None:
        raise SystemExit("topic must contain only letters, digits, dot, underscore, and hyphen")
    if shutil.which("jj") is None:
        raise SystemExit("jj is required")
    if not (ROOT / ".jj").is_dir():
        raise SystemExit("run just jj-init before review")
    run("jj", "git", "fetch", "--remote", "gerrit")
    tip = validate_stack(revset)
    run("just", "check")
    run("jj", "git", "export")
    run("git", "push", "gerrit", f"{tip}:refs/for/main%topic={topic}")
    print(f"review stack pushed: {tip} (topic {topic})")


if __name__ == "__main__":
    main()
