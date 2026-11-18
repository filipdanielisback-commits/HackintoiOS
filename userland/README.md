# HackintoiOS userland

**Status: initial open-source scaffold; not a Darwin or iOS user space.**

This directory is for original HackintoiOS programs, libraries, startup components and image-preparation tools. It follows the separation used by projects such as HakiOS: project-owned code belongs in Git, while proprietary operating-system files supplied by a user stay outside the repository.

## Current contents

- `src/hello/main.c`: a small portable C smoke-test program.
- `build.sh`: builds that program with the host C compiler into an output directory.
- `launchd/README.md`: startup integration notes and requirements.
- `libraries/README.md`: policy for future original libraries.

## Build the open smoke test

From the repository root:

```sh
sh userland/build.sh
./build/userland/hackintoios-hello
```

Or choose an output directory:

```sh
sh userland/build.sh /tmp/hackintoios-userland
/tmp/hackintoios-userland/hackintoios-hello
```

The current CI check builds and runs this program on Ubuntu. That validates ordinary C source and the host build script only. It does **not** demonstrate that the program runs on XNU, that a Darwin runtime is available, or that the phone can boot it.

## iOS / Darwin system files

The planned sysimage workflow may inspect a user-supplied IPSW and prepare a local filesystem workspace when the image format and contents are readable. Do not commit an IPSW, extracted Apple binaries, frameworks, fonts, assets, firmware, personal device data, signing material or credentials here. Generated system images and extracted payloads must remain local and ignored by Git.

The iPhone XR iOS 18.7.12 reference image is not a Moto G60 system image. Its compatibility with HANOIP and our XNU baseline is unproven. We must verify version alignment and filesystem requirements before attempting any Darwin startup.

## Planned work (not implemented)

1. Define a minimal, original userland ABI smoke test for the XNU/QEMU research path.
2. Document the expected process-start and filesystem interfaces.
3. Add original libraries only when their interfaces and licensing are clear.
4. Integrate a Darwin system-image layout only after the exact IPSW filesystem has been inspected and compatibility requirements are evidenced.
5. Add launch services only when a compatible kernel and user-space runtime can actually start them.

No Apple services, activation, Apple ID, iCloud or App Store support is claimed or planned.
