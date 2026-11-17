# XNU and Darwin research

**Status: research and documentation only.** This directory records upstream XNU/Darwin architecture research relevant to HackintoiOS. It is not an iOS 18 source tree, an XNU port, or a bootable system.

## Scope

- Study Apple's publicly released [XNU source](https://github.com/apple-oss-distributions/xnu) and its license.
- Document the relationship between XNU, the Darwin user-space environment, and the wider iOS platform.
- Track ARM64 architecture requirements and platform-specific dependencies.
- Record which components are open source and which iOS/device components are proprietary or unavailable.
- Keep experiments reproducible and isolated from the Moto G60 Linux reference-kernel build.

## Version context

iOS 18 belongs to the Darwin 24 generation. This is a version-family research reference, not evidence that Darwin 24 can be built for or booted on the Moto G60 Vision.

## Important boundaries

- The existing `kernel/` directory builds a Linux reference kernel for HANOIP. It is not XNU.
- A successful documentation or metadata check does not compile XNU.
- Public XNU source alone is not a complete iOS 18 operating system.
- Do not add proprietary Apple SDKs, firmware, IPSW contents, signing material, or credentials to this repository.
- Do not describe this project as running iOS, Darwin, or XNU on the phone unless that is independently demonstrated.

## Research checklist

1. Record the upstream XNU revision and license before studying or importing source.
2. Identify build-host, SDK, toolchain, and target-platform requirements from upstream documentation.
3. Map generic ARM64 kernel facilities separately from Apple-specific platform interfaces.
4. Maintain a compatibility matrix for the Moto G60 hardware; mark unknowns explicitly.
5. Keep all build checks clearly labeled as documentation/metadata checks unless they compile a real upstream target.

## References

- [Apple Open Source](https://opensource.apple.com/)
- [Apple XNU source repository](https://github.com/apple-oss-distributions/xnu)
- [HackintoiOS device profile](../device-profile.md)
- [HackintoiOS architecture overview](../architecture/overview.md)
