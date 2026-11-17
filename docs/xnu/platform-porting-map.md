# HANOIP XNU platform-porting map

## Purpose and status

This document maps the pinned public XNU source tree to the platform work that would be needed for a possible Motorola Moto G60 Vision (XT2135-2 / HANOIP) port.

**Status: research map only.** No HANOIP XNU platform implementation exists here. A generic ARM64 build, if achieved, would not demonstrate that XNU can boot on this phone.

## Confirmed device baseline

The target handset reports model XT2135-2, Android 12, firmware build `S2RIS32.32-20-9-9-2-3`, and channel `reteu`. The device family is referred to as HANOIP in the community kernel sources. The community Linux kernel tree uses the `sm6150` tree name; that name must not be mistaken for the handset's commercial SoC model.

The existing Linux reference build is useful as a source of device-tree, board, regulator, clock, pin-control, and peripheral evidence. It is not an XNU implementation and its drivers cannot simply be linked into XNU.

## Relevant upstream XNU areas

The following paths exist in the pinned `xnu-11215.1.10` source tree. Their presence is confirmed; their suitability for HANOIP is not.

| Upstream area | What it contains / why it matters |
| --- | --- |
| `osfmk/arm64/` | ARM64 low-level startup, exception handling, CPU routines, translation and platform-adjacent machine code. |
| `osfmk/arm/` | Shared ARM initialization, timer, CPU and machine-dependent interfaces. |
| `pexpert/arm/` | ARM platform-expert startup and early boot code, including `pe_bootargs.c`, `pe_init.c`, and machine-identification code. |
| `pexpert/pexpert/` | Platform-expert interfaces and boot/device-tree headers. |
| `bsd/` | BSD kernel layer; depends on the lower-level Mach and platform layers being initialized correctly. |
| `iokit/` and `libkern/` | Driver framework and supporting kernel C++ runtime; a framework is not a substitute for device-specific drivers. |
| `libsa/` | Kernel bootstrap support; does not itself provide a ready-made Moto G60 bootloader. |

## Porting gates and evidence required

1. **Boot contract:** document the actual bootloader handoff, loaded image format, entry conditions, device-tree or equivalent hardware description, memory map, and reserved regions for this exact firmware. Do not infer these from another phone.
2. **Early platform expert:** determine how HANOIP-specific machine identification and early console/boot arguments could be represented without relying on Apple-only platform assumptions.
3. **CPU and exceptions:** verify the actual CPU topology and supported architectural features, then map exception-level, interrupt, cache, and MMU expectations to the handset.
4. **Interrupt controller and timers:** identify the hardware blocks and firmware handoff used by this board; establish the interrupt and clock interfaces required by XNU.
5. **Physical memory and DMA:** map usable/reserved memory and define safe DMA/IOMMU behavior before enabling storage or other bus-mastering devices.
6. **Storage and root filesystem:** identify a safe, documented path for reading a test root filesystem. No user-data partitions should be modified as part of early bring-up.
7. **Console and diagnostics:** define a non-destructive diagnostic output path before attempting broader initialization.
8. **Device drivers:** treat display, GPU, touch, Wi-Fi, audio, camera, sensors, charging and thermal support as separate later projects. Existing Android/Linux drivers are research references, not drop-in XNU drivers.

## First implementation boundary

Do not add a speculative HANOIP C source file or change generic ARM64 startup merely to make the repository look more complete. The first code patch should follow from a verified boot contract and a reproducible upstream build.

A reasonable first implementation, once evidence exists, is a narrowly scoped platform-identification or boot-argument adaptation with a host-side test. It must not claim to initialize the phone's hardware until tested on the actual board.

## Immediate blockers

- The public macOS build probe has not completed a build attempt: its first jobs were cancelled before any step ran. This says nothing about whether the compiler would accept XNU.
- The upstream README documents an SDK-driven build and uses Apple's internal SDK in its example. Public SDK compatibility remains unverified.
- The exact board revision, bootloader handoff details, memory map, interrupt/timer configuration, and peripheral inventory still need authoritative evidence.
- No bootable XNU image, Darwin user space, or installation process is available.

## References

- Pinned source: [Apple XNU xnu-11215.1.10](https://github.com/apple-oss-distributions/xnu/tree/xnu-11215.1.10)
- Upstream build overview: [XNU README](https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/README.md)
- Device-specific research: [Moto G60 XT2135-2 profile](../../devices/moto-g60-xt2135-2/README.md)
- Community Linux reference tree: [android_kernel_motorola_sm6150](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150)
