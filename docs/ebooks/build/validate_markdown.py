#!/usr/bin/env python3
"""Validate code-fence and fenced-div balance without parsing headings in examples."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    fence: tuple[str, int, int] | None = None
    divs: list[int] = []
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fm = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            char, length, opened = fence
            if re.match(rf"^\s*{re.escape(char)}{{{length},}}\s*$", line):
                fence = None
            continue
        if fm:
            token = fm.group(1)
            fence = (token[0], len(token), no)
            continue
        if re.match(r"^\s*:::\s*\{", line):
            divs.append(no)
        elif re.match(r"^\s*:::\s*$", line):
            if divs:
                divs.pop()
            else:
                errors.append(f"line {no}: closing fenced div without opener")
    if fence:
        errors.append(f"line {fence[2]}: unclosed code fence")
    errors.extend(f"line {no}: unclosed fenced div" for no in divs)
    return errors


def main() -> int:
    failed = False
    for arg in sys.argv[1:]:
        path = Path(arg)
        errors = validate(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
