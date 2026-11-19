# HackintoiOS drivers

This directory is the home for original XNU-facing driver work, separated by subsystem and platform layer.

The organization takes inspiration from the subsystem-based layout used by projects such as HakiOS. It is an independent design: no HakiOS driver code or POCO X5 Pro / SC7280 hardware values are copied into this project.

## Current state

**No HANOIP XNU hardware driver is currently implemented and verified as working.**

The first [HANOIP platform contract](platform/README.md) now records source-backed observations separately from unresolved runtime values. It is an evidence ledger, not executable platform support. See [STATUS.md](STATUS.md) for the authoritative working list, not-yet-implemented list, available evidence, and status rules.

## Planned organization

| Path | Responsibility |
|---|---|
| `platform/` | Evidence-backed platform contract and future loader-to-kernel handoff |
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

Directories and source files will be added when evidence supports a real implementation. We will not add empty C files or label placeholders as drivers.

## Implementation sequence

1. Record verified source facts and unresolved values in the platform contract.
2. Define and test an ARM64 loader-to-kernel handoff in QEMU, including memory-map and device-tree representation.
3. Establish minimal platform identification and debug output.
4. Integrate interrupt and timer services once their handoff requirements are defined.
5. Evaluate read-only storage discovery and basic display/input paths.
6. Add remaining subsystems individually after exact component identities and dependencies are documented.

Each driver must record its hardware source, supported board revision, build result, test environment, and known limitations. Host or QEMU tests must be distinguished from validation on the exact Moto G60.

## Related documents

- [HANOIP platform contract](platform/README.md)
- [HANOIP resource inventory](../docs/architecture/HANOIP_RESOURCE_INVENTORY.md)
- [HANOIP kernel plan](../docs/architecture/HANOIP_KERNEL_PLAN.md)
- [Overall porting plan](../docs/architecture/PORTING_PLAN.md)
