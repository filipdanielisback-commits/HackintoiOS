# HanoipAdreno618

Original HackintoiOS driver core for the Moto G60's Adreno 618 GPU.

## Current implementation

The initial C module provides a small, host-testable lifecycle and validation layer:

- starts detached;
- accepts an Adreno 618 identity only when the platform layer explicitly marks that identity as verified;
- accepts a mapped resource only after identity and only when the platform layer marks the mapping as verified;
- rejects wrong GPU models, unverified inputs, empty mappings, and invalid state transitions;
- supports a clean detach/reset.

The core does not assume a GPU register map, MMIO base, interrupt number, firmware name, clock ID, power sequence, or memory layout. Those values are not yet established for this exact XT2135-2 unit.

## Not implemented

This is **not yet a functioning hardware GPU driver**. It does not access registers or perform GPU initialization, firmware loading, memory management, command submission, rendering, synchronization, interrupt handling, or power management. No XNU integration or Adreno hardware acceleration is claimed.

## Testing

Run the host-only tests with:

```sh
cc -std=c11 -Wall -Wextra -Werror -pedantic \
  drivers/gpu/adreno618/adreno618.c \
  drivers/gpu/adreno618/tests/test_adreno618.c \
  -o /tmp/test-adreno618
/tmp/test-adreno618
```

The test uses synthetic identity/resource descriptors. It does not touch a GPU or validate HANOIP hardware.

## Next evidence gates

1. Resolve the exact GPU node and compatible strings from the merged HANOIP device tree.
2. Establish the exact Adreno 618 GPU revision and hardware interface from target-applicable public evidence.
3. Identify the required firmware interface and permitted firmware source.
4. Define verified resource, interrupt, clock, power, and memory contracts.
5. Only then add hardware-specific initialization and XNU integration.

HakiOS is an architectural reference only. This implementation is original and does not copy its Adreno 642L code or POCO X5 Pro hardware assumptions.
