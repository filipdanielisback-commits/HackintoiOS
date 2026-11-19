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

The platform implementation owns the backing allocation and must honor the requested size/alignment. The portable core never receives or fabricates physical, DMA, or GPU virtual addresses. It does not define GPU page tables, IOMMU configuration, cache-coherency policy, or GPU address-space layout. Those remain platform-specific evidence gates.

## Not implemented

This is **not yet a functioning hardware GPU driver**. It does not access registers, load firmware, allocate physical pages itself, create DMA/GPU mappings, manage GPU page tables, submit commands, render, synchronize with hardware, handle interrupts, or manage power. No XNU integration or Adreno hardware acceleration is claimed.

All tests use a synthetic host allocator. They validate the portable callback contract only, not HANOIP memory behavior or GPU operation.

## Host tests

GitHub Actions compiles and runs the lifecycle, memory-object, and allocator tests with strict C11 warnings:

```sh
cc -std=c11 -Wall -Wextra -Werror -pedantic drivers/gpu/adreno618/adreno618.c drivers/gpu/adreno618/tests/test_adreno618.c -o /tmp/test-adreno618
/tmp/test-adreno618
cc -std=c11 -Wall -Wextra -Werror -pedantic drivers/gpu/adreno618/adreno618_memory.c drivers/gpu/adreno618/tests/test_adreno618_memory.c -o /tmp/test-adreno618-memory
/tmp/test-adreno618-memory
cc -std=c11 -Wall -Wextra -Werror -pedantic drivers/gpu/adreno618/adreno618_allocator.c drivers/gpu/adreno618/tests/test_adreno618_allocator.c -o /tmp/test-adreno618-allocator
/tmp/test-adreno618-allocator
```

## Evidence gates before hardware integration

1. Resolve the exact GPU node and compatible strings from the merged HANOIP device tree.
2. Establish the exact Adreno 618 revision and memory-management model from target-applicable public evidence.
3. Identify the platform's real physical-memory allocator and DMA/IOMMU ownership model.
4. Establish cache-maintenance and CPU/GPU synchronization requirements.
5. Define GPU virtual address-space/page-table behavior from verified Adreno documentation or source.
6. Only then add a hardware-backed memory manager, command submission, and XNU integration.

HakiOS is an architectural reference only. This implementation is original and does not copy its Adreno 642L code or POCO X5 Pro hardware assumptions.


## Hardware research

See [Adreno 618 HANOIP hardware research](../../../docs/architecture/ADRENO618_HARDWARE_RESEARCH.md) for source-backed GPU, GMU, firmware, IOMMU, clock and power evidence, plus the unresolved gates before hardware initialization. The inventory is research only; none of its Linux device-tree values are an XNU runtime configuration.
