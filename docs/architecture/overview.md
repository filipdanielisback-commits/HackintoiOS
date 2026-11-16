# Architecture overview

This document describes research boundaries, not a working port design.

## Major layers

1. **Physical platform:** CPU, memory, interrupt controller, timers, storage, display, and peripherals.
2. **Boot chain:** immutable boot ROM, vendor boot stages, bootloader, and the handoff to an operating-system kernel. Exact stages must be verified for this model.
3. **Kernel:** XNU contains Mach and BSD components, but an ARM64 kernel build alone does not provide the platform drivers or device integration required to operate a phone.
4. **Hardware support:** each peripheral needs compatible drivers, firmware interfaces, power sequencing, and device-tree or platform descriptions as applicable.
5. **User space:** a usable Darwin environment requires far more than a kernel. Apple's proprietary frameworks and services are outside this project's source scope.

## Portability questions

- Which ARM64 platform assumptions are present in the selected upstream XNU revision?
- What platform-specific drivers and interfaces would be missing?
- What boot protocol and memory layout does the device actually use?
- Which hardware facts can be established from public documentation?
- Which project tasks can be validated without flashing or changing the phone?

## Non-goals for the current phase

No boot image generation, firmware repackaging, device flashing, bypass of device security, or distribution of proprietary Apple components is implemented.
