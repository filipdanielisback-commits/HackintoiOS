#!/usr/bin/env python3
"""Validate the basic format of the built HackintoiOS AArch64 EFI application."""

from pathlib import Path
import struct
import sys


def fail(message: str) -> None:
    print(f"UEFI artifact check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    artifact = Path(sys.argv[1] if len(sys.argv) > 1 else "HackintoiOSLoader.efi")
    if not artifact.is_file():
        fail(f"file not found: {artifact}")

    data = artifact.read_bytes()
    if len(data) < 256:
        fail("file is unexpectedly small")

    if data[:2] != b"MZ":
        fail("missing DOS/PE MZ header")

    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if pe_offset + 6 > len(data):
        fail("invalid PE header offset")

    if data[pe_offset:pe_offset + 4] != b"PE\0\0":
        fail("missing PE signature")

    machine = struct.unpack_from("<H", data, pe_offset + 4)[0]
    if machine != 0xAA64:
        fail(f"expected AArch64 PE machine 0xAA64, got 0x{machine:04X}")

    print(f"Validated AArch64 PE/COFF UEFI application: {artifact} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
