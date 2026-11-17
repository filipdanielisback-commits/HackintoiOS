# XNU source integration

This directory tracks the public Apple XNU source revision selected for HackintoiOS research and future porting work.

## Pinned upstream

See [upstream.lock](upstream.lock). The initial reference is Apple's `xnu-11215.1.10` tag, pinned to commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`.

The upstream README describes XNU as part of Darwin, identifies ARM64 support, and documents an SDK-based build flow using Apple's build tools. That does **not** establish that this revision can be built for HANOIP or that its Apple platform code supports the Moto G60.

## Licensing

The pinned upstream revision includes Apple's **Apple Public Source License 2.0 (APSL-2.0)**. A copy of the upstream license is preserved in [APPLE_LICENSE](APPLE_LICENSE).

This project must preserve upstream copyright, license, and disclaimer notices. If we add or modify APSL-covered source files, the applicable APSL modification notices and file-change notices must be included. APSL also sets source-availability and licensing conditions for externally deployed modifications and executable distributions. Review the complete license before distributing a build; this note is a project checklist, not legal advice.

Do not apply HackintoiOS's own license to Apple-covered files in a way that overrides or restricts APSL rights. Keep independent HackintoiOS code clearly separated from APSL-covered code.

## Repository policy

- Upstream source is fetched by CI for verification; it is not copied wholesale into this repository yet.
- HackintoiOS-specific changes belong in `patches/` and must be small, reviewable, and traceable to the pinned upstream revision.
- Do not add Apple proprietary SDKs, firmware, IPSW contents, signing material, or credentials.
- Do not describe a successful source checkout or integrity check as an XNU build.
- Do not describe a generic ARM64 code path as Moto G60 support.

## Build feasibility probe

[`.github/workflows/xnu-build-probe.yml`](../.github/workflows/xnu-build-probe.yml) attempts an ARM64 DEVELOPMENT build on a GitHub-hosted macOS runner using the public macOS SDK exposed by Xcode. It is an experiment to discover missing prerequisites or unsupported build assumptions, not a supported HANOIP build and not a device image.

The upstream README uses `macosx.internal` in its example commands. The public-runner probe deliberately tests the public SDK instead; failure may indicate that the upstream build expects additional Apple-internal build inputs.

## HANOIP platform evidence

- [Platform porting map](../docs/xnu/platform-porting-map.md) maps relevant XNU source areas to the still-open HANOIP porting tasks.
- [HANOIP device-tree evidence audit](../docs/xnu/hanoip-device-tree-audit.md) records facts found in the public Motorola Linux DTS and defconfig, while explicitly separating those facts from the unknown retail bootloader handoff and board-overlay selection.

These are research documents, not a driver implementation, verified boot contract, or boot plan.

## Next engineering gates

1. Verify upstream licensing and exact build prerequisites for this revision.
2. Reproduce an upstream-supported XNU build in a compatible environment before changing kernel code.
3. Establish the actual HANOIP bootloader handoff and firmware-matched memory map; Linux DTS data is only a reference.
4. Identify the platform initialization, interrupt, timer, memory, and boot interfaces needed for a non-Apple ARM64 target.
5. Design HANOIP-specific changes only after those interfaces are understood.
6. Keep the existing Linux reference-kernel workflow separate from XNU work.
