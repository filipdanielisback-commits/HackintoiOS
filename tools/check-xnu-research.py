#!/usr/bin/env python3
"""Validate HackintoiOS XNU research docs; this does not build XNU."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = {
    "docs/xnu/README.md": [
        "research and documentation only",
        "not an iOS 18 source tree",
        "Darwin 24",
        "Apple XNU source repository",
        "not XNU",
    ],
    "docs/xnu/compatibility.md": [
        "preliminary research matrix",
        "Unknown",
        "Wi-Fi",
        "does not establish",
    ],
}

errors = []
for relative, phrases in required.items():
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"Missing required file: {relative}")
        continue
    content = path.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase.casefold() not in content.casefold():
            errors.append(f"{relative}: missing required phrase: {phrase}")

if errors:
    print("XNU research documentation check failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("XNU research documentation check passed.")
print("Note: this validates documentation only; it does not compile XNU or Darwin.")
