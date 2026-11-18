# HackintoiOS

**Experimental operating-system research for the Motorola Moto G60 (XT2135-2).**

HackintoiOS investigates the architectural and engineering challenges involved in studying Darwin and the open-source XNU kernel on non-Apple ARM64 hardware. The project is in the **research and early scaffolding stage**.

> **Project status:** No working iOS port, bootable Moto G60 image, or validated Moto G60 XNU drivers exist. The repository now includes an original host-built userland smoke test; this is not a Darwin runtime.

## Goals

- Document the Moto G60 platform and its publicly documented hardware.
- Study ARM64 boot concepts and the Android device boot chain at a high level.
- Explore the architecture and build requirements of the open-source XNU and Darwin components.
- Record hardware compatibility questions for CPU, GPU, Wi-Fi, audio, camera, storage, power, touchscreen, and haptics.
- Develop a transparent, reproducible documentation and build-scaffolding workflow.
- Keep third-party code, licenses, and provenance clearly documented.

## Device target

| Item | Value |
| --- | --- |
| Device | Motorola Moto G60 Vision |
| Model | XT2135-2 |
| Device family | HANOIP |
| Current project phase | Research and early scaffolding |

Hardware details will be added only when verified against reliable documentation or measurements. See [device research](devices/moto-g60-xt2135-2/README.md) and the [hardware bring-up tracker](devices/moto-g60-xt2135-2/hardware-status.md).

## Repository layout

```text
.
├── bootloader/       # UEFI application prototype and notes
├── devices/          # Moto G60 target profile and hardware status
├── docs/             # Architecture, roadmap and research notes
├── drivers/          # Planned XNU-facing driver work; none implemented yet
├── kernel/           # Linux reference-kernel build, not XNU
├── sysimage/         # Safe IPSW archive-inspection tools
├── userland/         # Original host smoke test and userland research
└── xnu/              # Pinned upstream XNU research baseline and patch manifest
```

## Build status

The project has separate checks for the Linux reference kernel, XNU source-baseline integrity, sysimage tooling, UEFI prototype and the initial host userland smoke test. A successful check proves only what that workflow tests; it does not establish that XNU boots on the phone.

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
- HakiOS and other projects are references for learning, not proof that their device configurations or patches work on the Moto G60.
- No Apple affiliation or endorsement is claimed. Apple, iOS, Darwin, and related marks belong to their respective owners.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting research or code. Please distinguish verified facts from hypotheses and include sources for technical claims.

## License

Original project material is provided under the MIT License in [LICENSE](LICENSE), unless a file or third-party notice states otherwise.
