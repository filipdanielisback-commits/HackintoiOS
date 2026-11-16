# Moto G60 — XT2135-2

**Status: research scaffold only. Not bootable. No device-specific kernel configuration exists yet.**

This is the primary HackintoiOS device-port target. The directory deliberately starts with documentation rather than guessed boot settings or copied configuration from another phone.

## Target identity

| Field | Current information | Confidence |
|---|---|---|
| Manufacturer / product | Motorola Moto G60 | Model-family identification |
| Model | XT2135-2 | Confirmed target model |
| SoC | Qualcomm Snapdragon 732G (SM7150-AC family) | Reported by public device specifications; verify on the actual unit |
| GPU | Qualcomm Adreno 618 | Reported; verify against the exact board revision |
| Board / platform codename | Not yet verified | Open |
| Bootloader and partition layout | Not yet documented | Open |
| Device-tree source and revision | Not yet identified | Open |
| RAM/storage configuration | Not yet verified for target unit | Open |

Do not treat reported SoC details as sufficient to select a kernel target. Exact board identity, device-tree compatibility, boot image format, bootloader behavior, and firmware dependencies must be established independently.

## Porting principles

1. Keep all Moto G60-specific material in this directory.
2. Record source URLs, revisions, and verification status for every hardware claim.
3. Do not copy HakiOS's POCO X5 Pro / SC7280 device configuration. The Moto G60 is a different platform.
4. Do not add fabricated addresses, register maps, firmware blobs, partition offsets, or boot arguments.
5. Keep early work to source inspection, reproducible builds, static checks, and emulator tests.
6. Never describe a generated artifact as bootable until it has passed appropriate device-specific validation.

## Milestones

- [ ] Verify exact board/platform identity from trustworthy device evidence.
- [ ] Identify the matching device-tree source and license.
- [ ] Document boot-chain and image-format requirements from authoritative sources.
- [ ] Map required hardware blocks and existing open drivers.
- [ ] Define a minimal, reviewable device configuration.
- [ ] Build the HackintoiOS kernel target in CI.
- [ ] Add automated tests for configuration and packaging.
- [ ] Establish a safe, independently reviewed hardware validation plan.

## Current build status

There is no HackintoiOS kernel implementation or Moto G60 boot image in this directory yet. The repository's initial CI checks documentation and device-profile consistency only. Passing those checks does not compile a kernel, emulate the phone, or establish bootability.

## Research log

Add dated entries to [the project research log](../../docs/research-log.md). Prefer primary sources such as Motorola documentation, Linux device-tree sources, Qualcomm documentation, and upstream driver code.
