# HackintoiOS

**Experimental operating-system research for the Motorola Moto G60 (XT2135-2).**

HackintoiOS investigates the architectural and engineering challenges involved in studying Darwin and the open-source XNU kernel on non-Apple ARM64 hardware. The project is currently in the **research and documentation stage**.

> **Project status:** Research only. This repository does not contain a working iOS port, a bootable image, device drivers, or a supported installation method.

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
| Device | Motorola Moto G60 |
| Model | XT2135-2 |
| CPU architecture | ARM64 target (exact platform details to be verified) |
| Current project phase | Research and documentation |

Hardware details will be added only when verified against reliable documentation or measurements. See [device research](docs/device-profile.md).

## Repository layout

```text
.
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── Makefile
├── build/
│   └── Makefile
├── bootloader/
│   └── README.md
├── docs/
│   ├── README.md
│   ├── architecture/
│   │   └── overview.md
│   ├── device-profile.md
│   ├── research-log.md
│   └── roadmap.md
├── firmware/
│   └── README.md
├── hardware/
│   └── README.md
└── kernel/
    └── README.md
```

## Research areas

| Area | Current focus |
| --- | --- |
| ARM64 platform | Identify verified SoC, memory, and platform information |
| Boot process | Document boot stages and device-specific constraints |
| XNU / Darwin | Study upstream source, build requirements, and portability boundaries |
| Kernel | Track architecture assumptions and required platform support |
| Hardware | Create a component-by-component compatibility matrix |
| Build system | Provide safe documentation and validation targets only |

See the [roadmap](docs/roadmap.md) and [research log](docs/research-log.md).

## Build status

The Makefiles currently provide **documentation and project-maintenance helpers only**. They do not compile XNU, create firmware, unpack IPSW files, generate boot images, or modify a phone.

Run:

```sh
make help
make docs-check
```

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
