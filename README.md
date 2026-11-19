# HackintoiOS

**Experimental operating-system research for the Motorola Moto G60 (XT2135-2).**

HackintoiOS investigates the engineering work required to run a genuine iOS 18.7.12-derived Darwin user-space environment on the Moto G60 Vision. The project's **official long-term end goal** is to boot that environment on the exact XT2135-2 target using an independently developed HANOIP-compatible XNU, loader, platform configuration, and drivers.

This is an ambitious research goal, not a claim of current compatibility or guaranteed success. The project is in the research and early scaffolding stage.

> **Current status:** No working iOS port, bootable Moto G60 image, HANOIP XNU implementation, or validated Moto G60 XNU drivers exist. Existing Linux kernel and UEFI checks are separate prototypes and do not establish phone boot support.

## Official target

| Item | Value |
| --- | --- |
| Device | Motorola Moto G60 Vision |
| Model | XT2135-2 |
| Device family | HANOIP |
| User-space research target | iOS 18.7.12, build 22H390 |
| Restore-image reference | iPhone XR, product iPhone11,8 |
| Current project phase | Architecture, source-version verification, and early scaffolding |

The iPhone XR restore image is a research reference, not a Moto G60 firmware image. Its device-specific components are not assumed to work on HANOIP. The current XNU pin was selected for the original iOS 18.0 / Darwin 24.0.0 research baseline and must be checked against the exact 18.7.12 build before it is treated as final.

See the [HakiOS-informed porting plan](docs/architecture/PORTING_PLAN.md), [device research](devices/moto-g60-xt2135-2/README.md), the [hardware bring-up tracker](devices/moto-g60-xt2135-2/hardware-status.md), and the [driver status list](drivers/STATUS.md).

## Goals

- Build an original XNU/loader/platform stack for the Moto G60, guided by evidence from its HANOIP device family.
- Study and implement the required ARM64 boot and kernel handoff interfaces.
- Develop original, independently tested hardware support for the target device.
- Investigate compatibility with the iOS 18.7.12-derived Darwin user-space environment.
- Use QEMU and GitHub Actions for repeatable development and regression tests.
- Keep third-party code, licenses, source provenance, and test results clearly documented.
- Distinguish verified facts, hypotheses, build results, emulation results, and physical-device results.

## Repository layout

```text
.
├── bootloader/       # AArch64 UEFI application prototype and boot-chain research
├── devices/          # Moto G60 target profile and hardware status
├── docs/             # Architecture, porting plan, development and research notes
├── drivers/          # XNU driver organization and working/pending status tracker
├── kernel/           # Linux reference-kernel build, not XNU
├── sysimage/         # Safe IPSW archive-inspection and metadata tools
├── userland/
│   ├── c/            # C user-space conventions and host tests
│   ├── cpp/          # C++17 foundations and compiler smoke test
│   └── objc/         # Objective-C syntax probe; runtime/framework work deferred
├── xnu/              # Pinned upstream XNU research baseline and patch manifest
├── xnu-env.sh        # Shared XNU build environment
└── xnu-build.sh      # Guarded XNU build entry point
```

## Language policy

C is the primary language for kernel, platform and hardware-driver work. C++17 is supported for components where it provides a concrete architectural benefit. Objective-C is reserved for future user-space/framework work and is not a kernel requirement. Python, Bash and Make support research, validation and build orchestration.

See [the language policy](docs/development/LANGUAGE_POLICY.md). The language-toolchain workflow compiles a C++ smoke test, checks Objective-C syntax only, and runs the existing C host smoke test. It does not provide Apple's frameworks or prove Darwin/IOKit integration.

## Build status

The project has separate checks for the Linux reference kernel, XNU source-baseline integrity, sysimage tooling, UEFI prototype and host userland smoke test. A successful check proves only what that workflow tests; it does not establish that XNU boots on the phone.

Run the documentation and host userland checks:

```sh
make help
make docs-check
make userland-check
```

The userland smoke test compiles with the host C compiler and runs on the CI host. It is not an iOS application, Darwin user space, XNU test, or phone boot test.

## Important technical and legal notes

- Apple's complete iOS source code and many device-specific components are proprietary. This project does not claim to recreate or distribute them.
- XNU and other open-source components retain their own upstream licenses. The repository's MIT license applies only to original project material that the maintainer has the right to license.
- Do not commit proprietary firmware, IPSW contents, signing material, credentials, or files whose redistribution rights are unclear.
- HakiOS and other projects are architectural references, not proof that their device configurations or patches work on the Moto G60. See the [porting plan](docs/architecture/PORTING_PLAN.md).
- Do not flash unverified images, replace device firmware, or bypass device security controls as part of this research.
- No Apple affiliation or endorsement is claimed. Apple, iOS, Darwin, and related marks belong to their respective owners.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting research or code. Please distinguish verified facts from hypotheses and include sources for technical claims.

## License

Original project material is provided under the MIT License in [LICENSE](LICENSE), unless a file or third-party notice states otherwise.
