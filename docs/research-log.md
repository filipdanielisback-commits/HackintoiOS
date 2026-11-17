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


## 2026-11-17 — HANOIP Wi-Fi driver source audit

- Finding: the HANOIP device tree's `modules.load` lists `qca_cld3_wlan.ko`. Its BoardConfig maps the Android vendor module name `wlan.ko` to the kernel module `qca_cld3_wlan.ko`.
- Sources: https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/modules.load and https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/lineage-20/BoardConfig.mk
- Applies to: public Moto G40/G60 HANOIP device-tree baseline.
- Confidence: high for the module mapping in that source tree.

- Finding: the pinned community kernel source includes the Qualcomm Atheros CLD WLAN driver under `drivers/staging/qcacld-3.0`. Its Kconfig symbol is `CONFIG_QCA_CLD_WLAN`; the HANOIP defconfig sets it to module mode (`CONFIG_QCA_CLD_WLAN=m`).
- Sources: https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/drivers/staging/qcacld-3.0/Kconfig, https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/drivers/staging/qcacld-3.0/Makefile, and https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/configs/vendor/hanoip_defconfig
- Applies to: community HANOIP kernel baseline.
- Confidence: high for the source configuration.

- Finding: the driver source/configuration identifies a Qualcomm CLD WLAN software stack, but the module name and these configuration files do not identify the exact physical Wi-Fi chipset/part number in this XT2135-2 unit.
- Source: same HANOIP device tree and kernel source references above; Motorola's declaration confirms WLAN standards but does not name the radio chipset: https://en-gb.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf
- Applies to: target model family; exact silicon remains unverified.
- Confidence: high that the exact chipset is not established by these files.

- Follow-up: inspect the matching vendor firmware manifest and kernel device-tree/board configuration for a specific WLAN hardware identifier. Do not claim an exact chipset or alter driver settings until a model-specific identifier is found.
