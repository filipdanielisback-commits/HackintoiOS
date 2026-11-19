# Build and platform configurations

This directory will hold reviewed, reproducible configuration inputs for HackintoiOS builds.

Configuration layers are intended to remain separate:
- common options that are device-neutral;
- the Moto G60 XT2135-2 device profile;
- QEMU-only development configuration.

No HakiOS configuration files are copied. Do not create enabled-driver lists, XNU options, or boot arguments until the matching XNU interfaces and build system are verified. Evidence-only hardware data remains in drivers/platform and docs.
