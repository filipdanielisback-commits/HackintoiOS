# XNU and Darwin research

**Status: pinned upstream baseline; research and documentation only.** This directory records XNU/Darwin architecture research relevant to HackintoiOS. It is not an iOS 18 source tree, an XNU port, or a bootable system.

## Scope

- Study Apple's publicly released [XNU source](https://github.com/apple-oss-distributions/xnu) and its license.
- Track a reproducible upstream source revision in [xnu/upstream.lock](../../xnu/upstream.lock).
- Document the relationship between XNU, the Darwin user-space environment, and the wider iOS platform.
- Track ARM64 architecture requirements and platform-specific dependencies.
- Record which components are open source and which iOS/device components are proprietary or unavailable.
- Keep experiments reproducible and isolated from the Moto G60 Linux reference-kernel build.

## Version baseline

The previous research pin `xnu-11215.1.10` (commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`) belongs to the iOS 18.0 / Darwin 24.0.0 generation and is too old to call the final iOS 18.7.12 baseline.

Research identifies Darwin `24.6.0` as the best-supported kernel version family for iOS 18.7.12 build `22H390`. The public XNU tag `xnu-11417.140.69` has been resolved to peeled commit `43a90889846e00bfb5cf1d255cdc0a701a1e05a4`. This is a reproducible public upstream candidate in the matching Darwin family, **not a proven exact source match** for the iPhone XR's 22H390 kernel. The exact build suffix remains unconfirmed, so `xnu/upstream.lock` has deliberately not been changed.

See the [version-mapping report](ios-18.7.12-version.md) for tag object metadata and evidence.

## HANOIP platform planning

The evidence-first [HANOIP kernel work plan](../architecture/HANOIP_KERNEL_PLAN.md) separates generic ARM64, Qualcomm SoC, and Motorola board responsibilities. It is planning documentation only; no HANOIP XNU platform implementation or validated device driver exists yet.

## Important boundaries

- The existing `kernel/` directory builds a Linux reference kernel for HANOIP. It is not XNU.
- A successful source checkout, patch check, or documentation check does not compile XNU.
- Public XNU source alone is not a complete iOS 18 operating system.
- Do not add proprietary Apple SDKs, firmware, IPSW contents, signing material, or credentials to this repository.
- Do not describe this project as running iOS, Darwin, or XNU on the phone unless that is independently demonstrated.

## Research checklist

1. Verify and preserve the upstream tag, commit, and license.
2. Identify build-host, SDK, toolchain, and target-platform requirements from upstream documentation.
3. Map generic ARM64 kernel facilities separately from Apple-specific platform interfaces.
4. Maintain a compatibility matrix for the Moto G60 hardware; mark unknowns explicitly.
5. Keep all CI checks clearly labeled as source/patch/documentation checks unless they compile a real upstream target.

## References

- [Apple Open Source](https://opensource.apple.com/)
- [Apple XNU source tag](https://github.com/apple-oss-distributions/xnu/tree/xnu-11417.140.69)
- [HackintoiOS XNU source integration](../../xnu/README.md)
- [HackintoiOS device profile](../device-profile.md)
- [HackintoiOS architecture overview](../architecture/overview.md)
