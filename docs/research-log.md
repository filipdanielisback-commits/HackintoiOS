# Research log

Use this file to record dated findings. Every technical claim should include a source and a confidence level.

## 2026-11-16 — Project initialized

- Target selected: Motorola Moto G60 family, exact model XT2135-2.
- Initial scope: research and documentation.
- No device-specific hardware inventory had yet been independently verified.

## 2026-11-16 — Moto G60 Vision and hanoip kernel baseline identified

- Finding: Motorola's EU declaration identifies XT2135-2 as Moto G60 Vision.
- Source: https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf
- Applies to: exact model XT2135-2.
- Confidence: high.

- Finding: the public Motorola G40 Fusion / G60 community device tree uses codename `hanoip`; its BoardConfig inherits the shared `sm6150` platform tree and selects `vendor/hanoip_defconfig`.
- Source: https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip/blob/lineage-20/BoardConfig.mk and https://github.com/motorola-sm6150-devs/android_device_motorola_sm6150-common/blob/lineage-20/BoardConfigCommon.mk
- Applies to: Moto G40/G60 hanoip family; exact target-unit match still to be checked.
- Confidence: high for the source-tree configuration.

- Finding: a public ARM64 kernel source tree contains `vendor/hanoip_defconfig`; its Makefile reports Linux 4.14.326. The selected source commit is `5b04fac0cb2a8311ae69c8644384426e838d91fe`.
- Source: https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/tree/lineage-20
- Applies to: community kernel baseline for the hanoip device family.
- Confidence: high for source contents; hardware boot compatibility is not established.

- Finding: the shared Android tree uses `sm6150` as its platform identifier. Do not conflate this with the marketing SoC name.
- Source: shared BoardConfigCommon.mk and the hanoip defconfig.
- Applies to: shared Android device/kernel source tree.
- Confidence: high.

- Follow-up: run the pinned-source build in GitHub Actions, then audit target-unit identity, DTBs, modules and boot-image metadata before any hardware compatibility claim.

## Entry template

```text
### YYYY-MM-DD — Short title
- Finding:
- Source:
- Applies to:
- Confidence: high / medium / low
- Follow-up:
```
