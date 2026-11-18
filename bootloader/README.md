# Boot-chain research and UEFI development prototype

**Status: AArch64 UEFI application with a basic menu and firmware-environment report. It is not a Moto G60 phone bootloader and does not load XNU.**

## Current implementation

- EDK II UEFI application targeting AArch64.
- Interactive UEFI console menu.
- Reports firmware vendor/revision, configuration-table count, and availability of console and boot-services interfaces.
- Reports the HANOIP target and explicitly marks native UEFI and device integration as unverified.
- GitHub Actions builds the EFI executable, checks its PE/COFF architecture, and launches it under emulated AArch64 UEFI firmware.

## Development boundary

The current QEMU `virt` machine is a development harness, not a hardware model of the Moto G60. A successful QEMU run proves only that the application runs under that emulated firmware. It does not establish compatibility with Motorola firmware or the XT2135-2 boot chain.

## Not implemented

- HANOIP-specific firmware integration or a Moto G60 boot image.
- XNU kernel loading, memory-map preparation for XNU, or kernel handoff.
- Device-tree/ACPI platform handoff for HANOIP.
- Display, touchscreen, storage, Wi-Fi, audio, power, or thermal drivers.
- APFS filesystem support.
- A phone-installable or flashable image.

## Next engineering milestones

1. Keep the UEFI application building and passing the QEMU smoke test.
2. Add deterministic tests for its firmware report and error handling where feasible.
3. Document the XT2135-2 boot architecture from trustworthy source evidence without attempting firmware replacement or security bypass.
4. Establish an XNU build-and-boot experiment in QEMU independently of phone support.
5. Design a HANOIP platform interface only from verified board and firmware facts.
6. Treat Android boot-image packaging as a later, separately validated artifact format—not as proof of device bootability.

## Safety and compatibility

Do not flash this EFI application or any generated image to a phone. This project does not provide instructions for bypassing device security, unlocking protected boot stages, or flashing unverified firmware. All current execution tests remain in CI/QEMU.
