# Hardware driver work

**Status: planning and source research only. No HackintoiOS hardware drivers are implemented here yet.**

This directory is reserved for original XNU-facing drivers, organized by hardware subsystem. HakiOS is an architectural reference, but its POCO X5 Pro / SC7280 driver code and register values are not evidence for the Moto G60 Vision (XT2135-2 / HANOIP).

## Planned subsystems

| Area | First milestone | Current status |
|---|---|---|
| Input | Identify the power, volume-up and volume-down event path; define a read-only input test | Not implemented |
| Display | Identify display controller, panel path and boot framebuffer handoff; show a basic test pattern only after a safe test environment exists | Not implemented |
| Battery / power | Identify battery gauge, charger and PMIC interfaces; report read-only status | Not implemented |
| Storage | Document the boot-time storage interface and read-only access requirements | Not implemented |
| Boot | Define a QEMU-first XNU handoff contract before any phone-specific integration | Research only; separate UEFI prototype is not a phone bootloader |
| GPU | Identify the exact Adreno and display stack; defer acceleration until basic display output is understood | Not implemented |
| Audio / wireless | Inventory device-tree nodes and firmware dependencies | Not implemented |

## Evidence required before writing a device driver

1. Exact target model and firmware baseline.
2. Relevant device-tree nodes and compatible strings from a trustworthy source.
3. Register ranges, interrupts, clocks, regulators and GPIO/pinctrl relationships, with provenance.
4. Existing vendor or upstream driver behavior and applicable license.
5. A documented test environment and a way to recover without changing phone partitions.

A Linux driver compiling or working on Android does not make it an XNU driver. Do not copy another phone's register addresses, GPIO numbers, power rails or firmware assumptions.

## Safety and validation boundaries

- Initial driver work should be static analysis, host tests and QEMU experiments.
- Do not write to phone partitions or alter firmware as part of driver discovery.
- Battery and power work must begin read-only; no charging-control or thermal-limit experiments.
- A driver is marked supported only after reproducible evidence on the exact XT2135-2 target. A source-level check or CI compile is not hardware validation.
