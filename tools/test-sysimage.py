#!/usr/bin/env python3
"""Synthetic tests for sysimage tools; no real Apple firmware is required."""
from __future__ import annotations

import json
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
                "Info": {"ProductType": "iPhone11,8", "DeviceClass": "N841AP"},
                "Manifest": {
                    "OS": {"Info": {"Path": "rootfs.dmg"}},
                    "Cryptex1,AppOS": {"Info": {"Path": "app-cryptex.dmg"}},
                },
            }],
        }
        ipsw = work / "synthetic.ipsw"
        with zipfile.ZipFile(ipsw, "w") as archive:
            archive.writestr("BuildManifest.plist", plistlib.dumps(manifest))
            archive.writestr("rootfs.dmg", b"synthetic-image-payload")
            archive.writestr("app-cryptex.dmg", b"synthetic-app-payload")
            archive.writestr("../unsafe.txt", b"not extracted")

        listing = run(sys.executable, str(SYSDIR / "ipsw-member.py"), "list", str(ipsw))
        assert listing.returncode == 0 and "BuildManifest.plist" in listing.stdout, listing.stderr

        extracted = run(sys.executable, str(SYSDIR / "ipsw-member.py"), "extract",
                        str(ipsw), "BuildManifest.plist", "--output",
                        str(work / "metadata/BuildManifest.plist"))
        assert extracted.returncode == 0, extracted.stderr

        selector = [sys.executable, str(SYSDIR / "select-system.py"),
                    str(work / "metadata/BuildManifest.plist")]
        selected = run(*selector, "--component", "OS", "--print-path")
        assert selected.returncode == 0 and selected.stdout.strip() == "rootfs.dmg", selected.stderr
        components = run(*selector, "--list-components")
        assert components.returncode == 0 and "Cryptex1,AppOS" in components.stdout

        fs_report = run(sys.executable, str(SYSDIR / "inspect-filesystem.py"),
                        str(work / "metadata/BuildManifest.plist"), "--json")
        assert fs_report.returncode == 0, fs_report.stderr
        fs_data = json.loads(fs_report.stdout)
        fs_components = {item["name"]: item for item in fs_data["identities"][0]["components"]}
        assert fs_components["OS"]["role"] == "root-filesystem-input-candidate"
        assert fs_components["Cryptex1,AppOS"]["role"] == "system-cryptex-input-candidate"
        assert fs_components["OS"]["ipsw_member"] == "rootfs.dmg"
        assert "APFS image creation is not implemented" in " ".join(fs_data["limitations"])

        unsafe_manifest = dict(manifest)
        unsafe_manifest["BuildIdentities"] = [{
            "Info": {"ProductType": "iPhone11,8", "DeviceClass": "N841AP"},
            "Manifest": {"OS": {"Info": {"Path": "../outside.dmg"}}},
        }]
        unsafe_path = work / "unsafe-BuildManifest.plist"
        unsafe_path.write_bytes(plistlib.dumps(unsafe_manifest))
        unsafe_report = run(sys.executable, str(SYSDIR / "inspect-filesystem.py"),
                            str(unsafe_path), "--json")
        assert unsafe_report.returncode == 0, unsafe_report.stderr
        assert unsafe_report.stdout.find("outside.dmg") == -1
        wrong_board = run(*selector, "--board", "wrong")
        assert wrong_board.returncode == 3, wrong_board.stderr

        unpacked = run("bash", str(SYSDIR / "unpack.sh"), str(ipsw), str(work / "unpacked"))
        assert unpacked.returncode == 0, unpacked.stderr + unpacked.stdout
        assert (work / "unpacked/payload/rootfs.dmg").read_bytes() == b"synthetic-image-payload"

        # Synthetic 7z technical listing with directory, file, symlink and unsafe path.
        slt = work / "rootfs.slt"
        slt.write_text(
            "Path = private/var\nMode = drwxr-xr-x\nUser ID = 0\nGroup ID = 0\n\n"
            "Path = private/var/mobile\nMode = drwx------\nUser ID = 501\nGroup ID = 501\n\n"
            "Path = private/var/mobile/data.db\nMode = -rw-------\nSize = 12\nUser ID = 501\nGroup ID = 501\n\n"
            "Path = private/var/tmp-link\nMode = lrwxrwxrwx\nSymbolic Link = /private/var/tmp\n\n"
            "Path = ../outside\nMode = drwxr-xr-x\n\n",
            encoding="utf-8",
        )
        indexed = run(sys.executable, str(SYSDIR / "rootfs-index.py"), str(slt))
        assert indexed.returncode == 0, indexed.stderr
        records = [json.loads(line) for line in indexed.stdout.splitlines()]
        assert len(records) == 4, records
        assert records[0]["path"] == "private/var", records

        var_manifest = run(sys.executable, str(SYSDIR / "mkvarskel.py"), str(slt))
        assert var_manifest.returncode == 0, var_manifest.stderr
        assert "d\t40700\t501\t501\t/private/var/mobile" in var_manifest.stdout
        assert "l\t/private/var/tmp\t/private/var/tmp-link" in var_manifest.stdout
        assert "data.db" not in var_manifest.stdout

        unsafe = run(sys.executable, str(SYSDIR / "ipsw-member.py"), "extract",
                     str(ipsw), "../unsafe.txt", "--output", str(work / "escape"))
        assert unsafe.returncode != 0, "archive traversal path must be rejected"
        assert not (work / "escape").exists()

    print("sysimage synthetic tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
