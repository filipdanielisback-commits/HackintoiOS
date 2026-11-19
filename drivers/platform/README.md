# HANOIP platform contract

This folder currently contains an **evidence-only contract**, not executable platform code.

- [hanoip-platform.json](hanoip-platform.json) records facts observed in the pinned Linux device-tree source.
- Facts are explicitly marked as source evidence and cannot directly enable XNU runtime code.
- Runtime values for CPU topology, PSCI conduit, memory ranges, reserved memory, device-tree handoff, interrupt routing, timer frequency, and console registers remain `null`.
- The exact XT2135-2 engineering board revision remains unresolved.

## Why this exists

A platform contract separates three things that must not be conflated:

1. **Source observation:** what the pinned Linux source says.
2. **Target validation:** whether that observation applies to this exact XT2135-2 unit and its boot handoff.
3. **Runtime configuration:** the values an XNU platform implementation may safely consume.

Only the first category is currently populated. The second and third require stronger evidence. The JSON validator rejects accidental promotion of unknown runtime values into guessed constants.

## Next engineering gates

1. Complete and review the recursive include audit and, where possible, a merged-DTB analysis from the pinned source.
2. Establish an independently testable ARM64 loader-to-kernel handoff contract in QEMU.
3. Determine which runtime information that handoff must provide.
4. Add implementation only when the exact value and its source are reviewed.

This directory does not contain an XNU driver, boot-time device tree, register map, or phone-specific executable configuration. CI checks the evidence document's structure and protects unresolved values; it does not validate physical hardware.
