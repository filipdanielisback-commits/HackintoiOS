# HANOIP Wi-Fi hardware research

**Status: source-backed driver-stack inventory; exact radio silicon and transport are not yet verified. No Wi-Fi hardware driver is implemented.**

Target: Motorola Moto G60 Vision XT2135-2, HANOIP. This document records evidence from the public HANOIP device configuration and its matching community kernel source. It deliberately distinguishes the WLAN software stack from the physical radio part number.

## Pinned source baselines

- Kernel/device-tree source: [motorola-sm6150-devs/android_kernel_motorola_sm6150](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150), commit `5b04fac0cb2a8311ae69c8644384426e838d91fe`.
- HANOIP Android device configuration: [motorola-sm6150-devs/device_motorola_hanoip](https://github.com/motorola-sm6150-devs/device_motorola_hanoip), commit `514e0261a117a0c7e7fa3cc3cd44f80819b0b779`.
- The kernel source tree identifies the shared platform through SDMMAGPIE device-tree files. Do not infer the exact radio from the repository's `sm6150` name.

## What is confirmed

### 1. Qualcomm CLD3 WLAN software stack

The HANOIP device's `modules.load` requests `qca_cld3_wlan.ko`. Its BoardConfig maps the Android module name `wlan.ko` to that kernel module.

The pinned HANOIP kernel defconfig enables:

- `CONFIG_QCA_CLD_WLAN=m`
- `CONFIG_CLD_LL_CORE=y`
- `CONFIG_CNSS_GENL=y`
- `CONFIG_ICNSS=y`
- `CONFIG_ICNSS_QMI=y`
- `CONFIG_WCNSS_MEM_PRE_ALLOC=y`

The CLD3 Kbuild selects `MODNAME=wlan` and `CONFIG_QCA_CLD_WLAN=m`. This confirms a Qualcomm CLD WLAN driver stack is part of the HANOIP Linux configuration. It does **not** uniquely identify the physical Wi-Fi chipset.

### 2. WLAN memory and inter-processor signalling

The shared SDMMAGPIE device tree defines:

- `wlan_msa_mem` at physical base `0x97500000`, size `0x180000` (1.5 MiB), marked `removed-dma-pool` and `no-map`.
- An SMP2P WLAN inbound state entry named `wlan`.

These are evidence of reserved WLAN memory and an application-processor/modem-side signalling path in the Linux platform description. They are not a complete DMA allocator, firmware map, or XNU memory contract.

### 3. Bluetooth is described separately

The shared SoC device tree contains a Bluetooth node:

- compatible: `qca,wcn3990`
- label: `bluetooth`
- separate IO, core, PA and crystal supply references.

This confirms the Bluetooth-side WCN3990 description. It does **not**, by itself, prove that the Wi-Fi function uses the same silicon or establish the Wi-Fi bus. Keep the Wi-Fi and Bluetooth inventories separate until a source explicitly connects them.

### 4. Bus and power evidence is incomplete

The kernel tree contains Qualcomm CNSS PCI and SDIO support code. The generic CNSS Kconfig describes both PCIe and SDIO transport variants. The HANOIP defconfig enables PCI support and ICNSS, but the reviewed HANOIP device-tree files do not yet establish a final Wi-Fi transport endpoint, its bus address, reset GPIO sequence, regulator set, or radio-specific interrupt mapping.

Therefore, **do not assume PCIe, SDIO, WCN3990 Wi-Fi, QCA6174, QCA6390, or any other exact radio model** from the CLD3 module name alone.


### 5. Official radio-capability declaration

Motorola's [XT2135-2 EU Declaration of Conformity](https://en-us.support.motorola.com/ci/fattach/get/79315385/1664922506/redirect/1/filename/XT2135-2_Moto%2BG60%2BVision%2BMC38C%2BRED%2BDoC.pdf) identifies the market model as moto g60 XT2135-2 and lists IEEE 802.11a/b/g/n/ac and Bluetooth 5.0. This confirms advertised radio capabilities for the model, but it does not identify the Wi-Fi chipset, bus, firmware package or the exact component fitted to this individual unit.

## What is not yet known

1. Exact Wi-Fi silicon/module part number for this XT2135-2 hardware revision.
2. Whether the Wi-Fi function is PCIe, SDIO, or another supported transport.
3. The final HANOIP merged device-tree node and board-variant applicability.
4. Radio-specific register, interrupt, reset and regulator resources.
5. Required firmware filenames, versions, provenance and licensing.
6. WLAN DMA/IOMMU stream IDs, address width, coherency and memory ownership.
7. MAC address source, calibration/NVM data and regulatory-domain handoff.
8. Whether the required radio firmware can be supplied legally without bundling proprietary blobs.

## XNU driver design gates

A future HANOIP XNU Wi-Fi implementation needs more than a CLD3 name or a generic network interface. Before hardware initialization, establish the exact radio and transport, then document:

- bus enumeration and resource ownership;
- power/reset sequencing and clock dependencies;
- firmware loading contract and error recovery;
- DMA/IOMMU mapping and cache-coherency rules;
- interrupt handling and sleep/wake behaviour;
- packet queues, transmit/receive descriptors and synchronization;
- regulatory and calibration data provenance;
- a portable network-interface boundary for Darwin networking.

Do not port Linux kernel APIs directly into XNU. Use the Linux driver as behavioural evidence only; do not copy code without a separate licence and compatibility review. No firmware blobs or calibration data are included in this research.

## Next research steps

1. Trace the HANOIP vendor firmware and boot configuration references to identify the radio family and firmware names.
2. Inspect the exact ICNSS/QMI integration and all applicable device-tree includes for a Wi-Fi bus endpoint.
3. Cross-check the candidate radio and transport against the exact XT2135-2 firmware/source baseline.
4. Publish a machine-readable, evidence-linked Wi-Fi resource contract with unknown runtime values disabled.
5. Only then begin a portable XNU-side bus/device and firmware-management layer, with host tests before any hardware-specific initialization.

## Evidence links

- [HANOIP kernel defconfig: CLD/ICNSS options](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/configs/vendor/hanoip_defconfig#L320-L326)
- [HANOIP kernel defconfig: QCA CLD WLAN module](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/configs/vendor/hanoip_defconfig#L527-L535)
- [WLAN reserved memory and Bluetooth WCN3990 node](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi#L553-L557)
- [Bluetooth WCN3990 supply description](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi#L1118-L1132)
- [WLAN SMP2P state entry](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi#L2013-L2017)
- [HANOIP module load list](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/514e0261a117a0c7e7fa3cc3cd44f80819b0b779/modules.load)
- [HANOIP module aliases and load configuration](https://github.com/motorola-sm6150-devs/device_motorola_hanoip/blob/514e0261a117a0c7e7fa3cc3cd44f80819b0b779/BoardConfig.mk)
- [CLD3 module build configuration](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/drivers/staging/qcacld-3.0/Makefile)
