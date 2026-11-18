#!/usr/bin/env python3
"""Emit a /private/var directory/symlink manifest from a 7z -slt listing.

Output is tab-separated:
  d<TAB>mode-octal<TAB>uid<TAB>gid<TAB>/absolute/path
  l<TAB>target<TAB>/absolute/path

Only metadata present in the supplied listing is used. No ownership or mode
values are guessed, and no host directories or Apple data are created.
"""
from __future__ import annotations

import argparse
import stat
import sys
from pathlib import Path

from slt_parser import entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("listing", type=Path, help="text produced by: 7z l -slt IMAGE")
    parser.add_argument("--output", type=Path, help="write manifest here (default: stdout)")
    args = parser.parse_args()
    if not args.listing.is_file():
        parser.error(f"listing file does not exist: {args.listing}")

    selected = []
    for item in entries(str(args.listing)):
        path = item["path"]
        if path != "private/var" and not path.startswith("private/var/"):
            continue
        mode = item["mode"]
        absolute = "/" + path
        if stat.S_ISDIR(mode):
            line = f"d\\t{item['mode_octal']}\\t{item['uid']}\\t{item['gid']}\\t{absolute}"
            selected.append((path, line))
        elif stat.S_ISLNK(mode):
            line = f"l\\t{item['symlink_target']}\\t{absolute}"
            selected.append((path, line))

    selected.sort(key=lambda row: row[0])
    output = args.output.open("w", encoding="utf-8") if args.output else sys.stdout
    try:
        for _path, line in selected:
            output.write(line + "\\n")
    finally:
        if args.output:
            output.close()
    print(f"wrote {len(selected)} /private/var directory and symlink records", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
