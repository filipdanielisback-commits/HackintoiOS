# Startup integration research

**Status: documentation only. No launchd implementation or compatible Darwin startup environment exists yet.**

HakiOS demonstrates the architectural goal of handing control from a kernel to a supplied user space. HackintoiOS must first establish its own verified XNU process-start contract and a compatible runtime.

Before adding startup jobs, we need evidence for:

- the kernel's initial user-space entry point and process ABI;
- executable and dynamic-library formats supported by the runtime;
- filesystem mount and permission requirements;
- required system services and their dependencies;
- a safe shutdown / return-to-firmware path for any future test environment.

Do not add Apple's proprietary launchd binaries or other extracted iOS components to this directory. Any future integration with a locally supplied system image must be documented separately and remain outside Git.
