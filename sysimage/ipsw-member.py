#!/usr/bin/env python3
"""List IPSW ZIP members or safely stream one named member to disk."""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


def safe_member_name(name: str) -> str:
    normalized = name.replace("\\\\", "/")
    member = PurePosixPath(normalized)
    if (member.is_absolute() or ".." in member.parts or not member.parts
            or (member.parts and ":" in member.parts[0])):
        raise ValueError(f"unsafe archive member path: {name!r}")
    return str(member)


def extract_member(archive: zipfile.ZipFile, name: str, output: Path) -> int:
    safe_name = safe_member_name(name)
    matches = [info for info in archive.infolist() if info.filename == safe_name]
    if not matches:
        print(f"error: member not found: {safe_name}", file=sys.stderr)
        return 2
    if len(matches) != 1:
        print(f"error: archive contains duplicate member names: {safe_name}", file=sys.stderr)
        return 2
    info = matches[0]
    if info.is_dir():
        print("error: selected member is a directory", file=sys.stderr)
        return 2
    if info.flag_bits & 0x1:
        print("error: encrypted ZIP members are not supported", file=sys.stderr)
        return 2

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".part",
                                          dir=output.parent)
    try:
        with os.fdopen(fd, "wb") as target, archive.open(info, "r") as source:
            while chunk := source.read(1024 * 1024):
                target.write(chunk)
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary_name, output)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise

    print(f"extracted {safe_name}: {info.file_size} bytes -> {output}")
    return 0


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
            return extract_member(archive, args.member, args.output)
    except (OSError, zipfile.BadZipFile, ValueError, RuntimeError) as exc:
        print(f"ipsw-member: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
