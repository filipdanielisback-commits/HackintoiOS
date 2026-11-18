# XNU source integration

**Status: pinned upstream baseline; no HANOIP patch has been written or built yet.**

HackintoiOS tracks Apple's public XNU source as a separate upstream dependency. The selected research baseline is recorded in [upstream.lock](upstream.lock).

## Pinned upstream

- Repository: https://github.com/apple-oss-distributions/xnu
- Tag: `xnu-11215.1.10`
- Commit: `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`
- Research version family: iOS 18.0 / Darwin 24.0.0

The pin is an upstream source reference, not proof that this XNU revision can be built for or booted on the Moto G60 Vision. The upstream source tree includes ARM64 code, but its supported Apple platform configurations and build dependencies do not establish HANOIP support.

## Layout

- `upstream.lock`: immutable upstream repository, tag, and commit reference.
- `patches/series`: ordered list of HackintoiOS patch files (currently empty).
- `patches/`: only original, reviewable HackintoiOS changes; never copy HakiOS device patches and assume they apply.
- `docs/xnu/`: compatibility research and build constraints.

## Source and licensing policy

- CI fetches the exact upstream tag and verifies that it resolves to the pinned commit.
- Do not vendor the entire upstream tree until its license, distribution implications, and repository strategy have been reviewed.
- Preserve Apple's upstream notices and license when working with source files.
- Do not add proprietary Apple SDKs, firmware, IPSW contents, signing material, or credentials.
- Do not describe a successful checkout or patch validation as an XNU build.
- Do not describe generic ARM64 code as Moto G60 support.

## Engineering gates

1. Verify the upstream tag, commit, and license (the source contains `APPLE_LICENSE`).
2. Reproduce an upstream-supported XNU build in a compatible environment before modifying kernel code. The public build instructions depend on Apple-specific SDK/build components; a generic Ubuntu ARM64 compile is not an equivalent test.
3. Map the XNU platform/boot interfaces and compare them with verified HANOIP hardware facts.
4. Write the first HANOIP patch only when a specific, evidenced kernel change is identified.
5. Validate each patch against this exact baseline and keep the Linux reference-kernel workflow separate.
