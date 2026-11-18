# XNU QEMU feasibility experiment

This workflow is the first automated XNU experiment. It checks out the public Darwin 24.6.0-family candidate at the exact pinned commit and records upstream build entry points, ARM64 source references, and available host tools.

It is deliberately a **feasibility/source-inspection experiment**, not a kernel compilation or successful QEMU boot. Public XNU source has Apple-platform dependencies and build requirements; a generic ARM64 source match does not establish a bootable QEMU kernel or HANOIP compatibility.

## Run

Use GitHub Actions → **XNU QEMU feasibility experiment** → Run workflow. The job uploads `xnu-qemu-feasibility-report`.

## Next gate

Use the report and upstream build documentation to select a supported build host, SDK, target configuration, and boot protocol. Only then add a real kernel-build job and QEMU launch test. Do not fabricate a kernel artifact or claim a boot if no kernel was produced and executed.
