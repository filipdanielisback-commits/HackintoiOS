# Repository architecture and directory map

This document records the repository structure adopted by HackintoiOS. HakiOS is used as an architectural reference only; this project writes its own implementation for the Moto G60 XT2135-2.

## Main layers

| HackintoiOS path | Responsibility | HakiOS architectural analogue |
|---|---|---|
| `xnu/` | Upstream XNU baseline metadata and original patch series | `xnu/` |
| `drivers/core/` | Planned device-neutral driver interfaces | `drivers/core/` |
| `drivers/<subsystem>/` | Original subsystem driver work and evidence | `drivers/<subsystem>/` |
| `drivers/qualcomm/sm7150/` | Shared Qualcomm-family layer, only for verified common behavior | `devices/<device>/soc/` |
| `drivers/motorola/hanoip/` | Moto G60/HANOIP board-specific glue | `devices/<device>/` |
| `devices/moto-g60-xt2135-2/` | Target identity, hardware inventory, and device status | `devices/<device>/` |
| `configs/` | Future common, target, and QEMU build configuration | `configs/` |
| `bootloader/` | AArch64 UEFI prototype and boot-chain research | `xnuloader/` (different implementation and maturity) |
| `sysimage/` | Safe IPSW metadata/archive inspection | `sysimage/` |
| `userland/` | Original host-side and future Darwin user-space work | `userland/` |
| `qemu/` | QEMU experiment index and test guidance | `qemu/` |
| `tools/` | Original validation and development utilities | `tools/` |
| `docs/` | Research, architecture, and engineering decisions | `docs/` |
| `.github/workflows/` | CI checks and reproducible host/QEMU tests | `ci/` / workflows |

## Important differences

- HackintoiOS already has a separate Linux reference-kernel build under `kernel/`; it is not the XNU kernel.
- `bootloader/` is an EDK II application prototype, not HakiOS's loader and not a phone bootloader.
- The QEMU XNU work currently inspects source feasibility; it does not yet compile or boot XNU.
- `configs/` currently documents intended layering. No unverified HANOIP XNU options or boot arguments are enabled.
- Driver directories are subsystem boundaries and research ownership locations. A README does not mean a driver exists.
- No `prebuilt/` directory is added while there are no validated project binaries intended for repository distribution.

## Development rules

1. Write original code; do not copy HakiOS implementation files.
2. Keep device-neutral code separate from Qualcomm-family and HANOIP-specific code.
3. Record source provenance, license, target revision, and test level for every imported dependency or driver.
4. Never guess hardware IDs, register maps, firmware names, boot arguments, or board revisions.
5. Report host, CI, QEMU, and exact-device results separately.
