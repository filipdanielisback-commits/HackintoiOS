#!/usr/bin/env python3
"""Inspect BuildManifest.plist and select an image component for iPhone XR."""
from __future__ import annotations

import argparse
import plistlib
import sys
from pathlib import Path

EXPECTED_PRODUCT = "iPhone11,8"
EXPECTED_BUILD = "22H390"


def read_manifest(path: Path) -> dict:
    with path.open("rb") as stream:
        value = plistlib.load(stream)
    if not isinstance(value, dict):
        raise ValueError("BuildManifest root is not a dictionary")
    return value


def matching_identities(manifest: dict, product: str, board: str | None):
    for index, identity in enumerate(manifest.get("BuildIdentities", [])):
        if not isinstance(identity, dict):
            continue
        info = identity.get("Info", {})
        if not isinstance(info, dict) or info.get("ProductType") != product:
            continue
        device_class = str(info.get("DeviceClass", ""))
        if board and device_class and device_class.casefold() != board.casefold():
            continue
        yield index, info, identity


def component_paths(identity: dict):
    components = identity.get("Manifest", {})
    if not isinstance(components, dict):
        return
    for name, component in sorted(components.items()):
        if not isinstance(component, dict):
            continue
        info = component.get("Info", {})
        path = info.get("Path") if isinstance(info, dict) else None
        if isinstance(path, str) and path:
            yield name, path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_manifest", type=Path)
    parser.add_argument("--product", default=EXPECTED_PRODUCT)
    parser.add_argument("--build", default=EXPECTED_BUILD)
    parser.add_argument("--board", help="optional DeviceClass, e.g. n841ap")
    parser.add_argument("--component", default="OS", help="component name (default: OS)")
    parser.add_argument("--list-components", action="store_true")
    parser.add_argument("--print-path", action="store_true",
                        help="print only the selected archive member path")
    args = parser.parse_args()

    try:
        manifest = read_manifest(args.build_manifest)
    except (OSError, plistlib.InvalidFileException, ValueError) as exc:
        print(f"select-system: cannot read BuildManifest.plist: {exc}", file=sys.stderr)
        return 1

    actual_build = manifest.get("ProductBuildVersion")
    if actual_build != args.build:
        print(f"select-system: expected build {args.build}, found {actual_build!r}", file=sys.stderr)
        return 2

    matches = list(matching_identities(manifest, args.product, args.board))
    if not matches:
        print(f"select-system: no build identity for {args.product}"
              + (f" / {args.board}" if args.board else ""), file=sys.stderr)
        return 3

    for index, info, identity in matches:
        components = list(component_paths(identity))
        paths = dict(components)
        if args.list_components:
            for name, path in components:
                print(f"{name}\\t{path}")
            return 0
        path = paths.get(args.component)
        if not path:
            continue
        if args.print_path:
            print(path)
        else:
            print(f"Product: {args.product}")
            print(f"Build: {actual_build}")
            print(f"Device class: {info.get('DeviceClass', 'unspecified')}")
            print(f"Build identity: {index}")
            print(f"Component: {args.component}")
            print(f"IPSW member: {path}")
        return 0

    available = sorted({name for _, _, identity in matches
                        for name, _ in component_paths(identity)})
    print(f"select-system: component {args.component!r} not found; available: "
          + ", ".join(available), file=sys.stderr)
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
