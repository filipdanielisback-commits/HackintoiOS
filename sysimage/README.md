# Sysimage research tools

HackintoiOS has an original, staged IPSW inspection pipeline. Its directory layout is inspired by a common research workflow, but the scripts here are independently written. We do not copy HakiOS implementation code or its iPhone X / iOS 16.5-specific filtering rules.

## Pinned IPSW research target

- Device: iPhone XR
- Product identifier: `iPhone11,8`
- Board identifier: `n841ap`
- iOS version: `18.7.12`
- Build: `22H390`
- IPSW filename: `iPhone11,8_18.7.12_22H390_Restore.ipsw`
- IPSW.me device page: https://ipsw.me/iPhone11%2C8/
- Version page: https://ipsw.me/download/iPhone11%2C8/22H390/
- SHA-256: `3b5c21c4dcf50df3f0865e6f3737a5cc47c929fbe595c05e18dc7074032dc759`

IPSW.me lists this 8.1 GiB image as signed at the time of the last check. Signing can change. The IPSW is not stored in this repository and CI never downloads it.

## Pipeline

1. `ipsw-member.py` lists archive members or safely streams one named member to a local file. Writes are atomic; duplicate names, encrypted members, and traversal paths are rejected.
2. `select-system.py` validates the build and product identity in `BuildManifest.plist`. It can list all named image components or select one component (default: `OS`).
3. `inspect-filesystem.py` reports the iOS 18.7.12 `OS` and `Cryptex1,AppOS` components as root-filesystem and system-Cryptex input candidates. It validates the product/build/board and rejects unsafe member paths in its report. This is metadata classification, not APFS construction.
4. `unpack.sh` extracts the build manifest and selected OS component. This is archive extraction only; it does not decrypt or install firmware.
5. If the extracted image is readable by a compatible 7-Zip build, create a technical listing:
   `7z l -slt path/to/image > rootfs.slt`
6. `rootfs-index.py` converts a 7-Zip technical listing into JSON Lines containing normalized paths, file types, modes, owners, sizes and symlink targets.
7. `mkvarskel.py` emits a tab-separated directory/symlink manifest for entries under `/private/var`, using metadata found in the listing rather than guessed permissions.

Example commands:

```sh
python3 sysimage/ipsw-member.py list /path/to/iPhone11,8_18.7.12_22H390_Restore.ipsw
bash sysimage/unpack.sh /path/to/iPhone11,8_18.7.12_22H390_Restore.ipsw ./work/ios18-xr
python3 sysimage/select-system.py ./work/ios18-xr/metadata/BuildManifest.plist --list-components
python3 sysimage/inspect-filesystem.py ./work/ios18-xr/metadata/BuildManifest.plist --json
7z l -slt ./work/ios18-xr/payload/ROOTFS_IMAGE.dmg > ./work/rootfs.slt
python3 sysimage/rootfs-index.py ./work/rootfs.slt --output ./work/rootfs-index.jsonl
python3 sysimage/mkvarskel.py ./work/rootfs.slt --output ./work/var.skel
```

Replace `ROOTFS_IMAGE.dmg` with the actual member name printed by the selector. The image may be encrypted or unsupported by the installed archive tools; the later listing steps are conditional, not guaranteed.

## What this does not do

- It does not decrypt an IPSW, bypass signing, defeat device security, or perform a restore.
- It does not create a bootable iOS system or a complete Darwin user space.
- It does not prove that the iPhone XR image can run on the Motorola Moto G60 (XT2135-2).
- It does not yet create `root.apfs` or `system.apfs`. `OS` and `Cryptex1,AppOS` are currently reported only as manifest component candidates; their payload formats and accessibility must be verified before a builder can be designed.
- It does not yet filter a complete iOS 18.7.12 root filesystem into a minimal bootable image. Such filtering needs evidence from this exact build, not rules copied from a different phone and OS version.

Do not commit IPSW files, extracted Apple binaries, personal device data, or other copyrighted firmware payloads to this repository.
