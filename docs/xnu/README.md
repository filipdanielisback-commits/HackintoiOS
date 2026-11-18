# XNU and Darwin research

**Status: pinned upstream baseline and research only.** This directory records XNU/Darwin architecture research relevant to HackintoiOS. It is not an iOS 18 source tree, an XNU port, or a bootable system.

## Scope

- Study Apple's publicly released [XNU source](https://github.com/apple-oss-distributions/xnu) and its license.
- Track a reproducible upstream source revision in [xnu/upstream.lock](../../xnu/upstream.lock).
- Document the relationship between XNU, the Darwin user-space environment, and the wider iOS platform.
- Track ARM64 architecture requirements and platform-specific dependencies.
- Record which components are open source and which iOS/device components are proprietary or unavailable.
- Keep experiments reproducible and isolated from the Moto G60 Linux reference-kernel build.

## Version baseline

The initial research baseline is Apple's XNU tag `xnu-11215.1.10`, pinned to commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`. It is associated with the iOS 18.0 / Darwin 24.0.0 version family. CI checks the upstream tag-to-commit mapping; this is a source-integrity check, not an XNU build or a device compatibility result.

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
- [Apple XNU source repository](https://github.com/apple-oss-distributions/xnu/tree/xnu-11215.1.10)
- [HackintoiOS XNU source integration](../../xnu/README.md)
- [HackintoiOS device profile](../device-profile.md)
- [HackintoiOS architecture overview](../architecture/overview.md)
