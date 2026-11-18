# HakiOS-informed porting plan

**Official end goal:** boot a genuine iOS 18.7.12-derived Darwin user-space environment on the Motorola Moto G60 Vision (XT2135-2), using an independently developed HANOIP-compatible XNU, loader, platform configuration, and drivers.

This is a long-term engineering target, not a claim that the target is currently supported or that success is guaranteed. The project must be willing to revise or stop a path when hardware, source, licensing, or compatibility evidence does not support it.

## Reference target

- Phone: Motorola Moto G60 Vision, model XT2135-2; device family HANOIP.
- iOS reference: iOS 18.7.12, build 22H390, from the iPhone XR (iPhone11,8) restore family.
- The iPhone XR restore image is a source of research metadata and user-space compatibility evidence. It is not a Moto G60 firmware image, and its device-specific firmware, kernel configuration, or boot chain must not be assumed to work on HANOIP.
- The existing XNU pin `xnu-11215.1.10` was selected for the original iOS 18.0 / Darwin 24.0.0 research baseline. It is **not yet approved as the final 18.7.12 kernel baseline**. Verify the exact Darwin/XNU build relationship before changing the pin.

## What HakiOS demonstrates

The public HakiOS documentation describes a layered XNU-on-Qualcomm-phone project:

1. A common XNU port and original kernel-side additions.
2. A loader (`xnuloader`) that prepares the handoff to XNU.
3. A firmware/boot stage, using UEFI or U-Boot depending on the device.
4. Shared SoC support plus a separate phone-specific configuration and device data.
5. Drivers enabled individually through a configuration system.
6. A Darwin user-space image supplied by the user, kept separate from the project's source.
7. QEMU as an earlier development and regression target.

HakiOS documents a working POCO X5 Pro 5G (`redwood`) target and QEMU. Its phone-specific code is not a Moto G60 port. We may learn from its architecture and engineering sequence, but must independently implement and validate HANOIP support.

## Current HackintoiOS baseline

| Area | What exists | What is still missing |
|---|---|---|
| XNU | Pinned upstream research reference; empty patch series | Verified 18.7.12-compatible baseline, original HANOIP changes, reproducible relevant build |
| Linux reference kernel | HANOIP Linux source/build workflow | This is not XNU and cannot substitute for it |
| Bootloader | Basic AArch64 UEFI console application and artifact checks | Real loader protocol, kernel loading/handoff, device integration |
| Firmware | Research notes and UEFI prototype | Verified, suitable HANOIP firmware path; availability is unknown |
| Device/SoC | XT2135-2 profile, HANOIP family and source references | Verified device tree, board revision, resource map and subsystem evidence |
| Drivers | Hardware research notes | Original, individually tested XNU-facing drivers |
| Darwin user space | IPSW inspection/indexing tools and host smoke-test scaffolding | Verified filesystem metadata and a compatible startup environment; no proprietary payloads in this repository |
| QEMU | UEFI prototype test being established | A meaningful open-kernel/loader test platform and automated regression coverage |
| CI | Separate documentation, Linux, XNU-baseline, sysimage and UEFI checks | End-to-end tests that prove each added capability without overstating what they prove |

## Implementation sequence

### Milestone 0 — architecture and evidence
- Keep this plan as the source of truth for scope and status.
- Inventory HakiOS's common, SoC, device, firmware, loader, driver, user-space, sysimage, and QEMU layers.
- Map each architectural responsibility to an original HackintoiOS component.
- Mark every hardware fact as verified, inferred, or unknown, with its source.
- Do not create empty directories merely to imitate another project.

**Done when:** the repository map and compatibility matrix identify the owner, inputs, outputs, evidence, and test for every planned subsystem.

### Milestone 1 — version and source baseline
- Identify the exact Darwin/XNU generation associated with iOS 18.7.12 build 22H390 using authoritative release/build evidence.
- Check whether the currently pinned public XNU source is the correct baseline or whether a later compatible public source revision exists.
- Record source provenance, license obligations, build constraints, and any unavailable proprietary dependencies.
- Keep the Linux reference-kernel build clearly separate.

**Done when:** the selected XNU source reference is justified by evidence and its limits are documented.

### Milestone 2 — open development target in QEMU
- Define a small, original ARM64 test environment that does not require Apple firmware or a phone.
- Build and test the loader/kernel interface in emulation.
- Add automated checks for boot protocol structures, memory-map handling, logging, and clean failure paths as those components are implemented.

**Done when:** the open test kernel and loader reach a documented milestone in QEMU. This is not proof of iOS user-space or Moto G60 support.

### Milestone 3 — HANOIP platform description
- Obtain and review trustworthy XT2135-2/HANOIP device-tree and public kernel-source evidence.
- Separate SoC-wide facts from phone-specific board facts.
- Document memory, interrupt, timer, storage, display, input, power, and firmware dependencies.
- Do not invent addresses, interrupts, pin assignments, or boot arguments.

**Done when:** every platform value used by code has a traceable source and unknowns remain explicitly disabled.

### Milestone 4 — original driver bring-up
- Start with the minimum platform services needed for safe kernel operation.
- Add each subsystem independently, with a documented source for every hardware-specific value.
- Keep unsupported hardware disabled rather than enabling another phone's driver.
- Record build, emulation, and physical-device evidence separately.

**Done when:** a driver is marked working only after the corresponding behavior is observed and recorded on the intended target.

### Milestone 5 — loader and device handoff
- Implement the loader only against a documented and testable firmware interface.
- Validate kernel image loading, memory layout, device-tree handoff, and error handling in emulation first.
- Treat Moto G60 firmware/boot-chain compatibility as an unresolved research question.
- Do not replace device firmware, bypass security controls, or write unverified images to the phone.

**Done when:** the loader-to-kernel handoff is reproducible in QEMU and a separate, reviewed feasibility assessment supports any later device test.

### Milestone 6 — Darwin user-space compatibility
- Inspect only metadata and files that can be handled lawfully and without bypassing encryption or access controls.
- Keep Apple restore payloads, keys, firmware, and proprietary binaries out of this public repository.
- Determine which user-space components can run on the HANOIP platform and which depend on Apple-specific hardware or services.
- Implement original compatibility support only where interfaces and licensing permit.

**Done when:** the required user-space inputs and incompatibilities are documented, and a permitted test reaches a reproducible startup milestone.

### Milestone 7 — integrated validation
- Test the open kernel, loader, device configuration, and permitted Darwin user-space path together.
- Publish exact test conditions and logs, including failures.
- Do not describe a QEMU pass, source checkout, successful Linux build, or artifact upload as a phone boot.

**Final success criterion:** independently reproducible evidence that the intended iOS 18.7.12-derived Darwin environment reaches its documented operating state on the exact Moto G60 XT2135-2 target. Until then, the project remains experimental.

## Non-goals and boundaries

- Reproducing Apple's complete proprietary source code.
- Distributing Apple's iOS, firmware, keys, certificates, or restore payloads.
- Claiming Apple ID, activation, App Store, cellular, camera, GPU, or other services work without direct evidence.
- Copying HakiOS code or its POCO X5 Pro / SC7280 device-specific values and presenting them as HANOIP support.
- Flashing, replacing firmware, bypassing verified boot, or making unverified writes to the phone as part of this development plan.
