# HANOIP XNU resource inventory

**Status: partial, source-backed board inventory; not an XNU platform implementation.**

This is the first source-backed inventory for the Motorola Moto G60 Vision (XT2135-2). It separates the HANOIP board overlays from the shared Qualcomm SoC description. Linux device-tree values are evidence about hardware; they are not ready-made XNU configuration or drivers.

## Source baseline

The inspected Linux source is the community `android_kernel_motorola_sm6150` tree, branch `lineage-20`, at the project-pinned source revision `5b04fac0cb2a8311ae69c8644384426e838d91fe`.

- [QCOM device-tree build Makefile](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/Makefile)
- [SDMMAGPIE shared SoC device tree](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi)
- [HANOIP common board overlay](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-common-overlay.dtsi)
- [HANOIP EVT1 overlay](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-evt1-overlay.dts)
- [HANOIP DVT1 overlay](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt1-overlay.dts)
- [HANOIP DVT2 overlay](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt2-overlay.dts)
- [HANOIP Linux defconfig](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/configs/vendor/hanoip_defconfig)

The source tree and defconfig are named `sm6150`, but the actual device-tree base describes `SDMMAGPIE` (`qcom,sdmmagpie`). The HANOIP overlay is a separate board layer. Do not use the repository name alone as the XNU platform identity. The automated audit now walks quoted includes recursively from the shared SoC tree, common HANOIP overlay, and each engineering/camera overlay, recording the include graph and any missing or unsafe paths. This is source-closure evidence only; it does not merge or compile the device tree.

## Verified device-tree observations

| Item | Source observation | Confidence / limit |
|---|---|---|
| Shared SoC-tree identity | `sdmmagpie.dtsi` declares model `Qualcomm Technologies, Inc. SDMMAGPIE`, compatible `qcom,sdmmagpie`, and `qcom,msm-name = "SDMMAGPIE"` | Verified in the pinned shared SoC tree |
| HANOIP board identity | HANOIP overlay declares `model = "hanoip"` | Verified in board overlay |
| Qualcomm platform ID | HANOIP overlay declares `qcom,msm-id = <365 0x0>` | Verified in board overlay; not an XNU identifier |
| Engineering board variants | Makefile lists EVT1, DVT1, and DVT2 HANOIP overlays; their board IDs are respectively `<0x4C 0xA100>`, `<0x4C 0xB100>`, and `<0x4C 0xB200>` | Verified source values; which variant matches this XT2135-2 unit is unknown |
| Shared interrupt parent | `sdmmagpie.dtsi` sets `interrupt-parent = <&pdc>` | Verified in shared SoC include; actual boot-time routing and XNU integration are not established |
| CPU interface | Shared SoC include declares ARMv8 CPU nodes and PSCI enable method | Verified in shared include; firmware handoff and online topology on this unit remain unverified |
| Serial alias | Shared SoC include aliases `serial0` to `qupv3_se8_2uart` | Verified in shared include; does not prove this UART is enabled or available as a console |
| HANOIP overlay composition | Common overlay includes Motorola common, audio, fingerprint, panel, battery/thermal, sensor, touchscreen, and HANOI audio overlays | Verified include list; included files still need recursive review before using any values |
| Linux architecture config | HANOIP defconfig enables `CONFIG_ARCH_QCOM`, `CONFIG_ARCH_SM6150`, and `CONFIG_ARCH_SDMMAGPIE` | Linux config only; these symbols are not XNU platform identifiers |
| Linux CPU limit | HANOIP defconfig sets `CONFIG_NR_CPUS=8` | Linux configuration evidence only; actual online CPU topology must be independently verified |

## Explicitly unresolved HANOIP facts

- Exact board revision / which EVT or DVT overlay applies to the user's XT2135-2.
- Complete overlay chain and final merged device tree for the exact target.
- Actual RAM banks, reserved-memory regions, and boot-time memory map delivered to a new kernel.
- Enabled CPU topology and firmware-provided CPU state.
- Interrupt-controller instance, interrupt routing, and timer configuration as delivered at boot.
- Whether the serial alias is enabled and usable during a custom kernel handoff.
- Display controller, panel, framebuffer handoff, and GPU identity.
- UFS controller instance, power/clock dependencies, and partition-independent read-only discovery contract.
- Exact Wi-Fi and Bluetooth chip identities and their bus connections.
- PMIC, regulators, clocks, resets, GPIOs, and thermal sensors.
- Exact firmware-to-loader and loader-to-kernel handoff contract.

## Implementation gate

Do not add HANOIP register addresses, interrupt numbers, clock IDs, GPIOs, memory ranges, or driver enablement based only on this partial inventory.

Next, recursively inspect the HANOIP common overlay and all included SoC/board files, then determine which engineering overlay matches the exact XT2135-2 source/firmware evidence. Only then define an original, minimal XNU platform contract. Generic bring-up remains in QEMU; this inventory does not authorize changes to phone firmware or partitions.

## Relationship to the port

- [HANOIP XNU kernel work plan](HANOIP_KERNEL_PLAN.md)
- [Adreno 618 hardware research](ADRENO618_HARDWARE_RESEARCH.md)
- [Overall porting plan](PORTING_PLAN.md)
- [XNU version mapping](../xnu/ios-18.7.12-version.md)
