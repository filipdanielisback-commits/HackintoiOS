#!/usr/bin/env python3
"""Synthetic tests for the IPSW inspection helpers; no real IPSW is required."""
from __future__ import annotations
import plistlib
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSDIR = ROOT / "sysimage"

def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(args, text=True, capture_output=True, check=False)

def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        work = Path(temporary)
        manifest = {
            "ProductBuildVersion": "22H390",
            "BuildIdentities": [{
                "Info": {"ProductType": "iPhone11,8"},
                "Manifest": {"OS": {"Info": {"Path": "rootfs.dmg"}}}
            }]
        }
        manifest_bytes = plistlib.dumps(manifest)
        ipsw = work / "synthetic.ipsw"
        with zipfile.ZipFile(ipsw, "w") as archive:
            archive.writestr("BuildManifest.plist", manifest_bytes)
            archive.writestr("rootfs.dmg", b"synthetic-image-payload")

        listing = run(sys.executable, str(SYSDIR / "ipsw-member.py"), "list", str(ipsw))
        assert listing.returncode == 0 and "BuildManifest.plist" in listing.stdout, listing.stderr

        selected = run(sys.executable, str(SYSDIR / "select-system.py"),
                       str(work / "BuildManifest.plist"))
        assert selected.returncode != 0, "selector must reject a missing manifest"

        extracted = run(sys.executable, str(SYSDIR / "ipsw-member.py"), "extract",
                        str(ipsw), "BuildManifest.plist", "--output",
                        str(work / "BuildManifest.plist"))
        assert extracted.returncode == 0, extracted.stderr

        selected = run(sys.executable, str(SYSDIR / "select-system.py"),
                       str(work / "BuildManifest.plist"), "--print-path")
        assert selected.returncode == 0 and selected.stdout.rstrip().endswith("rootfs.dmg"), selected.stderr

        unpacked = run("bash", str(SYSDIR / "unpack.sh"), str(ipsw), str(work / "unpacked"))
        assert unpacked.returncode == 0, unpacked.stderr + unpacked.stdout
        assert (work / "unpacked/payload/rootfs.dmg").read_bytes() == b"synthetic-image-payload"

        skeleton = run(sys.executable, str(SYSDIR / "mkvarskel.py"), str(work / "var"))
        assert skeleton.returncode == 0, skeleton.stderr
        assert (work / "var/private/var/mobile/Library").is_dir()

        unsafe = run(sys.executable, str(SYSDIR / "ipsw-member.py"), "extract",
                     str(ipsw), "../escape", "--output", str(work / "escape"))
        assert unsafe.returncode != 0, "archive traversal path must be rejected"

    print("sysimage synthetic tests passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
