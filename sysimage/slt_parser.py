"""Shared parser for 7-Zip technical listings (7z l -slt)."""
from __future__ import annotations

import stat
from pathlib import PurePosixPath
from typing import Iterator


_PERMISSION_BITS = (0o400, 0o200, 0o100, 0o040, 0o020, 0o010, 0o004, 0o002, 0o001)
_FILE_TYPES = {
    "-": stat.S_IFREG,
    "d": stat.S_IFDIR,
    "l": stat.S_IFLNK,
}


def safe_relative_path(value: str) -> str | None:
    """Normalize a listing path and reject absolute or parent-traversal paths."""
    value = value.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or value == ".":
        return None
    return str(path)


def parse_mode(value: str) -> int | None:
    """Convert a 7-Zip mode such as '-rwxr-xr-x' to a POSIX st_mode."""
    if len(value) < 10 or value[0] not in _FILE_TYPES:
        return None
    mode = _FILE_TYPES[value[0]]
    for index, char in enumerate(value[1:10]):
        if char in "rwx":
            mode |= _PERMISSION_BITS[index]
        elif char in "sStT":
            if index == 2:
                mode |= stat.S_ISUID
                if char == "s":
                    mode |= stat.S_IXUSR
            elif index == 5:
                mode |= stat.S_ISGID
                if char == "s":
                    mode |= stat.S_IXGRP
            elif index == 8:
                mode |= stat.S_ISVTX
                if char == "t":
                    mode |= stat.S_IXOTH
    return mode


def entries(filename: str) -> Iterator[dict]:
    """Yield normalized filesystem records from a 7-Zip -slt text file."""
    record: dict[str, str] = {}

    def convert(raw: dict[str, str]) -> dict | None:
        if "Path" not in raw or "Mode" not in raw:
            return None
        path = safe_relative_path(raw["Path"])
        mode = parse_mode(raw["Mode"])
        if path is None or mode is None:
            return None
        try:
            size = int(raw.get("Size", "0") or 0)
            uid = int(raw.get("User ID", "0") or 0)
            gid = int(raw.get("Group ID", "0") or 0)
        except ValueError:
            return None
        if size < 0:
            return None
        return {
            "path": path,
            "mode": mode,
            "mode_octal": format(mode, "o"),
            "type": "directory" if stat.S_ISDIR(mode) else
                    "symlink" if stat.S_ISLNK(mode) else "file",
            "size": size,
            "uid": uid,
            "gid": gid,
            "symlink_target": raw.get("Symbolic Link", ""),
        }

    with open(filename, encoding="utf-8", errors="replace") as stream:
        for line in stream:
            line = line.rstrip("\r\n")
            if not line:
                item = convert(record)
                if item is not None:
                    yield item
                record = {}
                continue
            if " = " in line or line.endswith(" ="):
                key, _, value = line.partition(" =")
                record[key] = value
    item = convert(record)
    if item is not None:
        yield item
