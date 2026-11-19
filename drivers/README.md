# HackintoiOS drivers

This directory is the home for original XNU-facing driver work, separated by subsystem and platform layer.

The organization takes inspiration from subsystem-based layouts such as HakiOS, but implementations and target configuration are independently developed. No HakiOS driver code or POCO X5 Pro / SC7280 hardware values are copied into this project.

## Current state

No HANOIP XNU hardware driver is verified as working. The first portable driver-core component is [HanoipAdreno618](gpu/adreno618/README.md): it validates platform-supplied identity and resource descriptors and has host-only tests. It does not initialize the GPU or provide hardware acceleration. The [Adreno 618 hardware research](../docs/architecture/ADRENO618_HARDWARE_RESEARCH.md) now inventories the HANOIP Linux GPU, GMU, IOMMU, firmware, clock and power evidence; it remains research only. The [HANOIP Wi-Fi research](../docs/architecture/HANOIP_WIFI_RESEARCH.md) records the Qualcomm CLD3/ICNSS stack and WLAN memory/signalling evidence. Exact radio silicon and transport remain unverified. See [STATUS.md](STATUS.md) for authoritative status.

## Organization

| Path | Responsibility |
|---|---|
| `platform/` | Evidence-backed platform contract and future loader-to-kernel handoff |
| `gpu/adreno618/` | Adreno 618 driver core and future HANOIP GPU integration |
| `qualcomm/sm7150/` | Verified Qualcomm SoC-wide support only |
| `motorola/hanoip/` | Moto G60 board-specific configuration and glue |
| `console/` | Early serial/debug console |
| `interrupts/` | Interrupt-controller integration |
| `timer/` | Architectural timer integration |
| `storage/` | Read-only storage discovery and storage interfaces |
| `display/` | Framebuffer/display integration |
| `input/` | Touchscreen and input |
| `connectivity/` | Wi-Fi and Bluetooth |
| `audio/` | Audio interfaces |
| `camera/` | Camera sensors and ISP interfaces |
| `sensors/` | Motion and environmental sensors |
| `power/` | PMIC, battery, thermal, and power interfaces |

## Implementation sequence

1. Record verified source facts and unresolved values in the platform contract.
2. Define and test an ARM64 loader-to-kernel handoff in QEMU, including memory-map and device-tree representation.
3. Establish minimal platform identification and debug output.
4. Integrate interrupt and timer services once their handoff requirements are defined.
5. Develop portable driver cores and tests, then add HANOIP-specific hardware operations only when their resources and interfaces are verified.
6. Evaluate read-only storage discovery and basic display/input paths, followed by connectivity, audio, sensors, camera, and power integration.

Each driver must record its hardware source, supported board revision, build result, test environment, and known limitations. Host or QEMU tests must be distinguished from validation on the exact Moto G60.

## Related documents

- [HANOIP platform contract](platform/README.md)
- [HANOIP resource inventory](../docs/architecture/HANOIP_RESOURCE_INVENTORY.md)
- [HANOIP kernel plan](../docs/architecture/HANOIP_KERNEL_PLAN.md)
- [Overall porting plan](../docs/architecture/PORTING_PLAN.md)
