# QEMU development

QEMU is a development and test environment, not a substitute for the Moto G60 hardware.

The current XNU experiment lives in [xnu/qemu-experiment/](../xnu/qemu-experiment/README.md). The UEFI prototype has a separate emulated AArch64 test. These tests must state exactly what they execute; source inspection, host tests, UEFI execution, and a real XNU boot are different milestones.

No QEMU machine currently emulates the Adreno 618 or the complete HANOIP platform.
