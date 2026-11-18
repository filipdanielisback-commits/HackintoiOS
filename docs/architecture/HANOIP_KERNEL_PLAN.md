# HANOIP-specific XNU kernel work plan

**Status: planning only.** This document defines the evidence and implementation sequence for an original HANOIP platform layer. It does not claim that XNU currently supports the Moto G60.

## Target identity

- Phone: Motorola Moto G60 Vision, XT2135-2.
- Device family: HANOIP.
- Shared community kernel tree platform label: `sm6150`. Treat this as a source-tree/platform label, not as proof of the retail SoC identity.
- SoC research identity: Qualcomm Snapdragon 732G / SM7150-AC.
- Reference firmware: Android 12, build `S2RIS32.32-20-9-9-2-3`, channel `reteu`.
- Linux reference baseline: community `android_kernel_motorola_sm6150`, branch `lineage-20`, defconfig `vendor/hanoip_defconfig`.
- XNU research baseline: Darwin 24.6.0 family; public candidate `xnu-11417.140.69`, peeled commit `43a90889846e00bfb5cf1d255cdc0a701a1e05a4`. Exact association with iOS build `22H390` remains unconfirmed; see [version mapping](../xnu/ios-18.7.12-version.md).

## Design rules

1. Separate generic ARM64/XNU code, Qualcomm SoC support, and Moto G60 board support.
2. Do not transplant POCO X5 Pro, SC7280, or other HakiOS device values into HANOIP.
3. Treat Linux device-tree values and Linux drivers as evidence about hardware only; they are not automatically XNU interfaces or drivers.
4. Every address, interrupt, clock, regulator, GPIO, pin, and compatible string used by future code must have a traceable source and confidence level.
5. Unknown hardware stays unimplemented/disabled. No guessed register maps or fabricated device-tree nodes.
6. Keep all early bring-up in QEMU or other controlled CI emulation. A QEMU result is not a Moto G60 result.
7. Do not alter phone firmware, partitions, or boot configuration as part of this planning work.

## Proposed source layout (create only when a milestone needs it)

| Layer | Future location | Responsibility |
|---|---|---|
| Common XNU baseline | `xnu/upstream.lock`, `xnu/patches/` | Reproducible upstream source and small, reviewable original patch series |
| ARM64 platform glue | `xnu/platform/arm64/` | Architecture-level entry, exception, and generic platform interfaces |
| Qualcomm SoC layer | `xnu/platform/qualcomm/sm7150/` | Only verified SoC-wide services and identifiers |
| HANOIP board layer | `xnu/platform/motorola/hanoip/` | XT2135-2 board description and board-specific resource mapping |
| Device configuration | `devices/moto-g60-xt2135-2/` | Source-linked hardware inventory and configuration |
| Loader contract | `bootloader/uefi/` | Explicit, testable loader-to-kernel handoff contract |
| Tests | `tests/xnu/` | Host-side structure checks and QEMU integration tests |

These are proposed boundaries, not a requirement to create empty directories immediately.

## Bring-up sequence

### A. Evidence inventory — first

Collect and cross-check public XT2135-2/HANOIP device-tree sources, kernel source, defconfig, module lists, board identifiers, and firmware release metadata. The initial [source-backed HANOIP resource inventory](HANOIP_RESOURCE_INVENTORY.md) now records the SDMMAGPIE shared SoC tree and the HANOIP EVT1/DVT1/DVT2 overlays. The [automated DTS audit](../../tools/audit-hanoip-dts.py) and its CI workflow check these pinned source files and publish a JSON evidence report. Continue the recursive overlay audit and determine which engineering variant matches the exact XT2135-2 unit before using board-specific values. Build a resource inventory with columns for subsystem, identifier/value, source URL/path, source revision, confidence, and unresolved questions.

Minimum domains:

- CPU topology and supported ARM64 features
- RAM ranges and reserved memory
- interrupt controller and interrupt routing
- architectural timers and clocks
- device-tree boot contract and console
- storage controller and partition-independent read-only discovery
- display pipeline and framebuffer handoff
- input/touchscreen
- Wi-Fi/Bluetooth chipset identity
- audio, camera, sensors
- PMIC, regulators, thermal monitoring, and power management

**Exit condition:** each value needed by a future platform implementation is backed by a target-specific source; unknowns are explicitly listed.

### B. QEMU platform-independent kernel path

Keep QEMU marked **in progress**. First establish a documented AArch64 loader/kernel handoff using an original test payload. Add tests for image format validation, memory-map parsing, command-line handling, serial logging, and controlled failure. Only add XNU-specific tests after the selected source can be built in a supported environment.

**Exit condition:** a repeatable CI run demonstrates the exact QEMU milestone named by the test. Do not label this as phone support.

### C. Minimal HANOIP platform contract

Before writing hardware drivers, define the minimum contract the kernel expects: CPU state, memory map, reserved regions, device-tree representation, timer/interrupt availability, and console output. Keep platform discovery and configuration separate from drivers.

**Exit condition:** the contract is documented and can be validated independently without accessing or changing phone firmware.

### D. Platform services, one at a time

Prioritize foundational services only after evidence is complete: CPU/platform identification, interrupt controller, timer, memory management integration, and serial/debug output. For each service, record prerequisites, source evidence, implementation owner, build test, QEMU test, and target-specific validation status.

Do not mark a service working merely because a related Linux driver exists.

### E. Device drivers

Evaluate storage, display, input, Wi-Fi, audio, sensors, and power subsystems independently. For each, first identify the exact XT2135-2 component and interface; then determine whether an existing public XNU interface applies or an original driver is needed. Keep proprietary firmware and unsupported services out of the public repository.

**Exit condition:** each driver has a separate evidence record and test result. No blanket "hardware supported" status.

### F. Integrated feasibility review

Only after the QEMU handoff and HANOIP resource inventory are mature should the project assess whether the known firmware interface and platform dependencies make a non-destructive device experiment technically feasible. This plan does not authorize firmware replacement, security bypass, or unverified writes.

## First concrete deliverables

1. A source-linked HANOIP hardware inventory derived from the exact device tree and kernel sources.
2. A short note separating SoC-wide SM7150-AC facts from HANOIP board-specific facts.
3. A QEMU milestone definition with an observable pass condition.
4. A driver dependency table identifying which hardware facts are still unknown.

## Current blockers

- Exact XNU build suffix for iOS 18.7.12 build 22H390 remains unconfirmed.
- Exact XT2135-2 board revision/overlay match and complete hardware resource map remain incomplete. The initial source audit is not yet a merged-DTB or XNU implementation.
- UEFI availability and the target firmware handoff contract are unverified.
- No HANOIP XNU platform code or validated Moto G60 XNU drivers exist.

The end goal remains experimental until reproducible evidence demonstrates each stage on the exact target.
