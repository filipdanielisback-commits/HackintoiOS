#!/usr/bin/env python3
"""Report iOS restore filesystem-related BuildManifest components.

This is metadata inspection only. It does not decrypt, extract, mount, or build APFS.
"""
from __future__ import annotations

import argparse
import json
import plistlib
import sys
from pathlib import PurePosixPath

EXPECTED_PRODUCT = "iPhone11,8"
EXPECTED_BUILD = "22H390"

# BuildManifest component names are reported as candidates, not proof that the
# payload is a directly mountable APFS image or that it maps 1:1 to a volume.
ROOT_CANDIDATES = {"OS"}
SYSTEM_CANDIDATES = {"Cryptex1,AppOS"}


def safe_member(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        return None
    return value


def inspect(path, product: str, build: str, board: str | None) -> dict:
    with path.open("rb") as stream:
        manifest = plistlib.load(stream)
    if not isinstance(manifest, dict):
        raise ValueError("BuildManifest root is not a dictionary")
    actual_build = manifest.get("ProductBuildVersion")
    if actual_build != build:
        raise ValueError(f"expected build {build}, found {actual_build!r}")

    matches = []
    for index, identity in enumerate(manifest.get("BuildIdentities", [])):
        if not isinstance(identity, dict):
            continue
        info = identity.get("Info", {})
        if not isinstance(info, dict) or info.get("ProductType") != product:
            continue
        device_class = str(info.get("DeviceClass", ""))
        if board and device_class.casefold() != board.casefold():
            continue
        entries = []
        components = identity.get("Manifest", {})
        if isinstance(components, dict):
            for name, component in sorted(components.items()):
                if not isinstance(component, dict):
                    continue
                component_info = component.get("Info", {})
                component_info = component_info if isinstance(component_info, dict) else {}
                member = safe_member(component_info.get("Path"))
                if not member:
                    continue
                if name in ROOT_CANDIDATES:
                    role = "root-filesystem-input-candidate"
                elif name in SYSTEM_CANDIDATES:
                    role = "system-cryptex-input-candidate"
                else:
                    role = "other-restore-component"
                entries.append({
                    "name": name,
                    "role": role,
                    "ipsw_member": member,
                    "is_encrypted_metadata": component.get("IsEncrypted"),
                    "digest_present": bool(component.get("Digest")),
                })
        matches.append({
            "identity_index": index,
            "device_class": device_class or None,
            "components": entries,
        })
    if not matches:
        raise ValueError(f"no matching build identity for {product}"
                         + (f" / {board}" if board else ""))
    return {
        "product": product,
        "build": actual_build,
        "board_filter": board,
        "identities": matches,
        "limitations": [
            "Component names are candidates, not proof of directly mountable APFS images.",
            "This tool reads BuildManifest metadata only; it does not decrypt or extract payloads.",
            "APFS image creation is not implemented by this tool.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_manifest")
    parser.add_argument("--product", default=EXPECTED_PRODUCT)
    parser.add_argument("--build", default=EXPECTED_BUILD)
    parser.add_argument("--board", default="n841ap")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    try:
        result = inspect(__import__("pathlib").Path(args.build_manifest),
                         args.product, args.build, args.board)
    except (OSError, plistlib.InvalidFileException, ValueError) as exc:
        print(f"inspect-filesystem: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Product: {result['product']}  Build: {result['build']}")
        for identity in result["identities"]:
            print(f"Build identity {identity['identity_index']} ({identity['device_class']}):")
            for item in identity["components"]:
                print(f"  {item['role']}: {item['name']} -> {item['ipsw_member']}")
        print("Metadata only: no decryption, mounting, or APFS creation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
