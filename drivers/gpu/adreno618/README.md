# HanoipAdreno618

Original HackintoiOS driver core for the Moto G60's Adreno 618 GPU.

## Portable lifecycle core

The initial C module provides a host-testable lifecycle and validation layer: verified Adreno 618 identity, resource-binding state checks, and clean detach/reset.

## Phase 1: CPU-side memory objects

The memory-object layer provides caller-owned buffers, power-of-two alignment validation, explicit read/write permissions, overflow-safe range checks, and single-view CPU map/unmap bookkeeping. It does not allocate or map hardware memory.

## Phase 1.5: platform allocator contract

`adreno618_allocator.c` and `adreno618_allocator.h` define a platform-supplied allocation interface:

- `allocate` requests a size and alignment and returns an opaque handle;
- `map_cpu` requests a bounded CPU view with explicit access permissions;
- `unmap_cpu` releases that view;
- `release` releases the platform allocation;
- failures are propagated without falsely changing object state;
- destruction is rejected while a CPU view remains mapped;
- range validation uses subtraction-based checks to avoid integer overflow.

The platform implementation owns the backing allocation and must honor the requested size/alignment. The portable core never receives or fabricates physical, DMA, or GPU virtual addresses. It does not define GPU page tables, IOMMU configuration, cache-coherency policy, or GPU address-space layout.

## Phase 2: bounded register-access interface

`adreno618_mmio.c` and `adreno618_mmio.h` add a hardware-facing 32-bit register access contract:

- platform-supplied read/write callbacks operate on an already-mapped resource;
- offsets must be 4-byte aligned and wholly inside the declared mapping;
- read-only windows reject writes;
- callback failures are returned to the caller;
- the portable layer never turns a physical address into a pointer or maps device memory itself.

The test backend is synthetic host memory. This validates bounds and callback behavior only; it does not access the Moto G60 GPU. No GPU-specific register offsets or initialization sequence are guessed in this layer. The platform backend must establish mapping, memory ordering, and access permissions from verified XNU/platform APIs before use.

## Not implemented

This is **not yet a functioning hardware GPU driver**. It does not contain a HANOIP XNU backend, access actual GPU registers, load firmware, allocate physical pages itself, create DMA/GPU mappings, manage GPU page tables, submit commands, render, synchronize with hardware, handle interrupts, or manage power. No XNU integration or Adreno hardware acceleration is claimed.

All tests use synthetic host backends. They validate portable contracts only, not HANOIP memory behavior or GPU operation.

## Host tests

GitHub Actions compiles and runs the lifecycle, memory-object, allocator, and bounded-MMIO tests with strict C11 warnings. The workflow does not prove hardware operation.

## Evidence gates before hardware integration

1. Resolve the exact GPU node and compatible strings from the merged HANOIP device tree.
2. Establish the exact Adreno 618 revision and memory-management model from target-applicable public evidence.
3. Identify the platform's real physical-memory allocator and DMA/IOMMU ownership model.
4. Establish cache-maintenance and CPU/GPU synchronization requirements.
5. Define GPU virtual address-space/page-table behavior from verified Adreno documentation or source.
6. Bind the callbacks to the selected XNU platform resource-mapping and memory-ordering APIs.
7. Only then add hardware-backed initialization, memory management, command submission, and XNU integration.

HakiOS is an architectural reference only. This implementation is original and does not copy its Adreno 642L code or POCO X5 Pro hardware assumptions.

## Hardware research

See [Adreno 618 HANOIP hardware research](../../../docs/architecture/ADRENO618_HARDWARE_RESEARCH.md) for source-backed GPU, GMU, firmware, IOMMU, clock and power evidence, plus unresolved gates. Linux device-tree values are research evidence, not an XNU runtime configuration.
