# Boot-chain research and UEFI prototype

**Status: early UEFI application prototype; not a phone bootloader yet.**

This directory tracks the target device's boot architecture and starts a separate UEFI loader project for HackintoiOS.

## Current prototype

- HackintoiOSLoader.efi is an AArch64 UEFI application.
- It displays a simple text menu using the UEFI console.
- It accepts UEFI console key input for a basic menu demonstration.
- GitHub Actions builds the application and checks that the output is an ARM64 PE/COFF executable.

## Build environment

The CI workflow uses the EDK II ArmVirtQemu platform as the build environment and builds our application module against its AArch64 configuration. This is a build target, not proof that the Moto G60 provides UEFI.

## Not implemented

- No Moto G60 / HANOIP firmware integration.
- No replacement for Motorola's existing bootloader.
- No XNU kernel loading or handoff.
- No framebuffer splash screen yet.
- No physical Power-button handling. UEFI console key input is not the same as a phone's power key.
- No flashing or installation image.

## Safety and validation

Do not flash this .efi file or treat it as a phone-installable image. The Moto G60's ability to launch a custom UEFI environment has not been established. QEMU/build success only validates the application build, not device compatibility.

## Next milestones

1. Build and inspect the AArch64 UEFI application in CI.
2. Add a QEMU UEFI execution test.
3. Implement a graphical splash/menu using UEFI Graphics Output Protocol.
4. Research a safe, device-specific way to enter a UEFI environment on HANOIP.
5. Only then investigate kernel loading and XNU handoff.

## Research checklist

- [ ] Find reliable documentation for the XT2135-2 boot stages.
- [ ] Record verified boot and bootloader-lock constraints.
- [ ] Document the kernel handoff format only when supported by evidence.
- [ ] Keep experiments non-destructive and separate from normal device use.

This project does not provide instructions for bypassing device security or flashing unverified images.
