# HANOIP XNU resource inventory

**Status: partial evidence inventory; not an XNU platform implementation.**

This is the first source-backed inventory for the Moto G60 Vision (XT2135-2). It deliberately separates generic SM6150-family Linux device-tree evidence from confirmed HANOIP board facts. Linux descriptions are evidence about hardware, not ready-made XNU configuration or drivers.

## Source baseline

The inspected Linux source is the community `android_kernel_motorola_sm6150` tree, branch `lineage-20`, at the project-pinned source revision `5b04fac0cb2a8311ae69e8644384426e838d91fe`.

- [Generic SM6150 device-tree include](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69e8644384426e838d91fe/arch/arm64/boot/dts/qcom/sm6150.dtsi)
- [HANOIP Linux defconfig](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69e8644384426e838d91fe/arch/arm64/configs/vendor/hanoip_defconfig)

The HANOIP defconfig is a Linux build configuration. It is not an XNU configuration and must not be copied into XNU.

## Observed generic SoC-tree facts

| Item | Source observation | Confidence / limit |
|---|---|---|
| Device-tree root identity | `model = "Qualcomm Technologies, Inc. SM6150"`; `compatible = "qcom,sm6150"`; `qcom,msm-name = "SM6150"` | Verified in the shared SoC include; does not independently identify the exact retail SoC or board |
| CPU node interface | CPU nodes use `compatible = "arm,armv8"` and `enable-method = "psci"` | Verified in shared include; actual firmware handoff on XT2135-2 remains unverified |
| Interrupt parent | Root node assigns `interrupt-parent = <&pdc>` | Verified in shared include; board routing and XNU interrupt-controller integration are not established |
| Serial alias | `serial0` aliases `qupv3_se0_2uart` | Verified in shared include; does not prove which console is enabled or usable on this phone |
| UFS alias | `ufshc1` aliases `ufshc_mem` | Verified in shared include; no XNU storage driver or safe device-level access is established |
| Linux architecture config | HANOIP defconfig enables `CONFIG_ARCH_QCOM`, `CONFIG_ARCH_SM6150`, and `CONFIG_ARCH_SDMMAGPIE` | Verified Linux config only; these symbols are not XNU platform identifiers |
| Linux CPU limit | HANOIP defconfig sets `CONFIG_NR_CPUS=8` | Linux configuration evidence only; actual online CPU topology must be independently verified |

## Explicitly unresolved HANOIP facts

The generic SoC include is insufficient to implement a board-specific XNU platform. The following remain unknown until the exact HANOIP board device-tree source and its dependencies are inspected:

- XT2135-2 board compatible string and exact board revision.
- Actual RAM banks, reserved-memory regions, and boot-time memory map.
- Enabled CPU topology and firmware-provided CPU state.
- Interrupt-controller instance, interrupt routing, and timer configuration as delivered at boot.
- Enabled debug UART, its pinmux, clock, and usable console path.
- Display controller, panel, framebuffer handoff, and GPU identity.
- UFS controller instance, power/clock dependencies, and partition layout.
- Wi-Fi and Bluetooth chip identities and their bus connections.
- PMIC, regulators, clocks, resets, GPIOs, and thermal sensors.
- Exact firmware-to-loader and loader-to-kernel handoff contract.

A file lookup for `arch/arm64/boot/dts/qcom/hanoip.dts` and `hanoip.dtsi` in the inspected tree did not find either path. This only means those assumed paths were not present; it does not prove the device tree is absent or that another source path does not exist.

## Implementation gate

Do not add HANOIP register addresses, interrupt numbers, clock IDs, GPIOs, memory ranges, or driver enablement based only on this partial inventory.

The next platform-code gate is to locate and inspect the exact XT2135-2 board device tree (including included files and overlays), then trace each required value to the pinned kernel source. Only after that should we define an original, minimal XNU platform contract. Generic bring-up remains in QEMU; this inventory does not authorize changes to phone firmware or partitions.

## Relationship to the port

- [HANOIP XNU kernel work plan](HANOIP_KERNEL_PLAN.md)
- [Overall porting plan](PORTING_PLAN.md)
- [XNU version mapping](../xnu/ios-18.7.12-version.md)
