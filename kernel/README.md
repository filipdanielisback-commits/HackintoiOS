# Kernel implementation and build baseline

## Scope

HackintoiOS now has a reproducible build target for the Motorola hanoip device-family kernel baseline. The kernel source is maintained in a separate public repository and checked out at a pinned commit by `build-hanoip.sh`; this repository does not vendor or silently rewrite that source.

This is **not yet an original HackintoiOS kernel**. The first HackintoiOS-specific change is a small Kconfig fragment that sets the build local version to `-hackintoiOS`. Device drivers, kernel patches, and an iOS-compatible kernel/userspace implementation have not been written.

## Source baseline

- Repository: https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150
- Branch used for source provenance: `lineage-20`
- Pinned commit: `5b04fac0cb2a8311ae69c8644384426e838d91fe`
- Kernel version in source Makefile: Linux 4.14.326
- Device configuration: `arch/arm64/configs/vendor/hanoip_defconfig`
- Target architecture: ARM64
- Build mode: LLVM/Clang, matching the device family's BoardConfig flags
- License: GPL-2.0 kernel source; preserve upstream notices and comply with source redistribution terms.

The Motorola device tree identifies the shared platform build as `sm6150` and points to `vendor/hanoip_defconfig`. This platform-tree name is not a substitute for verifying the physical SoC identity.

## Build

Run on a Linux host with Git, Make, Python 3, Clang/LLVM 14, and standard kernel build dependencies:

```sh
JOBS=2 ./kernel/build-hanoip.sh
```

The script builds the kernel image and device-tree blobs into `out/hanoip/`. GitHub Actions runs the same script and stores the outputs as a CI artifact.

## What a successful build means

- The pinned kernel source compiles with the hanoip defconfig and HackintoiOS local-version fragment.
- It does not prove the kernel boots on the exact XT2135-2 hardware.
- It does not create a complete Android boot image.
- It does not implement iOS, Darwin, XNU, Apple drivers, or a complete iOS 18 environment.
- It must not be flashed or treated as a device-ready image.

## Planned engineering work

1. Verify target-unit identifiers and firmware provenance.
2. Audit the inherited device tree, DTBs, and module dependencies.
3. Add original, reviewable HackintoiOS kernel changes in separate patches.
4. Add static checks and regression tests for each change.
5. Keep device boot validation separate from CI compilation.
