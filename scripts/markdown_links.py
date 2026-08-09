from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+['\"].*?['\"])?\)")
EXCLUDED_PARTS = {".codex", ".git", ".venv", "dist"}


def main() -> None:
    failures: list[str] = []
    paths = sorted(
        path
        for path in ROOT.rglob("*.md")
        if not EXCLUDED_PARTS.intersection(path.relative_to(ROOT).parts)
    )
    for document in paths:
        for match in LINK.finditer(document.read_text(encoding="utf-8")):
            raw = match.group("target").strip("<>")
            parsed = urlsplit(raw)
            if parsed.scheme or parsed.netloc or raw.startswith("#"):
                continue
            local = unquote(parsed.path)
            if not local or any(character in local for character in "{}*"):
                continue
            target = ROOT / local.lstrip("/") if local.startswith("/") else document.parent / local
            if not target.exists():
                failures.append(f"{document.relative_to(ROOT)}: broken local link {raw!r}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"checked {len(paths)} Markdown files")


if __name__ == "__main__":
    main()
