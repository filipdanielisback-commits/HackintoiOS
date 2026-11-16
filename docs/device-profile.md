# Device profile: Motorola Moto G60 Vision (XT2135-2)

## Identity

- Manufacturer: Motorola Mobility
- Product: Moto G60 Vision
- Exact target model: XT2135-2
- Android device-family codename: hanoip
- Shared Android platform-tree name: sm6150
- Project phase: kernel baseline build and device research

## Verified / sourced information

Motorola's EU declaration identifies XT2135-2 as Moto G60 Vision. The community Android device tree identifies the Moto G40 Fusion / Moto G60 family as `hanoip`. Its BoardConfig inherits the shared `sm6150` platform tree and selects `vendor/hanoip_defconfig`. The corresponding public kernel tree contains that ARM64 defconfig and identifies itself as Linux 4.14.326.

The `sm6150` platform-tree naming is distinct from the marketed SoC name. Public device specifications identify the Snapdragon 732G family, often referenced as SM7150-AC, but exact silicon and board revision should still be checked against the target unit.

## Evidence

| Component | Identifier | Status | Source |
| --- | --- | --- | --- |
| Exact model | XT2135-2 / Moto G60 Vision | Officially identified | Motorola EU declaration |
| Device-family codename | hanoip | Community device tree for Moto G40/G60 family | Device tree |
| Shared platform-tree name | sm6150 | Explicit in shared BoardConfig | Common BoardConfig |
| Kernel config | vendor/hanoip_defconfig | Present in kernel source tree | Kernel source |
| Kernel source baseline | Linux 4.14.326 | Source Makefile | Kernel source |
| Marketing SoC | Snapdragon 732G / SM7150-AC family | Public specs; verify target unit | Device specifications |
| GPU | Adreno 618 | Family specification; verify target unit | Device specifications |
| RAM/storage | Not yet verified for target unit | Open | — |
| Bootloader / partition map | Not yet verified for XT2135-2 | Open | — |
| Display/touch controllers | Not yet verified | Open | — |
| Radio, audio, camera and sensor parts | Not yet verified individually | Open | — |

## Source URLs

- Motorola declaration: https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf
- Device tree: https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip
- Shared BoardConfig: https://github.com/motorola-sm6150-devs/android_device_motorola_sm6150-common/blob/lineage-20/BoardConfigCommon.mk
- Kernel source: https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150
- Hanoip defconfig: https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/configs/vendor/hanoip_defconfig

## Remaining verification

- [ ] Confirm the target unit's reported model, board, SoC and firmware build from its own system information.
- [ ] Identify exact RAM/storage variant.
- [ ] Verify DTB/DTBO and boot-image format from model-matched firmware documentation.
- [ ] Identify display, touch, Wi-Fi, Bluetooth, audio, camera and sensor components.
- [ ] Record bootloader and verified-boot constraints from official sources.

Do not infer partition offsets, memory addresses, panel IDs, or boot arguments from another model or from generic family documentation.
