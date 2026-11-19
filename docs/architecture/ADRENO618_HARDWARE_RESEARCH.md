# Adreno 618 hardware research — Moto G60 / HANOIP

**Status: source-backed hardware inventory; not an XNU driver and not proof of hardware acceleration.**

Target: Motorola Moto G60 Vision, XT2135-2, HANOIP. The purpose of this document is to establish what the public Linux device tree and driver source say about the GPU, while keeping Linux runtime settings separate from a future XNU implementation.

## Source baseline

The primary board source is the public community kernel repository:

- Repository: `motorola-sm6150-devs/android_kernel_motorola_sm6150`
- Branch: `lineage-20`
- Pinned commit: `5b04fac0cb2a8311ae69c8644384426e838d91fe` (verified by fetching the exact commit)
- GPU device tree: [sdmmagpie-gpu.dtsi](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-gpu.dtsi)
- Shared SoC tree: [sdmmagpie.dtsi](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi)
- HANOIP overlays: [EVT1](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-evt1-overlay.dts), [DVT1](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt1-overlay.dts), [DVT2](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-dvt2-overlay.dts)
- Qualcomm Linux GPU core table: [adreno-gpulist.h](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/drivers/gpu/msm/adreno-gpulist.h)
- A6xx implementation reference: [adreno_a6xx.c](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/drivers/gpu/msm/adreno_a6xx.c)

The source repository name contains `sm6150`, but the shared device tree identifies its platform as `qcom,sdmmagpie`. Keep the repository label, SoC tree identity, and retail device marketing name distinct.

## Findings

### 1. GPU identity and generation

The HANOIP GPU node is `qcom,kgsl-3d0@5000000`, compatible with `qcom,kgsl-3d0` and `qcom,kgsl-3d`. It declares:

- `qcom,chipid = <0x06010800>`
- `qcom,highest-bank-bit = <14>`
- `qcom,min-access-length = <32>`
- `qcom,ubwc-mode = <2>`

The matching Linux GPU core table has an `ADRENO_REV_A618` entry with core 6, major 1, minor 8. It declares 512 KiB GMEM, 32-bit bus width, and the A6xx GPU implementation. This is strong source evidence for an Adreno 618-class A6xx target. The exact retail unit's live chip identity has not been independently read from hardware.

Mesa's Freedreno device table also includes GPU ID 618 in its A6xx generation-1 group. This is useful as a cross-check and a future graphics-stack reference, not a substitute for target-specific initialization evidence.

### 2. GPU register resources in the Linux device tree

The GPU node lists these named resources:

| Name | Base | Size |
|---|---:|---:|
| `kgsl_3d0_reg_memory` | `0x05000000` | `0x40000` |
| `cx_dbgc` | `0x05061000` | `0x800` |
| `cx_misc` | `0x0509e000` | `0x1000` |
| `qfprom_memory` | `0x00780000` | `0x6300` |

The node declares interrupt specifier `<0 300 IRQ_TYPE_LEVEL_HIGH>` named `kgsl_3d0_irq`. The shared SoC tree sets an inherited `interrupt-parent = <&pdc>`. These are Linux device-tree descriptions, not an XNU interrupt number or a ready-to-use MMIO mapping. The exact controller routing and loader handoff still need to be resolved.

The node also declares `qcom,gpu-qdss-stm = <0x161c0000 0x40000>`; its debug/trace integration is not part of the first minimal bring-up path.

### 3. GMU and firmware requirements

The GPU companion GMU node is `qcom,gmu@506a000`, compatible with `qcom,gpu-gmu`. Its resources are:

| Name | Base | Size |
|---|---:|---:|
| `kgsl_gmu_reg` | `0x0506a000` | `0x31000` |
| `kgsl_gmu_pdc_cfg` | `0x0b290000` | `0x10000` |
| `kgsl_gmu_pdc_seq` | `0x0b490000` | `0x10000` |

The GMU node declares two interrupt specifiers, `<0 304 IRQ_TYPE_LEVEL_HIGH>` and `<0 305 IRQ_TYPE_LEVEL_HIGH>`, named `kgsl_hfi_irq` and `kgsl_gmu_irq`.

The A618 Linux core-table entry records:

- SQE firmware name: `a630_sqe.fw`
- GMU firmware name: `a618_gmu.bin`
- secure/ZAP firmware name: `a615_zap`
- GMU version: major 1, minor 8
- GMEM size: 512 KiB
- 64-bit addressing, RPMh, preemption, GPMU, content-protection, IFPC and I/O-coherency feature flags in that Linux driver revision.

The device-tree PIL node independently names `a615_zap`. These names establish Linux driver expectations; they do not establish that the firmware files are present, redistributable, compatible with a future XNU loader, or safe to substitute. No firmware blobs are included or extracted by this research.

### 4. IOMMU and GPU memory

The GPU source describes a `qcom,kgsl-iommu@5040000` node compatible with `qcom,kgsl-smmu-v2`, with a register region at `0x05040000` of size `0x10000`. It defines separate context-bank descriptions for:

- `gfx3d_user`
- `gfx3d_secure`
- `gmu_user`
- `gmu_kernel`

The user graphics context includes `qcom,gpu-offset = <0x48000>`. Secure and GMU contexts are separately described. This confirms that a future driver cannot be just a register-write wrapper: it needs a verified GPU address-space and IOMMU design, including secure-context policy.

The shared SoC tree also contains a `pil_gpu_mem` reserved region at `0x97715000`, size `0x2000`, marked `removed-dma-pool`. Do **not** treat this small PIL carveout as general GPU VRAM or as the complete GPU memory pool. The Linux GPU node separately describes page-pool policy; those allocator settings are Linux implementation details, not an XNU allocator contract.

### 5. Clocks, power and bandwidth

The GPU node names five clocks: `core_clk`, `rbbmtimer_clk`, `mem_clk`, `mem_iface_clk`, and `gmu_clk`. It references the GPU clock controller and the GCC DDR/GPU memory-network clocks.

It references two power domains/supplies, `vddcx` and `vdd`, through the GPU CX/GX GDSC nodes. The shared SoC tree describes the GPU clock controller at `0x05090000` with size `0x9000`. The GPU node also describes GPU/HTW LLC cache slices and bus-bandwidth operating points.

The Linux device tree has multiple GPU speed-bin profiles and power levels. The exact speed bin for this XT2135-2 unit is not established. Do not hardcode the listed frequencies, voltage levels, clock IDs, or regulator transitions into XNU based solely on these Linux values.

## Graphics-stack reference

- [Mesa Freedreno documentation](https://docs.mesa3d.org/drivers/freedreno.html): Freedreno provides GL/GLES support across Adreno 2xx–6xx; Turnip is the Vulkan driver for Adreno 6xx. The documentation describes A6xx command processing, SQE microcode, tiling/GMEM and system-memory rendering.
- [Mesa Adreno device table](https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/freedreno/common/freedreno_devices.py): GPU ID 618 is included in an A6xx generation-1 group.
- [Mesa A6xx register database](https://gitlab.freedesktop.org/mesa/mesa/-/blob/main/src/freedreno/registers/adreno/a6xx.xml): public register descriptions can guide research, but must be matched to the exact GPU revision and never treated as a complete power/clock/firmware sequence.

Mesa is a possible userspace graphics stack after a working kernel-facing GPU interface exists. It does not supply an XNU kernel driver or make the hardware work by itself. Metal is not implied by Freedreno support.

## Unresolved before hardware initialization

1. Identify which HANOIP engineering overlay (EVT1, DVT1, or DVT2) matches this exact XT2135-2 unit and derive the final merged device tree.
2. Verify the actual GPU chip ID and all MMIO regions as delivered at a supported loader handoff.
3. Establish the exact clock, reset, regulator, GDSC, RPMh and GMU power-on sequence from target-applicable public sources.
4. Define the GPU SMMU/IOMMU context, page-table format, address width, secure-memory policy and fault handling.
5. Establish DMA coherency, cache maintenance, UBWC and GPU/CPU synchronization requirements.
6. Confirm the compatible SQE/GMU/ZAP firmware provenance, availability and licensing; do not bundle proprietary blobs.
7. Establish interrupt-controller routing, masking, acknowledgement and reset behavior.
8. Confirm GMEM and other hardware capabilities against the exact A618 revision.
9. Keep display controller, panel, framebuffer handoff and compositor integration as a separate milestone.

## Implementation plan

1. Keep the existing portable lifecycle, CPU-memory and allocator-contract tests.
2. Add a machine-readable, source-linked evidence contract and CI checks for the facts above.
3. Build a HANOIP platform-resource description with unresolved runtime values disabled by default.
4. Implement and test portable resource parsing and state management without MMIO.
5. Only after the handoff and power/IOMMU contracts are verified, add hardware-specific initialization in small reviewable steps.
6. Add command submission and rendering only after memory mapping, firmware and synchronization are established.
7. Evaluate Mesa/Freedreno integration after a real kernel-facing interface exists.

Generic QEMU does not emulate this Adreno GPU. Host tests and generic QEMU can validate parsers, state machines and interfaces, but cannot prove Adreno initialization or acceleration. No phone firmware or partitions are accessed or modified in this project.

## Evidence links

- [GPU device-tree node](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-gpu.dtsi#L47-L125)
- [GMU and IOMMU device-tree nodes](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie-gpu.dtsi#L580-L691)
- [A618 Linux GPU core entry](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/drivers/gpu/msm/adreno-gpulist.h#L399-L416)
- [GPU reserved-memory region](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi#L569-L580)
- [GPU clock-controller node](https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150/blob/5b04fac0cb2a8311ae69c8644384426e838d91fe/arch/arm64/boot/dts/qcom/sdmmagpie.dtsi#L912-L925)
