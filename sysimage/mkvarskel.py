#!/usr/bin/env python3
"""Create a minimal empty private/var directory skeleton for research."""
from __future__ import annotations
import argparse
from pathlib import Path

DIRECTORIES = (
    "private/var/db",
    "private/var/db/diagnostics",
    "private/var/log",
    "private/var/tmp",
    "private/var/run",
    "private/var/mobile",
    "private/var/mobile/Library",
    "private/var/root",
)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    root = args.destination.resolve()
    for relative in DIRECTORIES:
        directory = root / relative
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ".gitkeep").touch(exist_ok=True)
    print(f"created empty variable-data skeleton at {root}")
    print("no Apple data, accounts, keys, databases, or firmware were copied")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
