# Moto G60 Vision — XT2135-2

**Status: research scaffold only. Kernel baseline identified; CI build is being established. Not a bootable HackintoiOS port.**

This is the primary HackintoiOS device-port target. There is no HackintoiOS kernel implementation yet; the current kernel work is a Linux reference build only.

## Target identity

| Field | Current information | Confidence |
|---|---|---|
| Manufacturer / product | Motorola Moto G60 Vision | High; Motorola EU declaration |
| Model | XT2135-2 | High; confirmed on the target phone in Settings → About phone |
| Android version | 12 | Confirmed on target phone |
| Android security update | 2023-11-01 | Confirmed on target phone |
| Firmware build | `S2RIS32.32-20-9-9-2-3` | Confirmed on target phone |
| Software channel | `reteu` | Confirmed on target phone; European retail channel |
| Firmware family codename | hanoip | Motorola kernel-source request for this exact build identifies HANOIP |
| Android device codename | hanoip | High for the Moto G40/G60 device family; exact target-unit codename not independently read |
| Qualcomm platform tree name | sm6150 | High; shared Motorola device-tree BoardConfig |
| Marketing SoC | Snapdragon 732G; commonly identified as SM7150-AC | Medium; verify against the target unit's reported hardware |
| GPU | Adreno 618 | Medium; family specification, verify exact board |
| Kernel base | Motorola SM6150-family Linux 4.14.326 community source tree | High for the referenced source branch |
| Device kernel config | `vendor/hanoip_defconfig` | High; present in the referenced kernel tree |
| Bootloader / partition details | Not yet verified for XT2135-2 | Open |
| RAM/storage configuration | Not yet verified for target unit | Open |

**Important naming distinction:** `sm6150` is the platform name used by the shared Android device/kernel tree. It must not be confused with the marketing SoC identifier. The device-family specifications identify the Snapdragon 732G. Do not infer register maps or silicon revisions from the tree name alone.

## Firmware and kernel-source match

The target phone reports Android 12, security update 2023-11-01, build `S2RIS32.32-20-9-9-2-3`, and channel `reteu`.

Motorola's public `kernel-msm` issue [#574](https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574) names the corresponding firmware package `XT2135-2_HANOIP_RETEU_12_S2RIS32.32-20-9-9-2-3` and is marked as published open-source code. This is a strong firmware-to-source reference. It does not, by itself, prove that every file in the community kernel branch is byte-for-byte identical to the firmware's shipped kernel.

## Source references

- Motorola EU declaration identifies XT2135-2 as Moto G60 Vision: https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf
- Motorola kernel source request for the exact XT2135-2 HANOIP RETEU build: https://github.com/MotorolaMobilityLLC/kernel-msm/issues/574
- Community Android device tree for Moto G40 Fusion / Moto G60 (hanoip): https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip
- Shared platform BoardConfig: https://github.com/motorola-sm6150-devs/android_device_motorola_sm6150-common/blob/lineage-20/BoardConfigCommon.mk
- Kernel source tree: https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/tree/lineage-20
- Target defconfig: https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/configs/vendor/hanoip_defconfig
- Pinned kernel source commit: `5b04fac0cb2a8311ae69c8644384426e838d91fe`

The community kernel source is a baseline reference, not an original HackintoiOS kernel. Its license and notices must remain intact. The initial HackintoiOS configuration fragment changes only the build's local version label.

## Porting principles

1. Keep Moto G60-specific configuration and notes in this directory.
2. Preserve upstream source attribution and GPL-2.0 obligations for kernel-derived work.
3. Do not copy HakiOS's POCO X5 Pro / SC7280 device configuration.
4. Do not invent addresses, register maps, firmware blobs, partition offsets, or boot arguments.
5. Treat a successful compile as a compile result only—not proof of hardware compatibility.
6. Do not create or publish a flash-ready image until the exact boot chain, image format, and device variant have been independently validated.

## Milestones

- [x] Identify Motorola model XT2135-2.
- [x] Confirm the target phone reports XT2135-2 in Settings → About phone.
- [x] Record Android version, security patch, build number, and software channel from the target phone.
- [x] Match the reported firmware build to Motorola's published kernel-source request.
- [x] Identify the hanoip device-family tree and matching defconfig.
- [x] Locate a public ARM64 kernel source baseline.
- [ ] Confirm exact target-unit SoC and board revision.
- [ ] Complete a reproducible kernel compile in GitHub Actions.
- [ ] Add HackintoiOS-specific kernel patches beyond the build-label fragment.
- [ ] Map device-tree and driver dependencies.
- [ ] Establish a safe, independently reviewed hardware-validation plan.

## Current build status

The repository now contains a reproducible build script and CI workflow for the referenced hanoip kernel baseline. Until GitHub Actions completes successfully, the kernel build remains unverified. Even after a successful compile, the output is not a boot image and is not confirmed bootable on XT2135-2.
