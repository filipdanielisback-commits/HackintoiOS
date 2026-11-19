# Driver implementation status

This is the authoritative status list for HackintoiOS driver work on the Moto G60 Vision (XT2135-2, HANOIP).

**Current result: no HANOIP XNU hardware driver is implemented and verified as working.** The project has Linux reference-source evidence, a machine-checked platform evidence contract, and research scaffolding—not functioning XNU drivers.

## Working

_None yet._

A driver may move here only when its implementation is present in this repository, builds in the relevant XNU configuration, and has a recorded test result. The test environment must be stated explicitly: host test, QEMU, or exact physical target. A source audit or successful Linux build is not a driver test.

## Foundation artifacts (not drivers)

| Artifact | Status | What it proves |
|---|---|---|
| HANOIP device-tree source audit | Research tooling | Audits pinned source files and quoted-include closure; does not compile/merge a DTB |
| HANOIP platform contract | Evidence-only; CI-validated when workflow passes | Records source observations and keeps runtime values unresolved; does not initialize hardware |
| ARM64 UEFI console prototype | QEMU-oriented prototype | Exercises a UEFI application path; does not prove HANOIP firmware support or XNU handoff |

## Not yet implemented / not validated

| Subsystem | Status | What is needed before implementation |
|---|---|---|
| ARM64 platform identification | Research only | Define the original XNU platform interface and validate the handoff data |
| CPU bring-up / PSCI | Not implemented | Confirm CPU topology and firmware handoff; add a testable ARM64 platform path |
| Memory map / reserved memory | Not implemented | Obtain and validate the actual loader-provided memory map |
| Interrupt controller / routing | Not implemented | Resolve the delivered interrupt-controller description and routing |
| Architectural timer | Not implemented | Identify the timer interface and frequency from reliable platform evidence |
| Serial / debug console | Not implemented | Verify the actual console device and boot-time availability |
| UFS storage | Not implemented | Confirm controller, clocks, power dependencies, and a read-only discovery interface |
| Display / framebuffer | Not implemented | Identify the panel/controller and define a safe framebuffer handoff |
| Adreno GPU | Not implemented | Establish GPU identity, firmware requirements, and a permitted driver interface |
| Touchscreen / input | Not implemented | Confirm the exact controller and its bus/interrupt wiring |
| Wi-Fi | Not implemented | Identify the exact radio and firmware/interface requirements |
| Bluetooth | Not implemented | Identify the exact radio and transport |
| Audio | Not implemented | Map audio codec/DSP and required interfaces |
| Camera | Not implemented | Identify sensors and ISP interfaces |
| Sensors | Not implemented | Identify each sensor and its bus/address/interrupt evidence |
| Haptics | Not implemented | Identify the vibration controller and safe control interface |
| Power / battery / thermal | Not implemented | Map PMIC, regulators, sensors, and thermal dependencies |
| Modem / cellular | Not implemented | Establish hardware identity and interface requirements |

"Not implemented" does **not** mean the hardware is broken. It means this repository has no validated HANOIP XNU driver for that subsystem yet.

## Evidence available (not working drivers)

The pinned Linux reference source provides useful clues, but none of these is an XNU implementation:

- Shared device-tree identity: `qcom,sdmmagpie`.
- HANOIP engineering overlays: EVT1, DVT1, and DVT2; exact match to this XT2135-2 unit remains unknown.
- Shared device-tree CPU nodes describe ARMv8 CPUs with a PSCI enable method.
- Shared tree sets `interrupt-parent = <&pdc>`.
- Shared tree aliases `serial0` to `qupv3_se8_2uart`; this does not prove it is enabled/usable at custom-kernel handoff.
- Linux HANOIP configuration and module lists provide subsystem clues, but do not establish XNU compatibility or exact component identity.

See [HANOIP platform contract](platform/README.md), [HANOIP resource inventory](../docs/architecture/HANOIP_RESOURCE_INVENTORY.md), [HANOIP kernel plan](../docs/architecture/HANOIP_KERNEL_PLAN.md), and [device profile](../devices/moto-g60-xt2135-2/README.md).

## Status rules

- **Working:** code exists, builds, and its behavior is demonstrated by a named test. State whether that test is host, QEMU, or exact-device.
- **Partial:** some code or evidence exists, but the full behavior or required test is incomplete.
- **Not implemented:** no driver implementation exists.
- **Blocked:** implementation cannot proceed until a named hardware/interface fact is resolved.

Do not mark a driver working because a Linux driver exists, a device-tree node is present, a module is listed, or a workflow merely passes source-text checks.

No POCO X5 Pro / SC7280 values or HakiOS driver code should be copied into HANOIP. Use public projects as architectural references only. Keep early tests in CI/QEMU; do not write to device firmware or partitions.
