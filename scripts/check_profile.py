#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_LINK_RE = re.compile(r"\[[^\]]+\]\(([^):#][^):]*\.md)(#[^)]+)?\)")
PHONE_RE = re.compile(r"(?<!\d)(?:\+33|0)[ .-]?[1-9](?:[ .-]?\d{2}){4}(?!\d)")


def fail(message: str) -> None:
    print(f"check_profile: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    markdown_files = sorted(ROOT.glob("**/*.md"))
    if not markdown_files:
        fail("no Markdown files found")

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        if PHONE_RE.search(text):
            fail(f"possible phone number found in {path.relative_to(ROOT)}")

        for match in LOCAL_LINK_RE.finditer(text):
            target = (path.parent / match.group(1)).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                fail(f"local link escapes repository in {path.relative_to(ROOT)}: {match.group(1)}")
            if not target.exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {match.group(1)}")

    print(f"check_profile: ok ({len(markdown_files)} Markdown files)")


if __name__ == "__main__":
    main()
