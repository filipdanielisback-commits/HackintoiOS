#!/usr/bin/env python3
"""Select and report the iPhone XR OS image member from BuildManifest.plist."""
from __future__ import annotations
import argparse
import plistlib
import sys
from pathlib import Path

EXPECTED_PRODUCT = "iPhone11,8"
EXPECTED_BUILD = "22H390"

def find_os_path(identity: dict) -> str | None:
    manifest = identity.get("Manifest", {})
    if not isinstance(manifest, dict):
        return None
    candidates = []
    if "OS" in manifest:
        candidates.append(("OS", manifest["OS"]))
    candidates.extend((name, value) for name, value in manifest.items()
                      if name != "OS" and ("OS" in name.upper() or "SYSTEM" in name.upper()))
    for _name, component in candidates:
        if isinstance(component, dict):
            info = component.get("Info", {})
            if isinstance(info, dict) and isinstance(info.get("Path"), str):
                return info["Path"]
    return None

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_manifest", type=Path)
    parser.add_argument("--product", default=EXPECTED_PRODUCT)
    parser.add_argument("--build", default=EXPECTED_BUILD)
    parser.add_argument("--print-path", action="store_true")
    args = parser.parse_args()
    try:
        with args.build_manifest.open("rb") as stream:
            manifest = plistlib.load(stream)
    except (OSError, plistlib.InvalidFileException) as exc:
        print(f"error reading BuildManifest.plist: {exc}", file=sys.stderr)
        return 1
    actual_build = manifest.get("ProductBuildVersion")
    if actual_build != args.build:
        print(f"error: expected build {args.build}, found {actual_build!r}", file=sys.stderr)
        return 2
    for index, identity in enumerate(manifest.get("BuildIdentities", [])):
        info = identity.get("Info", {}) if isinstance(identity, dict) else {}
        if not isinstance(info, dict) or info.get("ProductType") != args.product:
            continue
        path = find_os_path(identity)
        if not path:
            print("error: matching identity has no OS image path", file=sys.stderr)
            return 3
        print(f"Device: iPhone XR ({args.product})")
        print(f"Build: {actual_build}")
        print(f"Identity index: {index}")
        print(f"OS image member: {path}")
        if args.print_path:
            print(path)
        return 0
    print(f"error: no build identity for {args.product} in build {actual_build}", file=sys.stderr)
    return 4

if __name__ == "__main__":
    raise SystemExit(main())
