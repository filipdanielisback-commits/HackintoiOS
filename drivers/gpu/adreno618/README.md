# HanoipAdreno618

Original HackintoiOS driver core for the Moto G60's Adreno 618 GPU.

## Implemented portable core

The initial C module provides a host-testable lifecycle and validation layer:

- starts detached;
- accepts an Adreno 618 identity only when the platform layer explicitly marks that identity as verified;
- accepts a mapped resource only after identity and only when the platform layer marks the mapping as verified;
- rejects wrong GPU models, unverified inputs, empty mappings, and invalid state transitions;
- supports a clean detach/reset.

## Phase 1: GPU memory-object abstraction

The portable memory layer in `adreno618_memory.c` and `adreno618_memory.h` now provides:

- caller-owned backing buffers (no hidden allocator or ownership transfer);
- power-of-two base-alignment validation;
- explicit read/write access permissions;
- overflow-safe offset/length bounds checks;
- a single active CPU-side view per object, with map/unmap state validation;
- reset of descriptor metadata without freeing caller memory.

This is a CPU-side memory-object contract only. It deliberately does not invent physical addresses, DMA addresses, GPU virtual addresses, page tables, cache-coherency operations, or GPU mappings. Those require a verified platform memory manager and Adreno-specific evidence.

## Not implemented

This is **not yet a functioning hardware GPU driver**. It does not access registers or perform GPU initialization, firmware loading, physical/DMA allocation, GPU page-table management, command submission, rendering, synchronization with hardware, interrupt handling, or power management. No XNU integration or Adreno hardware acceleration is claimed.

The supplied backing store remains owned by the caller and must remain valid for the lifetime of the object and any active view. This portable layer is intended for interface development and host testing, not direct hardware operation.

## Testing

Run both host-only test programs:

```sh
cc -std=c11 -Wall -Wextra -Werror -pedantic \
  drivers/gpu/adreno618/adreno618.c \
  drivers/gpu/adreno618/tests/test_adreno618.c \
  -o /tmp/test-adreno618
/tmp/test-adreno618

cc -std=c11 -Wall -Wextra -Werror -pedantic \
  drivers/gpu/adreno618/adreno618_memory.c \
  drivers/gpu/adreno618/tests/test_adreno618_memory.c \
  -o /tmp/test-adreno618-memory
/tmp/test-adreno618-memory
```

Tests use synthetic, caller-owned host buffers. They do not touch a GPU, create DMA mappings, or validate HANOIP hardware.

## Next evidence gates

1. Resolve the exact GPU node and compatible strings from the merged HANOIP device tree.
2. Establish the exact Adreno 618 revision and memory-management model from target-applicable public evidence.
3. Identify the required firmware interface and permitted firmware source.
4. Define verified platform allocation, mapping, cache-coherency, interrupt, clock, and power contracts.
5. Only then add hardware-specific GPU memory mapping, command submission, and XNU integration.

HakiOS is an architectural reference only. This implementation is original and does not copy its Adreno 642L code or POCO X5 Pro hardware assumptions.
