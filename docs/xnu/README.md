# XNU and Darwin research

**Status: upstream source research and guarded build-wrapper scaffolding.** This directory records XNU/Darwin architecture research relevant to HackintoiOS. It is not an iOS 18 source tree, an XNU port, or a bootable system.

## Scope

- Study Apple's publicly released [XNU source](https://github.com/apple-oss-distributions/xnu) and its license.
- Track upstream source revisions and distinguish confirmed pins from research candidates.
- Document the relationship between XNU, Darwin user space, and the wider iOS platform.
- Track ARM64 architecture requirements and platform-specific dependencies.
- Keep experiments reproducible and isolated from the Moto G60 Linux reference-kernel build.

## Version baseline

The historical `xnu/upstream.lock` pin `xnu-11215.1.10` belongs to the iOS 18.0 / Darwin 24.0.0 generation and is too old to call the final iOS 18.7.12 baseline.

Research identifies Darwin `24.6.0` as the best-supported kernel version family for iOS 18.7.12 build `22H390`. Public tag `xnu-11417.140.69` resolves to commit `43a90889846e00bfb5cf1d255cdc0a701a1e05a4`. It is a reproducible candidate in the matching Darwin family, **not a proven exact source match** for build 22H390. The exact build suffix remains unconfirmed, so the historical lock has not been changed.

See the [version-mapping report](ios-18.7.12-version.md).

## XNU environment and build wrappers

The repository now includes:

- `xnu-env.sh`: repository-relative source/dependency paths, host metadata, ARM64 target metadata, and the candidate source identity.
- `xnu-build.sh --print-env`: print environment settings without compiling.
- `xnu-build.sh --check`: verify the pinned source checkout and explicit SDK/configuration inputs.
- `xnu-build.sh --dry-run`: show the make command after preflight.
- `XNU_BUILD_ENABLE=1 bash xnu-build.sh`: explicit opt-in to invoke upstream `make`.

The wrappers are original scaffolding inspired by the role of HakiOS's scripts; they do not copy HakiOS's device-specific build flags or dependency setup. They do not fetch source or SDKs, and they do not assume a HANOIP machine configuration. No HANOIP XNU target has been implemented or validated. CI checks shell syntax and guard behavior only; it does **not** compile XNU.

See [XNU source integration and build instructions](../../xnu/README.md).

## HANOIP platform planning

The evidence-first [HANOIP kernel work plan](../architecture/HANOIP_KERNEL_PLAN.md) separates generic ARM64, Qualcomm SoC, and Motorola board responsibilities. It is planning documentation only; no HANOIP XNU platform implementation or validated device driver exists yet.

## Important boundaries

- The existing `kernel/` directory builds a Linux reference kernel for HANOIP. It is not XNU.
- A successful source checkout, shell check, or wrapper preflight does not compile XNU.
- Public XNU source alone is not a complete iOS 18 operating system.
- Do not add proprietary Apple SDKs, firmware, IPSW contents, signing material, or credentials.
- Do not describe this project as running iOS, Darwin, or XNU on the phone unless that is independently demonstrated.

## Research checklist

1. Confirm the exact XNU source revision for iOS 18.7.12 build 22H390.
2. Identify compatible build-host, SDK, toolchain, and target-platform requirements.
3. Reproduce a supported upstream build before making HANOIP kernel changes.
4. Map generic ARM64 facilities separately from Apple-specific platform interfaces.
5. Maintain the Moto G60 compatibility matrix and mark unknowns explicitly.
6. Keep CI checks clearly labeled as source/wrapper checks unless they compile a real upstream target.

## References

- [Apple Open Source](https://opensource.apple.com/)
- [Apple XNU source candidate](https://github.com/apple-oss-distributions/xnu/tree/xnu-11417.140.69)
- [HackintoiOS XNU source integration](../../xnu/README.md)
- [HackintoiOS device profile](../device-profile.md)
- [HackintoiOS architecture overview](../architecture/overview.md)
