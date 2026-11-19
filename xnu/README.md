# XNU source integration

**Status: pinned upstream baseline; no HANOIP patch has been written or built yet.**

HackintoiOS tracks Apple's public XNU source as a separate upstream dependency. The historical lock is recorded in [upstream.lock](upstream.lock). The build wrappers currently target a separately pinned research candidate described below; they do not silently rewrite the lock.

## Upstream source references

- Repository: https://github.com/apple-oss-distributions/xnu
- Historical lock: `xnu-11215.1.10`, commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585` (iOS 18.0 / Darwin 24.0.0; too old for the final target).
- Build-wrapper candidate: `xnu-11417.140.69`, commit `43a90889846e00bfb5cf1d255cdc0a701a1e05a4` (Darwin 24.6.0 family).

The candidate is **not a proven exact source match** for iOS 18.7.12 build `22H390`; its exact kernel build suffix remains unconfirmed. Do not update `upstream.lock` or describe this candidate as the final 22H390 source until that evidence is found.

## Build wrapper scripts

- `xnu-env.sh`: source this file to establish repository-relative XNU paths, host information, ARM64 target metadata, and the candidate source identity.
- `xnu-build.sh --print-env`: print the selected environment without building.
- `xnu-build.sh --check`: validate the source checkout, SDK path, and explicit build configuration.
- `xnu-build.sh --dry-run`: print the proposed `make` command after preflight.
- `XNU_BUILD_ENABLE=1 bash xnu-build.sh`: explicit opt-in to run the upstream `make` command.

The wrappers intentionally do not download XNU, install an SDK, invent a HANOIP machine configuration, or include proprietary Apple files. A real build requires the candidate source checkout at the pinned commit, a compatible SDK/toolchain, and a machine configuration actually supported by that source tree. No HANOIP machine configuration has been implemented or validated. CI checks only shell syntax and wrapper safeguards; they do **not** compile XNU.

## Layout

- `upstream.lock`: historical upstream repository, tag, and commit reference.
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
5. Validate each patch against a verified baseline and keep the Linux reference-kernel workflow separate.
