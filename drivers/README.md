# HackintoiOS drivers

This directory is the home for original XNU-facing driver work, separated by subsystem and platform layer.

The organization takes inspiration from the subsystem-based layout used by projects such as HakiOS. It is an independent design: no HakiOS driver code or POCO X5 Pro / SC7280 hardware values are copied into this project.

## Current state

**No HANOIP XNU hardware driver is currently implemented and verified as working.**

See [STATUS.md](STATUS.md) for the authoritative working list, not-yet-implemented list, available evidence, and status rules.

## Planned organization

| Path | Responsibility |
|---|---|
| `platform/` | Common ARM64 platform services and loader-to-kernel handoff |
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

1. Define the platform contract: CPU state, memory map, device-tree handoff, console, timer, and interrupts.
2. Establish minimal platform identification and debug output.
3. Evaluate read-only storage discovery and basic display/input paths.
4. Add remaining subsystems individually after exact component identities and dependencies are documented.

Each driver must record its hardware source, supported board revision, build result, test environment, and known limitations. Host or QEMU tests must be distinguished from validation on the exact Moto G60.

## Related documents

- [HANOIP resource inventory](../docs/architecture/HANOIP_RESOURCE_INVENTORY.md)
- [HANOIP kernel plan](../docs/architecture/HANOIP_KERNEL_PLAN.md)
- [Overall porting plan](../docs/architecture/PORTING_PLAN.md)
