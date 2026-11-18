#!/usr/bin/env python3
"""Index filesystem metadata from a 7-Zip technical listing; does not extract files."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from listing import entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("listing", type=Path, help="text produced by: 7z l -slt IMAGE")
    parser.add_argument("--prefix", help="include only paths under this relative prefix")
    parser.add_argument("--output", type=Path, help="write JSON Lines here (default: stdout)")
    args = parser.parse_args()
    if not args.listing.is_file():
        parser.error(f"listing file does not exist: {args.listing}")

    prefix = args.prefix.strip("/") if args.prefix else None
    count = total_bytes = 0
    output = args.output.open("w", encoding="utf-8") if args.output else sys.stdout
    try:
        for item in entries(str(args.listing)):
            if prefix and item["path"] != prefix and not item["path"].startswith(prefix + "/"):
                continue
            output.write(json.dumps(item, sort_keys=True) + "\n")
            count += 1
            total_bytes += item["size"]
    except OSError as exc:
        print(f"rootfs-index: {exc}", file=sys.stderr)
        return 1
    finally:
        if args.output:
            output.close()
    print(f"indexed {count} entries; {total_bytes} bytes of listed file data", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
