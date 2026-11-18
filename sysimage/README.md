# Sysimage research tools

This directory contains original, minimal tools for inspecting a user-supplied Apple IPSW and preparing a local variable-data directory skeleton. The layout is inspired by the general workflow used by other open-source projects; these scripts are independently written for HackintoiOS.

## Pinned research target

- Device: iPhone XR
- Product identifier: `iPhone11,8`
- iOS version: `18.7.12`
- Build: `22H390`
- IPSW filename: `iPhone11,8_18.7.12_22H390_Restore.ipsw`
- IPSW.me device page: https://ipsw.me/iPhone11%2C8/
- Version page: https://ipsw.me/download/iPhone11%2C8/22H390/
- SHA-256: `3b5c21c4dcf50df3f0865e6f3737a5cc47c929fbe595c05e18dc7074032dc759`

The IPSW is approximately 8.1 GiB. It is **not** stored in this repository and CI does not download it. Signing status is time-sensitive; check the IPSW.me page again before any restore operation.

## Tools

- `ipsw-member.py`: list IPSW ZIP members or extract one named member safely.
- `select-system.py`: inspect `BuildManifest.plist` and select the iPhone XR build identity, then report its OS image member path.
- `mkvarskel.py`: create a basic, empty local `private/var` directory skeleton for later research.
- `unpack.sh`: inspect a local IPSW, extract its build manifest and selected OS image member into a caller-chosen output directory.

The unpacker only extracts the selected archive member as stored in the IPSW. It does not decrypt, bypass signing, defeat device security, modify firmware, or install/restore anything. The extracted image may remain encrypted.

## Scope and limitations

These utilities are for local metadata and archive inspection. They do not provide an iOS user space, a working Darwin system, an activation mechanism, or a bootable image. They do not make the iPhone XR IPSW compatible with the Motorola Moto G60 (XT2135-2). The iPhone XR is a separate Apple-device reference target for studying the iOS 18.7.12 restore-image layout.

Do not commit IPSW files, extracted Apple binaries, personal device data, or other copyrighted firmware payloads to this repository.
