#!/usr/bin/env python3
"""List or extract a named member from an IPSW ZIP archive."""
from __future__ import annotations
import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath

def safe_member_name(name: str) -> str:
    member = PurePosixPath(name)
    if member.is_absolute() or ".." in member.parts or not member.parts:
        raise ValueError(f"unsafe archive member path: {name!r}")
    return str(member)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="list archive members")
    listing.add_argument("ipsw", type=Path)
    listing.add_argument("--prefix")
    extraction = sub.add_parser("extract", help="extract one named member")
    extraction.add_argument("ipsw", type=Path)
    extraction.add_argument("member")
    extraction.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.ipsw.is_file():
        parser.error(f"IPSW file does not exist: {args.ipsw}")
    try:
        with zipfile.ZipFile(args.ipsw) as archive:
            if args.command == "list":
                for info in archive.infolist():
                    if args.prefix is None or info.filename.startswith(args.prefix):
                        print(f"{info.file_size:>12}  {info.filename}")
                return 0
            member = safe_member_name(args.member)
            try:
                info = archive.getinfo(member)
            except KeyError:
                print(f"error: member not found: {member}", file=sys.stderr)
                return 2
            if info.is_dir():
                print("error: selected member is a directory", file=sys.stderr)
                return 2
            output = args.output.resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info, "r") as source, output.open("wb") as target:
                while chunk := source.read(1024 * 1024):
                    target.write(chunk)
            print(f"extracted {member} -> {output}")
            return 0
    except (OSError, zipfile.BadZipFile, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
