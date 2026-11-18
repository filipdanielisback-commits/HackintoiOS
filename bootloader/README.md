# Boot-chain research and UEFI prototype

**Status: early AArch64 UEFI application; QEMU execution test is being added. This is not a Moto G60 phone bootloader.**

This directory tracks the target device's boot architecture and develops a safe, isolated UEFI prototype.

## Current prototype

- `HackintoiOSLoader.efi` is an AArch64 UEFI application.
- It displays a simple text menu using the UEFI console.
- It accepts UEFI console key input for a basic menu demonstration.
- GitHub Actions builds the application and validates its ARM64 PE/COFF format.
- A separate QEMU test attempts to launch the application under emulated AArch64 UEFI firmware.

## What a successful QEMU test means

It demonstrates only that the UEFI application can be launched by the selected emulated firmware. It does **not** establish that the Moto G60 provides UEFI, that Motorola's boot chain can launch this application, or that XNU can boot.

## Not implemented

- No Moto G60 / HANOIP firmware integration.
- No replacement for Motorola's existing bootloader.
- No XNU kernel loading or handoff.
- No physical Power/Volume button handling.
- No Moto G60 display, touchscreen, battery, charging, or GPU drivers.
- No flashing or installation image.

## Next milestones

1. Build and validate the AArch64 UEFI application in CI.
2. Run it under QEMU's AArch64 UEFI firmware and capture its console output.
3. Research the XT2135-2 boot stages from trustworthy, device-specific sources.
4. Define a non-destructive, device-specific feasibility assessment. Do not attempt firmware replacement or security bypass.
5. Separately inspect the genuine iPhone XR iOS 18.7.12 IPSW and record verified filesystem metadata. Keep Apple firmware payloads out of this repository.
6. Only after the boot and compatibility interfaces are evidenced, investigate a test-kernel handoff.

## Research checklist

- [ ] Find reliable documentation for the XT2135-2 boot stages.
- [ ] Record verified-boot and bootloader-lock constraints.
- [ ] Document the kernel handoff format only when supported by evidence.
- [ ] Keep experiments non-destructive and separate from normal device use.

Do not flash this `.efi` file or treat it as a phone-installable image. This project does not provide instructions for bypassing device security or flashing unverified images.
