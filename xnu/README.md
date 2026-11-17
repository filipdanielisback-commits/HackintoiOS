# XNU source integration

This directory tracks the public Apple XNU source revision selected for HackintoiOS research and future porting work.

## Pinned upstream

See [upstream.lock](upstream.lock). The initial reference is Apple's `xnu-11215.1.10` tag, pinned to commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`.

The upstream README describes XNU as part of Darwin, identifies ARM64 support, and documents a build flow that relies on an SDK and Apple build tooling. That does **not** establish that this revision can be built for HANOIP or that its Apple platform code supports the Moto G60.

## Repository policy

- Upstream source is fetched by CI for verification; it is not copied wholesale into this repository yet.
- HackintoiOS-specific changes belong in `patches/` and must be small, reviewable, and traceable to the pinned upstream revision.
- Do not add Apple proprietary SDKs, firmware, IPSW contents, signing material, or credentials.
- Do not describe a successful source checkout or integrity check as an XNU build.
- Do not describe a generic ARM64 code path as Moto G60 support.

## Next engineering gates

1. Verify upstream licensing and the exact build prerequisites for this revision.
2. Reproduce an upstream-supported XNU build in a compatible environment before changing kernel code.
3. Identify the platform initialization, interrupt, timer, memory, and boot interfaces needed for a non-Apple ARM64 target.
4. Design HANOIP-specific changes only after those interfaces are understood.
5. Keep the existing Linux reference-kernel workflow separate from XNU work.
