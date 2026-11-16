# Boot-chain research

This directory is for high-level documentation of the target device's boot architecture.

## Current status

No custom bootloader, EFI implementation, boot image, or device handoff code is provided.

## Research checklist

- [ ] Find reliable documentation for the XT2135-2 boot stages.
- [ ] Record verified boot and bootloader-lock constraints.
- [ ] Document the kernel handoff format only when supported by evidence.
- [ ] Keep experiments non-destructive and separate from normal device use.

This project does not provide instructions for bypassing device security or flashing unverified images.
