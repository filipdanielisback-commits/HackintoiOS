# HANOIP device-tree evidence audit

## Status and scope

This is a source-level audit of the public Motorola/Qualcomm Linux kernel tree, branch `lineage-20`. It records hardware-description evidence relevant to future XNU research. It does **not** establish the exact device tree loaded by the user's retail handset, recover the bootloader handoff contract, or prove that XNU can boot.

No phone partitions are read or changed by this audit. No boot image is produced.

## Source identity

- Repository: [motorola-sm6150-devs/android_kernel_motorola_sm6150](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150)
- Branch inspected: `lineage-20`
- HANOIP overlay family: `arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-*`
- SoC-level description: `arch/arm64/boot/dts/qcom/sdmmagpie.dtsi`
- Motorola common base: `arch/arm64/boot/dts/qcom/sdmmagpie-moto-base.dtsi`
- HANOIP kernel configuration: `arch/arm64/configs/vendor/hanoip_defconfig`

The device-tree files identify the platform as SDMMAGPIE and include HANOIP-specific overlays. The community kernel directory name `sm6150` should not be treated as the handset's commercial SoC model.

## Findings confirmed in source

| Area | Source evidence | What can safely be concluded |
| --- | --- | --- |
| Board identification | `sdmmagpie-hanoip-dvt2-overlay.dts` sets `model = "hanoip"`, `qcom,msm-id = <365 0x0>`, and `qcom,board-id = <0x4C 0xB200>`. | A DVT2 HANOIP overlay exists with those identifiers. This does not prove this particular handset selects DVT2. |
| Overlay composition | The DVT2 overlay includes `sdmmagpie-hanoip-common-overlay.dtsi` and a DVT2 camera-sensor overlay. The common overlay includes Motorola common, audio, panel, battery/thermal, sensor and touchscreen descriptions. | The platform description is layered; the HANOIP overlay alone is not the complete hardware description. |
| CPU topology | `sdmmagpie.dtsi` declares CPU nodes CPU0 through CPU7 and a CPU map. | The source describes eight logical CPU nodes. Runtime online state and exact retail-device topology are not established by this source audit. |
| Interrupt controller | The SoC DTSI declares `arm,gic-v3` at `0x17a00000` and a Qualcomm PDC interrupt controller. | GICv3/PDC are represented in this Linux hardware description. XNU interrupt-controller support and exact handoff remain unimplemented/unverified. |
| Timer | The DTSI declares `arm,armv8-timer` with four PPI interrupts and a 19.2 MHz clock-frequency property. | The Linux description expects the ARMv8 architectural timer. This is not proof that XNU can initialize it on the phone. |
| Boot arguments | The DTSI's `chosen` node contains Linux-specific `rcupdate.rcu_expedited=1 rcu_nocbs=0-7`. | These are Linux kernel arguments, not a reusable XNU boot-argument contract. |
| Reserved memory | The Motorola base DTSI and SoC DTSI declare multiple `reserved-memory` regions, including no-map/removed-DMA-pool regions for firmware and other platform clients. | Memory must not be treated as one flat free RAM range. Exact usable memory and ownership need a complete, firmware-matched map before any XNU allocator work. |
| Console aliases | The SoC DTSI aliases `serial0` to `qupv3_se8_2uart`. | A UART alias exists in the Linux DTSI. Its physical accessibility, pinmux, console configuration and usefulness for independent XNU diagnostics are not yet verified. |
| Kernel configuration | `hanoip_defconfig` enables SDMMAGPIE architecture support, `CONFIG_NR_CPUS=8`, `CONFIG_HANOIP_DTB=y`, MSM GENI serial, SDMMAGPIE pinctrl, and ARM GIC-related support. | This corroborates Linux's expected platform support, not XNU driver availability. |

## Important limits

1. The DVT1, DVT2 and EVT1 HANOIP overlays are distinct source files. The firmware build string alone does not tell us which overlay was selected by the phone's boot chain.
2. A Linux DTS describes devices and resources for that Linux kernel. It is not automatically the device tree passed to another kernel, and Linux-specific properties/arguments must not be copied into XNU as if they were an Apple boot protocol.
3. The source files do not document the full bootloader handoff: entry address/state, exception level, cache/MMU state, exact FDT pointer convention, loaded image layout, or all firmware-reserved memory.
4. Address and clock properties in DTS are evidence to investigate, not permission to access hardware directly. The corresponding XNU code and safe initialization order do not exist yet.
5. No physical-device test has been performed. No XNU code, device tree, boot image, or installation procedure is created by this audit.

## Consequences for the porting plan

- Keep the first XNU platform work blocked on a verified boot contract and a complete, firmware-matched memory map.
- Preserve the Linux DTS as a reference and record the exact upstream file/revision for each fact.
- Do not hard-code the DVT2 board ID or assume the retail phone uses that overlay.
- Before implementing interrupt or timer code, reconcile the firmware's actual handoff with the GIC/PDC and ARMv8 timer descriptions.
- Before memory-management work, account for every reserved region and its owner; do not infer free RAM by subtracting only the obvious firmware ranges.
- Treat the UART alias as a candidate for later investigation, not as a confirmed working debug console.

## Source links

- [HANOIP DVT2 overlay](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt2-overlay.dts)
- [HANOIP common overlay](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-common-overlay.dtsi)
- [SDMMAGPIE SoC DTSI](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi)
- [Motorola base DTSI](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/boot/dts/qcom/sdmmagpie-moto-base.dtsi)
- [HANOIP defconfig](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/lineage-20/arch/arm64/configs/vendor/hanoip_defconfig)
