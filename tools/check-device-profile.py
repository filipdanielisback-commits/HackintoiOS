#!/usr/bin/env python3
"""Validate the documented Moto G60 target profile; this does not build a kernel."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "devices/moto-g60-xt2135-2/README.md"

REQUIRED = (
    "# Moto G60",
    "XT2135-2",
    "research scaffold only",
    "SM7150-AC",
    "Not yet verified",
    "There is no HackintoiOS kernel implementation",
)

def main() -> int:
    if not PROFILE.is_file():
        print(f"ERROR: missing device profile: {PROFILE.relative_to(ROOT)}")
        return 1

    content = PROFILE.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED if item not in content]
    if missing:
        for item in missing:
            print(f"ERROR: device profile is missing required marker: {item!r}")
        return 1

    print("Moto G60 device profile check passed.")
    print("Note: this validates documentation only; it does not build or test a kernel.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
